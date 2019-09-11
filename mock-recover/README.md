# 项目描述
本项目是用于模拟服务商如何通过Agent以及Listener与BCOS区块链进行交互

# 项目部署注意事项

## 项目依赖
### Run Requirements
- python3
- pip3


### Install Python Requirements
```bash
pip3 install -r requirements.txt 
```

## 项目配置

#### 其他项目的配置
`mock-interact`中的`moduleUrl`固定是`/api/v1/recoverdata/`,
`listener`里面的配置应该是这个值

#### 服务商配置文件`provider.json`
json 样例：
```json
[
  {
    "id": "PARCEL0X2019050000000001",
    "name": "服务商测试01号"
  },
  {
    "id": "PARCEL0X2019050000000002",
    "name": "服务商测试02号"
  }
]
```
需要根据实际情况来配置

#### 模拟服务配置文件`config.ini`
具体的内容可以到项目里面去看，主要需要修改的部分有
```ini
[mock-service]
port: 8001
```
这个端口是`app`暴露给外面的`api`端口
```ini
[bcos-agent]
# mock服务地址
sync-chain-url: http://bcos-agent/api/v1/parcelx/bcosagent/add

# api 配置上链信息
groupId: 1
```
`sync-chain-url`是`agent`的上传待缓存数据的接口
`groupId`是对应组织的groupId


### Run
```bash
python mock-web.py
```