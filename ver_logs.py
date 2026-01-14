import psycopg2
import os
from dotenv import load_dotenv

# Cargar variables de entorno (.env) para no poner la clave a mano
load_dotenv()

# Si por lo que sea no lee el .env, usa la URL que tenías en crear_tabla.py
# URL_RENDER = "postgresql://weekender_db_user:..." 
URL_RENDER = os.getenv("DATABASE_URL")

def ver_historial():
    try:
        print("🔌 Conectando a la base de datos...")
        conn = psycopg2.connect(URL_RENDER)
        cursor = conn.cursor()
        
        # Consultamos todo lo que hay en la tabla
        print("🔍 Leyendo la tabla 'chat_logs'...\n")
        cursor.execute("SELECT id, fecha, hora, pregunta, respuesta FROM chat_logs ORDER BY id DESC LIMIT 5;")
        
        filas = cursor.fetchall()
        
        if not filas:
            print("📭 La tabla está vacía. Aún no se han guardado chats.")
        else:
            print(f"✅ Se encontraron {len(filas)} registros (Mostrando los últimos 5):")
            print("-" * 50)
            for fila in filas:
                _id, fecha, hora, preg, resp = fila
                print(f"ID: {_id} | {fecha} {hora}")
                print(f"👤 USUARIO: {preg}")
                print(f"🤖 WEEKENDER: {resp[:100]}...") # Solo mostramos los primeros 100 caracteres
                print("-" * 50)

        cursor.close()
        conn.close()
        
    except Exception as e:
        print("❌ Error al conectar o leer:")
        print(e)

if __name__ == "__main__":
    ver_historial()
    