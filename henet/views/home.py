from bottle import view, route, request, app


@route("/")
@app.view("home")
def home():
    return {}
