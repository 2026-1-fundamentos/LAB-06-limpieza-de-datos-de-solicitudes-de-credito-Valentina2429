import os
import pandas as pd


def pregunta_01():
    entrada = "files/input/solicitudes_de_credito.csv"
    salida = "files/output/solicitudes_de_credito.csv"

    df = pd.read_csv(entrada, sep=";")

    # Eliminar la primera columna, que corresponde al índice guardado.
    df = df.drop(columns=[df.columns[0]])

    # Eliminar registros con datos faltantes.
    df = df.dropna()

    # Guardar barrio antes de limpiar las demás columnas.
    barrios = df["barrio"].copy()

    def limpieza_general(serie):
        return (
            serie.astype(str)
            .str.lower()
            .str.replace(r"[-_.]", " ", regex=True)
            .str.replace(r"[!\"#$%&'()*+,/:;<=>?@[\\\]^`{|}~]", "", regex=True)
            .str.replace(r"\s+", " ", regex=True)
            .str.strip()
        )

    columnas_texto = [
        "sexo",
        "tipo_de_emprendimiento",
        "idea_negocio",
        "línea_credito",
    ]

    for columna in columnas_texto:
        df[columna] = limpieza_general(df[columna])

    # Limpieza especial para barrio. porque asi lo piede el test
    df["barrio"] = (
        barrios.loc[df.index]
        .astype(str)
        .str.lower()
        .str.replace(r"[-_]", " ", regex=True)
        .str.replace(r"[!\"#$%&'()*+,/:;<=>?@[\\\]^`{|}~]", "", regex=True)
        .str.replace(r"\s+", " ", regex=True)
    )

    # Limpiar monto del crédito.
    df["monto_del_credito"] = (
        df["monto_del_credito"]
        .astype(str)
        .str.replace(r"\.\d+", "", regex=True)
        .str.replace(r"[^0-9]", "", regex=True)
    )

    # Normalizar fechas con formato año/mes/día.
    fechas = df["fecha_de_beneficio"].astype(str).str.strip()

    fechas_dia_mes_anio = pd.to_datetime(
        fechas,
        format="%d/%m/%Y",
        errors="coerce"
    )

    fechas_anio_mes_dia = pd.to_datetime(
        fechas,
        format="%Y/%m/%d",
        errors="coerce"
    )

    df["fecha_de_beneficio"] = (
        fechas_dia_mes_anio
        .fillna(fechas_anio_mes_dia)
        .dt.strftime("%d/%m/%Y"))

    # Convertir columnas numéricas.
    df["estrato"] = pd.to_numeric(df["estrato"], errors="coerce").astype("Int64")
    df["comuna_ciudadano"] = pd.to_numeric(
        df["comuna_ciudadano"], errors="coerce"
    ).astype("Int64")

    # Eliminar duplicados después de limpiar.
    df = df.drop_duplicates()

    os.makedirs("files/output", exist_ok=True)

    df.to_csv(salida, sep=";", index=False)

    return df