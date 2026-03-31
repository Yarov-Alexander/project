# My Project

![Project Screenshot](screenshots/main_page.png)

## Описание
Проект представляет собой **FastAPI приложение с PostgreSQL**, использует Alembic для миграций и полностью контейнеризирован через Docker и Docker Compose.  
Позволяет быстро запускать сервис локально или на сервере, с готовой базой данных и API документацией через Swagger.

---

## Технологии
- Python 3.12  
- FastAPI  
- PostgreSQL  (sqlite для тестов)
- SQLAlchemy + Alembic  
- Docker & Docker Compose  
- Pydantic для настроек и валидации  

---

## Установка и запуск

### 1. Клонирование репозитория
```bash
git clone https://github.com/Yarov-Alexander/project
cd My_Project
```
### 2. Заполнение `.env` файла
```bash
Введите свои данные в .env:
DATABASE_URL=postgresql+asyncpg://user:password@db:5432/dbname
SECRET_KEY=your_secret_key
```
### 3. Создание Docker image
```bash
docker compose up --build
```
Приложение будет доступно по адресу: http://localhost:8000/docs
