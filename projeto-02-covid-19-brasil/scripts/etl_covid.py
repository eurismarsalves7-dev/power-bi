"""
ETL - Consolidação de casos, óbitos e vacinação (COVID-19 Brasil).
Autor: Eurismar Silveira Alves
"""

import pandas as pd

CASOS_PATH = "data/casos_obitos_raw.csv"
VACINA_PATH = "data/vacinacao_raw.csv"
POP_PATH = "data/populacao_ibge.csv"

OUT_CASOS = "data/casos_obitos.csv"
OUT_VACINA = "data/vacinacao.csv"


def load_casos() -> pd.DataFrame:
    df = pd.read_csv(CASOS_PATH, sep=";", encoding="utf-8", low_memory=False)
    df.columns = [c.strip().lower() for c in df.columns]
    df = df.rename(columns={
        "data": "data", "municipio": "cidade", "uf": "uf",
        "novoscasos": "casos", "novosobitos": "obitos",
    })
    df["data"] = pd.to_datetime(df["data"], errors="coerce")
    df["casos"] = pd.to_numeric(df["casos"], errors="coerce").fillna(0)
    df["obitos"] = pd.to_numeric(df["obitos"], errors="coerce").fillna(0)
    return df.dropna(subset=["data"])


def load_vacina() -> pd.DataFrame:
    df = pd.read_csv(VACINA_PATH, sep=";", encoding="utf-8", low_memory=False)
    df.columns = [c.strip().lower() for c in df.columns]
    df["data"] = pd.to_datetime(df["data"], errors="coerce")
    for col in ["doses_1", "doses_2", "doses_reforco"]:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0)
    return df.dropna(subset=["data"])


def main():
    casos = load_casos()
    vacina = load_vacina()

    casos.to_csv(OUT_CASOS, index=False, encoding="utf-8")
    vacina.to_csv(OUT_VACINA, index=False, encoding="utf-8")

    print(f"Casos/óbitos: {len(casos)} registros")
    print(f"Vacinação: {len(vacina)} registros")


if __name__ == "__main__":
    main()
