"""Build the local RAG vector index during a Render build.

Keeping this work out of a web request prevents Gunicorn from timing out on
the first chat request after each deploy.
"""
from RagSystem.rag.pipeline import RAGPipeline


def main():
    result = RAGPipeline().initialize()
    if not result['success']:
        raise SystemExit(result['message'])
    print(result['message'])


if __name__ == '__main__':
    main()
