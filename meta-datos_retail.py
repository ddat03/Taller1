# -*- coding: utf-8 -*-
"""
Created on Fri Apr 11 10:11:44 2025

@author: DIEGO
"""

import sqlite3
import pandas as pd

# Conectar y cargar datos
conexion = sqlite3.connect('online_retail_limpio.db')
df = pd.read_sql_query("SELECT * FROM retail_data", conexion)
conexion.close()

# Información básica estructural
print("Dimensiones del DataFrame:", df.shape)
print("\nTipos de datos por columna:")
print(df.dtypes)
print("\nResumen de información:")
print(df.info())


# Valores nulos por columna
print("Cantidad de valores nulos por columna:")
print(df.isnull().sum())

# Porcentaje de valores nulos
print("\nPorcentaje de valores nulos por columna:")
print((df.isnull().sum() / len(df)) * 100)

# Valores duplicados
print("\nTotal de filas duplicadas:", df.duplicated().sum())

# Valores únicos por columna
print("\nCantidad de valores únicos por columna:")
for columna in df.columns:
    print(f"{columna}: {df[columna].nunique()} valores únicos")
    
    
# Estadísticas descriptivas para columnas numéricas
print("Estadísticas descriptivas:")
print(df.describe())

# Estadísticas para columnas categóricas
print("\nEstadísticas para columnas categóricas:")
print(df.describe(include=['object']))

# Frecuencias de valores (para columnas categóricas)
for columna in df.select_dtypes(include=['object']).columns:
    print(f"\nFrecuencia de valores en '{columna}':")
    print(df[columna].value_counts().head())


from ydata_profiling import ProfileReport

# Generar reporte completo
perfil = ProfileReport(df, title="Reporte de perfil - Online Retail")
perfil.to_file("reporte_online_retail.html")
print("Reporte generado y guardado como 'reporte_online_retail.html'")


# Matriz de correlación entre variables numéricas
columnas_numericas = df.select_dtypes(include=['number']).columns

if len(columnas_numericas) > 1:
    print("\nMatriz de correlación:")
    correlacion = df[columnas_numericas].corr()
    print(correlacion)

# Sesgo (skewness) para variables numéricas
print("\nSesgo de variables numéricas:")
print(df.select_dtypes(include=['number']).skew())

# Curtosis para variables numéricas
print("\nCurtosis de variables numéricas:")
print(df.select_dtypes(include=['number']).kurtosis())
