# Localización Paraguaya para Odoo

## Descripción

Módulo de localización contable para Paraguay (`l10n_py`) que implementa los requisitos
fiscales y contables específicos del país.

## Características

### Gestión de Timbrados

- **Modelo de Autorización (Timbrado)**: Gestión completa de timbrados otorgados por la
  SET (Subsecretaría de Estado de Tributación)
- Control de fechas de vigencia
- Rango de numeración autorizada
- Establecimiento y punto de expedición
- Alertas de vencimiento
- Validación automática de disponibilidad

### Facturación

- **Campos específicos paraguayos en facturas**:

  - Número completo de factura (formato: 001-001-0000001)
  - Discriminación automática de IVA por alícuota (5%, 10%, Exento)
  - Total en letras (guaraníes)
  - Validación de timbrado obligatorio

- **Cálculos automáticos**:
  - Subtotal por alícuota (5%, 10%, exento)
  - IVA calculado por cada alícuota
  - Total de IVA

### RUC (Registro Único de Contribuyentes)

- Campo RUC en clientes y proveedores
- Validación de formato
- Dígito verificador
- Tipo de contribuyente (Persona Física, Jurídica, Extranjero)
- Búsqueda por RUC

### Impuestos

- **IVA 10%**: Alícuota estándar
- **IVA 5%**: Alícuota reducida
- **Exento**: Productos/servicios exentos de IVA

Configurados tanto para ventas como para compras.

## Instalación

1. Copiar el módulo `l10n_py` en el directorio de addons de Odoo
2. Actualizar la lista de módulos
3. Instalar el módulo "Paraguay - Accounting"

## Configuración Inicial

### 1. Configurar Timbrados

Ir a: **Contabilidad > Configuración > Timbrados**

Crear un nuevo timbrado con:

- Número de timbrado (8 dígitos)
- Fechas de inicio y vencimiento
- Rango de numeración autorizada
- Establecimiento (3 dígitos, ej: 001)
- Punto de expedición (3 dígitos, ej: 001)
- Tipo de documento

### 2. Configurar Clientes y Proveedores

Agregar el RUC en los contactos:

- Ir a **Contactos**
- Editar o crear un contacto
- Ingresar el RUC en el campo correspondiente
- Seleccionar el tipo de contribuyente

### 3. Configurar Productos con Impuestos

- Asignar los impuestos correctos a cada producto:
  - IVA 10% para productos gravados
  - IVA 5% para productos con alícuota reducida
  - Exento para productos sin IVA

## Uso

### Crear Factura de Venta

1. Crear nueva factura desde **Contabilidad > Clientes > Facturas**
2. Seleccionar cliente con RUC configurado
3. Agregar líneas de productos con sus respectivos impuestos
4. **Seleccionar el timbrado** antes de confirmar
5. Confirmar la factura

Al confirmar, el sistema:

- Valida que el timbrado sea vigente
- Asigna automáticamente el próximo número disponible
- Calcula la discriminación de IVA
- Genera el número completo de factura

### Ver Información Fiscal

En la factura confirmada, ir a la pestaña **"Información Fiscal Paraguay"** para ver:

- Discriminación de IVA (5%, 10%, exento)
- Subtotales por alícuota
- Total de IVA
- Información del timbrado
- Monto total en letras

## Estructura del Módulo

```
l10n_py/
├── __init__.py
├── __manifest__.py
├── models/
│   ├── __init__.py
│   ├── account_authorization.py   # Modelo de timbrados
│   ├── account_move.py             # Extensión de facturas
│   └── res_partner.py              # Extensión de contactos
├── views/
│   ├── account_authorization_views.xml
│   ├── account_move_views.xml
│   └── res_partner_views.xml
├── data/
│   ├── account_chart_template_data.xml
│   └── account_tax_group_data.xml
├── security/
│   └── ir.model.access.csv
└── README.md
```

## Permisos

- **Usuario de Facturación**: Puede ver timbrados
- **Gerente Contable**: Puede crear, editar y eliminar timbrados
- **Asesor Contable**: Solo lectura

## Validaciones Implementadas

### Timbrados

- Número de timbrado: 8 dígitos numéricos
- Establecimiento y punto de expedición: 3 dígitos numéricos
- Rango de numeración válido
- Fechas coherentes (inicio < vencimiento)

### Facturas

- Timbrado obligatorio para facturas de venta
- Timbrado debe estar vigente
- Número de factura dentro del rango autorizado
- Número de factura único por timbrado

### RUC

- Entre 7 y 9 dígitos (incluyendo dígito verificador)
- Solo caracteres numéricos
- RUC único por contacto

## Limitaciones Conocidas

- La conversión a letras está implementada de forma básica
- No incluye integración con SIFEN (pendiente para futuras versiones)
- No incluye generación automática de reportes fiscales

## Roadmap

### Versión 1.1 (Planeada)

- Mejora en conversión de números a letras
- Reportes fiscales adicionales
- Datos demo

### Versión 2.0 (Futuro)

- Integración con SIFEN
- Facturación electrónica
- Libros fiscales electrónicos

## Soporte

Para reportar issues o solicitar características:

- GitHub: https://github.com/kmee

## Licencia

LGPL-3

## Autores

- KMEE

## Versión

- **Versión actual**: 17.0.1.0.0
- **Compatible con Odoo**: 17.0
- **Fecha de release**: 2025
