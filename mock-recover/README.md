# Run Requirements
- python3
- pip3


# Install Python Requirements
```bash
pip3 install -r requirements.txt 
```

# Config
服务商配置文件`provider.json`设置,  json 样例：
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

模拟服务配置文件`config.ini`设置： 
```ini
# 开发测试服务
[mock-service]
port: 8001
# 服务商配置 json 文件路径
provider: provider.json

# parcel-no 过滤条件
[parcel-no]
# 创建包裹轨迹 所对应监控的 url 子路径
upload-parcel-path: /parcel/upload
# 创建包裹轨迹 parcelNo 起始字符串过滤条件
startswith:
# 创建包裹轨迹 parcelNo 包含字符串过滤条件
contains:
# 创建包裹轨迹所在最低区块设置
min-block-number: 0

# 模拟包裹轨迹路径任务
[task]
# 任务名
id: mockParcelTrack
# 任务间隔时间
seconds: 15
# 任务下包裹该次调用是否执行概率 0 ~ 100. 例如80: 包裹轨迹更新该次有80%执行概率
ratio: 80

[bcos-agent]
# mock服务地址
sync-chain-url: http://127.0.0.1:8080/api/v1/fabricData/add
# 是否推送
post: false

# api 配置上链信息
groupId: 1
```

# Run
```bash
python mock-web.py
```