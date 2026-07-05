FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# ✅ THIS LINE IS THE MOST IMPORTANT
CMD ["sh", "-c", "python -u metrics.py & exec streamlit run streamlit_app.py --server.address=0.0.0.0 --server.port=8501"]