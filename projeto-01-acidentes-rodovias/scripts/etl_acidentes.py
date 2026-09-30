"""
ETL - Limpeza e padronização dos dados abertos da PRF.
Autor: Eurismar Silveira Alves
"""

import pandas as pd

INPUT_PATH = "data/acidentes_prf_raw.csv"
OUTPUT_PATH = "data/acidentes_prf.csv"

COLUNAS = [
    "data_inversa", "horario", "uf", "municipio", "causa_acidente",
    "tipo_acidente", "classificacao_acidente", "fase_dia",
    "condicao_metereologica", "tipo_pista", "tracado_via",
    "uso_solo", "feridos", "mortos",
]

RENOMEAR = {
    "data_inversa": "data",
    "horario": "hora",
    "municipio": "cidade",
    "condicao_metereologica": "condicao_meteorologica",
    "classificacao_acidente": "classificacao",
    "tipo_pista": "tipo_pista",
    "tracado_via": "tracado",
    "uso_solo": "uso_solo",
}


def load(path: str) -> pd.DataFrame:
    df = pd.read_csv(path, sep=";", encoding="latin-1", low_memory=False)
    df.columns = [c.strip().lower() for c in df.columns]
    return df


def clean(df: pd.DataFrame) -> pd.DataFrame:
    df = df[[c for c in COLUNAS if c in df.columns]].copy()
    df = df.rename(columns=RENOMEAR)

    df["data"] = pd.to_datetime(df["data"], errors="coerce")
    df["hora"] = pd.to_datetime(
        df["hora"], format="%H:%M:%S", errors="coerce"
    ).dt.hour

    df["feridos"] = pd.to_numeric(
        df["feridos"], errors="coerce"
    ).fillna(0).astype(int)
    df["mortos"] = pd.to_numeric(
        df["mortos"], errors="coerce"
    ).fillna(0).astype(int)

    for col in df.select_dtypes(include="object").columns:
        df[col] = df[col].astype(str).str.strip().str.title()

    df = df.dropna(subset=["data"])
    return df


def main():
    df = load(INPUT_PATH)
    df = clean(df)
    df.to_csv(OUTPUT_PATH, index=False, encoding="utf-8")
    print(f"Arquivo gerado: {OUTPUT_PATH} | {len(df)} registros")


if __name__ == "__main__":
    main()
