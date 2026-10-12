# l10n_py_libros/models/l10n_py_libro_serializer.py
"""Serialización posicional del Libro DNIT (CSV/TXT, sin cabecera).

FIELD_ORDER define, para cada tipo_registro, la orden exacta de campos del
layout oficial (19/20/15/18 campos para Ventas/Compras/Ingresos/Egresos).
"""

TIPO_REGISTRO_CODE = {
    "ventas": "1",
    "compras": "2",
    "ingresos": "3",
    "egresos": "4",
}

FIELD_ORDER = {
    "ventas": [  # 19 campos
        "tipo_registro_code",
        "f_tipo_identificacion",
        "f_numero_identificacion",
        "f_nombre_razon_social",
        "f_tipo_comprobante",
        "f_fecha_emision_fmt",
        "f_timbrado",
        "f_numero_comprobante",
        "f_monto_gravado_10",
        "f_monto_gravado_5",
        "f_monto_exento",
        "f_monto_total",
        "f_condicion",
        "f_moneda_extranjera",
        "f_imputa_iva",
        "f_imputa_ire",
        "f_imputa_irp_rsp",
        "f_comprobante_asociado_numero",
        "f_comprobante_asociado_timbrado",
    ],
    "compras": [  # 20 campos
        "tipo_registro_code",
        "f_tipo_identificacion",
        "f_numero_identificacion",
        "f_nombre_razon_social",
        "f_tipo_comprobante",
        "f_fecha_emision_fmt",
        "f_timbrado",
        "f_numero_comprobante",
        "f_monto_gravado_10",
        "f_monto_gravado_5",
        "f_monto_exento",
        "f_monto_total",
        "f_condicion",
        "f_moneda_extranjera",
        "f_imputa_iva",
        "f_imputa_ire",
        "f_imputa_irp_rsp",
        "f_no_imputa",
        "f_comprobante_asociado_numero",
        "f_comprobante_asociado_timbrado",
    ],
    "ingresos": [  # 15 campos
        "tipo_registro_code",
        "f_tipo_comprobante",
        "f_fecha_emision_fmt",
        "f_numero_comprobante",
        "f_tipo_identificacion",
        "f_numero_identificacion",
        "f_nombre_razon_social",
        "f_monto_gravado",
        "f_monto_no_gravado_exonerado",
        "f_monto_total",
        "f_imputa_ire",
        "f_imputa_irp_rsp",
        "f_especificar_tipo_documento",
        "f_comprobante_asociado_numero",
        "f_comprobante_asociado_timbrado",
    ],
    "egresos": [  # 18 campos
        "tipo_registro_code",
        "f_tipo_comprobante",
        "f_fecha_emision_fmt",
        "f_numero_comprobante",
        "f_tipo_identificacion",
        "f_numero_identificacion",
        "f_nombre_razon_social",
        "f_monto_total",
        "f_imputa_iva",
        "f_imputa_ire",
        "f_imputa_irp_rsp",
        "f_no_imputa",
        "f_numero_cuenta",
        "f_banco",
        "f_empleador_ips",
        "f_especificar_tipo_documento",
        "f_comprobante_asociado_numero",
        "f_comprobante_asociado_timbrado",
    ],
}

PERIODO_CODES = {"208", "206"}


def get_field_value(line, field_name):
    """Return the serialized (string) value of one FIELD_ORDER entry."""
    if field_name == "tipo_registro_code":
        return TIPO_REGISTRO_CODE.get(line.tipo_registro, "")
    if field_name == "f_fecha_emision_fmt":
        if line.f_tipo_comprobante in PERIODO_CODES and line.f_periodo_mm_aaaa:
            return line.f_periodo_mm_aaaa
        if line.f_fecha_emision:
            return line.f_fecha_emision.strftime("%d/%m/%Y")
        return ""
    value = line[field_name]
    if value is False or value is None:
        return ""
    if isinstance(value, int):
        return str(value)
    return str(value)


def serialize_line(line):
    """Return the ordered list of string values for a libro line."""
    order = FIELD_ORDER[line.tipo_registro]
    return [get_field_value(line, field_name) for field_name in order]
