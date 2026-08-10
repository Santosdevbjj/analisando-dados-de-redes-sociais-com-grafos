import pytest
import pandas as pd
import glob
import os

SAMPLES_DIR = "data/samples"

def get_sample_files():
    return glob.glob(os.path.join(SAMPLES_DIR, "*.csv"))

def test_samples_directory_exists():
    assert os.path.exists(SAMPLES_DIR), f"O diretório {SAMPLES_DIR} não existe."

@pytest.mark.parametrize("csv_file", get_sample_files())
def test_csv_files_not_empty(csv_file):
    df = pd.read_csv(csv_file)
    assert not df.empty, f"O arquivo {csv_file} está vazio."

def test_genz_usage_sample_schema():
    genz_file = os.path.join(SAMPLES_DIR, "genz_social_media_usage_sample_1000.csv")
    if os.path.exists(genz_file):
        df = pd.read_csv(genz_file)
        expected_columns = [
            "age", "gender", "country", "daily_usage_hours", 
            "primary_platform", "num_platforms_used", "purpose", 
            "avg_session_minutes", "night_usage", "mental_health_score", 
            "addiction_level", "screen_time_before_sleep"
        ]
        for col in expected_columns:
            assert col in df.columns, f"Coluna esperada '{col}' não encontrada em {genz_file}."

def test_genz_data_value_ranges():
    genz_file = os.path.join(SAMPLES_DIR, "genz_social_media_usage_sample_1000.csv")
    if os.path.exists(genz_file):
        df = pd.read_csv(genz_file)
        assert df['age'].between(13, 27).all(), "Idades fora da faixa Gen-Z (13-27)."
        assert df['mental_health_score'].between(1, 10).all(), "Score de saúde mental fora do intervalo 1-10."
        assert df['daily_usage_hours'].between(0.5, 10.0).all(), "Horas de uso diário fora do intervalo permitido."
