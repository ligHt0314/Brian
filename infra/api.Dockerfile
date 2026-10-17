FROM python:3.12.13-slim
WORKDIR /app
COPY requirements.lock /app/requirements.lock
RUN pip install --no-cache-dir -r requirements.lock
COPY services /app/services
COPY fixtures /app/fixtures
COPY scripts /app/scripts
ENV PYTHONPATH=/app/services/api
EXPOSE 8000
CMD ["sh", "/app/scripts/start-api.sh"]
