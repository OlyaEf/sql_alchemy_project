from flask import Flask, jsonify, request, json
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

import data_base

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
db = SQLAlchemy(app)


class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    age = db.Column(db.Integer)
    email = db.Column(db.String(100), nullable=False)
    role = db.Column(db.String(10))
    phone = db.Column(db.String(100), unique=True)

    # Функция возвращает словарь
    def to_dict(self):
        return {col.name: getattr(self, col.name) for col in self.__table__.columns}


class Order(db.Model):
    __tablename__ = 'order'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    description = db.Column(db.String())
    start_date = db.Column(db.Date)
    end_date = db.Column(db.Date)
    address = db.Column(db.String(255))
    price = db.Column(db.Float)
    customer_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    executor_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    # Функция возвращает словарь
    def to_dict(self):
        return {col.name: getattr(self, col.name) for col in self.__table__.columns}


class Offer(db.Model):
    __tablename__ = 'offer'
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'))
    executor_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    # Функция возвращает словарь
    def to_dict(self):
        return {col.name: getattr(self, col.name) for col in self.__table__.columns}


# для последней версии Alchemy использовать:
with app.app_context():
    db.create_all()

    # распаковка словарей из data
    users = [User(**user_dict) for user_dict in data_base.users]
    db.session.add_all(users)
    db.session.commit()

    for order_dict in data_base.orders:
        order_dict['start_date'] = datetime.strptime(order_dict['start_date'], '%m/%d/%Y').date()
        order_dict['end_date'] = datetime.strptime(order_dict['end_date'], '%m/%d/%Y').date()
        new_order = Order(**order_dict)
        db.session.add(new_order)
        db.session.commit()

    offers = [Offer(**offer_dict) for offer_dict in data_base.offers]
    db.session.add_all(offers)
    db.session.commit()


@app.route('/users', methods=['GET', 'POST'])
def get_all_users():
    """
    Представление для пользователей, которое обрабатывает GET-запросы получения всех пользователей.
    Реализует создание пользователя user посредством метода POST на URL /users для users.
    :return: Возвращает пользователей в формате JSON.
    """
    if request.method == 'GET':
        users = User.query.all()
        result = [user.to_dict() for user in users]
        return jsonify(result)
    elif request.method == 'POST':
        user_data = json.loads(request.data)
        db.session.add(User(**user_data))
        db.session.commit()
        return '', 201


@app.route('/users/<int:user_id>', methods=['GET', 'PUT', 'DELETE'])
def get_user_by_id(user_id: int):
    """
    Представление для пользователей, которое обрабатывало бы GET-запросы получения
    одного пользователя по идентификатору /users/1.
    Обновление пользователя user посредством метода PUT на URL /users/<id> для users.
    Удаление пользователя user посредством метода DELETE на URL /users/<id> для users.
    :param user_id: Идентификационный номер пользователя.
    :return: Возвращает пользователя в формате JSON.
    """
    user = User.query.get(user_id)
    if request.method == 'GET':
        return jsonify(user.to_dict())
    if request.method == 'DELETE':
        db.session.delete(user)
        db.session.commit()
        return '', 204
    if request.method == 'PUT':
        user_data = json.loads(request.data)
        user.first_name = user_data['first_name']
        user.last_name = user_data['last_name']
        user.role = user_data['role']
        user.phone = user_data['phone']
        user.email = user_data['email']
        user.age = user_data['age']
        db.session.add(user)
        db.session.commit()
        return '', 204


@app.route('/orders', methods=['GET', 'POST'])
def get_all_orders():
    """
    Представление для заказов, которое обрабатывает GET-запросы получения всех заказов.
    Реализует создание заказа order посредством метода POST на URL /orders для users.
    :return: Возвращает заказ в формате JSON.
    """
    if request.method == 'GET':
        orders = Order.query.all()
        result = [order.to_dict() for order in orders]
        return jsonify(result)
    elif request.method == 'POST':
        order_data = json.loads(request.data)
        db.session.add(Order(**order_data))
        db.session.commit()
        return '', 201


@app.route('/orders/<int:oid>', methods=['GET', 'PUT', 'DELETE'])
def get_order_by_id(oid: int):
    """
    Представление для заказа, которое обрабатывало бы GET-запросы получения по идентификатору
     /orders/<id>
    Обновление заказа order посредством метода PUT на URL /orders/<id>  для orders.
    Удаление заказа order посредством метода DELETE на URL /orders/<id> для orders.
    :param oid: Идентификационный номер заказа.
    :return: Возвращает заказ в формате JSON.
    """
    order = Order.query.get(oid)
    if request.method == 'GET':
        return jsonify(order.to_dict())
    if request.method == 'DELETE':
        db.session.delete(order)
        db.session.commit()
        return '', 204
    if request.method == 'PUT':
        order_data = json.loads(request.data)
        order.name = order_data['name']
        order.description = order_data['description']
        order.start_date = order_data['start_date']
        order.end_date = order_data['end_date']
        order.address = order_data['address']
        order.price = order_data['price']
        order.customer_id = order_data['address']
        order.executor_id = order_data['executor_id']
        db.session.add(order)
        db.session.commit()
        return '', 204


@app.route('/offers', methods=['GET', 'POST'])
def get_all_offers():
    """
    Представление, которое обрабатывает GET-запросы получения всех предложений /offers.
    Реализуйте создание предложения offer посредством метода POST на URL /offers для offers.
    :return: Возвращает предложения в формате JSON.
    """
    if request.method == 'GET':
        offers = Offer.query.all()
        result = [offer.to_dict() for offer in offers]
        return jsonify(result)
    elif request.method == 'POST':
        offer_data = json.loads(request.data)
        db.session.add(Offer(**offer_data))
        db.session.commit()
        return '', 201


@app.route('/offers/<int:oid>', methods=['GET', 'PUT', 'DELETE'])
def offer(oid: int):
    """
    Представление для предложения, которое обрабатывало бы GET-запросы получения предложения
    по идентификатору /offers/<id>. Создание предложения offer посредством метода POST на URL /offers для offers.
    Обновление предложения offer посредством метода PUT на URL /offers/<id> для offers.
    Удаление предложения offer посредством метода DELETE на URL /offers/<id> для offers.
    :param oid: Идентификационный номер пользователя.
    :return: Возвращает предложение в формате JSON.
    """
    offer = Offer.query.get(oid)
    if request.method == 'GET':
        return jsonify(offer.to_dict())
    if request.method == 'DELETE':
        db.session.delete(offer)
        db.session.commit()
        return '', 204
    if request.method == 'PUT':
        offer_data = json.loads(request.data)
        # offer.id = offer_data['id']
        offer.order_id = offer_data['order_id']
        offer.executor_id = offer_data['executor_id']
        db.session.add(offer)
        db.session.commit()
        return '', 204


if __name__ == '__main__':
    app.run(debug=True)
