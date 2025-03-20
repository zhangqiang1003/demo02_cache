# 生成缓存键（带参数哈希）
import hashlib


class HashUtil(object):

    @staticmethod
    def generate_cache_key(params: dict) -> str:
        """
        生成redis缓存key
        :param params: 请求对象
        :return: str
        """
        return f"query_{hashlib.md5(str(params).encode()).hexdigest()}"
