# scsx-market

一个超市进销存系统

## 使用方法

下载并进入目录：

```shell
git clone git@github.com:KZNS/scsx-market.git
cd scsx-market
```

安装依赖:

```shell
pip install -r requirements.txt
```

启动服务：

```shell
python serve.py
```

之后可以通过服务器地址在公网中访问。

或者可以通过以下地址在内网访问：

```text
http://127.0.0.1:5000
```

## 使用技术

### 前端

前端使用js的jquery库和ajax来异步获取数据，动态更新页面，提高了用户体验

### 后端

后端使用python的flask框架

### 数据库

数据库部分使用了Flask-SQLAlchemy，即ORM（关系对象模型）技术

## 制作

by 普通上班组
