import pandas as pd
import numpy as np
import os
from ydata_profiling import ProfileReport

ruta = os.path.join(os.path.dirname(os.path.abspath(__file__)), "uber_limpio.csv")
df = pd.read_csv(ruta)

# Convertir la fecha otra vez porque al leer el csv se pierde el tipo
df["pickup_datetime"] = pd.to_datetime(df["pickup_datetime"], utc=True)


print("Generando informe de profiling, puede tardar un poco...")
perfil = ProfileReport(df, title="Análisis Uber Dataset", explorative=True)
ruta_informe = os.path.join(os.path.dirname(os.path.abspath(__file__)), "informe_uber.html")
perfil.to_file(ruta_informe)
print(f"Informe guardado en: {ruta_informe}")


print("\nEstadísticas descriptivas:")
print(df.describe())


print("\nDistribución de pasajeros:")
print(df["passenger_count"].value_counts().sort_index())


# Detección de outliers en el precio con el método IQR
Q1 = df["fare_amount"].quantile(0.25)
Q3 = df["fare_amount"].quantile(0.75)
IQR = Q3 - Q1
limite_superior = Q3 + 1.5 * IQR
limite_inferior = Q1 - 1.5 * IQR

outliers = df[(df["fare_amount"] < limite_inferior) | (df["fare_amount"] > limite_superior)]
print(f"\nOutliers en fare_amount:")
print(f"Q1: {Q1}, Q3: {Q3}, IQR: {IQR}")
print(f"Límite inferior: {limite_inferior:.2f}, Límite superior: {limite_superior:.2f}")
print(f"Outliers detectados: {len(outliers)} ({len(outliers)/len(df)*100:.2f}%)")


# Extraemos hora, día y mes de la fecha para sacar información nueva
df["hora"] = df["pickup_datetime"].dt.hour
df["dia_semana"] = df["pickup_datetime"].dt.day_name()
df["mes"] = df["pickup_datetime"].dt.month

print("\nPrecio medio por hora del día:")
print(df.groupby("hora")["fare_amount"].mean().round(2))

hora_pico = df["hora"].value_counts().idxmax()
dia_mas_viajes = df["dia_semana"].value_counts().idxmax()
print(f"\nHora con más viajes: {hora_pico}h")
print(f"Día con más viajes: {dia_mas_viajes}")

print("\nPrecio medio según número de pasajeros:")
print(df.groupby("passenger_count")["fare_amount"].mean().round(2))

print("\nCorrelaciones entre variables numéricas:")
columnas = ["fare_amount", "passenger_count", "pickup_latitude", "pickup_longitude",
            "dropoff_latitude", "dropoff_longitude"]
print(df[columnas].corr().round(3))