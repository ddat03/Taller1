# -*- coding: utf-8 -*-
"""
Created on Thu Apr 10 08:30:18 2025

@author: DIEGO
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import sqlite3
import plotly.express as px

# Conectar a tu base de datos
conexion = sqlite3.connect('online_retail_limpio.db')

# Utilizar el nombre correcto de la tabla
query = "SELECT * FROM retail_data"

# Cargar los datos en un DataFrame
df = pd.read_sql_query(query, conexion)

# Cerrar la conexión
conexion.close()

plot3 = pd.DataFrame(df.groupby(['Hora'])['InvoiceNo'].count()).reset_index()

# Crear el gráfico
plt.figure(figsize=(12, 6))

# Usando countplot en lugar de barplot (otra opción)
ax = sns.barplot(
    x='Hora', 
    y='InvoiceNo', 
    hue='Hora',
    dodge=False,  # Esta es la clave: evita separar barras del mismo grupo
    palette='Set1', 
    legend=False, 
    data=plot3
)

# Mejorar la visualización
plt.title('Número Promedio de Facturas por Hora del Día', fontsize=14, fontweight='bold')
plt.xlabel('Hora del Día', fontsize=12)
plt.ylabel('Promedio de Facturas', fontsize=12)
plt.xticks(rotation=45)
plt.grid(axis='y', linestyle='--', alpha=0.6)
plt.tight_layout()
plt.show()