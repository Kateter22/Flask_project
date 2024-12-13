from flask import Flask, request, jsonify
from elasticsearch import Elasticsearch

app = Flask(__name__)
es = Elasticsearch("http://localhost:9200")

@app.route("/<index_name>", methods=["GET"])
def get_all(index_name):
    try:
        response = es.search(index=index_name, body={"query": {"match_all": {}}}, size=100)
        return jsonify([hit["_source"] for hit in response["hits"]["hits"]])
    except Exception as e:
        return jsonify({"error": str(e)})

@app.route("/<index_name>/<doc_id>", methods=["GET"])
def get_by_id(index_name, doc_id):
    try:
        response = es.get(index=index_name, id=doc_id)
        return jsonify(response["_source"])
    except Exception as e:
        return jsonify({"error": str(e)})

@app.route("/<index_name>", methods=["POST"])
def add_document(index_name):
    try:
        document = request.json
        response = es.index(index=index_name, document=document)
        return jsonify({"result": "Document added", "id": response["_id"]})
    except Exception as e:
        return jsonify({"error": str(e)})

@app.route("/<index_name>/<doc_id>", methods=["PUT"])
def update_document(index_name, doc_id):
    try:
        document = request.json
        response = es.update(index=index_name, id=doc_id, body={"doc": document})
        return jsonify({"result": "Document updated"})
    except Exception as e:
        return jsonify({"error": str(e)})

@app.route("/<index_name>/<doc_id>", methods=["DELETE"])
def delete_document(index_name, doc_id):
    try:
        es.delete(index=index_name, id=doc_id)
        return jsonify({"result": "Document deleted"})
    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == "__main__":
    app.run(debug=True)