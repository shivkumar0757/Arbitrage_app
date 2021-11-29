from flask import Flask

app = Flask(__name__)

# Members api Route
@app.route("/")
def home_page():
    return "Hi There welcome to home"

@app.route("/list")
def data_list():
    return {'data':[1,2,3,6,9,0]}

if __name__ == "__main__":
    app.run(debug=True)