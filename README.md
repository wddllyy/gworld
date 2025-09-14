# 生存游戏模拟器

这是一个简单的生存游戏模拟器，包含服务器端和客户端。

## 项目结构

```
.
├── server/             # 服务器端代码
│   ├── game_server.py  # 主服务器文件
│   └── requirements.txt # Python依赖
└── client/            # 客户端代码
    ├── index.html     # 主页面
    └── js/            # JavaScript文件
        └── game.js    # 游戏逻辑
```

## 安装依赖

1. 进入server目录
2. 运行以下命令安装Python依赖：
```bash
pip install -r requirements.txt
```

## 运行服务器

1. 在server目录下运行：
```bash
python game_server.py
```

2. 服务器将在 http://localhost:5000 启动

## 访问游戏

1. 打开浏览器访问 http://localhost:5000
2. 你将看到一个100x100的地图，其中：
   - 灰色方块(█)表示障碍物
   - 红色方块(P)表示玩家
   - 玩家会每秒随机移动一格，遇到障碍物会自动绕行
