from redis import Redis
from uuid import uuid4


class redis_session:
    prefix = 'session_key:'
    server_ip = 'localhost'
    port = 5002
    timeout = 3600

    def __init__(self):
        self.db = Redis(self.server_ip, self.port)

    def open_session(self, session_key):
        name = self.db.get(self.prefix+session_key)

        if name is not None:
            self.db.expire(self.prefix+session_key, self.timeout)

        return name

    def save_session(self, name):
        session_key = str(uuid4())

        self.db.setex(self.prefix+session_key, name, self.timeout)

        return session_key

if __name__ == '__main__':
    r_session = redis_session()