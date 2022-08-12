from flask import jsonify, Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func

import models

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:test@db:5432/test_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SQLALCHEMY_POOL_SIZE'] = 1
app.config['SQLALCHEMY_MAX_OVERFLOW'] = 0
db = SQLAlchemy(app, session_options={'autocommit': True})


# Получение всех заказов
@app.route('/data')
def orders():
    all_orders = models.Order.query.order_by(models.Order.id)
    results = [order.format() for order in all_orders]
    return jsonify(
        {
            'success': True,
            'results': results,
            'count': len(results)
        }
    )


# Заказы (фильтр - валюта)
@app.route('/data/order_by_valute/<valute>')
def orders_by_valute(valute):
    if valute == 'usd':
        all_orders = models.Order.query.order_by(models.Order.value_usd)
    elif valute == 'rub':
        all_orders = models.Order.query.order_by(models.Order.value_rub)
    else:
        return None
    results = [order.format() for order in all_orders]
    return jsonify(
        {
            'success': True,
            'results': results,
            'count': len(results)
        }
    )


# Заказы (фильтр - дата)
@app.route('/data/order_by_date')
def orders_by_date():
    all_orders = models.Order.query.order_by(models.Order.delivery_date)
    results = [order.format() for order in all_orders]
    return jsonify(
        {
            'success': True,
            'results': results,
            'count': len(results)
        }
    )


# Заказы (фильтр - просуммированы заказы на каждую дату)
@app.route('/data/order_by_date_and_values')
def order_by_date_and_values():
    all_orders = models.Order.query.with_entities(models.Order.delivery_date,
                                                  func.sum(models.Order.value_usd).label('total')).group_by(
        models.Order.delivery_date).order_by(models.Order.delivery_date)
    results = [{'date': order[0].strftime('%Y-%m-%d'), 'total': order[1]} for order in all_orders]
    return jsonify(
        {
            'success': True,
            'results': results,
            'count': len(results)
        }
    )


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
