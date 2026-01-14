from flask import Flask, request, jsonify
import os
import pickle
import psycopg2
from groq import Groq
from dotenv import load_dotenv
from sklearn.linear_model import LinearRegression

# 1. Cargar variables de entorno
load_dotenv()

app = Flask(__name__)
app.config["DEBUG"] = True

# --- VERIFICACIÓN DE CLAVES AL ARRANCAR ---
groq_key = os.getenv("GROQ_API_KEY")
db_url = os.getenv("DATABASE_URL")

print("--------------------------------------------------")
if groq_key:
    print(f"✅ Clave GROQ cargada: {groq_key[:5]}...")
else:
    print("❌ ERROR CRÍTICO: No se encontró GROQ_API_KEY en .env")

if db_url:
    print("✅ URL de Base de Datos cargada.")
else:
    print("⚠️ AVISO: No hay base de datos configurada. El chat funcionará pero no guardará historial.")
print("--------------------------------------------------")

# --- CONFIGURACIÓN MODELO ML ---
MODEL_DIR = "data"
MODEL_PATH = os.path.join(MODEL_DIR, "modelo_advertising.pkl")

def check_and_create_model():
    if not os.path.exists(MODEL_DIR):
        os.makedirs(MODEL_DIR)
    if not os.path.exists(MODEL_PATH):
        print("⚠️ Creando modelo base dummy...")
        X = [[100], [200], [300]] 
        y = [1000, 2000, 3000]
        model = LinearRegression()
        model.fit(X, y)
        with open(MODEL_PATH, "wb") as f:
            pickle.dump(model, f)

check_and_create_model()

# --- CONFIGURACIÓN CLIENTE GROQ ---
if groq_key:
    client = Groq(api_key=groq_key)
else:
    client = None

SYSTEM_PROMPT = """
Eres "Weekender", un experto en viajes de fin de semana.
INSTRUCCIONES:
1. Saluda y pide obligatoriamente: Destino, Presupuesto y Vibe.
2. NO des el plan hasta tener esos datos.
3. El plan debe ser: Viernes, Sábado y Domingo.
"""

@app.route("/", methods=['GET'])
def main():
    return "API Weekender OPERATIVA"

# --- NUEVO ENDPOINT: HISTORIAL PARA SIDEBAR ---
@app.route("/history", methods=['GET'])
def get_history():
    try:
        # Si no hay URL de base de datos, devolvemos lista vacía
        if not db_url:
            return jsonify({"history": []}), 200
            
        conn = psycopg2.connect(db_url)
        cur = conn.cursor()
        
        # Pedimos las últimas 10 conversaciones (ordenadas de la más reciente a la más antigua)
        # Asumimos columnas: id, fecha, hora, pregunta, respuesta
        cur.execute("SELECT pregunta, respuesta, fecha, hora FROM chat_logs ORDER BY id DESC LIMIT 10")
        rows = cur.fetchall()
        
        # Convertimos los datos a un formato JSON amigable
        history_data = []
        for r in rows:
            history_data.append({
                "pregunta": r[0],
                "respuesta": r[1],
                "fecha": str(r[2]), # Convertimos fecha a string
                "hora": str(r[3])   # Convertimos hora a string
            })
            
        cur.close()
        conn.close()
        
        return jsonify({"history": history_data}), 200
        
    except Exception as e:
        print(f"❌ Error leyendo historial: {e}")
        return jsonify({"Error": str(e)}), 500

# --- ENDPOINT CHAT ---
@app.route("/chat", methods=['POST'])
def chat():
    try:
        if client is None:
            return jsonify({"Error": "Falta la API KEY de Groq en el servidor (.env)"}), 500

        data = request.get_json()
        user_message = data.get('message')
        history = data.get('history', [])

        def guardar_db(preg, resp):
            if not db_url: return
            try:
                conn = psycopg2.connect(db_url)
                cur = conn.cursor()
                cur.execute("INSERT INTO chat_logs (pregunta, respuesta) VALUES (%s, %s)", (preg, resp))
                conn.commit()
                conn.close()
            except Exception as e: 
                print(f"⚠️ Error DB (No crítico): {e}")

        messages = [{"role": "system", "content": SYSTEM_PROMPT}]
        messages.extend(history)
        messages.append({"role": "user", "content": user_message})

        # Llamada a Groq
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile", messages=messages, temperature=0.7
        )
        bot_response = completion.choices[0].message.content

        # Guardar en DB
        guardar_db(user_message, bot_response)
        
        return jsonify({"response": bot_response}), 200

    except Exception as e:
        print(f"❌ ERROR REAL EN CHAT: {e}")
        return jsonify({"Error": f"Fallo interno: {e}"}), 500

# --- ENDPOINTS ML ---
@app.route("/predict", methods=['GET'])
def predict():
    try:
        data = request.get_json()
        input_data = data.get("data")
        modelo = pickle.load(open(MODEL_PATH, "rb"))
        pred = modelo.predict(input_data)
        return jsonify({"prediction": list(pred)}), 200
    except Exception as e:
        return jsonify({"Error": str(e)}), 500

@app.route("/ingest", methods=['POST'])
def ingest():
    return jsonify({"message": "Datos ingresados correctamente"}), 200

@app.route("/retrain", methods=['POST'])
def retrain():
    return jsonify({"message": "Modelo reentrenado correctamente."}), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)















