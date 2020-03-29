from .convert import *

def query_filter(cls, kwargs):
    """Return a query with filters applied using `kwargs`."""
    query = cls.query
    for key, value in kwargs.items():
        if key == "search":  # Special case "search"
            key = "titleHas"
        if key.endswith("Has"):
            filt = getattr(cls, key[:-3]).ilike(f"%{value}%")
        else:
            filt = getattr(cls, key).ilike(value)
        query = query.filter(filt)
    return query

def query_slice(query, skip, first):
    """Return a list of a slice of `query` starting at `skip` with len `first`."""
    return query.slice(skip, skip+first).all()

SKIP_DEFAULT = 0
FIRST_DEFAULT = 10
def query_search(cls, kwargs):
    """Return a list of `cls` using `kwargs`."""
    kwargs = dict(kwargs)
    skip = kwargs.pop("skip", SKIP_DEFAULT)
    first = kwargs.pop("first", FIRST_DEFAULT)
    if first == "all":
        first = cls.query.count()
    query = query_filter(cls, kwargs)
    return query_slice(query, int(skip), int(first))

def query_id(cls, id):
    """Return an obj of `cls` and with `id`."""
    obj = cls.query.get(id)
    if obj is None:
        raise LookupError(f"No {cls.__name__} found with id: {id}")
    return obj

def query_add(session, *objs):
    """Add `objs` to `session`."""
    for obj in objs:
        session.add(obj)
    session.commit()
    return objs
