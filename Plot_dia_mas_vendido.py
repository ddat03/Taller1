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

plt.style.use('seaborn-v0_8-whitegrid')
sns.set(font_scale=1.1)
plt.rcParams['figure.figsize'] = (14, 10)

ventas_por_fecha = df[df['Tipo_Transaccion'] == 'VENTA'].groupby(['Mes', 'Dia'])['Importe Total'].sum().reset_index()
    
    # Convertir a matriz para el heatmap
matriz_ventas = ventas_por_fecha.pivot(index='Dia', columns='Mes', values='Importe Total')
    
plt.figure(figsize=(12, 10))
ax = sns.heatmap(matriz_ventas, annot=False, cmap='YlGnBu', 
                    cbar_kws={'label': 'Importe Total de Ventas'},
                    linewidths=0.5)
    
    # Mejorar el formato
plt.title('Mapa de Calor: Ventas por Día y Mes', fontsize=16, pad=20)
plt.xlabel('Mes', fontsize=12)
plt.ylabel('Día', fontsize=12)
    
    # Añadir nombres de meses en lugar de números
meses = {1:'Enero', 2:'Febrero', 3:'Marzo', 4:'Abril', 5:'Mayo', 6:'Junio',
            7:'Julio', 8:'Agosto', 9:'Septiembre', 10:'Octubre', 11:'Noviembre', 12:'Diciembre'}
    
    # Ajustar las etiquetas de los ejes según los datos disponibles
meses_en_datos = sorted(df['Mes'].unique())
etiquetas_meses = [meses.get(mes, str(mes)) for mes in meses_en_datos]
    
plt.xticks(ticks=np.arange(len(meses_en_datos))+0.5, labels=etiquetas_meses, rotation=45)
    
plt.tight_layout()
