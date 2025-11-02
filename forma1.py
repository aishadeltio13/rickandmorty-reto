# Forma 1: usando los conocmientos de clase

import os, psycopg, requests

url = os.getenv("DATABASE_URL")
connection = psycopg.connect(url)
cur = connection.cursor()
print("BD conectada con éxito")

# Crear tabla characters
def createTableCharacters():
    try:
        query = """CREATE TABLE characters (
                            id INTEGER PRIMARY KEY,
                            name TEXT,
                            status TEXT,
                            species TEXT,
                            type TEXT,
                            gender TEXT,
                            origin_name TEXT,
                            location_name TEXT,
                            image TEXT,
                            url TEXT,
                            created TIMESTAMPTZ
                        );"""
        cur.execute(query)
        connection.commit()
        print("Tabla characters creada")
    except Exception as e :
        print('Error creando la tabla characters' , e)

    # createTableCharacters()

# Petición get para obtener datos de la API pública
def obtenerAPI():
    try:
        url = "https://rickandmortyapi.com/api/character"
        response = requests.get(url)
        data = response.json()
        print("Se pudo conectar con la API")
        return data
    except:
        print("No se pudo conectar con la API")
        return None
        
data = obtenerAPI()

# Los datos los tenemos guardados en la variable "data"

# Verificar que se trata de un diccionario y ver sus keys para saber de donde extraer los datos.
def inspeccionar_data(data):
    print(f"Tipo de 'data': {type(data)}")
    if isinstance(data, dict):
        print("Es un diccionario. Claves disponibles:")
        print(list(data.keys()))

# inspeccionar_data(data) Diccionario: ['info', 'results'].

# Extraer la informacion en forma de lista.
def extraer_personajes(data):
    resultados = []
    for p in data["results"]:
        personaje = {
            "id": p["id"],
            "name": p["name"],
            "status": p["status"],
            "species": p["species"],
            "type": p["type"],
            "gender": p["gender"],
            "origin.name": p["origin"]["name"],
            "location.name": p["location"]["name"],
            "image": p["image"],
            "url": p["url"],
            "created": p["created"]
        }
        resultados.append(personaje)

    return resultados

    # personajes = extraer_personajes(data)

# Insertar personajes en la tabla characters. Utilizamos el "id" extraido de la API
def insertar_characters(personajes):
    try:
        query = """
        INSERT INTO characters (id, name, status, species, type, gender, origin_name, location_name, image, url, created ) 
        VALUES (%s,%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        for p in personajes:
            params = (
                p['id'],
                p['name'], 
                p['status'], 
                p['species'], 
                p['type'],
                p['gender'], 
                p['origin.name'], 
                p['location.name'], 
                p['image'],
                p['url'], 
                p['created']
            )
            cur.execute(query, params)
        connection.commit()
        print("¡Éxito! Todos los personajes fueron guardados.")

    except Exception as e:
        print(f"ERROR: {e}")
      
    # insertar_characters(personajes)

# Ver la tabla junto con sus datos:
cur.execute("SELECT id, name, species FROM characters LIMIT 10;")
    # print(cur.fetchall())


# Cerrar conexión y cursor
cur.close()
connection.close()

