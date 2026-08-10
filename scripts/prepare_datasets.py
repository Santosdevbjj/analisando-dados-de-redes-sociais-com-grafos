from __future__ import annotations

import csv
import io
import zipfile
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
RAW_DIR = ROOT / "data" / "raw"
PROCESSED_DIR = ROOT / "data" / "processed"
SAMPLES_DIR = ROOT / "data" / "samples"


def find_raw_file(file_pattern: str) -> Path | None:
    """Procura por um arquivo .zip ou .csv no diretório data/raw baseado em um padrão de nome."""
    if not RAW_DIR.exists():
        return None
    for item in RAW_DIR.glob(f"*{file_pattern}*"):
        if item.suffix.lower() in [".zip", ".csv"]:
            return item
    return None


def clean_global_demographics(file_path: Path) -> pd.DataFrame:
    """Limpa e normaliza o dataset global de demografia por faixa etária/gênero."""
    rows: list[list[str]] = []
    
    if file_path.suffix.lower() == ".zip":
        with zipfile.ZipFile(file_path) as z:
            csv_name = next(n for n in z.namelist() if n.lower().endswith(".csv"))
            with z.open(csv_name) as f:
                text = io.TextIOWrapper(f, encoding="utf-8", errors="replace")
                reader = csv.reader(text)
                header = next(reader)
                for row in reader:
                    if len(row) < 8:
                        row += [""] * (8 - len(row))
                    elif len(row) > 8:
                        row = row[:7] + [",".join(row[7:])]
                    rows.append(row)
    else:
        with open(file_path, encoding="utf-8", errors="replace") as f:
            reader = csv.reader(f)
            header = next(reader)
            for row in reader:
                if len(row) < 8:
                    row += [""] * (8 - len(row))
                elif len(row) > 8:
                    row = row[:7] + [",".join(row[7:])]
                rows.append(row)

    df = pd.DataFrame(rows, columns=header)
    
    # Extração e normalização numérica
    df["mau_billion"] = (
        df["Total Monthly Active Users (Billion)"]
        .astype(str)
        .str.extract(r"([0-9]+(?:\.[0-9]+)?)")[0]
        .astype(float)
    )
    df["female_within_age_pct"] = (
        pd.to_numeric(df["% Female Users (within age group)"].astype(str).str.replace("%", "", regex=False), errors="coerce")
    )
    df["male_within_age_pct"] = (
        pd.to_numeric(df["% Male Users (within age group)"].astype(str).str.replace("%", "", regex=False), errors="coerce")
    )
    df["overall_female_pct"] = (
        pd.to_numeric(df["Overall % Female Users"].astype(str).str.replace("%", "", regex=False), errors="coerce")
    )
    df["overall_male_pct"] = (
        pd.to_numeric(df["Overall % Male Users"].astype(str).str.replace("%", "", regex=False), errors="coerce")
    )
    return df


