from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///dog_walking.db'
db = SQLAlchemy(app)

# Модель базы данных для заказа
class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    flat_number = db.Column(db.String(50), nullable=False)
    pet_name = db.Column(db.String(50), nullable=False)
    pet_breed = db.Column(db.String(50), nullable=False)
    start_time = db.Column(db.DateTime, nullable=False)
    end_time = db.Column(db.DateTime, nullable=False)
    walker = db.Column(db.String(50), nullable=False)  # 'Petr' или 'Anton'

# Инициализация базы данных
@app.before_first_request
def create_tables():
    db.create_all()

# Функция валидации времени начала прогулки
def validate_time(time):
    # Прогулки только с 07:00 до 23:00
    if time.hour < 7 or time.hour > 22:
        return False
    # Прогулка должна начинаться в 00 или 30 минут
    if time.minute not in [0, 30]:
        return False
    return True

# Проверка занятости исполнителя в указанное время
def check_walker_availability(start_time):
    # Прогулка длится 30 минут
    end_time = start_time + timedelta(minutes=30)
    # Проверяем, занят ли кто-то из исполнителей на это время
    existing_order = Order.query.filter(Order.start_time <= end_time, Order.end_time >= start_time).first()
    return existing_order is None

# API для вывода заказов на указанную дату
@app.route('/orders/<date>', methods=['GET'])
def get_orders(date):
    try:
        # Конвертируем строку в дату
        query_date = datetime.strptime(date, '%Y-%m-%d').date()
        orders = Order.query.filter(db.func.date(Order.start_time) == query_date).all()

        return jsonify([
            {
                'flat_number': order.flat_number,
                'pet_name': order.pet_name,
                'pet_breed': order.pet_breed,
                'start_time': order.start_time.strftime('%H:%M'),
                'walker': order.walker
            }
            for order in orders
        ])
    except ValueError:
        return jsonify({'error': 'Invalid date format, use YYYY-MM-DD'}), 400

# API для оформления нового заказа
@app.route('/orders', methods=['POST'])
def create_order():
    data = request.get_json()

    try:
        flat_number = data['flat_number']
        pet_name = data['pet_name']
        pet_breed = data['pet_breed']
        start_time = datetime.strptime(data['start_time'], '%Y-%m-%d %H:%M')

        # Валидация времени начала прогулки
        if not validate_time(start_time):
            return jsonify({'error': 'Invalid start time. Must be on the hour or half-hour between 07:00 and 23:00'}), 400

        # Проверяем, доступен ли исполнитель на это время
        if not check_walker_availability(start_time):
            return jsonify({'error': 'No available walker for this time'}), 400

        # Выбираем исполнителя
        walker = 'Petr' if not Order.query.filter_by(walker='Petr', start_time=start_time).first() else 'Anton'

        # Создаем новый заказ
        new_order = Order(
            flat_number=flat_number,
            pet_name=pet_name,
            pet_breed=pet_breed,
            start_time=start_time,
            end_time=start_time + timedelta(minutes=30),
            walker=walker
        )
        db.session.add(new_order)
        db.session.commit()

        return jsonify({'message': 'Order created successfully!'}), 201

    except KeyError:
        return jsonify({'error': 'Missing required fields'}), 400
    except ValueError:
        return jsonify({'error': 'Invalid date format, use YYYY-MM-DD HH:MM'}), 400

if __name__ == '__main__':
    app.run(debug=True)
