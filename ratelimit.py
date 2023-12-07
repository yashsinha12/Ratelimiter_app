from flask import Flask
import time

class RateLimiter:
    def __init__(self, limit, window_size):
        self.limit = limit
        self.window_size = window_size
        self.timestamps = []

    def is_allowed(self):
        current_time = time.time()
        self.timestamps = [t for t in self.timestamps if t > current_time - self.window_size]

        if len(self.timestamps) < self.limit:
            self.timestamps.append(current_time)
            return True
        else:
            return False

app = Flask(__name__)
limiter = RateLimiter(limit=10, window_size=60)

@app.route('/api/resource', methods=['GET'])
def get_resource():
    if limiter.is_allowed():
        return "Resource available"
    else:
        return "Rate limit exceeded", 429  # HTTP 429 Too Many Requests

if __name__ == '__main__':
    app.run(debug=True)
