# Build the Vue application separately so the runtime image only contains
# the compiled assets and the Python API.
FROM node:22-alpine AS frontend-build

WORKDIR /build/interface-quiz

COPY interface-quiz/package*.json ./
RUN npm ci

COPY interface-quiz/ ./
RUN npm run build


FROM python:3.11-slim AS production

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app/quiz/src

WORKDIR /app

COPY requirements.txt ./
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

COPY quiz/ ./quiz/
COPY --from=frontend-build /build/interface-quiz/dist ./frontend/

EXPOSE 8000

CMD ["uvicorn", "presentation.http.main:app", "--app-dir", "/app/quiz/src", "--host", "0.0.0.0", "--port", "8000"]
