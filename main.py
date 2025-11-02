import os, psycopg

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

createTableCharacters()
