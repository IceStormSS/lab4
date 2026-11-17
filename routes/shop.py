from flask import Blueprint, render_template, request
import models

shop_bp = Blueprint('shop_bp', __name__)

@shop_bp.route('/shop')
def shop():
    category = request.args.get('category', 'all')
    search = request.args.get('search', '').strip()

    items = models.get_all_products(category=category, search=search)
    categories = models.get_categories()

    return render_template(
        'shop.html',
        items=items,
        categories=categories,
        current_category=category,
        search_query=search
    )

@shop_bp.route('/product/<int:product_id>')
def product_detail(product_id):
    product = models.get_product_by_id(product_id)
    if not product:
        return render_template('404.html'), 404
    return render_template('product_detail.html', product=product)
