#!/usr/bin/env python3
import sys

current_key = None
current_sum = 0.0

for line in sys.stdin:
    line = line.strip()
    if not line:
        continue

    partes = line.split("\t")
    if len(partes) != 3:
        continue

    categoria, mes, ingreso_str = partes

    try:
        ingreso = float(ingreso_str)
    except ValueError:
        continue

    key = f"{categoria}\t{mes}"

    if current_key == key:
        current_sum += ingreso
    else:
        if current_key:
            cat_out, mes_out = current_key.split("\t")
            print(f"{cat_out}\tMes {mes_out}\t{current_sum:.2f}")
        current_key = key
        current_sum = ingreso

if current_key:
    cat_out, mes_out = current_key.split("\t")
    print(f"{cat_out}\tMes {mes_out}\t{current_sum:.2f}")