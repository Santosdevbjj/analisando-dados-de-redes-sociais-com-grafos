\
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


def clean_global_demographics(zip_path: Path) -> pd.DataFrame:
    """Clean the global age/gender platform dataset, which has a few malformed rows."""
    with zipfile.ZipFile(zip_path) as z:
        csv_name = next(n for n in z.namelist() if n.lower().endswith(".csv"))
        with z.open(csv_name) as f:
            text = io.TextIOWrapper(f, encoding="utf-8", errors="replace")
            reader = csv.reader(text)
            header = next(reader)
            rows: list[list[str]] = []
            for row in reader:
                if len(row) < 8:
                    row += [""] * (8 - len(row))
                elif len(row) > 8:
                    row = row[:7] + [",".join(row[7:])]
                rows.append(row)

    df = pd.DataFrame(rows, columns=header)
    df["mau_billion"] = (
        df["Total Monthly Active Users (Billion)"].astype(str).str.extract(r"([0-9]+(?:\.[0-9]+)?)")[0].astype(float)
    )
    df["female_within_age_pct"] = df["% Female Users (within age group)"].astype(str).str.replace("%", "", regex=False)
    df["male_within_age_pct"] = df["% Male Users (within age group)"].astype(str).str.replace("%", "", regex=False)
    df["overall_female_pct"] = df["Overall % Female Users"].astype(str).str.replace("%", "", regex=False)
    df["overall_male_pct"] = df["Overall % Male Users"].astype(str).str.replace("%", "", regex=False)
    return df


def prepare_genz_profiles(zip_path: Path) -> pd.DataFrame:
    """Aggregate the 1M-row Gen-Z dataset into profile-level nodes that fit AuraDB Free."""
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

    with zipfile.ZipFile(zip_path) as z:
        csv_name = next(n for n in z.namelist() if n.lower().endswith(".csv"))
        chunks: list[pd.DataFrame] = []
        for chunk in pd.read_csv(z.open(csv_name), dtype=dtypes, chunksize=200_000):
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
    return agg


def main() -> None:
    PROCESSED_DIR.mkdir(exist_ok=True, parents=True)
    if not RAW_DIR.exists():
        raise FileNotFoundError(f"Missing raw data directory: {RAW_DIR}")

    global_zip = RAW_DIR / "Global Social Media Users by Age-Gender 2025.zip"
    genz_zip = RAW_DIR / "Gen-Z Social Media Usage Dataset.zip"

    if global_zip.exists():
        global_df = clean_global_demographics(global_zip)
        global_df.to_csv(PROCESSED_DIR / "global_social_media_users_clean.csv", index=False)
    else:
        print(f"Skipping missing file: {global_zip}")

    if genz_zip.exists():
        genz_profiles = prepare_genz_profiles(genz_zip)
        genz_profiles.to_csv(PROCESSED_DIR / "genz_usage_profiles.csv", index=False)
    else:
        print(f"Skipping missing file: {genz_zip}")


if __name__ == "__main__":
    main()
