from flask import Flask, jsonify, request, render_template, redirect, url_for
from elasticsearch import Elasticsearch

app = Flask(__name__, template_folder='templates')
es = Elasticsearch("http://localhost:9200")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/products', methods=['GET'])
def get_products():
    res = es.search(index="products", body={"query": {"match_all": {}}})
    products = [hit["_source"] for hit in res['hits']['hits']]
    return render_template('view_products.html', products=products)

@app.route('/products/category/<category>', methods=['GET'])
def get_products_by_category(category):
    res = es.search(index="products", body={
        "query": {
            "match": {
                "category": category
            }
        }
    })
    products = [hit["_source"] for hit in res['hits']['hits']]
    return render_template('view_products.html', products=products)

@app.route('/add_product', methods=['GET', 'POST'])
def add_product():
    if request.method == 'POST':
        product_data = request.form.to_dict()
        es.index(index="products", body=product_data)
        return redirect(url_for('get_products'))
    return render_template('add_product.html')

@app.route('/update_product/<int:product_id>', methods=['GET', 'POST'])
def update_product(product_id):
    if request.method == 'POST':
        new_price = request.form['price']
        es.update(index="products", id=product_id, body={"doc": {"price": new_price}})
        return redirect(url_for('get_products'))
    
    product = es.get(index="products", id=product_id)['_source']
    return render_template('update_product.html', product=product)

@app.route('/delete_product/<int:product_id>', methods=['POST'])
def delete_product(product_id):
    es.delete(index="products", id=product_id)
    return redirect(url_for('get_products'))

@app.route('/orders/user/<int:user_id>', methods=['GET'])
def get_orders_by_user(user_id):
    res = es.search(index="orders", body={
        "query": {
            "match": {
                "user_id": user_id
            }
        }
    })
    orders = [hit["_source"] for hit in res['hits']['hits']]
    return render_template('view_orders.html', orders=orders)

@app.route('/order_status/<int:order_id>', methods=['GET'])
def order_status(order_id):
    order = es.get(index="orders", id=order_id)['_source']
    return render_template('order_status.html', order=order)

if __name__ == '__main__':
    app.run(debug=True)