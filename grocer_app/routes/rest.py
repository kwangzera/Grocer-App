from functools import wraps
from traceback import format_exc

from flask import Blueprint, redirect, request, url_for

from ..extensions import db
from ..models import *
from ..queries import *

rest = Blueprint("rest", __name__)

def error(exc):
    return {"error": {"message": repr(exc), "messageFull": [format_exc().splitlines()]}}
def data(data):
    return {"data": data}

# Decorator to automatically change errors into error objects.
def obj_always(func):
    @wraps(func)
    def _wrapper(*args, **kwargs):
        try:
            return data(func(*args, **kwargs))
        except Exception as e:
            return error(e)
    return _wrapper


@rest.route("/items", methods=["GET", "POST"])
@obj_always
def items_query():
    if request.method == "GET":
        return [
            to_dict(StoreItem, item)
            for item in query_search(StoreItem, request.args)
        ]
    else:
        query_add(db.session, *from_dict(StoreItem, request.json))

@rest.route("/lists", methods=["GET", "POST"])
@obj_always
def lists_query():
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


@rest.route("/items/<int:id>")
@obj_always
def items_id(id):
    return to_dict(StoreItem, query_id(StoreItem, id))

@rest.route("/lists/<int:id>")
@obj_always
def lists_id(id):
    obj = query_id(CustomerList, id)
    return {**to_dict(CustomerList, obj), "items": to_json(CustomerItem, *obj.items)}


@rest.route("/items/all")
def items_all():
    return redirect(url_for("items_query", first=StoreItem.query.count()))

@rest.route("/lists/all")
def lists_all():
    return redirect(url_for("lists_query", first=CustomerList.query.count()))


@rest.route("/eval")
@obj_always
def expr():
    expr = request.args.get("expr", "None")
    return eval(expr)
