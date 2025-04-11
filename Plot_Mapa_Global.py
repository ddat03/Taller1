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
# Agrupar ventas por país
ventas_por_pais = df.groupby('Country')['Importe Total'].sum().reset_index()
ventas_por_pais.columns = ['Country', 'Total_Ventas']

ventas_por_pais = ventas_por_pais[ventas_por_pais['Country'] != 'United Kingdom']

# Crear mapa
fig = px.choropleth(
    ventas_por_pais,
    locations='Country',
    locationmode='country names',
    color='Total_Ventas',
    hover_name='Country',
    color_continuous_scale=px.colors.sequential.Plasma,
    title='Distribución global de ventas por país',
    labels={'Total_Ventas': 'Volumen de ventas'},
)

fig.update_layout(
    geo=dict(
        showframe=False,
        showcoastlines=True,
        projection_type='natural earth'
    ),
    height=600,
    margin=dict(l=0, r=0, t=50, b=0)
)

# Para mostrar en un notebook
fig.show()

# Para guardar como HTML (en caso de no poder mostrar interactivamente)
fig.write_html("mapa_ventas_global.html")