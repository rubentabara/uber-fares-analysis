import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt
import seaborn as sns
from ydata_profiling import ProfileReport

ruta = os.path.join(os.path.dirname(os.path.abspath(__file__)), "uber_limpio.csv")
df = pd.read_csv(ruta)

# Convertir la fecha otra vez porque al leer el csv se pierde el tipo
df["pickup_datetime"] = pd.to_datetime(df["pickup_datetime"], utc=True)

df["hora"] = df["pickup_datetime"].dt.hour
df["dia_semana"] = df["pickup_datetime"].dt.day_name()
df["mes"] = df["pickup_datetime"].dt.month

carpeta_graficas = os.path.join(os.path.dirname(os.path.abspath(__file__)), "charts")
os.makedirs(carpeta_graficas, exist_ok=True)


print("Generating profiling report, this may take a while...")
perfil = ProfileReport(df, title="Uber Fares Dataset Analysis", explorative=True)
ruta_informe = os.path.join(os.path.dirname(os.path.abspath(__file__)), "informe_uber.html")
perfil.to_file(ruta_informe)
print(f"Report saved at: {ruta_informe}")


print("\nDescriptive statistics:")
print(df.describe())


# Detección de outliers en el precio con el método IQR
Q1 = df["fare_amount"].quantile(0.25)
Q3 = df["fare_amount"].quantile(0.75)
IQR = Q3 - Q1
limite_superior = Q3 + 1.5 * IQR
limite_inferior = Q1 - 1.5 * IQR

outliers = df[(df["fare_amount"] < limite_inferior) | (df["fare_amount"] > limite_superior)]
print(f"\nOutliers in fare_amount (IQR method):")
print(f"Q1: {Q1}, Q3: {Q3}, IQR: {IQR}")
print(f"Lower limit: {limite_inferior:.2f}, Upper limit: {limite_superior:.2f}")
print(f"Outliers found: {len(outliers)} ({len(outliers)/len(df)*100:.2f}%)")

hora_pico = df["hora"].value_counts().idxmax()
dia_mas_viajes = df["dia_semana"].value_counts().idxmax()
print(f"\nBusiest hour: {hora_pico}h")
print(f"Busiest day: {dia_mas_viajes}")

print("\nAverage fare by number of passengers:")
print(df.groupby("passenger_count")["fare_amount"].mean().round(2))


# --- Gráfica 1: Distribución del precio ---
plt.figure(figsize=(10, 5))
# Limitamos a 100 para que se vea bien, los outliers distorsionan mucho
df_sin_outliers = df[df["fare_amount"] <= 100]
sns.histplot(df_sin_outliers["fare_amount"], bins=50, color="steelblue")
plt.title("Fare Amount Distribution")
plt.xlabel("Fare ($)")
plt.ylabel("Number of trips")
plt.tight_layout()
plt.savefig(os.path.join(carpeta_graficas, "fare_distribution.png"))
plt.close()
print("\nChart saved: fare_distribution.png")


# --- Gráfica 2: Viajes por hora del día ---
plt.figure(figsize=(10, 5))
viajes_por_hora = df["hora"].value_counts().sort_index()
sns.barplot(x=viajes_por_hora.index, y=viajes_por_hora.values, color="steelblue")
plt.title("Number of Trips by Hour of Day")
plt.xlabel("Hour")
plt.ylabel("Number of trips")
plt.tight_layout()
plt.savefig(os.path.join(carpeta_graficas, "trips_by_hour.png"))
plt.close()
print("Chart saved: trips_by_hour.png")


# --- Gráfica 3: Precio medio por hora ---
plt.figure(figsize=(10, 5))
precio_por_hora = df.groupby("hora")["fare_amount"].mean()
sns.lineplot(x=precio_por_hora.index, y=precio_por_hora.values, marker="o", color="steelblue")
plt.title("Average Fare by Hour of Day")
plt.xlabel("Hour")
plt.ylabel("Average fare ($)")
plt.tight_layout()
plt.savefig(os.path.join(carpeta_graficas, "avg_fare_by_hour.png"))
plt.close()
print("Chart saved: avg_fare_by_hour.png")


# --- Gráfica 4: Mapa de calor de correlaciones ---
plt.figure(figsize=(8, 6))
columnas = ["fare_amount", "passenger_count", "pickup_latitude", "pickup_longitude",
            "dropoff_latitude", "dropoff_longitude"]
sns.heatmap(df[columnas].corr().round(3), annot=True, cmap="coolwarm", fmt=".2f")
plt.title("Correlation Heatmap")
plt.tight_layout()
plt.savefig(os.path.join(carpeta_graficas, "correlation_heatmap.png"))
plt.close()
print("Chart saved: correlation_heatmap.png")

print("\nAll charts saved in the 'charts' folder.")