import uuid
from io import BytesIO

from minio import Minio
from minio.error import BucketAlreadyExists, BucketAlreadyOwnedByYou, NoSuchKey

from flask_plus import exts


class Storage:
    def __init__(self, endpoint, access_key=None, secret_key=None, bucket='storage'):
        self.client = Minio(
            endpoint=endpoint, access_key=access_key, secret_key=secret_key, secure=False, region='cn-north-1')
        self.bucket = bucket

        self._bucket_init()

    def _bucket_init(self):
        try:
            self.client.make_bucket(self.bucket, location='cn-north-1')
        except (BucketAlreadyOwnedByYou, BucketAlreadyExists):
            pass

    def exist(self, name):
        try:
            self.client.stat_object(self.bucket, name)
            return True
        except NoSuchKey:
            return False

    def get(self, name):
        return self.client.get_object(self.bucket, name)

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
        name = uuid.uuid1().hex

        self.client.put_object(self.bucket, name, data, length)
        return name, length

    def fget(self, name, file_path=None):
        if file_path is None:
            file_path = name.rsplit('/', 1)[-1]
        return self.client.fget_object(self.bucket, name, file_path)

    def fput(self, file_path):
        with open(file_path, 'rb') as data:
            return self.put(data)

    def remove(self, name):
        return self.client.remove_object(self.bucket, name)


def active(app):
    assert app.config.MINIO_URL, '请先设置MINIO_URL'
    assert app.config.MINIO_ACCESS_KEY, '请先设置MINIO_ACCESS_KEY'
    assert app.config.MINIO_SECRET_KEY, '请先设置MINIO_SECRET_KEY'
    assert not hasattr(exts, 'storage'), '变量storage已被挂载'

    exts.storage = Storage(
        app.config.MINIO_URL,
        access_key=app.config.MINIO_ACCESS_KEY,
        secret_key=app.config.MINIO_SECRET_KEY,
        bucket=app.config.MINIO_BUCKET or 'default'
    )
