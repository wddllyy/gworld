import random
import time
from flask import Flask, render_template, send_from_directory
from flask_socketio import SocketIO
import threading
import os
from mapobj.tree import Tree
from mapobj.stone import Stone
from mapobj.player import Player

app = Flask(__name__, static_folder='../client')
socketio = SocketIO(app, cors_allowed_origins="*")

# 游戏状态
MAP_WIDTH = 40
MAP_HEIGHT = 30
TREE_COUNT = 20  # 树的数量
STONE_COUNT = 15  # 石头的数量
OBSTACLE_COUNT = 10  # 不可行tiles的数量
game_map = []
game_objects = []  # 存储所有游戏对象
player = None

def init_map():
    global game_map, game_objects, player
    # 初始化空白地图
    game_map = [[0 for _ in range(MAP_WIDTH)] for _ in range(MAP_HEIGHT)]
    game_objects = []
    
    # 随机设置不可行tiles
    for _ in range(OBSTACLE_COUNT):
        x = random.randint(0, MAP_WIDTH-1)
        y = random.randint(0, MAP_HEIGHT-1)
        game_map[y][x] = 1

    # 随机放置树
    tree_count = 0
    while tree_count < TREE_COUNT:
        x = random.randint(0, MAP_WIDTH-1)
        y = random.randint(0, MAP_HEIGHT-1)
        if game_map[y][x] == 0:  # 只在空白位置放置树
            tree = Tree(x, y)
            game_objects.append(tree)
            tree_count += 1
    
    # 随机放置石头
    stone_count = 0
    while stone_count < STONE_COUNT:
        x = random.randint(0, MAP_WIDTH-1)
        y = random.randint(0, MAP_HEIGHT-1)
        if game_map[y][x] == 0:  # 只在空白位置放置石头
            stone = Stone(x, y)
            game_objects.append(stone)
            stone_count += 1
    
    # 随机放置玩家
    while True:
        x = random.randint(0, MAP_WIDTH-1)
        y = random.randint(0, MAP_HEIGHT-1)
        if game_map[y][x] == 0:
            player = Player(x, y)
            break

def get_valid_moves(pos):
    moves = []
    x, y = pos
    for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
        new_x, new_y = x + dx, y + dy
        if (0 <= new_x < MAP_WIDTH and 
            0 <= new_y < MAP_HEIGHT and 
            game_map[new_y][new_x] == 0):
            moves.append((new_x, new_y))
    return moves

def game_loop():
    while True:
        # 获取可能的移动方向
        valid_moves = get_valid_moves(player.get_position())
        if valid_moves:
            # 随机选择一个有效移动
            new_x, new_y = random.choice(valid_moves)
            # 更新地图
            old_x, old_y = player.get_position()
            game_map[old_y][old_x] = 0
            game_map[new_y][new_x] = 1
            player.set_position(new_x, new_y)
        
        # 发送游戏状态给所有客户端
        socketio.emit('game_state', {
            'map': game_map,
            'player': player.to_dict(),
            'objects': [obj.to_dict() for obj in game_objects]
        })
        
        time.sleep(1)  # 每秒更新一次

@app.route('/')
def index():
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/js/<path:path>')
def send_js(path):
    return send_from_directory(os.path.join(app.static_folder, 'js'), path)

@socketio.on('connect')
def handle_connect():
    print('Client connected')
    socketio.emit('game_state', {
        'map': game_map,
        'player': player.to_dict(),
        'objects': [obj.to_dict() for obj in game_objects]
    })

if __name__ == '__main__':
    init_map()
    # 启动游戏循环线程
    game_thread = threading.Thread(target=game_loop)
    game_thread.daemon = True
    game_thread.start()
    
    socketio.run(app, debug=True, host='0.0.0.0', port=5000) 