# 💰 Expense Tracker API

API RESTful para registrar y consultar gastos personales, desarrollada con Flask y SQLAlchemy.

## ⚙️ Tecnologías utilizadas

- Python
- Flask
- SQLAlchemy
- postgresql
- Flask-RESTful

## 🚀 Cómo ejecutar el proyecto localmente

1. Clona el repositorio y accede al directorio:

```bash
git clone https://github.com/Samuels2018/backend_raodmap_compose_python.git
cd backend_raodmap_compose_python/expense_tracker_API
Crea un entorno virtual y actívalo:

python -m venv venv
source venv/bin/activate  # En Windows usa `venv\Scripts\activate`
Instala las dependencias:

pip install -r requirements.txt
Ejecuta el servidor Flask:

python app.py
Accede a la API en:
http://localhost:5000

📚 Endpoints disponibles
Método	Ruta	Descripción
GET	/expenses	Lista todos los gastos
POST	/expenses	Crea un nuevo gasto
GET	/expenses/{id}	Obtiene un gasto por su ID
PUT	/expenses/{id}	Actualiza un gasto existente
DELETE	/expenses/{id}	Elimina un gasto