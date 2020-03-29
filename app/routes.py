from functools import wraps
from flask import redirect, request, url_for

from . import app, db
from .models import *
from .queries import *

def error(message):
    return {"error": {"message": repr(message)}}
def data(data):
    return {"data": data}

# Decorator to automatically change errors into error objects.
@wraps(app.route)
def rest_route(*args, **kwargs):
    def _outer_route(func):
        @app.route(*args, **kwargs)
        @wraps(func)
        def _inner_route(*args, **kwargs):
            try:
                return data(func(*args, **kwargs))
            except Exception as e:
                return error(e)
        return _inner_route
    return _outer_route


@app.route("/")
def index():
    # should give error lol
    return url_for('static', filename='index.html')


@rest_route("/items", methods=["GET", "POST"])
def items():
    if request.method == "GET":
        return [
            to_dict(StoreItem, item)
            for item in query_search(StoreItem, request.args)
        ]
    else:
        print(f"Adding {request.json}")
        try:
            query_add(db.session, *from_json(StoreItem, request.json))
        except:
            query_add(db.session, *from_dict(StoreItem, request.json))

@rest_route("/lists", methods=["GET", "POST"])
def lists():
    if request.method == "GET":
        return [
            {**to_dict(CustomerList, obj), "items": to_json(CustomerItem, *obj.items)}
            for obj in query_search(CustomerList, request.args)
        ]
    else:
        json = request.json
        list = from_dict(CustomerList, json)
        query_add(db.session, list)
        for item in from_json(CustomerItem, json["items"]):
            query_add(db.session, item)
            list.items.append(item)


@rest_route("/items/<int:id>")
def items_id(id):
    return to_dict(StoreItem, query_id(StoreItem, id))

@rest_route("/lists/<int:id>")
def lists_id(id):
    obj = query_id(CustomerList, id)
    return {**to_dict(CustomerList, obj), "items": to_json(CustomerItem, *obj.items)}


@app.route("/items/all")
def items_all():
    return redirect(url_for("items", first=StoreItem.query.count()))

@app.route("/lists/all")
def lists_all():
    return redirect(url_for("lists", first=CustomerList.query.count()))


@rest_route("/eval")
def expr():
    expr = request.args.get("expr", "None")
    return eval(expr)
