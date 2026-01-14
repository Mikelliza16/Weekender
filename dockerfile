FROM python:3.9-slim

WORKDIR /app

# Instalar dependencias
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar todo el código
COPY . .

# Exponer puertos (8000=Backend, 8501=Frontend)
EXPOSE 8000
EXPOSE 8501

# Script de arranque (Corregido: frontend.py -> streamlit.py)
RUN echo '#!/bin/bash\npython app.py & streamlit run streamlit.py --server.port 8501 --server.address 0.0.0.0' > start.sh
RUN chmod +x start.sh

CMD ["./start.sh"]