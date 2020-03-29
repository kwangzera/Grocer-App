# convert.py
# Conversion land

from random import getrandbits

def from_obj(obj, fields):
    return {field: getattr(obj, field) for field in fields}
def to_obj(dict, fields):
    return {field: dict[field] for field in fields}

def from_dict(cls, dict, *, new_id=True):
    id = (getrandbits(63) if new_id else dict["id"])
    return cls(id=id, **to_obj(dict, cls.fields))
def to_dict(cls, obj):
    return {"id": obj.id, **from_obj(obj, cls.fields)}

def from_list(cls, lists):
    for value in lists:
        yield from_dict(cls, value)
def to_list(cls, *objs):
    ret = []
    for obj in objs:
        ret.append(from_dict(obj, cls.fields))
    return ret

def from_json(cls, json):
    for key, value in json.items():
        yield cls(id=int(key), **to_obj(value, cls.fields))
def to_json(cls, *objs):
    ret = {}
    for obj in objs:
        ret.update({str(obj.id): from_obj(obj, cls.fields)})
    return ret

