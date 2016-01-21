from bottle import route, app


@route("/")
@app.view("home")
def home():
    return {}
