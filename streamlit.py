import streamlit as st
import requests

# 1. CONFIGURACIÓN DE PÁGINA
st.set_page_config(
    page_title="Weekender AI",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. ESTILOS CSS PERSONALIZADOS (El "Maquillaje")
def local_css():
    st.markdown("""
    <style>
    /* Importar fuente Google (Poppins) */
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600&display=swap');

    html, body, [class*="css"]  {
        font-family: 'Poppins', sans-serif;
    }

    /* Fondo general con degradado suave */
    .stApp {
        background: linear-gradient(to right top, #f0f2f6, #e2eafc);
    }

    /* Estilo de la Barra Lateral */
    [data-testid="stSidebar"] {
        background-color: #ffffff;
        border-right: 1px solid #e0e0e0;
    }

    /* Títulos */
    h1 {
        color: #2c3e50;
        font-weight: 600;
    }
    
    /* Botones personalizados */
    div.stButton > button {
        background-color: #FF4B4B;
        color: white;
        border-radius: 10px;
        border: none;
        padding: 0.5rem 1rem;
        transition: all 0.3s ease;
    }
    div.stButton > button:hover {
        background-color: #ff3333;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }

    /* Ocultar menú default de Streamlit y footer */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Cajas de sugerencia (Cards) */
    .suggestion-card {
        background-color: white;
        padding: 20px;
        border-radius: 15px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
        text-align: center;
        margin-bottom: 10px;
        transition: transform 0.2s;
    }
    .suggestion-card:hover {
        transform: scale(1.02);
        box-shadow: 0 6px 8px rgba(0,0,0,0.1);
    }
    </style>
    """, unsafe_allow_html=True)

local_css()

# 3. BARRA LATERAL (HISTORIAL)
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/201/201623.png", width=80)
    st.title("Historial de Viajes")
    st.caption("Tus planes guardados en la nube")
    
    if st.button("🔄 Refrescar Lista"):
        st.rerun()
    
    st.markdown("---")
    
    try:
        # Nota: Si usas Docker, cambia 127.0.0.1 por 'host.docker.internal' o el nombre del servicio
        response_hist = requests.get("http://127.0.0.1:8000/history")
        
        if response_hist.status_code == 200:
            data_hist = response_hist.json().get("history", [])
            
            if not data_hist:
                st.info("📭 Aún no tienes viajes guardados.")
            
            for item in data_hist:
                fecha = item.get('fecha', '')
                preg = item.get('pregunta', '')
                
                with st.expander(f"📍 {preg[:20]}... ({fecha})"):
                    st.markdown(f"**Tú:** {preg}")
                    st.success(f"**Weekender:** {item['respuesta'][:150]}...")
        else:
            st.error("⚠️ Error de conexión con el servidor.")

    except Exception:
        st.warning("Servidor desconectado (app.py)")

# 4. ZONA PRINCIPAL
col1, col2 = st.columns([1, 5])

with col1:
    # Un pequeño logo o emoji grande al lado del título
    st.markdown("# 🌍")

with col2:
    st.title("Weekender AI")
    st.markdown("### Tu diseñador de escapadas perfecto")

# 5. GESTIÓN DEL CHAT
if "messages" not in st.session_state:
    st.session_state.messages = []

# Si no hay mensajes, mostramos pantalla de bienvenida
if not st.session_state.messages:
    st.markdown("---")
    st.subheader("Sugerencias para empezar tu aventura:")
    
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown("""
        <div class="suggestion-card">
            <h3>🍷</h3>
            <b>Gastronomía</b><br>
            "Ruta de vinos y tapas en Logroño por 300€"
        </div>
        """, unsafe_allow_html=True)
    with c2:
        st.markdown("""
        <div class="suggestion-card">
            <h3>🏔️</h3>
            <b>Aventura</b><br>
            "Senderismo en Picos de Europa, dormir en refugios"
        </div>
        """, unsafe_allow_html=True)
    with c3:
        st.markdown("""
        <div class="suggestion-card">
            <h3>🏖️</h3>
            <b>Relax</b><br>
            "Playa tranquila en Menorca, presupuesto medio"
        </div>
        """, unsafe_allow_html=True)
    st.markdown("---")

# Mostrar mensajes anteriores
for message in st.session_state.messages:
    # Elegimos avatar según quién hable
    avatar = "🧑‍🚀" if message["role"] == "user" else "✈️"
    
    with st.chat_message(message["role"], avatar=avatar):
        st.markdown(message["content"])

# 6. INPUT DEL USUARIO
if prompt := st.chat_input("¿A dónde quieres ir este finde?"):
    
    # Usuario
    st.chat_message("user", avatar="🧑‍🚀").markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Preparar datos
    history_payload = [{"role": m["role"], "content": m["content"]} for m in st.session_state.messages]

    # Bot (Weekender)
    try:
        with st.chat_message("assistant", avatar="✈️"):
            message_placeholder = st.empty()
            message_placeholder.markdown("⏳ *Consultando mapas y guías...*")
            
            # Llamada API
            response = requests.post(
                "http://127.0.0.1:8000/chat", 
                json={"message": prompt, "history": history_payload}
            )
            
            if response.status_code == 200:
                bot_reply = response.json()["response"]
                message_placeholder.markdown(bot_reply)
                st.session_state.messages.append({"role": "assistant", "content": bot_reply})
            else:
                message_placeholder.error("❌ El servidor tuvo un problema.")
                
    except Exception as e:
        st.error(f"⚠️ Error de conexión: {e}")
