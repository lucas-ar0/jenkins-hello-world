from flask import Flask

app = Flask(__name__)

@app.get("/")
def hello():
    return "Hola mundo desde Jenkins + Docker + Ubuntu!"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)