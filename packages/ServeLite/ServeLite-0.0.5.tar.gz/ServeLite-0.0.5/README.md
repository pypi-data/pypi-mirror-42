# ServeLite
### 轻量级服务化框架

# 特性
- 一键部署 开发便捷
- 字段级访问权限控制
- 封装的私有安全协议
- 支持第三方安全地开发拓展服务

# Usage
> 由于flask-restless的bug, 需要**手动**将`\flask_restless\manager.py`
`create_api_blueprint`方法下的`collection_name = model.__tablename__`修改为`collection_name = model.__table__.name`
<br>(win版本line 551)

> flask-restless在2016年merge了该[pull request](https://github.com/jfinkels/flask-restless/pull/436)
当前版本中仍然存在的原因不清楚

### to be finished...

# 设计
## 身份验证
系统使用JWT协议进行身份认证。JWT密钥为服务公钥签名字符串，盐值为签名前四位。负载为服务hash、服务权限。

该设计的好处是，发现JWT持有者和记录请求服务hash不同时，说明该JWT已经被盗用，服务通知注册中心作废该token。


# TODO
### 名称表
确保双端名称解耦
### 服务发现
注册中心的api也应该被纳入到服务发现中
### session管理