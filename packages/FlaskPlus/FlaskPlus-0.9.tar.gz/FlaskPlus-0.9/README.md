# Flask Plus

flask 加强版，轻松编程。

```
pip install flaskplus
```

### 基本功能

- app提供直接注册文件或函数的方式来自动注册route
- config支持从远程，本地文件，环境变量来获取配置
- 默认返回json类型的数据
- response支持超多类型直接返回
- exception自动处理全部异常
- field支持url参数与json参数的解析
- 自由激活的ext扩展

### ext扩展

- file_logging实现记录日志到文件
- mongo_logging实现记录日志到mongodb
- auth_header实现解析Authorization
- kong_header实现解析X-Consumer-Custom-Id/Username
- mongo实现mongo连接
- redis实现redis连接
- minio_storage实现minio文件存储
- minio_hash_storage实现minio无重复文件存储
