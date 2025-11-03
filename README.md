# **Apuntes: Reto Rick and Morty (Python + Postgres + Docker)**
Ha sido un reto de backend muy completo. He montado un servicio entero que consume una API, guarda los datos en una base de datos y expone mi propia API, todo 'dockerizado'.
## **El Stack que usé**
- Python: Para todo el scripting y la lógica de la API.
- PostgreSQL: Mi base de datos, corriendo en un contenedor.
- Flask: Para crear mi propio servidor web y el endpoint /species.
- Docker: Para gestionar el entorno de la app (app) y la base de datos (db) con docker-compose.yml.
## **Pasos Clave del Proceso**
1. Conexión (Paso 1):

   Conecté mi script de Python a la base de datos Postgres usando la librería psycopg (versión 3). La URL de la base de datos la leí de forma segura desde la variable de entorno DATABASE\_URL.

1. Creación de Tabla (Paso 2):

   Definí la estructura de la base de datos. Creé una tabla (characters2) usando CREATE TABLE IF NOT EXISTS para que el script no fallara si lo ejecutaba varias veces.

1. Poblado de Datos (Paso 3):

   Usé requests para hacer peticiones GET a la API de Rick and Morty. Manejé la paginación para descargar los datos. Usé cur.executemany() para insertar la lista de personajes en la base de datos de forma eficiente.

1. Creación de mi API (Paso 4):

   Monté un servidor web simple con Flask. Creé el endpoint /species que, al ser llamado, ejecuta una consulta SQL (SELECT species, COUNT(\*) ... GROUP BY species) contra mi base de datos characters2. Devolví los resultados como un JSON.
## **Problemas y Soluciones**
- ERR\_CONNECTION\_REFUSED:

  El error más persistente. Mi servidor Flask funcionaba, pero mi navegador no podía acceder a él.\
  Solución: El problema era de Docker. No había conectado el puerto de mi máquina (localhost:5000) con el puerto del contenedor (5000). Lo arreglé añadiendo ports: ["5000:5000"] al servicio app en mi docker-compose.yml.

- 'Solo se guardan 20 personajes':

  Mi script de poblado solo descargaba la primera página.\
  Solución: El script leía la variable de entorno RM\_PAGES. Como no estaba definida, usaba '1' por defecto. Lo solucioné añadiendo RM\_PAGES=42 (el total de páginas) a mi archivo .env. Al reiniciar Docker, el script leyó la variable y descargó los 826 personajes.

- Errores SQL ('La tabla no existe'):

  A veces me daba error de que la tabla characters no existía.\
  Solución: Fue un simple despiste. Había llamado a mi tabla characters2 pero en la función get\_species (y en mis comprobaciones) a veces escribía characters. Tuve que revisar y estandarizar todo a characters2.

- Orden de Ejecución:

  Mi API fallaba al inicio porque la tabla no existía o estaba vacía.\
  Solución: Organicé el bloque if \_\_name\_\_ == '\_\_main\_\_': en mi app.py. Ahora, antes de lanzar el servidor (app.run()), el script se conecta, ejecuta createTableCharacters() y populate\_characters() en orden.
