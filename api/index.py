# api/index.py

from app.main import app

# Nenhuma outra configuração é necessária aqui.
# FastAPI já monta o /docs (Swagger UI) e /openapi.json automaticamente.

# OBS.: No Vercel, assim que ele detectar este arquivo em /api/index.py
# com a dependência de FastAPI, ele vai disponibilizar o app inteiro como uma função serverless.

