from elasticsearch import Elasticsearch, helpers
import csv

es = Elasticsearch("http://localhost:9200")

def load_data_to_es(index_name, file_path):
    with open(file_path, encoding="utf-8") as f:
        reader = csv.DictReader(f)
        actions = [
            {
                "_index": index_name,
                "_source": row
            }
            for row in reader
        ]
        helpers.bulk(es, actions)

load_data_to_es("users", "users.csv")
load_data_to_es("products", "products.csv")
load_data_to_es("orders", "orders.csv")
load_data_to_es("order_details", "order_details.csv")
load_data_to_es("reviews", "reviews.csv")

print("Данные успешно загружены в Elasticsearch!")