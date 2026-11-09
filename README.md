# examen
**Matrícula:** <125053130>
Explica la diferencia entre los modos standalone, pseudo-distribuido y totalmente distribuido de Hadoop. ¿En cuál de ellos se usa HDFS?
Standalone es una computadora sin HDFS.
Pseudo-distribuido: una computadora hace varios procesos, con HDFS.
Totalmente distribuido: varias computadoras trabajando juntas, con HDFS.

(3 pts) ¿Por qué el dataset se monta como volumen y no se copia dentro de la imagen con COPY? Menciona al menos dos razones.
Para editar datos y que no afecte a la imagen y ahorran espacio
(3 pts) ¿Qué ocurre con los datos de la base de datos al ejecutar docker compose down? ¿Y con docker compose down -v?
docker compose down no elimina losmvolumenes y docker compose down -v elimina todo

(3 pts) ¿Por qué MapReduce no siempre es más rápido que un script secuencial con un archivo de 400 MB? ¿A partir de qué condiciones conviene?
porque mapreduce distribuye el trabajo, y el script es mas rapido para volumenes no tan pesados
(3 pts) Diferencia entre CMD y ENTRYPOINT, y entre COPY y ADD.
CMD es como decirle a Docker que cuando inicie, ejecute “tal"
ENTRYPOINT es lo que siempre va a ejecutar
COPY = Copiar archivos
ADD = Agregar archivos 

# Entrar al contenedor
docker exec -it hadoop-standalone bash

# Dar permisos a los scripts de MapReduce
chmod 755 mapreduce/mapper.py mapreduce/reducer.py

# Ejecutar el Job de Hadoop Streaming
hadoop jar /opt/hadoop/share/hadoop/tools/lib/hadoop-streaming-3.3.6.jar \
  -input ventas_125053130.csv \
  -output output_mapreduce \
  -mapper mapreduce/mapper.py \
  -reducer mapreduce/reducer.py \
  -file mapreduce/mapper.py \
  -file mapreduce/reducer.py

# Ver los resultados generados
cat output_mapreduce/part-00000 | head -n 20
# Ejecutar el script de ingesta a la base de datos SQLite
python scripts/cargar_resultados.py

# La API REST estará disponible en localhost:8000
# Probar endpoints:
# GET General: http://localhost:8000/resultados
# GET Filtro por categoría: http://localhost:8000/resultados/Abarrotes
[Ver archivo de evidencias en PDF](evidencias/evidencias.pdf)