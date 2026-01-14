# 🧳 Weekender AI: Tu Asistente de Viajes Personal

¡Bienvenido a **Weekender AI**! 👋

Este proyecto es una aplicación inteligente que te ayuda a planear escapadas de fin de semana. Tú le dices dónde quieres ir y cuánto dinero tienes, y la Inteligencia Artificial te crea un plan detallado día por día.

Si eres nuevo en esto de la programación, ¡no te preocupes! Este documento te guiará paso a paso para que lo hagas funcionar en tu ordenador.

---

## 🍎 ¿Cómo funciona esto? (Explicación Sencilla)

Imagina que esta aplicación es como un **Restaurante**:

1.  **La Interfaz (`streamlit.py`):** Es el **Comedor**. Es la pantalla bonita donde escribes (chateas) y ves los resultados.
2.  **El Servidor (`app.py`):** Es la **Cocina**. Recibe tu pedido, organiza las cosas y manda las órdenes.
3.  **La IA (Groq):** Es el **Chef Experto**. La cocina le dice "El cliente quiere ir a París con 200€", y el Chef inventa el menú (el itinerario) en segundos.
4.  **La Base de Datos:** Es el **Libro de Reservas**. Guarda todo lo que hablas para que no se pierda.

---

## 🛠️ ¿Qué necesito tener instalado?

Antes de empezar, asegúrate de tener estas dos cosas en tu ordenador:

1.  **Python:** (El lenguaje en el que está escrito todo).
2.  **VS Code:** (El programa para ver y ejecutar el código).

---

## 🚀 Pasos para ponerlo en marcha

Sigue estos pasos uno a uno y lo tendrás funcionando en 5 minutos.

### Paso 1: Prepara el terreno (Instalar librerías)
Las "librerías" son herramientas extra que el código necesita para funcionar (como una calculadora o un traductor).

1.  Abre la carpeta del proyecto en VS Code.
2.  Abre una **Terminal nueva** (Menú: *Terminal > New Terminal*).
3.  Copia y pega este comando y pulsa Enter:
    ```bash
    pip install -r requirements.txt
    ```

### Paso 2: Configura las Claves Secretas (`.env`)
El proyecto necesita contraseñas para conectarse a la IA y a la Base de Datos. Por seguridad, no se ponen en el código, sino en un archivo secreto.

1.  Crea un archivo nuevo y llámalo **`.env`** (sí, empieza con un punto).
2.  Pega esto dentro:
    ```env
    GROQ_API_KEY=tu_clave_de_groq_aqui
    DATABASE_URL=tu_url_de_render_aqui
    ```
    *(Nota: Pide al autor del proyecto las claves reales para rellenar esto).*

### Paso 3: Prepara la Memoria (Base de Datos)
Necesitamos decirle a la base de datos que cree una "tabla" (una hoja de papel) para empezar a apuntar cosas.

1.  En la terminal, escribe:
    ```bash
    python crear_tabla.py
    ```
    *Si sale un mensaje verde diciendo "ÉXITO", ¡vamos bien!*

---

## 🎮 ¡A jugar! (Cómo ejecutar la App)

Para que esto funcione, necesitamos encender **la Cocina** (Backend) y abrir **el Comedor** (Frontend) a la vez. Para eso usaremos **dos terminales**.

### 1. Enciende el Cerebro (Backend)
En tu terminal actual, escribe:
```bash
python app.py

### 2. Abrir el streamlit(fronted)
streamlit run streamlit.py

### 3. Para comprobar si se guardan mis chats o combersaciones
python ver_logs.py