# -*- coding: utf-8 -*-
"""
Created on Fri Apr 11 09:55:57 2025

@author: DIEGO
"""
import sqlite3
import pandas as pd

# Conectar a tu base de datos
conexion = sqlite3.connect('online_retail_limpio.db')

# Utilizar el nombre correcto de la tabla
query = "SELECT * FROM retail_data"

# Cargar los datos en un DataFrame
df = pd.read_sql_query(query, conexion)

# Cerrar la conexión
conexion.close()

# Explorar los datos
print("Dimensiones del DataFrame:", df.shape)
print("\nPrimeras 5 filas:")
print(df.head())
print("\nInformación de columnas:")
print(df.info())