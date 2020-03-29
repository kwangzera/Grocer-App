''' 
API Standard
https://docs.google.com/document/d/11vNLSPNwHVRYiJ0l_K0Ug8o_rNdTN7updBXO1Tzy2Do/edit?ts=5e7d7675

GET: /groceries?search=<string>&skip=<int>&first=<int>
- Return list of grocery items that match the search, skipping the first <skip> and returning the first <first> amounts (pagination)
- Send image URLs (maybe instead of hardcoding, find a way to automate the process)
Yo do you understand this part
I don't understand the concept of skip and first

lol you know how there's pages
the skip means to skip the first # of items
the first means to return # amount of items


GET: /lists?location=<string>&skip=<int>&first=<int>
- Returns a list of grocery list summaries (e.g. id, number of items, etc.)  based on a location (we're hardcoding the available locations)
- Pagination with <skip> and <first>

GET: /lists/:id
- Returns the details of a grocery list (items, Bar code, etc.) by its id

POST: /lists/create
- Creates a grocery list/request that gets uploaded to the server

'''


from flask import Flask
from markupsafe import escape
# https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-iv-database

app = Flask(__name__.split()[0])

@app.route("/")
def index():
    return """
    <div>
    Home Page
    </div>
    <a href="/groceries"> groceries </a>
    <a href="/lists"> lists </a>
    <a href="/groceries_json"> groceries_json </a>
    """

@app.route("/groceries")
def groceries():
    return "matched search groceries"

@app.route("/lists")
def list_groceries():
    return "List of groceries"

@app.route("/groceries_json")
def groceries_json():
    # returning a dict is special cased for json
    return {
        "fruits": ["apple", "banana", "orange", "watermelon", "peach"],
        "veg": ["bok choy", "rutabaga", "pea", "chard", "lettuce"],
        "meat": ["willson", "fax mcclad", "bessie the cow"],
        "snack": ["doritos", "mtn dew", "smarties"],
        "frozen goodz": ["pizza popz", "chicken nuggets", "pogo"],
        "others" : ["questionable goods"]
    }

"""@app.route("/user/<string:username>/")
def show_profile(username):
    # Show the user profile for that user
    return f"User {escape(username)}"  # Escape incase "<" and ">" in the string

@app.route("/post/<int:post_id>")
def show_id(post_id):
    # Show the post with the given id, the id is an integer
    return f"Post {post_id}"

@app.route("/path/<path:subpath>")
def show_subpath(subpath):
    # Show the subpath aftclicer /path/
    return f"Subpath {escape(subpath)}"""

if __name__ == "__main__":
    app.run(debug=True)  # Has auto reloading (ebic)



# Cd\Users\boblu\Desktop\Programming\Temporary Queue\flask_intro\venv\venv
