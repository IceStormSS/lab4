from flask import Blueprint, render_template, request, redirect, url_for, flash
import models

admin_bp = Blueprint('admin_bp', __name__, url_prefix='/admin')

@admin_bp.route('/')
def dashboard():
    """Головна сторінка адмін-панелі зі статистикою."""
    feedbacks = models.get_all_feedbacks()
    products = models.get_all_products()
    customers = models.get_all_customers()

    return render_template(
        'admin/dashboard.html',
        feedbacks_count=len(feedbacks),
        products_count=len(products),
        customers_count=len(customers)
    )

# --- КЕРУВАННЯ ВІДГУКАМИ (FEEDBACK) ---
@admin_bp.route('/feedbacks')
def feedbacks_list():
    feedbacks = models.get_all_feedbacks()
    return render_template('admin/feedbacks.html', feedbacks=feedbacks)

@admin_bp.route('/feedbacks/delete/<int:feedback_id>', methods=['POST'])
def feedback_delete(feedback_id):
    models.delete_feedback(feedback_id)
    flash('Відгук успішно видалено!', 'success')
    return redirect(url_for('admin_bp.feedbacks_list'))

# --- КЕРУВАННЯ ТОВАРАМИ (PRODUCTS) ---
@admin_bp.route('/products')
def products_list():
    products = models.get_all_products()
    categories = models.get_categories()
    return render_template('admin/products.html', products=products, categories=categories)

@admin_bp.route('/products/add', methods=['POST'])
def product_add():
    name = request.form.get('name', '').strip()
    category = request.form.get('category', '').strip()
    price = request.form.get('price', '').strip()
    description = request.form.get('description', '').strip()

    if not name or not category or not price:
        flash('Будь ласка, заповніть обов\'язкові поля (назва, категорія, ціна).', 'error')
    else:
        try:
            price_float = float(price)
            models.add_product(name, category, price_float, description)
            flash(f'Товар "{name}" успішно додано до бази даних!', 'success')
        except ValueError:
            flash('Ціна повинна бути числовим значенням.', 'error')

    return redirect(url_for('admin_bp.products_list'))

@admin_bp.route('/products/delete/<int:product_id>', methods=['POST'])
def product_delete(product_id):
    models.delete_product(product_id)
    flash('Товар успішно видалено з бази даних!', 'success')
    return redirect(url_for('admin_bp.products_list'))

# --- КЕРУВАННЯ КЛІЄНТАМИ (CUSTOMERS - Рівень 2) ---
@admin_bp.route('/customers')
def customers_list():
    customers = models.get_all_customers()
    return render_template('admin/customers.html', customers=customers)

@admin_bp.route('/customers/add', methods=['POST'])
def customer_add():
    name = request.form.get('name', '').strip()
    email = request.form.get('email', '').strip()
    phone = request.form.get('phone', '').strip()
    address = request.form.get('address', '').strip()

    if not name or not email:
        flash('Ім\'я та Email є обов\'язковими для створення клієнта.', 'error')
    else:
        models.add_customer(name, email, phone, address)
        flash(f'Клієнта "{name}" успішно додано!', 'success')

    return redirect(url_for('admin_bp.customers_list'))

@admin_bp.route('/customers/delete/<int:customer_id>', methods=['POST'])
def customer_delete(customer_id):
    models.delete_customer(customer_id)
    flash('Клієнта успішно видалено.', 'success')
    return redirect(url_for('admin_bp.customers_list'))

# =========================================================================
# TODO: ЧАСТИНА ДЛЯ НАПАРНИКА (Замовлення та статуси замовлень)
# Напарнику потрібно реалізувати:
# 1. @admin_bp.route('/orders') - перегляд списку всіх замовлень із таблиці orders
# 2. @admin_bp.route('/orders/<int:order_id>') - деталі замовлення (товари з order_items)
# 3. @admin_bp.route('/orders/<int:order_id>/status', methods=['POST']) - зміна статусу
# =========================================================================
