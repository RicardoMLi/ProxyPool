import redis
import re

from random import choice

from .settings import REDIS_HOST, REDIS_PASSWORD, REDIS_PORT, REDIS_KEY, INITIAL_SCORE
from .settings import MAX_SCORE, MIN_SCORE
from .error import PoolEmptyError

class RedisClient(object):
    def __init__(self, host=REDIS_HOST, port=REDIS_PORT, password=REDIS_PASSWORD):
        self.db = redis.StrictRedis(host=host, port=port, password=password, decode_responses=True)

    def add(self, proxy, score=INITIAL_SCORE):
        """
        :param proxy: 待添加代理
        :param score: 代理分数
        :return: 添加结果
        """
        if not re.match('\d+\.\d+\.\d+\.\d+\:\d+', proxy):
            print('代理不符合规范:', proxy)
            return None

        # 代理分数不低于0才加入代理池
        if not self.db.zscore(REDIS_KEY,proxy):
            return self.db.zadd(REDIS_KEY, score, proxy)

    def get(self):
        """
        获取随机代理，首先尝试获取分数为100代理，如果不存在，按照排名获取，否则异常
        :return: 随机代理
        """
        proxies = self.db.zrangebyscore(REDIS_KEY, MAX_SCORE, MAX_SCORE)

        if len(proxies) == 0:
            proxies = self.db.zrevrange(REDIS_KEY, 0, 100)
            if proxies:
                return choice(proxies)
            else:
                raise PoolEmptyError
        else:
            return choice(proxies)

    def decrease(self, proxy):
        """
        将对应代理减分
        :param proxy: 代理
        :return: 减分后的代理分数
        """
        score = self.db.zscore(REDIS_KEY, proxy)
        if score and score > MIN_SCORE:
            print('当前代理:', proxy, '分数:', score, '减1')
            return self.db.zincrby(REDIS_KEY, proxy , -1)
        else:
            print('当前代理分数过低，已移除:' + proxy)
            return self.db.zrem(REDIS_KEY, proxy)

    def exists(self, proxy):
        """
        判断代理是否存在
        :param proxy: 输入代理
        :return: 代理是否存在
        """
        return not self.db.zscore(REDIS_KEY, proxy) == None

    def max(self, proxy):
        """
        将代理设置为MAX_SCORE
        :param proxy: 代理
        :return: 设置结果
        """
        print('代理', proxy, '可用，设置为', MAX_SCORE)
        return self.db.zadd(REDIS_KEY, MAX_SCORE, proxy)

    def count(self):
        """
        获取数量
        :return: 数量
        """
        return self.db.zcard(REDIS_KEY)

    def all(self):
        """
        获取全部代理
        :return: 全部代理列表
        """
        return self.db.zrangebyscore(REDIS_KEY, MIN_SCORE, MAX_SCORE)

    def batch(self, start, stop):
        """
        批量获取代理
        :param start: 开始索引
        :param stop: 结束索引
        :return: 代理列表
        """
        return self.db.zrevrange(REDIS_KEY, start, stop - 1)

if __name__ == '__main__':
    conn = RedisClient()
    result = conn.all()
    print(result)



