import sqlite3
from flask import g, current_app

def get_db():
    """Отримує з'єднання з базою даних для поточного контексту запиту."""
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row
        # Обов'язково вмикаємо перевірку зовнішніх ключів для SQLite
        g.db.execute('PRAGMA foreign_keys = ON;')
    return g.db

def close_db(e=None):
    """Закриває з'єднання з базою даних після завершення запиту."""
    db = g.pop('db', None)
    if db is not None:
        db.close()

def init_db(app):
    """Ініціалізує таблиці бази даних та заповнює початковими даними."""
    with app.app_context():
        db = get_db()
        cursor = db.cursor()

        # 1. Таблиця відгуків (Рівень 1)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS feedbacks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT NOT NULL,
                message TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        ''')

        # 2. Таблиця товарів (Рівень 1)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS products (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                category TEXT NOT NULL,
                price REAL NOT NULL,
                description TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        ''')

        # 3. Таблиця клієнтів (Рівень 2 - Предметна область магазину)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS customers (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT NOT NULL,
                phone TEXT,
                address TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        ''')

        # Заповнення початковими товарами, якщо таблиця пуста
        cursor.execute('SELECT COUNT(*) FROM products;')
        if cursor.fetchone()[0] == 0:
            initial_products = [
                ('Зимова куртка-пуховик', 'Куртки', 3200, 'Теплий пуховик з водовідштовхувальної тканини.'),
                ('Демісезонна куртка', 'Куртки', 2400, 'Зручна вітрозахисна куртка на весну та осінь.'),
                ('Шкіряна куртка', 'Куртки', 5800, 'Стильна куртка з натуральної шкіри.'),
                ('Джинсова куртка', 'Куртки', 1900, 'Класична джинсовка з міцного деніму.'),
                ('Бомбер', 'Куртки', 2100, 'Молодіжний легкий бомбер на блискавці.'),
                ('Класичне пальто', 'Пальта', 4500, 'Елегантне двобортне пальто прямого крою.'),
                ('Вовняне пальто оверсайз', 'Пальта', 5200, 'Тепле затишне пальто з натуральної вовни.'),
                ('Тренч', 'Пальта', 3900, 'Класичний бежевий тренчкот.'),
                ('Пальто-кокон', 'Пальта', 4800, 'Об\'ємне пальто вільного силуету.'),
                ('Вітровка', 'Легкий верхній одяг', 1800, 'Ультралегка вітровка для пробіжок та прогулянок.'),
                ('Дощовик', 'Легкий верхній одяг', 1500, 'Непромокальний стильний плащ-дощовик.'),
                ('Софтшелл', 'Легкий верхній одяг', 2300, 'Функціональна мембранна куртка.'),
                ('Жилет утеплений', 'Жилети', 1700, 'Зручний жилет на синтепоні для прохолодних днів.'),
                ('Жилет пуховий', 'Жилети', 2000, 'Легкий та теплий жилет з пуховим наповнювачем.'),
                ('Парка з капюшоном', 'Парки', 4100, 'Подовжена куртка-парка з глибоким капюшоном.'),
                ('Парка зимова з хутром', 'Парки', 4900, 'Зимова утеплена парка з натуральним хутром.'),
                ('Анорак', 'Парки', 2600, 'Куртка-анорак з великою кишенею-кенгуру.'),
                ('Дублянка', 'Зимовий одяг', 7500, 'Тепла натуральна дублянка високої якості.'),
                ('Шуба штучна', 'Зимовий одяг', 6200, 'Модна еко-шуба з м\'якого штучного хутра.'),
                ('Куртка гірськолижна', 'Спортивний одяг', 5400, 'Професійна гірськолижна куртка зі снігозахистом.')
            ]
            cursor.executemany(
                'INSERT INTO products (name, category, price, description) VALUES (?, ?, ?, ?)',
                initial_products
            )

        # Заповнення тестовими клієнтами, якщо таблиця пуста
        cursor.execute('SELECT COUNT(*) FROM customers;')
        if cursor.fetchone()[0] == 0:
            initial_customers = [
                ('Олександр Коваленко', 'oleksandr@example.com', '+380501234567', 'м. Київ, вул. Хрещатик, 1'),
                ('Марія Шевченко', 'maria@example.com', '+380679876543', 'м. Львів, вул. Городоцька, 15'),
                ('Іван Бондаренко', 'ivan@example.com', '+380931112233', 'м. Одеса, вул. Дерибасівська, 8')
            ]
            cursor.executemany(
                'INSERT INTO customers (name, email, phone, address) VALUES (?, ?, ?, ?)',
                initial_customers
            )

        # Заповнення тестовим відгуком, якщо таблиця пуста
        cursor.execute('SELECT COUNT(*) FROM feedbacks;')
        if cursor.fetchone()[0] == 0:
            cursor.execute(
                'INSERT INTO feedbacks (name, email, message) VALUES (?, ?, ?)',
                ('Марія Шевченко', 'maria@example.com', 'Чудовий магазин! Замовляла пальто оверсайз — якість перевершила очікування!')
            )

        db.commit()

# --- ФУНКЦІЇ ДЛЯ РОБОТИ З ВІДГУКАМИ (FEEDBACK CRUD) ---
def get_all_feedbacks():
    db = get_db()
    return db.execute('SELECT * FROM feedbacks ORDER BY created_at DESC;').fetchall()

def add_feedback(name, email, message):
    db = get_db()
    db.execute(
        'INSERT INTO feedbacks (name, email, message) VALUES (?, ?, ?);',
        (name, email, message)
    )
    db.commit()

def delete_feedback(feedback_id):
    db = get_db()
    db.execute('DELETE FROM feedbacks WHERE id = ?;', (feedback_id,))
    db.commit()

# --- ФУНКЦІЇ ДЛЯ РОБОТИ З ТОВАРАМИ (PRODUCTS CRUD) ---
def get_all_products(category=None, search=None):
    db = get_db()
    query = 'SELECT * FROM products WHERE 1=1'
    params = []

    if category and category != 'all':
        query += ' AND category = ?'
        params.append(category)

    if search:
        query += ' AND (name LIKE ? OR description LIKE ?)'
        search_pattern = f'%{search}%'
        params.extend([search_pattern, search_pattern])

    query += ' ORDER BY id DESC;'
    return db.execute(query, params).fetchall()

def get_product_by_id(product_id):
    db = get_db()
    return db.execute('SELECT * FROM products WHERE id = ?;', (product_id,)).fetchone()

def add_product(name, category, price, description):
    db = get_db()
    cursor = db.execute(
        'INSERT INTO products (name, category, price, description) VALUES (?, ?, ?, ?);',
        (name, category, price, description)
    )
    db.commit()
    return cursor.lastrowid

def delete_product(product_id):
    db = get_db()
    db.execute('DELETE FROM products WHERE id = ?;', (product_id,))
    db.commit()

def get_categories():
    db = get_db()
    rows = db.execute('SELECT DISTINCT category FROM products ORDER BY category;').fetchall()
    return [row['category'] for row in rows]

# --- ФУНКЦІЇ ДЛЯ РОБОТИ З КЛІЄНТАМИ (CUSTOMERS - Рівень 2) ---
def get_all_customers():
    db = get_db()
    return db.execute('SELECT * FROM customers ORDER BY created_at DESC;').fetchall()

def add_customer(name, email, phone, address):
    db = get_db()
    cursor = db.execute(
        'INSERT INTO customers (name, email, phone, address) VALUES (?, ?, ?, ?);',
        (name, email, phone, address)
    )
    db.commit()
    return cursor.lastrowid

def delete_customer(customer_id):
    db = get_db()
    db.execute('DELETE FROM customers WHERE id = ?;', (customer_id,))
    db.commit()
