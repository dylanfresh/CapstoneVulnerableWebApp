# from flask import Flask
# import argparse

# app = Flask(__name__)

# @app.route('/')
# def helloWorld():
#     return 'Hello, World!'

# if __name__ == '__main__':
#     parser = argparse.ArgumentParser()
#     parser.add_argument('--port', type=int, default=5000)
#     args = parser.parse_args()

#     app.run(port=args.port, debug=True)

from flask import Flask
import argparse
import os

app = Flask(__name__)

@app.route('/')
def helloWorld():
    return f'Hello, World! Server PID: {os.getpid()}'

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--port', type=int, default=5000)
    args = parser.parse_args()

    print(f"Starting server on port {args.port}")
    app.run(port=args.port, debug=True, use_reloader=False)
    
