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

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# Asumiendo que df es tu DataFrame con los datos
# Primero calculamos las ventas y devoluciones por producto (StockCode)

# Separamos ventas y devoluciones
ventas = df[df['Tipo_Transaccion'] == 'VENTA'].copy()
devoluciones = df[df['Tipo_Transaccion'] == 'DEVOLUCION'].copy()

# Convertimos las cantidades de devoluciones a valores positivos para el análisis
devoluciones['Quantity_Abs'] = devoluciones['Quantity'].abs()

# Agrupamos por código de producto
ventas_por_producto = ventas.groupby('StockCode')['Quantity'].sum().reset_index()
ventas_por_producto.columns = ['StockCode', 'Cantidad_Vendida']

devoluciones_por_producto = devoluciones.groupby('StockCode')['Quantity_Abs'].sum().reset_index()
devoluciones_por_producto.columns = ['StockCode', 'Cantidad_Devuelta']

# Unimos los DataFrames
analisis_productos = pd.merge(ventas_por_producto, devoluciones_por_producto, 
                             on='StockCode', how='left')

# Rellenamos los NaN con 0 (productos que no tienen devoluciones)
analisis_productos['Cantidad_Devuelta'] = analisis_productos['Cantidad_Devuelta'].fillna(0)

# Calculamos la tasa de devolución
analisis_productos['Tasa_Devolucion'] = (analisis_productos['Cantidad_Devuelta'] / 
                                       (analisis_productos['Cantidad_Vendida'] + 
                                        analisis_productos['Cantidad_Devuelta'])) * 100

# Añadimos las descripciones de los productos
descripciones = df[['StockCode', 'Description']].drop_duplicates()
analisis_productos = pd.merge(analisis_productos, descripciones, on='StockCode', how='left')

# AQUÍ EXCLUIMOS LOS PRODUCTOS CON CÓDIGOS ESPECÍFICOS
analisis_productos = analisis_productos[~analisis_productos['StockCode'].isin(['80995', '78033'])]

# Filtramos para productos con un mínimo de ventas + devoluciones para evitar casos atípicos
min_transacciones = 20  # Ajusta este valor según necesites
analisis_productos = analisis_productos[(analisis_productos['Cantidad_Vendida'] + 
                                      analisis_productos['Cantidad_Devuelta']) >= min_transacciones]

analisis_productos = analisis_productos[~analisis_productos['StockCode'].isin(['23843', '23166', '84347'])]
# Tomamos los 10 productos con mayor tasa de devolución
top_10_devoluciones = analisis_productos.sort_values('Tasa_Devolucion', ascending=False).head(10)

# Creamos un nombre abreviado para mostrar en el gráfico
top_10_devoluciones['Nombre_Corto'] = top_10_devoluciones['Description'].str.slice(0, 20) + '...'
top_10_devoluciones['Nombre_Corto'] = top_10_devoluciones['Nombre_Corto'] + ' (' + top_10_devoluciones['StockCode'] + ')'

# Ordenamos por tasa de devolución
top_10_devoluciones = top_10_devoluciones.sort_values('Tasa_Devolucion')

# Creamos el gráfico
plt.figure(figsize=(12, 8))
bar_width = 0.8

# Creamos las barras apiladas
plt.barh(top_10_devoluciones['Nombre_Corto'], 
        top_10_devoluciones['Cantidad_Vendida'], 
        color='#2c7fb8', 
        label='Vendidos', 
        alpha=0.8, 
        height=bar_width)

plt.barh(top_10_devoluciones['Nombre_Corto'], 
        top_10_devoluciones['Cantidad_Devuelta'], 
        left=top_10_devoluciones['Cantidad_Vendida'], 
        color='#d73027', 
        label='Devueltos', 
        alpha=0.8, 
        height=bar_width)

# Añadimos la tasa de devolución como texto en las barras
for i, row in enumerate(top_10_devoluciones.itertuples()):
    plt.text(row.Cantidad_Vendida + row.Cantidad_Devuelta + 5, 
             i, 
             f"{row.Tasa_Devolucion:.1f}%", 
             va='center', 
             fontweight='bold')

# Personalización del gráfico
plt.title('Productos con Mayor Tasa de Devolución (excluyendo códigos 80995 y 78033)', fontsize=16, pad=20)
plt.xlabel('Cantidad de Unidades', fontsize=12)
plt.ylabel('Producto', fontsize=12)
plt.grid(axis='x', linestyle='--', alpha=0.7)
plt.legend(loc='upper right')

# Ajustamos los márgenes
plt.tight_layout()

# Guardamos la imagen
plt.savefig('productos_mayor_tasa_devolucion.png', dpi=300, bbox_inches='tight')

# Mostramos el gráfico
plt.show()