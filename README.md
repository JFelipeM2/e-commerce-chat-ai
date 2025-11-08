E-commerce Chat AI

API REST desarrollada con FastAPI y Docker que simula una tienda de zapatos con un asistente inteligente integrado (Google Gemini o modo local).
El sistema permite consultar productos, mantener un historial de conversación y obtener recomendaciones automáticas.

e-commerce-chat-ai/
│
├── src/
│   ├── application/
│   ├── domain/
│   ├── infrastructure/
│   │   ├── api/
│   │   ├── db/
│   │   ├── llm_providers/
│   │   └── repositories/
│   └── config.py
│
├── tests/
│
├── data/
│   └── ecommerce_chat.db
│
├── docker-compose.yml
├── Dockerfile
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md

INSTALACION Y EJECUCION
Opción 1 — Ejecución local (entorno virtual)

1.Crear y activar entorno virtual

python -m venv venv
venv\Scripts\activate

2.Instalar dependencias

pip install -r requirements.txt

3.Ejecutar la API

uvicorn src.infrastructure.api.main:app --reload

Opción 2 — Con Docker

1.Construir y levantar los contenedores

docker-compose up --build

ENDPOINTS PRINCIPALES

| Método | Endpoint                     | Descripción                                         |
| ------ | ---------------------------- | --------------------------------------------------- |
| `GET`  | `/health`                    | Verifica el estado de la API                        |
| `GET`  | `/products`                  | Lista todos los productos del catalogo              |
| `GET`  | `/products/{id}`             | Muestra los detalles de un producto especifico      |
| `POST` | `/chat`                      | Envia un mensaje al asistente virtual               |
| `GET`  | `/chat/history/{session_id}` | Devuelve el historial de conversacion de una sesion |


ASISTENTE DE IA

El sistema utiliza Google Gemini como motor principal.
Si no hay conexión o falla la API, se usa un modo local de respaldo que genera respuestas automáticas basadas en el catálogo de productos para no andar peleando con gemini.

VARIABLES DE ENTORNO(.env)
ejemplo de configuracion:

GEMINI_API_KEY=tu_api_key_de_gemini
DATABASE_URL=sqlite:///./data/ecommerce_chat.db
ENVIRONMENT=development

PRUEBAS UNITARIAS
Ejecutar los tests con Pytest:
pytest -v

EVIDENCIAS
Se encuentran en la carpeta /evidencias del repositorio

TECNOLOGIAS UTILIZADAS
    
Python 3.11

FastAPI

SQLAlchemy

SQLite

Docker / Docker Compose

Google Generative AI (Gemini)

Pytest


AUTORES 

Juan Felipe Martínez De La Ossa
Universidad EAFIT — Arquitectura de Software
2025