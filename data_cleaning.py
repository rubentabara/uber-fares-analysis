import pandas as pd
import numpy as np
import os

ruta = os.path.join(os.path.dirname(os.path.abspath(__file__)), "uber.csv")
df = pd.read_csv(ruta)

print("Estado inicial del dataset:")
print(f"Filas: {len(df)}")
print(f"Columnas: {list(df.columns)}")
print(f"\nValores nulos:\n{df.isnull().sum()}")


# La columna Unnamed: 0 es un índice duplicado que no sirve para nada
df = df.drop(columns=["Unnamed: 0"])


# Eliminar filas duplicadas
antes = len(df)
df = df.drop_duplicates()
print(f"\nDuplicados eliminados: {antes - len(df)}")


# Solo hay 1 nulo en las coordenadas de destino, directamente lo quitamos
df = df.dropna(subset=["dropoff_longitude", "dropoff_latitude"])
print(f"Filas tras eliminar nulos: {len(df)}")


# Precios negativos o 0 no tienen sentido
antes = len(df)
df = df[df["fare_amount"] > 0]
print(f"Filas eliminadas por precio inválido: {antes - len(df)}")


# Un taxi no puede llevar 0 pasajeros ni más de 6
antes = len(df)
df = df[(df["passenger_count"] >= 1) & (df["passenger_count"] <= 6)]
print(f"Filas eliminadas por pasajeros inválidos: {antes - len(df)}")


# Filtramos coordenadas fuera del rango de Nueva York
antes = len(df)
df = df[
    (df["pickup_latitude"].between(40.0, 42.0)) &
    (df["pickup_longitude"].between(-75.0, -72.0)) &
    (df["dropoff_latitude"].between(40.0, 42.0)) &
    (df["dropoff_longitude"].between(-75.0, -72.0))
]
print(f"Filas eliminadas por coordenadas fuera de rango: {antes - len(df)}")


df["pickup_datetime"] = pd.to_datetime(df["pickup_datetime"], utc=True)


# Normalización min-max de fare_amount y passenger_count
df["fare_amount_norm"] = (df["fare_amount"] - df["fare_amount"].min()) / (df["fare_amount"].max() - df["fare_amount"].min())
df["passenger_count_norm"] = (df["passenger_count"] - df["passenger_count"].min()) / (df["passenger_count"].max() - df["passenger_count"].min())


print("\nEstado final del dataset:")
print(f"Filas: {len(df)}")
print(f"\nEstadísticas de fare_amount:")
print(df["fare_amount"].describe())
print(f"\nEstadísticas de passenger_count:")
print(df["passenger_count"].describe())
print(f"\nTipos de datos:")
print(df.dtypes)

ruta_salida = os.path.join(os.path.dirname(os.path.abspath(__file__)), "uber_limpio.csv")
df.to_csv(ruta_salida, index=False)
print(f"\nDataset limpio guardado en: {ruta_salida}")