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


# Conectar a tu base de datos
conexion = sqlite3.connect('online_retail_limpio.db')

# Utilizar el nombre correcto de la tabla
query = "SELECT * FROM retail_data"

# Cargar los datos en un DataFrame
df = pd.read_sql_query(query, conexion)

# Cerrar la conexión
conexion.close()

# Crear fecha de referencia (último día en el dataset + 1)
fecha_referencia = pd.to_datetime(f"{max(df['Ano'])}-{max(df['Mes'])}-{max(df['Dia'])}") + pd.Timedelta(days=1)

# Convertir a fecha para cálculos
df['Fecha'] = pd.to_datetime(df[['Ano', 'Mes', 'Dia']].rename(
    columns={'Ano': 'year', 'Mes': 'month', 'Dia': 'day'}))

df_clientes_registrados = df[df['CustomerID'] != 'NO_REGISTRADO']

# Crear dataframe RFM
rfm = df_clientes_registrados.groupby('CustomerID').agg({
    'Fecha': lambda x: (fecha_referencia - x.max()).days,  # Recencia
    'InvoiceNo': 'nunique',  # Frecuencia
    'Importe Total': 'sum'   # Valor monetario
})

# Renombrar columnas
rfm.columns = ['Recencia', 'Frecuencia', 'Monetario']

rfm['Monetario'] = rfm['Monetario'].clip(upper=10000)

# Asignar puntuaciones a los cuartiles (1 es el mejor, 4 es el peor)
quintiles = rfm[['Recencia', 'Frecuencia', 'Monetario']].quantile([.2, .4, .6, .8]).to_dict()

def rfm_score(x, col):
    if col == 'Recencia':
        if x <= quintiles[col][.2]:
            return 5
        elif x <= quintiles[col][.4]:
            return 4
        elif x <= quintiles[col][.6]:
            return 3
        elif x <= quintiles[col][.8]:
            return 2
        else:
            return 1
    else:  # Para Frecuencia y Monetario, mayor es mejor
        if x <= quintiles[col][.2]:
            return 1
        elif x <= quintiles[col][.4]:
            return 2
        elif x <= quintiles[col][.6]:
            return 3
        elif x <= quintiles[col][.8]:
            return 4
        else:
            return 5

# Calcular puntuaciones
rfm['R_Score'] = rfm['Recencia'].apply(lambda x: rfm_score(x, 'Recencia'))
rfm['F_Score'] = rfm['Frecuencia'].apply(lambda x: rfm_score(x, 'Frecuencia'))
rfm['M_Score'] = rfm['Monetario'].apply(lambda x: rfm_score(x, 'Monetario'))

# Calcular RFM Score combinado
rfm['RFM_Score'] = rfm['R_Score'] * 100 + rfm['F_Score'] * 10 + rfm['M_Score']

# Crear segmentos
def segment_customer(df):
    if df['RFM_Score'] >= 444:
        return 'Campeones'
    elif (df['RFM_Score'] >= 344) & (df['RFM_Score'] < 444):
        return 'Leales'
    elif (df['RFM_Score'] >= 244) & (df['RFM_Score'] < 344):
        return 'Potenciales'
    elif (df['RFM_Score'] >= 144) & (df['RFM_Score'] < 244):
        return 'Prometedores'
    elif (df['RFM_Score'] >= 111) & (df['RFM_Score'] < 144):
        return 'Necesitan atención'
    else:
        return 'En riesgo'

rfm['Segmento'] = rfm.apply(segment_customer, axis=1)

# Visualización de segmentos
plt.figure(figsize=(12, 8))
segment_counts = rfm['Segmento'].value_counts().sort_values(ascending=False)
ax = sns.barplot(x=segment_counts.index, y=segment_counts.values, hue=segment_counts.index, palette='viridis')

# Añadir etiquetas con porcentajes
total = len(rfm)
for i, v in enumerate(segment_counts.values):
    percentage = v / total * 100
    ax.text(i, v + 1, f"{percentage:.1f}%", ha='center', fontweight='bold')

plt.title('Segmentación de clientes por RFM', fontsize=16, fontweight='bold')
plt.xlabel('Segmento', fontsize=14)
plt.ylabel('Número de clientes', fontsize=14)
plt.xticks(rotation=45)
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.tight_layout()
plt.show()

# Gráfico de dispersión 3D para visualizar los tres componentes RFM
from mpl_toolkits.mplot3d import Axes3D

fig = plt.figure(figsize=(14, 10))
ax = fig.add_subplot(111, projection='3d')

# Colores por segmento
colores = {
    'Campeones': 'gold',
    'Leales': 'royalblue',
    'Potenciales': 'green',
    'Prometedores': 'purple',
    'Necesitan atención': 'orange',
    'En riesgo': 'red'
}

# Limitamos a una muestra para no saturar el gráfico
sample_size = min(500, len(rfm))
rfm_sample = rfm.sample(sample_size, random_state=42)

for segmento, color in colores.items():
    segmento_data = rfm_sample[rfm_sample['Segmento'] == segmento]
    ax.scatter(
        segmento_data['Recencia'],
        segmento_data['Frecuencia'],
        segmento_data['Monetario'],
        c=color,
        s=40,
        label=segmento,
        alpha=0.7
    )

ax.set_xlabel('Recencia (días)', fontsize=12)
ax.set_ylabel('Frecuencia (compras)', fontsize=12)
ax.set_zlabel('Monetario ($)', fontsize=12)
ax.set_title('Visualización 3D de segmentos RFM', fontsize=16, fontweight='bold')
plt.legend(title='Segmentos')
plt.tight_layout()
plt.show()# -*- coding: utf-8 -*-
