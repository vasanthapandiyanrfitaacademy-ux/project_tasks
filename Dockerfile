FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . .

# Expose ports
EXPOSE 8501
EXPOSE 8000

# Run both processes properly
CMD ["sh", "-c", "python -u metrics.py & exec streamlit run streamlit_app.py --server.address=0.0.0.0 --server.port=8501"]