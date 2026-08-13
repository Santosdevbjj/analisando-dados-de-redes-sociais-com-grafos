import glob
import os
import pandas as pd
import pytest

SAMPLES_DIR = "data/samples"
GENZ_SAMPLE_FILE = os.path.join(SAMPLES_DIR, "genz_social_media_usage_sample_1000.csv")
GLOBAL_SAMPLE_FILE = os.path.join(SAMPLES_DIR, "global_social_media_users_clean.csv")


def get_sample_files():
    """Retorna lista de arquivos CSV no diretório de amostras."""
    return glob.glob(os.path.join(SAMPLES_DIR, "*.csv"))


def test_samples_directory_exists():
    """Garante que o diretório de amostras existe."""
    assert os.path.exists(SAMPLES_DIR), f"O diretório '{SAMPLES_DIR}' não foi encontrado."


def test_samples_directory_not_empty():
    """Garante que existem arquivos CSV para testar no diretório."""
    csv_files = get_sample_files()
    assert len(csv_files) > 0, f"Nenhum arquivo CSV encontrado em '{SAMPLES_DIR}'."


@pytest.mark.parametrize("csv_file", get_sample_files() or [None])
def test_csv_files_not_empty(csv_file):
    """Verifica se cada arquivo CSV de amostra não está vazio."""
    if csv_file is None:
        pytest.skip("Nenhum arquivo CSV encontrado para validação.")
    
    assert os.path.getsize(csv_file) > 0, f"O arquivo {csv_file} está zerado em disco (0 bytes)."
    df = pd.read_csv(csv_file)
    assert not df.empty, f"O arquivo {csv_file} foi lido mas não contém linhas."


def test_genz_usage_sample_schema():
    """Valida o esquema de colunas da amostra de uso da Gen-Z."""
    if not os.path.exists(GENZ_SAMPLE_FILE):
        pytest.skip(f"Arquivo {GENZ_SAMPLE_FILE} não encontrado para teste de schema.")

    df = pd.read_csv(GENZ_SAMPLE_FILE)
    expected_columns = [
        "age",
        "gender",
        "country",
        "daily_usage_hours",
        "primary_platform",
        "num_platforms_used",
        "purpose",
        "avg_session_minutes",
        "night_usage",
        "mental_health_score",
        "addiction_level",
        "screen_time_before_sleep",
    ]
    
    missing_columns = [col for col in expected_columns if col not in df.columns]
    assert not missing_columns, f"Colunas ausentes em {GENZ_SAMPLE_FILE}: {missing_columns}"


def test_genz_data_value_ranges():
    """Valida os intervalos de valores (boundary test) para o dataset Gen-Z."""
    if not os.path.exists(GENZ_SAMPLE_FILE):
        pytest.skip(f"Arquivo {GENZ_SAMPLE_FILE} não encontrado para teste de limites.")

    df = pd.read_csv(GENZ_SAMPLE_FILE)

    # Validações de limites (ranges)
    assert df["age"].between(13, 27).all(), (
        f"Idades fora da faixa esperada Gen-Z (13-27). Min: {df['age'].min()}, Max: {df['age'].max()}"
    )
    assert df["mental_health_score"].between(1, 10).all(), (
        "Score de saúde mental fora do intervalo [1, 10]."
    )
    assert df["daily_usage_hours"].between(0.0, 24.0).all(), (
        "Horas de uso diário fora do intervalo realista [0, 24]."
    )
    assert df["avg_session_minutes"].ge(0).all(), (
        "Duração média de sessão não pode conter valores negativos."
    )


def test_no_all_null_columns():
    """Garante que nenhuma coluna nas amostras esteja 100% nula."""
    for csv_file in get_sample_files():
        df = pd.read_csv(csv_file)
        null_cols = [col for col in df.columns if df[col].isnull().all()]
        assert not null_cols, f"O arquivo {csv_file} possui colunas 100% nulas: {null_cols}"
