# My Project

![Project Screenshot]([[screenshots/main_page.png](https://github.com/Yarov-Alexander/project/issues/1#issue-4179220371)](https://private-user-images.githubusercontent.com/239799992/571917566-e17011ff-1c0e-41dd-b4e3-a1aae717a180.jpg?jwt=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJnaXRodWIuY29tIiwiYXVkIjoicmF3LmdpdGh1YnVzZXJjb250ZW50LmNvbSIsImtleSI6ImtleTUiLCJleHAiOjE3NzQ5NjQxNTYsIm5iZiI6MTc3NDk2Mzg1NiwicGF0aCI6Ii8yMzk3OTk5OTIvNTcxOTE3NTY2LWUxNzAxMWZmLTFjMGUtNDFkZC1iNGUzLWExYWFlNzE3YTE4MC5qcGc_WC1BbXotQWxnb3JpdGhtPUFXUzQtSE1BQy1TSEEyNTYmWC1BbXotQ3JlZGVudGlhbD1BS0lBVkNPRFlMU0E1M1BRSzRaQSUyRjIwMjYwMzMxJTJGdXMtZWFzdC0xJTJGczMlMkZhd3M0X3JlcXVlc3QmWC1BbXotRGF0ZT0yMDI2MDMzMVQxMzMwNTZaJlgtQW16LUV4cGlyZXM9MzAwJlgtQW16LVNpZ25hdHVyZT04OGRiMDg3Y2QxZmY4NTE2OWQ5ZDYyMWNhYzE0MWM4NWI5MWNjNzAwM2ExZWM0NjE4OTIwYWFhZTUyOWM5YzA4JlgtQW16LVNpZ25lZEhlYWRlcnM9aG9zdCJ9.WlxVDasPSr2ouL3erxUJIwPMIvrwbfajEJpvavl7MKM))

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
### 3. Создание image и запуск контейнера
```bash
docker compose up --build
```
Приложение будет доступно по адресу: http://localhost:8000/docs
