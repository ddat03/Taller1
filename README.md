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


2.2 Análisis Detallado por Campo

InvoiceNo
•Identificador alfanumérico único para cada transacción
•Permite rastrear todas las líneas de una misma factura
•Total de 23,796 facturas únicas

StockCode
•3,938 códigos únicos de productos
•Permite identificar artículos específicos en el inventario
•Códigos consistentes a través de diferentes transacciones

Description
•Descripciones textuales de los productos
•1,454 valores faltantes (0.27% del total)
•Incluye principalmente artículos decorativos, productos para el hogar y artículos de temporada (especialmente navideños)

Quantity
•Rango: -80,995 a 80,995 unidades
•Media: 10.04 unidades
•Mediana: 3 unidades (significativamente menor que la media)
•Desviación estándar: 217.61 (alta variabilidad)
•Valores negativos: Representan devoluciones de productos, ajustes contables o correcciones de errores

InvoiceDate
Contiene fecha y hora de cada transacción
•Muestra patrones claros de actividad comercial:
oPicos durante horas laborales (especialmente 12:00 y 15:00)
oActividad mínima antes de las 8:00 y después de las 18:00
oMayor volumen en temporada navideña (octubre-diciembre)
oDía 9 de diciembre muestra actividad particularmente alta

UnitPrice
•Media: 4.69 unidades monetarias
•Mediana: 2.10 unidades monetarias
•Valor máximo: 38,970 unidades monetarias
•Sesgo: Positivo muy pronunciado (205.86)
•Curtosis: Extremadamente alta (63,568)
•La mayoría de productos tienen precios bajos, con pocos artículos premium


CustomerID
•135,080 valores faltantes (aproximadamente 25% del total)
•Permite seguimiento de compras por cliente
•Segmentación según análisis RFM (Recencia, Frecuencia, Monto):
o28.5% "Campeones" (clientes de alto valor)
o19.5% "Necesitan atención"
o14.2% "Leales"
o13.8% "Prometedores"
o12.5% "Potenciales"
o11.5% "En riesgo"


Country
•38 países diferentes registrados
•Reino Unido domina con 482,548 transacciones (91.3%)
•Negocio con presencia internacional pero fuertemente centrado en mercado británico

3. Metadata Generada
3.1 Metadata Estructural
•Dimensiones: 541,900 registros × 8 columnas
•Tipos de datos:
oStrings: InvoiceNo, StockCode, Description, Country
oNuméricos: Quantity, UnitPrice
oFecha/hora: InvoiceDate
oID: CustomerID

•Valores únicos:
o23,796 facturas únicas
o3,938 códigos de producto
o7 tipos de transacción (predomina "VENTA" con 512,169 registros)
o38 países

3.2 Metadata de Calidad de Datos

•Completitud:
oColumnas principales de transacción: ~100% (InvoiceNo, StockCode, Quantity, InvoiceDate, UnitPrice)
oDescription: 99.73% (1,454 faltantes)
oCustomerID: 75% (135,080 faltantes)
oCountry: 100%

•Consistencia:
oPresencia de valores negativos en Quantity (indicando devoluciones)
oVariabilidad significativa en cantidades y precios

•Valores atípicos:
oCantidades extremadamente altas (máximo 80,995)
oPrecios unitarios muy elevados (máximo 38,970)
oImporte total máximo: 168,469 unidades monetarias

3.3 Metadata Estadística
•Quantity:
oMedia: 10.04
oMediana: 3
oDesviación estándar: 217.61
oSesgo: -0.12 (ligera asimetría hacia la izquierda)
oCurtosis: 123,766 (extremadamente alta)

•UnitPrice:
oMedia: 4.69
oMediana: 2.10
oDesviación estándar: 95.14
oSesgo: 205.86 (muy pronunciado)


3.4 Metadata de Correlación
•Correlación fuerte (0.90) entre Quantity e Importe Total
•Correlación negativa (-0.18) entre UnitPrice e Importe Total
•Correlaciones débiles entre variables temporales y métricas de ventas


3.5 Metadata de Sesgo y Distribución
•Quantity: Distribución con colas muy pesadas y valores atípicos frecuentes
•UnitPrice: Distribución extremadamente asimétrica con larga cola hacia valores altos
•Importe Total: Consistente con un negocio donde la mayoría de transacciones son pequeñas pero existen algunas compras de valor extremadamente alto
•Variables temporales: Distribuciones más planas que la normal (curtosis negativas)


4. Visualizaciones y su Interpretación
4.1 Productos con Mayores Tasas de Devolución

<img width="541" alt="image" src="https://github.com/user-attachments/assets/5ee15bda-5775-40c4-8f91-0ecaa64d44ed" />

<img width="553" alt="image" src="https://github.com/user-attachments/assets/3b631394-02de-4f8c-ae34-6502ad05f302" />

4.2 Distribución de Ventas por Hora del Día

![image](https://github.com/user-attachments/assets/db94795a-9582-46de-aaa7-1be9ee25cecd)

4.3 Segmentación de Clientes (RFM)

![image](https://github.com/user-attachments/assets/f76fe2ac-c7f1-448d-93be-3eb5e2ce15dc)

![image](https://github.com/user-attachments/assets/7a479cdf-ba5c-42ed-b80d-c765825651c6)

4.4 Estacionalidad de Ventas (Mensual)

![image](https://github.com/user-attachments/assets/86a4be32-224b-41f6-95c3-5e93a01cb27f)


7. Conclusiones
Perfil de negocio claramente definido: Los datos revelan una empresa minorista especializada en artículos decorativos y productos para el hogar, con fuerte enfoque en artículos de temporada, especialmente navideños. Esta especialización se refleja tanto en los patrones de ventas como en la naturaleza de los productos más vendidos y devueltos.

Marcada estacionalidad: Existe un patrón estacional muy pronunciado con incremento significativo de ventas durante el último trimestre del año (octubre-diciembre). Esta temporalidad debería ser fundamental para la planificación estratégica de inventario, marketing y asignación de recursos.

Problemas críticos de calidad: Las elevadísimas tasas de devolución en ciertos productos (hasta 96.8% en muestras y más del 50% en productos navideños específicos) indican problemas graves
Concentración geográfica: A pesar de tener presencia en 38 países, más del 91% de las transacciones provienen del Reino Unido, lo que sugiere tanto una dependencia del mercado local como una oportunidad no aprovechada de expansión internacional.

Segmentación de clientes valiosa: La distribución relativamente equilibrada entre segmentos de clientes (con predominio de "Campeones" en 28.5%) ofrece oportunidades específicas para estrategias diferenciadas de retención, desarrollo y recuperación según el valor y comportamiento de cada grupo.