def prepare_genz_profiles(file_path: Path) -> tuple[pd.DataFrame, pd.DataFrame]:
    """
    Processa o dataset de 1M da Gen-Z por chunks, gera agregação para os perfis
    do Neo4j e extrai uma amostra crua de 1.000 linhas para testes de qualidade.
    """
    dtypes = {
        "age": "int16",
        "gender": "category",
        "country": "category",
        "daily_usage_hours": "float32",
        "primary_platform": "category",
        "num_platforms_used": "int8",
        "purpose": "category",
        "avg_session_minutes": "float32",
        "night_usage": "int8",
        "mental_health_score": "float32",
        "addiction_level": "category",
        "screen_time_before_sleep": "float32",
    }

    chunks: list[pd.DataFrame] = []
    raw_sample_chunks: list[pd.DataFrame] = []

    def process_file_stream(stream):
        for chunk in pd.read_csv(stream, dtype=dtypes, chunksize=200_000):
            # Guarda os primeiros chunks para extrair a amostra crua
            if sum(len(c) for c in raw_sample_chunks) < 10_000:
                raw_sample_chunks.append(chunk)

            grouped = chunk.groupby(
                ["age", "gender", "country", "primary_platform", "purpose", "addiction_level", "num_platforms_used", "night_usage"],
                observed=True,
            ).agg(
                sample_count=("age", "size"),
                avg_daily_usage_hours=("daily_usage_hours", "mean"),
                avg_session_minutes=("avg_session_minutes", "mean"),
                avg_mental_health_score=("mental_health_score", "mean"),
                avg_screen_time_before_sleep=("screen_time_before_sleep", "mean"),
            ).reset_index()
            chunks.append(grouped)

    if file_path.suffix.lower() == ".zip":
        with zipfile.ZipFile(file_path) as z:
            csv_name = next(n for n in z.namelist() if n.lower().endswith(".csv"))
            process_file_stream(z.open(csv_name))
    else:
        process_file_stream(file_path)

    # Consolidação das agregações
    agg = pd.concat(chunks, ignore_index=True)
    agg = agg.groupby(
        ["age", "gender", "country", "primary_platform", "purpose", "addiction_level", "num_platforms_used", "night_usage"],
        observed=True,
    ).agg(
        sample_count=("sample_count", "sum"),
        avg_daily_usage_hours=("avg_daily_usage_hours", "mean"),
        avg_session_minutes=("avg_session_minutes", "mean"),
        avg_mental_health_score=("avg_mental_health_score", "mean"),
        avg_screen_time_before_sleep=("avg_screen_time_before_sleep", "mean"),
    ).reset_index()

    # Identificador único determinístico
    agg["profile_id"] = (
        "P-" + agg["age"].astype(str)
        + "-" + agg["gender"].astype(str)
        + "-" + agg["country"].astype(str)
        + "-" + agg["primary_platform"].astype(str)
        + "-" + agg["purpose"].astype(str)
        + "-" + agg["addiction_level"].astype(str)
        + "-" + agg["num_platforms_used"].astype(str)
        + "-" + agg["night_usage"].astype(str)
    ).str.replace(" ", "_", regex=False).str.replace("/", "_", regex=False)

    # Amostra crua de 1.000 linhas reproduzível
    df_raw_combined = pd.concat(raw_sample_chunks, ignore_index=True)
    sample_1000 = df_raw_combined.sample(n=min(1000, len(df_raw_combined)), random_state=42)

    return agg, sample_1000


def main() -> None:
    PROCESSED_DIR.mkdir(exist_ok=True, parents=True)
    SAMPLES_DIR.mkdir(exist_ok=True, parents=True)

    if not RAW_DIR.exists():
        RAW_DIR.mkdir(exist_ok=True, parents=True)
        print(f"Diretório {RAW_DIR} criado. Adicione os arquivos raw para processamento.")
        return

    global_file = find_raw_file("Global") or find_raw_file("demographics")
    genz_file = find_raw_file("Gen-Z") or find_raw_file("genz")

    # 1. Processar Demografia Global
    if global_file and global_file.exists():
        print(f"Processando dataset demográfico: {global_file.name}")
        global_df = clean_global_demographics(global_file)
        global_df.to_csv(PROCESSED_DIR / "global_social_media_users_clean.csv", index=False)
        
        # Amostra limpa em data/samples/
        global_df.head(100).to_csv(
            SAMPLES_DIR / "global_social_media_users_by_age_gender_2025_clean.csv", index=False
        )
    else:
        print("Dataset global demográfico não encontrado em data/raw/. Pulando...")

    # 2. Processar Dataset Gen-Z
    if genz_file and genz_file.exists():
        print(f"Processando dataset Gen-Z: {genz_file.name}")
        genz_profiles, genz_sample_1000 = prepare_genz_profiles(genz_file)
        
        # Salvar dataset de perfis agregados em processed/
        genz_profiles.to_csv(PROCESSED_DIR / "genz_usage_profiles.csv", index=False)
        
        # Salvar amostras em samples/
        genz_sample_1000.to_csv(SAMPLES_DIR / "genz_social_media_usage_sample_1000.csv", index=False)
        genz_profiles.head(500).to_csv(SAMPLES_DIR / "genz_profile_aggregation_sample_500.csv", index=False)
        print("Processamento concluído com sucesso!")
    else:
        print("Dataset Gen-Z não encontrado em data/raw/. Pulando...")


if __name__ == "__main__":
    main()
