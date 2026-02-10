import argparse
import os
from app import create_app

app = create_app()  #uses factory instead of Flask directly 

@app.after_request
def add_pid_header(response):
    response.headers["X-Server-PID"] = str(os.getpid())
    return response

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--port', type=int, default=5000)
    args = parser.parse_args()

    print(f"Starting server on port {args.port}")
    app.run(port=args.port, debug=True, use_reloader=False)
