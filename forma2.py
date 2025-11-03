# Forma 2: usando la ayuda de la IA

# PASO 1: CONEXIÓN A LA BASE DE DATOS
import os, psycopg, requests

url = os.getenv("DATABASE_URL")
connection = psycopg.connect(url)
cur = connection.cursor()
print("BD conectada con éxito")

# PASO 2: CREACION TABLA "characters2"
def createTableCharacters():
    try:
        query = """CREATE TABLE characters2 (
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
    

# PASO 3: CONSUMIR LA API DE RICK AND MORTY.

def populate_characters():
    print("Iniciando la carga de datos desde la API...")
    
    # MIRAR SI LA API TIENE UNA O VARIAS PÁGINAS:
    try:
        # Lee la variable de entorno RM_PAGES
        pages_to_fetch_str = os.getenv("RM_PAGES")
        
        # Si no está definida o está vacía, carga solo 1. Si está, conviértela a int.
        if not pages_to_fetch_str:
            pages_to_fetch = 1
            print("Variable RM_PAGES no definida. Cargando solo 1 página.")
        else:
            pages_to_fetch = int(pages_to_fetch_str)
            print(f"Variable RM_PAGES detectada. Cargando {pages_to_fetch} páginas.")
            
    except ValueError:
        print(f"Error: RM_PAGES ('{pages_to_fetch_str}') no es un número válido. Cargando 1 página.")
        pages_to_fetch = 1
    except Exception as e:
        print(f"Error leyendo RM_PAGES: {e}. Cargando 1 página.")
        pages_to_fetch = 1

    
    # URL DE LA API
    next_page_url = "https://rickandmortyapi.com/api/character"
    
    # Esta lista guardará tuplas, una por cada personaje
    all_characters_to_insert = []

    try:
        # DESCARGAR LAS PÁGINAS
        for page_num in range(pages_to_fetch):
            if not next_page_url:
                print("No hay más páginas en la API. Deteniendo.")
                break # Salir del bucle si la API dice que no hay más páginas

            print(f"Descargando página {page_num + 1} de {pages_to_fetch}...")
            
            # PETICION GET
            response = requests.get(next_page_url)
            response.raise_for_status() # Lanza un error si la petición falla (ej. 404, 500)
            data = response.json()

            # PROCESAR LOS DATOS
            for char in data['results']:
                # Extraemos los campos anidados de forma segura
                origin_name = char.get('origin', {}).get('name', 'unknown')
                location_name = char.get('location', {}).get('name', 'unknown')
                
                # Creamos una tupla con los datos en el orden correcto
                character_tuple = (
                    char['id'],
                    char['name'],
                    char['status'],
                    char['species'],
                    char['type'],
                    char['gender'],
                    origin_name,
                    location_name,
                    char['image'],
                    char['url'],
                    char['created']
                )
                all_characters_to_insert.append(character_tuple)

            # Actualizamos la URL para la siguiente iteración del bucle
            next_page_url = data['info']['next'] 

        if not all_characters_to_insert:
            print("No se encontraron personajes para insertar.")
            return

        print(f"Datos de {len(all_characters_to_insert)} personajes listos para insertar.")

        # INSERTAR LOS DATOS EN LA BASE DE DATOS
        insert_query = """
            INSERT INTO characters2 (
                id, name, status, species, type, gender, 
                origin_name, location_name, image, url, created
            ) 
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (id) DO NOTHING; 
        """
        cur.executemany(insert_query, all_characters_to_insert)
        connection.commit()
        
        print(f"¡Éxito! {len(all_characters_to_insert)} personajes insertados/actualizados en la tabla 'characters2'.")

    except requests.exceptions.RequestException as e:
        print(f"Error al conectar con la API de Rick and Morty: {e}")
    except psycopg.Error as e:
        print(f"Error de base de datos al insertar datos: {e}")
        connection.rollback() # Revertir cambios si hay un error de BD
    except Exception as e:
        print(f"Ha ocurrido un error inesperado: {e}")
        connection.rollback()

populate_characters()
    
    
# PASO 4: COMPROBACION DE QUE EFECTIVAMENTE SE HAN GUARDADO LOS DATOS
cur.execute("SELECT id, name, species FROM characters2;")
print(cur.fetchall())


# PASO 5: CERRAR LA CONEXIÓN
connection.commit()
cur.close()
connection.close()

