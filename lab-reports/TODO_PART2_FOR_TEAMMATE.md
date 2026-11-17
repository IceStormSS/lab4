# Інструкція для напарника: Реалізація Частини 2 (Лабораторна робота №4)

Привіт! Першу половину лабораторної роботи №4 вже повністю реалізовано:
- Налаштовано з'єднання з SQLite (`models.py`) з підтримкою `PRAGMA foreign_keys = ON;` та `sqlite3.Row`.
- Реалізовано модульну структуру з Blueprint-ами (`routes/feedback.py`, `routes/shop.py`, `routes/admin.py`, `app.py`).
- Створено таблиці: `feedbacks`, `products`, `customers` (Рівень 2).
- Повністю працює CRUD для відгуків та товарів, фільтрація/пошук у каталозі, а також адмін-панель для відгуків, товарів та клієнтів.

---

## 🎯 Твоє завдання (Частина 2):

Тобі потрібно реалізувати функціональність **замовлень (Orders)**, зв'язок між замовленнями й товарами (**many-to-many**), керування **статусами замовлень** в адмінці та **другу додаткову фічу (Рівень 3)**.

---

### Крок 1. Додати таблиці замовлень у `models.py`
У функцію `init_db(app)` в `models.py` додай створення двох таблиць:

```python
# 1. Таблиця замовлень
cursor.execute('''
    CREATE TABLE IF NOT EXISTS orders (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        customer_id INTEGER,
        customer_name TEXT NOT NULL,
        customer_phone TEXT NOT NULL,
        customer_address TEXT NOT NULL,
        status TEXT NOT NULL DEFAULT 'Нове',
        total_price REAL NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (customer_id) REFERENCES customers(id) ON DELETE SET NULL
    );
''')

# 2. Таблиця зв'язку замовлень і товарів (Many-to-Many)
cursor.execute('''
    CREATE TABLE IF NOT EXISTS order_items (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        order_id INTEGER NOT NULL,
        product_id INTEGER NOT NULL,
        quantity INTEGER NOT NULL DEFAULT 1,
        price REAL NOT NULL,
        FOREIGN KEY (order_id) REFERENCES orders(id) ON DELETE CASCADE,
        FOREIGN KEY (product_id) REFERENCES products(id) ON DELETE CASCADE
    );
''')
```

І додай допоміжні функції в `models.py`:
- `create_order(name, phone, address, items)`: створює запис у `orders`, додає позиції в `order_items` та робить `db.commit()`.
- `get_all_orders()`: вибірка всіх замовлень (`SELECT * FROM orders ORDER BY created_at DESC;`).
- `get_order_details(order_id)`: повертає замовлення та список товарів із `order_items JOIN products ON order_items.product_id = products.id`.
- `update_order_status(order_id, new_status)`: `UPDATE orders SET status = ? WHERE id = ?;`.

---

### Крок 2. Оформлення замовлення користувачем у `routes/shop.py`
Додай маршрут для оформлення замовлення, наприклад:
- Кнопка «Купити в 1 клік» або «Замовити» на сторінці товару (`/product/<id>`) чи простий кошик у сесії (`session['cart']`).
- При відправці форми створюється запис у таблиці `orders` та `order_items`.
- Користувачу виводиться повідомлення: *"Дякуємо! Ваше замовлення #... успішно прийнято в обробку!"*

---

### Крок 3. Керування замовленнями в адмінці (`routes/admin.py`)
Додай маршрути:
1. `GET /admin/orders` — таблиця всіх замовлень із їхніми статусами (`Нове`, `В обробці`, `Відправлено`, `Виконано`, `Скасовано`).
2. `GET /admin/orders/<int:order_id>` — перегляд деталей замовлення (хто замовив, адреса, які товари та в якій кількості).
3. `POST /admin/orders/<int:order_id>/status` — зміна статусу замовлення через випадаючий список (`<select name="status">`).

Створи шаблони для цих сторінок:
- `templates/admin/orders.html`
- `templates/admin/order_detail.html`

---

### Крок 4. Додаткова функція (Рівень 3 - Фіча №2)
Обери одну з простих, але ефектних функцій:
- **Варіант А (Рекомендовано - Промокоди):** Таблиця `coupons` (`code`, `discount_percent`). При оформленні замовлення поле "Промокод" робить знижку 10-20% на загальну суму.
- **Варіант Б (Авторизація адміна):** Проста форма входу `/admin/login` з перевіркою пароля через Flask сесію, щоб адмінка була захищена.
- **Варіант В (Історія замовлень клієнта):** Сторінка `/my-orders`, де за введеним номером телефону або email показуються всі попередні замовлення.

---

### Крок 5. Створити свій звіт
Скопіюй шаблон із `lab-reports/lab04-report-part1.md` у `lab-reports/lab04-report-part2.md`, заповни своїми даними, опиши реалізацію замовлень та додай скріншоти роботи адмінки!
