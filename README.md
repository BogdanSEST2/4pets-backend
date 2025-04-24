# 4Pets Backend 🐾

Серверная часть для веб сайта **4Pets** — платформа для общения владельцев животных.

## 🚀 Быстрый старт

1. Клонируй репозиторий:

git clone https://github.com/yourname/4pets_backend.git

cd 4pets_backend


2. Создай виртуальное окружение и активируй его:


python -m venv venv source venv/bin/activate # Windows: venv\Scripts\activate


3. Установи зависимости:

pip install -r requirements.txt

4. Настрой файл `.env` (пример ниже).

5. Запусти сервер:

python run.py


FLASK_ENV=development 
FLASK_APP=run.py 
SECRET_KEY=supersecretkey 
SQLALCHEMY_DATABASE_URI=sqlite:///db.sqlite3

