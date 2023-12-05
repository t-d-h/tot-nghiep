from flask import Flask
from redis import Redis
import os, time #for correcting timezone

app = Flask(__name__)
redis = Redis(host='redis', port=6379)

os.environ['TZ'] = 'Asia/Ho_Chi_Minh'
time.tzset()

@app.route('/')
def hello():
    count = redis.incr('hits')
    print(time.strftime('%Y-%m-%d %H:%M:%S'))
    return 'Hello World! I have been seen {} times.\n'.format(count)

if __name__ == "__main__":
    app.run(host="0.0.0.0")#debug=True