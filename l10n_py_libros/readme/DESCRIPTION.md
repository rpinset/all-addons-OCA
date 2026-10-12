Genera los cuatro registros de comprobantes exigidos por la RG 90/2021 de la
DNIT (Marangatu) para Paraguay: Ventas, Compras, Ingresos y Egresos.

El "libro" es un objeto persistido (cabecera + líneas) por empresa, tipo de
registro y período (obligación 955 mensual u obligación 956 anual). Las
líneas de Ventas/Compras se generan automáticamente a partir de las facturas
del período (con exclusión de los comprobantes ya aceptados en el SIFEN o
marcados como electrónicos por el proveedor); las líneas de Ingresos/Egresos
se cargan manualmente.

El módulo exporta un archivo CSV/TXT delimitado (coma o punto y coma) y su
respectivo ZIP homónimo, respetando el límite de 5.000 líneas por archivo y
la nomenclatura oficial de la DNIT.
