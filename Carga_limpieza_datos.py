
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 10 08:30:18 2025

@author: DIEGO
"""

import pandas as pd
import numpy as np
from sqlalchemy import create_engine


# Cargar los datos
# Asumimos que el archivo está en formato CSV. Ajusta la ruta según sea necesario
def cargar_y_limpiar_datos(ruta_archivo):
    df = pd.read_excel('C:/Users/DIEGO/OneDrive/Escritorio/Maestria Ciencia de datos/Fundamentos de ciencia de datos/Taller1/Online Retail.xlsx')
  
    # Mostrar información general del dataset
    print("\nInformación general del dataset original:")
    print(f"Filas: {df.shape[0]}, Columnas: {df.shape[1]}")
    print("\nColumnas en el dataset:")
    print(df.columns.tolist())
    
    # Mostrar primeras filas
    print("\nPrimeras 5 filas del dataset:")
    print(df.head())
    
    # Comprobar valores faltantes
    print("\nValores faltantes por columna:")
    print(df.isnull().sum())
    
    # Estadísticas básicas
    print("\nEstadísticas básicas:")
    print(df.describe())
    
    return df

def procesar_datos(df):
    # Hacer una copia para no modificar el original
    df_limpio = df.copy()
    
    # Manejo de CustomerID NaN - Crear campo para indicar si es cliente registrado
    
    df_limpio['CustomerID'] = np.where(df_limpio['CustomerID'].isna(), 'NO_REGISTRADO', df_limpio['CustomerID'])

    #Condiciones para describir que tipo de transaccione es cada valor

    condiciones = [
    # Condición para identificar comisiones
    df_limpio['Description'].str.contains('amazon|Amazon|AMAZON|fee|Comission', case=False, na=False),
    
    # Condición para identificar ajustes
    df_limpio['Description'].str.contains('adjust|ADJUST|bad debt', case=False, na=False),
    
    # Condición para identificar envíos
    df_limpio['Description'].str.contains('postage|POSTAGE|shipping|SHIPPING|carriage', case=False, na=False),
    
    df_limpio['Description'].str.contains('manual|MANUAL|Manual', case=False, na=False),
    
    df_limpio['Description'].str.contains('BANK|bank|discount', case=False, na=False),

    
    # Condición para devoluciones (cantidad negativa)
    df_limpio['Quantity'] < 0,
    
    # Condición por defecto para ventas normales
    df_limpio['Quantity'] > 0
]
    categorias = [
    'COMISION',
    'AJUSTE',
    'ENVIO',
    'AJUSTE MANUAL',
    'DESCUENTOS BANCARIOS',
    'DEVOLUCION',
    'VENTA'
]
    
    df_limpio['Tipo_Transaccion'] = np.select(condiciones, categorias, default='OTROS')
    
    
    
    # Verificamos valores negativos o cero en UnitPrice
    precio_invalido = (df_limpio['UnitPrice'] <= 0)
    if precio_invalido.any():
        print(f"\nSe encontraron {precio_invalido.sum()} registros con precios inválidos (<=0)")
        # Puedes decidir si eliminarlos o marcarlos
        df_limpio = df_limpio[~precio_invalido]  # Para eliminarlos
    
    #Separaramos de formato fecha en Ano, mes, dia, hora y minutos
    df_limpio['Mes'] = df_limpio['InvoiceDate'].dt.month
    df_limpio['Ano'] = df_limpio['InvoiceDate'].dt.year
    df_limpio['Dia'] = df_limpio['InvoiceDate'].dt.day
    df_limpio['Hora'] = df_limpio['InvoiceDate'].dt.hour
    df_limpio['Minutos'] = df_limpio['InvoiceDate'].dt.minute

    # Definimos las columnas para buscar duplicados
    columnas_duplicados = ['InvoiceDate', 'UnitPrice', 'CustomerID', 'Description']

    # Encontrar los duplicados basados en estas columnas
    duplicados = df_limpio.duplicated(subset=columnas_duplicados, keep=False)

    # Filtramos el dataframe para obtener solo los registros duplicados
    df_duplicados = df_limpio[duplicados].sort_values(by=columnas_duplicados)
    #creamos una copia de la lista con un nuevo ordenamiento  de variables
    columnas =  ['InvoiceNo', 'StockCode', 'Description', 'InvoiceDate' ]
    df_consolidado = df_limpio.groupby(columnas).agg({
        'Quantity': 'sum',
        'UnitPrice': 'first',
        'CustomerID': 'first',
        'Hora': 'first',
        'Minutos': 'first',
        'Dia': 'first',
        'Mes': 'first',
        'Ano': 'first',
        'Tipo_Transaccion': 'first',# Mantenemos el primer código de stock
        'Country': 'first'
        
    }).reset_index()


    # Calculamos el importe total después de consolidar el nuevo orden
    df_consolidado['Importe Total'] = df_consolidado['Quantity'] * df_consolidado['UnitPrice']
        
    #El dataframe df_limpio ha sido actualizado con los datos consolidados
    df_limpio = df_consolidado.copy()
    #Eliminamos formato fecha completa
    df_limpio = df_limpio.drop('InvoiceDate', axis=1)  
    df_limpio = df_limpio.reset_index(drop=True)
   
    return df_limpio



def guardar_datos_limpios(df, ruta_salida):
    """Guardar el dataframe limpio en un archivo CSV y en una base de datos SQLite."""
    # Guardar como CSV
    df.to_csv(ruta_salida.replace('.db', '.csv'), index=False)
    print(f"\nDatos limpios guardados en: {ruta_salida.replace('.db', '.csv')}")
    
    
    # Creamos una conexión a la base de datos
    engine = create_engine(f'sqlite:///{ruta_salida}')
    
    # Guardamos el DataFrame en la base de datos
    df.to_sql('retail_data', engine, if_exists='replace', index=False)
    
    print(f"Datos limpios guardados en base de datos: {ruta_salida}")

def main():
    # Ruta del archivo (ajustar según sea necesario)
    ruta_archivo = "online_retail.csv"
    ruta_salida = "online_retail_limpio.db"
    
    try:
        # Cargar datos
        df_original = cargar_y_limpiar_datos(ruta_archivo)
        

        # Procesar y limpiar datos
        df_limpio = procesar_datos(df_original)
        
        
        # Guardar datos limpios
        guardar_datos_limpios(df_limpio, ruta_salida)
        
        print("\nProceso completado exitosamente.")
        
    except Exception as e:
        print(f"Error durante el procesamiento: {e}")

if __name__ == "__main__":
    main()
    
    