Tema: Análisis del Dataset de Transacciones Comerciales

Resumen:
El presente informe analiza un conjunto de datos de transacciones comerciales que contiene información sobre 541,900 registros de ventas minoristas y mayoristas. El dataset consta de 8 columnas principales que incluyen información sobre facturas, productos, cantidades, precios, clientes y ubicaciones geográficas.

2. Descripción del Dataset
2.1 Estructura General
El set de datos consta de 8 columnas: InvoiceNo, StockCode, Description, Quantity, InvoiceDate, UnitPrice, CustomerID, Country y un total de 541,900 registros (filas).
Los datos indagados tienen datos de transacciones comerciales, probablemente ventas o facturas
En lo que se refiere a disponibilidad de datos, la mayoría de las columnas están completas (pocos valores faltantes en Description y CustomerID).
Datos de varios países, incluyendo Reino Unido según las primeras 5 filas, se asume que debe haber muchos más a primera vista.
Las variables numéricas, por ejemplo, Quantity tiene mínimo de -80995 y máximo de 80995, lo cual se considera de un amplio rango.
A primer informe se tiene 1,454 valores faltantes en la columna Description y tiene 135,080 valores faltantes en la columna CustomerID (aproximadamente un 25% del total)
No hay información sobre la naturaleza de los valores negativos en Quantity (posiblemente devoluciones)

Se pueden observar completitud en las columnas principales de transacción (InvoiceNo, StockCode, Quantity, UnitPrice), también:
•Diversidad de datos (variedad de países, productos y clientes)
•Volumen de datos (más de medio millón de registros)
•Información sobre fechas de facturación (InvoiceDate)
•Identificadores únicos para facturas, productos y clientes

Este parece ser un dataset de ventas minoristas y con poquísimas mayoristas con información completa sobre transacciones, aunque con ciertos vacíos en la identificación de clientes y descripciones de productos.
El conjunto de datos consta de 541,900 registros con 8 columnas principales:

<img width="518" alt="image" src="https://github.com/user-attachments/assets/cc1cb777-bc9b-44e5-99c4-73ec010d1cd3" />



