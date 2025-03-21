## 测试启动入口文件
- main.py

## 测试启动前配置
- 修改redis文件，在路径`core/redis/RedisConfig.py`，也可以在实例化RedisConfig传参
- 这里平时的开发习惯是会把这些配置弄成环境变量等



## 接口调用
```json
# 请求地址
http://127.0.0.1:18080/api/search

# 请求方式：POST

# body参数
{
    "query": "what is cat?"
}
```

