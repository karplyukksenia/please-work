from flask import Flask, render_template, request, jsonify
import sqlite3
import os
from datetime import datetime

app = Flask(__name__)


# Функция для создания таблиц в SQLite
def init_db():
    conn = sqlite3.connect('pkm_database.db')
    cursor = conn.cursor()

    # Создаем таблицы как в SQL Server базе
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            email TEXT NOT NULL UNIQUE,
            password_hash TEXT NOT NULL
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS notes(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            title TEXT NOT NULL,
            content TEXT NOT NULL,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tags(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            name TEXT NOT NULL,
            UNIQUE(user_id, name),
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS note_tags(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            tag_id INTEGER NOT NULL,
            note_id INTEGER NOT NULL,
            UNIQUE(note_id, tag_id),
            FOREIGN KEY (tag_id) REFERENCES tags (id),
            FOREIGN KEY (note_id) REFERENCES notes (id) ON DELETE CASCADE
        )
    ''')

    # Создаем демо-пользователя если нет пользователей
    cursor.execute("SELECT COUNT(*) FROM users")
    if cursor.fetchone()[0] == 0:
        cursor.execute(
            "INSERT INTO users (username, email, password_hash) VALUES (?, ?, ?)",
            ('demo_user', 'demo@example.com', 'demo_hash')
        )

    conn.commit()
    conn.close()


def get_db_connection():
    """Подключение к SQLite базе"""
    conn = sqlite3.connect('pkm_database.db')
    conn.row_factory = sqlite3.Row
    return conn


# Инициализируем базу при старте
init_db()


# Главная страница - создание заметок
@app.route('/')
def index():
    return render_template('index.html')


# Страница всех заметок
@app.route('/all-notes')
def all_notes():
    return render_template('all_notes.html')


# API для получения заметок
@app.route('/api/notes', methods=['GET'])
def get_notes_api():
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        cursor.execute('''
            SELECT n.id, n.user_id, n.title, n.content, n.created_at, n.updated_at
            FROM notes n
            ORDER BY n.updated_at DESC
        ''')

        notes = []
        for row in cursor:
            notes.append({
                'id': row['id'],
                'user_id': row['user_id'],
                'title': row['title'],
                'content': row['content'],
                'created_at': row['created_at'],
                'updated_at': row['updated_at']
            })

        return jsonify(notes)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        conn.close()


# API для создания заметки
@app.route('/api/notes', methods=['POST'])
def create_note_api():
    data = request.get_json()

    if not data or not all(k in data for k in ['user_id', 'title', 'content']):
        return jsonify({"error": "Missing required fields: user_id, title, content"}), 400

    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        cursor.execute(
            'INSERT INTO notes (user_id, title, content) VALUES (?, ?, ?)',
            (data['user_id'], data['title'], data['content'])
        )
        conn.commit()
        return jsonify({"message": "Note created successfully"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    finally:
        conn.close()


# API для получения всех заметок с полной информацией
@app.route('/api/notes/all', methods=['GET'])
def get_all_notes_api():
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        cursor.execute('''
            SELECT n.id, n.user_id, u.username, n.title, n.content, n.created_at, n.updated_at
            FROM notes n
            JOIN users u ON n.user_id = u.id
            ORDER BY n.updated_at DESC
        ''')

        notes = []
        for row in cursor:
            notes.append({
                'id': row['id'],
                'user_id': row['user_id'],
                'username': row['username'],
                'title': row['title'],
                'content': row['content'],
                'created_at': row['created_at'],
                'updated_at': row['updated_at']
            })

        return jsonify(notes)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        conn.close()


# API для получения пользователей
@app.route('/api/users', methods=['GET'])
def get_users_api():
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        cursor.execute('SELECT id, username, email FROM users')

        users = [{'id': row['id'], 'username': row['username'], 'email': row['email']} for row in cursor]
        return jsonify(users)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        conn.close()


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    print("🚀 Запуск Flask PKM API...")
    print(f"🌐 Сайт будет доступен по: http://localhost:{port}")
    print("📊 База данных инициализирована")
    app.run(host='0.0.0.0', port=port)