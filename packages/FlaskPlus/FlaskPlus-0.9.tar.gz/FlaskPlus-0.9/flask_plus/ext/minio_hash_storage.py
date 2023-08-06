import hashlib
from io import BytesIO

from flask_plus import exts
from .minio_storage import Storage


class HashStorage(Storage):
    """
    无重复文件的存储桶，文件使用sha1算法命名
    """

    def put(self, data):
        if hasattr(data, 'read') and callable(getattr(data, 'read')):
            raw = data.read()
            data.seek(0)
        elif isinstance(data, bytes):
            raw, data = data, BytesIO(data)
        elif isinstance(data, str):
            raw = data.encode()
            data = BytesIO(raw)
        else:
            raise AssertionError('Invalid data')

        length = len(raw)
        name = hashlib.sha1(raw).hexdigest()

        if self.exist(name):
            return name, length

        self.client.put_object(self.bucket, name, data, length)
        return name, length


def active(app):
    assert app.config.MINIO_URL, '请先设置MINIO_URL'
    assert app.config.MINIO_ACCESS_KEY, '请先设置MINIO_ACCESS_KEY'
    assert app.config.MINIO_SECRET_KEY, '请先设置MINIO_SECRET_KEY'
    assert not hasattr(exts, 'storage'), '变量storage已被挂载'

    exts.storage = HashStorage(
        app.config.MINIO_URL,
        access_key=app.config.MINIO_ACCESS_KEY,
        secret_key=app.config.MINIO_SECRET_KEY,
        bucket=app.config.MINIO_BUCKET or 'default'
    )
