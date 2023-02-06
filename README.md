# Поиск исполнителя и заказа

## Приложение на Flask

***

- Есть пользователь, он может быть как заказчиком, так и исполнителем.
- Пользователь с ролью Заказчик может создать Заказ.
- Пользователь с ролью Исполнитель может откликнуться на Заказ и предложить выполнить его (Offer).

***


* data_base
* main

'''


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

'''