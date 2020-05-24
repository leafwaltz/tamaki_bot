import redis
from .config import redis_port

class redis_delegate:
    def __init__(self):
        pool = redis.ConnectionPool(host='localhost', port=redis_port, decode_responses=True)
        self.redis = redis.Redis(connection_pool=pool)

        self.guild_table = {
            "loop" : 0,
            "boss_index" : 1
        }
        
    def init_state(self):
        self.redis.set("guilds", ["test"])
        print(self.redis.get("guilds"))
        