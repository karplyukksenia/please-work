# New Project

# Please Work — Личная база знаний (PKM) на Flask

![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![Flask](https://img.shields.io/badge/Flask-3.0%2B-lightgrey)
![SQLite](https://img.shields.io/badge/SQLite-3-green)
![License](https://img.shields.io/badge/License-MIT-yellow)

Простое, лёгкое и полностью локальное веб-приложение для ведения личных заметок и организации знаний.  

## Функционал 

- Регистрация / вход / выход  
- Создание, редактирование и удаление заметок  
- Прикрепление тегов к заметкам  
- Просмотр всех своих заметок в одной таблице  
- Полная привязка заметок к пользователю  
- Минималистичный и чистый интерфейс  
- Работает оффлайн после первого запуска  

## Технологии

- Backend:**Flask**
- База данных: **SQLite** 
- Хэширование паролей:**bcrypt**
- Фронтенд: HTML + немного CSS (всё в `/templates` и `/static`)


## Структура

```bash

please-work/
├── main.py              # точка входа
├── pkm_database.db      # создаётся автоматически
├── templates/           # HTML-шаблоны
│   ├── index.html
│   ├── login.html
│   ├── register.html
│   ├── all_notes.html
│   └── ...
├── static/              # CSS
└── requirements.txt     
```


