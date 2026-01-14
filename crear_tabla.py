import psycopg2

# HE PUESTO TU URL AQUÍ ABAJO ENTRE COMILLAS. NO LA TOQUES.
URL_RENDER = "postgresql://weekender_db_user:r0e7ddT6GHAfVdxaQx5FpvUKo4ieWcc1@dpg-d5h8pjer433s73bk5cig-a.frankfurt-postgres.render.com/weekender_db"

def crear_la_tabla():
    try:
        print("🔌 Conectando a Render...")
        # Nos conectamos a la nube
        conn = psycopg2.connect(URL_RENDER)
        cursor = conn.cursor()
        
        print("🔨 Creando la tabla 'chat_logs'...")
        # Esta es la orden SQL
        sql_command = """
        CREATE TABLE IF NOT EXISTS chat_logs (
            id SERIAL PRIMARY KEY,
            fecha DATE DEFAULT CURRENT_DATE,
            hora TIME DEFAULT CURRENT_TIME,
            pregunta TEXT,
            respuesta TEXT
        );
        """
        
        # Ejecutamos la orden
        cursor.execute(sql_command)
        
        # Guardamos los cambios (Commit)
        conn.commit()
        
        # Cerramos conexión
        cursor.close()
        conn.close()
        print("✅ ¡ÉXITO! La tabla ha sido creada correctamente en la nube.")
        
    except Exception as e:
        print("❌ ERROR. Algo falló:")
        print(e)

if __name__ == "__main__":
    crear_la_tabla()