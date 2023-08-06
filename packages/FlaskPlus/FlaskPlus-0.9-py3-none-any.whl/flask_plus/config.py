import os

from flask.config import Config as _Config


def json2object(rv):
    """
    如果一个dict中有__class__属性，说明该dict在序列化之前是一个class，则还原为class
    """

    if isinstance(rv, (int, str)):
        return rv
    if isinstance(rv, list):
        return [json2object(_) for _ in rv]
    if isinstance(rv, dict):

        if '__class__' in rv:
            del rv['__class__']
            obj = type('obj', (), {})
            for key, value in rv.items():
                setattr(obj, json2object(key), json2object(value))
            return obj
        else:
            return {json2object(k): json2object(v) for k, v in rv.items()}
    return rv


class Config(_Config):
    """
    从远程（URL）和本地（配置.py）载入配置
    本地配置可以覆盖远程配置
    优先级：远程 > 本地 > 环境变量
    以配置中心的配置为准，如果不存在，否以本地文件配置为准，如果不存在，则以环境变量为准，如果不存在，None。
    """

    def from_remote(self, url):
        # config from network
        import requests

        req = requests.get(url)
        assert req.status_code == 200, '请求远程配置失败'

        json = req.json()
        module = json2object(json)

        if isinstance(module, dict):
            self.from_mapping(**module)
        else:
            self.from_object(module)

    def __getattr__(self, item):
        if item in self:
            return self[item]
        # config from environment variable
        return os.environ.get(item)
