# Render deployment

The RAG index must be built during the **build command**, not during the first
chat request. The repository's `render.yaml` configures that automatically for
new Blueprint deployments.

For the existing Render service, set these values in **Settings** and redeploy:

- Root Directory: `RagBackendAI`
- Build Command: `pip install -r requirements.txt && python manage.py collectstatic --noinput && python build_rag_index.py`
- Start Command: `gunicorn RagBackend.wsgi:application --bind 0.0.0.0:$PORT --workers 1 --threads 2 --timeout 120`
- Health Check Path: `/`

Set `GROQ_API_KEY` (or `GROQ_API_KEY_1`) and, if request logging is needed,
`MONGODB_URI` in Render's environment settings. Never add these values to the
repository.
