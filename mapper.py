#!/usr/bin/env python3
import sys

for line in sys.stdin:
    line = line.strip()
    if not line:
        continue

    # Ignorar la cabecera
    if line.startswith("id,fecha_hora") or line.startswith('"id"'):
        continue

    campos = line.split(",")

    # Validar que la línea tenga las 8 columnas requeridas
    if len(campos) != 8:
        continue

    try:
        # Estructura del CSV: id, fecha_hora, tienda, categoria, producto, cantidad, precio_unitario, metodo_pago
        fecha_hora = campos[1].strip()
        categoria = campos[3].strip()
        cantidad = float(campos[5])
        precio_unitario = float(campos[6])

        # Extraer el mes de la fecha (YYYY-MM-DD HH:MM:SS)
        mes = fecha_hora.split("-")[1]
        ingreso = cantidad * precio_unitario

        # Clave: Categoria\tMes, Valor: Ingreso
        print(f"{categoria}\t{mes}\t{ingreso}")

    except Exception:
        # Ignorar líneas mal formadas sin truncar el job
        continue