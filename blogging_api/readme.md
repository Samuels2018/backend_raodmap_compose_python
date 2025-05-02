# 📝 Blogging Platform API

Este proyecto es una API RESTful desarrollada con FastAPI que permite crear, leer, actualizar y eliminar publicaciones de blog.


## ⚙️ Tecnologías utilizadas

- Python
- FastAPI
- SQLAlchemy
- mongodb
- Uvicorn

## 🚀 Cómo ejecutar el proyecto localmente

1. Clona el repositorio y accede al directorio:

```bash
git clone https://github.com/Samuels2018/backend_raodmap_compose_python.git
cd backend_raodmap_compose_python/blogging_api
Crea un entorno virtual y actívalo:

python -m venv venv
source venv/bin/activate  # En Windows usa `venv\Scripts\activate`
Instala las dependencias necesarias:

pip install -r requirements.txt
Ejecuta el servidor de desarrollo:

uvicorn main:app --reload


📚 Endpoints disponibles
Método	Ruta	Descripción
GET	/posts	Lista todas las publicaciones
POST	/posts	Crea una nueva publicación
GET	/posts/{id}	Obtiene una publicación por ID
PUT	/posts/{id}	Actualiza una publicación por ID
DELETE	/posts/{id}	Elimina una publicación por ID


# http://127.0.0.1:5000/api/v1//posts
[
    {
        "_id": "68142e6f9accdcc1acd861e0",
        "field": "value",
        "category": "!",
        "content": "fwfwfwfw",
        "tags": [],
        "title": "some 111 dwdwdwd",
        "updatedAt": {
            "$date": "2025-05-02T03:05:57.791Z"
        }
    },
    {
        "_id": "681435f73149fb77d9a76084",
        "title": "some",
        "content": "fwfwfwfw",
        "category": "!",
        "tags": [],
        "createdAt": {
            "$date": "2025-05-02T03:03:19.613Z"
        },
        "updatedAt": {
            "$date": "2025-05-02T03:03:19.613Z"
        }
    },
    {
        "_id": "6814363c3149fb77d9a76085",
        "title": "some 111",
        "content": "fwfwfwfw",
        "category": "!",
        "tags": [],
        "createdAt": {
            "$date": "2025-05-02T03:04:28.140Z"
        },
        "updatedAt": {
            "$date": "2025-05-02T03:04:28.140Z"
        }
    }
]

http://127.0.0.1:5000/api/v1//posts/create

{
    "title": "some 111 dwdwdwd 11111",
    "content": "fwfwfwfw",
    "category": "!",
    "tags": [],
    "createdAt": {
        "$date": "2025-05-02T03:07:22.110Z"
    },
    "updatedAt": {
        "$date": "2025-05-02T03:07:22.110Z"
    },
    "_id": "681436ea3149fb77d9a76086"
}

http://127.0.0.1:5000/api/v1//posts/68142e6f9accdcc1acd861e0

{
    "_id": "68142e6f9accdcc1acd861e0",
    "field": "value",
    "category": "!",
    "content": "fwfwfwfw",
    "tags": [],
    "title": "some 111 dwdwdwd",
    "updatedAt": {
        "$date": "2025-05-02T03:05:57.791Z"
    }
}