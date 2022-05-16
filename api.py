import mysql.connector
from flask import Flask, Response
from flask import jsonify
from flask import request
import jsonpickle

def get_connection_to_database():
    connection = mysql.connector.connect(
        user='root',
        password='',
        host='localhost',
        database='python')
    return connection

class Product:
    def __init__(self, product_id, product_name, product_value):
        self.product_id = product_id
        self.product_name = product_name
        self.product_value = product_value

class Order:
    def __init__(self, order_id, order_content):
        self.order_id = order_id
        self.order_content = order_content


app = Flask(__name__)


@app.route('/products', methods=['GET'])
def get_products():
    products = []
    connection = get_connection_to_database()
    cursor = connection.cursor(dictionary=True)
    query = 'SELECT id, name, value FROM products'
    cursor.execute(query)

    for row in cursor:
        products.append(Product(row['id'], row['name'], row['value']))

    connection.close()

    return Response(jsonpickle.encode(products, unpicklable=False), mimetype='application/json')


@app.route('/products', methods=['POST'])
def add_product():
    request_data = request.json
    try:
        connection = get_connection_to_database()
        cursor = connection.cursor()
            
        query = 'INSERT INTO products(name, value) VALUES(%(product_name)s, %(product_value)s)'
        cursor.execute(query, request_data)
        connection.commit()
    except mysql.connector.Error as error:
        return jsonify(details=error.msg), 400
    finally:
        connection.close()

    return request_data, 201

### ORDERS

@app.route('/orders', methods=['GET'])
def get_orders():
    orders = []
    connection = get_connection_to_database()
    cursor = connection.cursor(dictionary=True)
    query = 'SELECT * FROM orders'
    cursor.execute(query)

    for row in cursor:
        orders.append(Order(row['id'], row['product_id']))

    connection.close()

    return Response(jsonpickle.encode(orders, unpicklable=False), mimetype='application/json')

@app.route('/orders', methods=['POST'])
def create_order():
    request_data = request.json
    try:
        connection = get_connection_to_database()
        cursor = connection.cursor()
            
        query = 'INSERT INTO orders(product_id) VALUES(%(product_id)s)'
        cursor.execute(query, request_data)
        connection.commit()
    except mysql.connector.Error as error:
        return jsonify(details=error.msg), 400
    finally:
        connection.close()

    return request_data, 201

@app.route('/orders/<order_id>', methods=['PUT'])
def edit_order(order_id):
    request_data = request.json
    request_data['order_id'] = order_id
    try:
        connection = get_connection_to_database()
        cursor = connection.cursor()
            
        query = 'UPDATE orders SET product_id=%(product_id)s WHERE id=%(order_id)s'
        cursor.execute(query, request_data)
        connection.commit()
    except mysql.connector.Error as error:
        return jsonify(details=error.msg), 400
    finally:
        connection.close()

    return request_data, 200

@app.route('/orders/<order_id>', methods=['DELETE'])
def delete_order(order_id):
    request_data = {}
    request_data['order_id'] = order_id
    try:
        connection = get_connection_to_database()
        cursor = connection.cursor()
            
        query = 'DELETE FROM orders WHERE id=%(order_id)s'
        cursor.execute(query, request_data)
        connection.commit()
    except mysql.connector.Error as error:
        return jsonify(details=error.msg), 400
    finally:
        connection.close()

    return jsonify()


app.run(debug=True)