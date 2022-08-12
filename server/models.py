from run_server import db


class Order(db.Model):
    __tablename__ = 'orders'

    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, nullable=False, unique=True)
    value_usd = db.Column(db.Float, nullable=False)
    value_rub = db.Column(db.Float)
    delivery_date = db.Column(db.Date)
    notification_sent = db.Column(db.Boolean, server_default="false", default=False)

    def __init__(self, order_id, value_usd, value_rub, delivery_date, notification_sent):
        self.order_id = order_id
        self.value_usd = value_usd
        self.value_rub = value_rub
        self.delivery_date = delivery_date
        self.notification_sent = notification_sent

    def format(self):
        return {
            'id': self.id,
            'order_id': self.order_id,
            'value_usd': self.value_usd,
            'value_rub': self.value_rub,
            'delivery_date': self.delivery_date,
            'notification_sent': self.notification_sent
        }


class UserBot(db.Model):
    __tablename__ = 'bot_users'

    id = db.Column(db.Integer, primary_key=True, autoincrement='auto')
    user_id = db.Column(db.Integer, nullable=False, unique=True)

    def __init__(self, user_id):
        self.user_id = user_id

    def format(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
        }


db.create_all()
