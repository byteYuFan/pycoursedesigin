import random
import string
import redis


def generate_verification_code(length=6):
    characters = string.digits  # 仅包含数字的字符集
    code = ''.join(random.choice(characters) for _ in range(length))
    return code


def store_verification_code(email, code, expire_time=300):
    redis_client = get_redis_connection()
    redis_key = email
    redis_client.set(redis_key, code, ex=expire_time)


def check_verification_code(email, code):
    redis_client = get_redis_connection()
    redis_key = email
    stored_code = redis_client.get(redis_key)

    if stored_code and stored_code.decode() == code:
        return True

    return False


def get_redis_connection():
    redis_host = 'localhost'
    redis_port = 6379
    redis_db = 0
    redis_client = redis.Redis(host=redis_host, port=redis_port, db=redis_db)
    return redis_client
