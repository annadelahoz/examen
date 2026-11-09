#######
import pandas as pd
print("cargando dataset y calculando resultados")
df = pd.read_csv("ventas_125053130.csv")
#cambio de formato a datetime
df["fecha_hora"] = pd.to_datetime(df["fecha_hora"])
#
df["ingreso"] = df["cantidad"] * df["precio_unitario"]
df["mes"] = df["fecha_hora"].dt.month
resultado = df.groupby(["categoria", "mes"])["ingreso"].sum().reset_index()
print("ingreso total por categoria y mes")
print(resultado.to_string(index=False))
resultado.to_csv("pregunta_negocio.csv", index=False)
print("\nResultado guardado en 'pregunta_negocio.csv'")