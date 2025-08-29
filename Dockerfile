# Dockerfile para TaskFlow Kanban App
# NOTA: Este es un Dockerfile de ejemplo. Se requiere configuración adicional para producción.

FROM python:3.9-slim

WORKDIR /app

# Copiar archivos de requerimientos
COPY requirements.txt .

# Instalar dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Copiar código fuente
COPY . .

# Exponer puerto
EXPOSE 5002

# Comando por defecto
CMD ["python", "-m", "kanban_app.run", "web"]