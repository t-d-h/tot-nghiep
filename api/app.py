from flask import Flask, request
import os, time

app = Flask(__name__)
auth_key = os.getenv("AUTHORIZATION_KEY")

@app.route('/')
def hello():
    now = time.strftime('%Y-%m-%d %H:%M:%S')
    # print("---")
    # print(request.headers.get('Authorization'), flush=True)
    if request.headers.get('Authorization') == auth_key:
        return str(now) + ": Authen succeed"
    # read http body data: https://stackoverflow.com/questions/10434599/get-the-data-received-in-a-flask-request
    return str(now) + ": who the hell r u 403", 403

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)