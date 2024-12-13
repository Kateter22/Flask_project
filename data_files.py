import random
from faker import Faker
import pandas as pd

fake = Faker()

# Словари с примерами товаров для каждой категории
categories = {
    'Одежда': [
        'Платье', 'Туфли', 'Джинсы', 'Футболка', 'Куртка',
        'Шорты', 'Свитер', 'Кроссовки'
    ],
    'Косметика': [
        'Помада', 'Тональный крем', 'Тушь для ресниц', 'Парфюм',
        'Лосьон для тела', 'Шампунь', 'Маска для лица', 'Крем для рук'
    ],
    'Электроника': [
        'Смартфон', 'Ноутбук', 'Телевизор', 'Наушники', 
        'Планшет', 'Цифровая камера', 'Умные часы', 'Bluetooth колонка'
    ],
    'Игрушки': [
        'Плюшевый медведь', 'Конструктор', 'Кукла', 
        'Машинка', 'Настольная игра', 'Робот', 
        'Пазл', 'Набор для творчества'
    ],
    'Продукты питания': [
        'Хлеб', 'Молоко', 'Яйца', 'Фрукты', 
        'Овощи', 'Мясо', 'Рыба', 'Сыр'
    ]
}

def generate_users(n=100):
    users = []
    for i in range(1, n + 1):
        users.append({
            "id": i,
            "name": fake.name(),
            "email": fake.email(),
            "address": fake.address(),
            "phone": fake.phone_number()
        })
    return users

def generate_products(n=100):
    products = []
    category_names = list(categories.keys())
    
    for i in range(1, n + 1):
        category = random.choice(category_names)
        product_name = random.choice(categories[category])
        products.append({
            "id": i,
            "name": product_name,
            "price": round(random.uniform(10, 500), 2),
            "category": category
        })
    return products

def generate_orders(users, n=100):
    orders = []
    for i in range(1, n + 1):
        orders.append({
            "id": i,
            "user_id": random.choice(users)["id"],
            "order_date": fake.date_this_year(),
            "status": random.choice(["Pending", "Completed", "Cancelled"])
        })
    return orders

def generate_order_details(orders, products, n=300):
    order_details = []
    for i in range(1, n + 1):
        order_details.append({
            "id": i,
            "order_id": random.choice(orders)["id"],
            "product_id": random.choice(products)["id"],
            "quantity": random.randint(1, 5)
        })
    return order_details

def generate_reviews(users, products, n=200):
    reviews = []
    for i in range(1, n + 1):
        reviews.append({
            "id": i,
            "user_id": random.choice(users)["id"],
            "product_id": random.choice(products)["id"],
            "rating": random.randint(1, 5),
            "comment": fake.text(max_nb_chars=200)
        })
    return reviews

users = generate_users()
products = generate_products()
orders = generate_orders(users)
order_details = generate_order_details(orders, products)
reviews = generate_reviews(users, products)

users_df = pd.DataFrame(users)
products_df = pd.DataFrame(products)
orders_df = pd.DataFrame(orders)
order_details_df = pd.DataFrame(order_details)
reviews_df = pd.DataFrame(reviews)

users_df.to_csv("users.csv", index=False)
products_df.to_csv("products.csv", index=False)
orders_df.to_csv("orders.csv", index=False)
order_details_df.to_csv("order_details.csv", index=False)
reviews_df.to_csv("reviews.csv", index=False)

print("Закончили!")