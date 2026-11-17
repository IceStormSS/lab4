import os
from flask import Flask, render_template
import models
from routes.feedback import feedback_bp
from routes.shop import shop_bp
from routes.admin import admin_bp

app = Flask(__name__)

# Конфігурація додатка
app.config['SECRET_KEY'] = 'dev-secret-key-lab04-security'
app.config['DATABASE'] = os.path.join(app.root_path, 'db.sqlite')

# Реєстрація автоматичного закриття з'єднання з БД після кожного запиту
app.teardown_appcontext(models.close_db)

# Реєстрація Blueprint-ів
app.register_blueprint(feedback_bp)
app.register_blueprint(shop_bp)
app.register_blueprint(admin_bp)

@app.route('/')
def home():
    """Головна сторінка з новинками та останніми відгуками з БД."""
    products = models.get_all_products()[:4]
    feedbacks = models.get_all_feedbacks()[:3]
    return render_template('home.html', products=products, feedbacks=feedbacks)

@app.route('/about')
def about():
    """Сторінка 'Про нас'."""
    return render_template('about.html')

# Ініціалізація бази даних SQLite при запуску
with app.app_context():
    models.init_db(app)

if __name__ == '__main__':
    # debug=True: автоматичний перезапуск після змін у коді під час розробки
    app.run(debug=True)
