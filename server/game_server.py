import random
import time
from flask import Flask, render_template, send_from_directory
from flask_socketio import SocketIO
import threading
import os

app = Flask(__name__, static_folder='../client')
socketio = SocketIO(app, cors_allowed_origins="*")

# 游戏状态
MAP_SIZE = 100
OBSTACLE_COUNT = 90
game_map = []
player_pos = [0, 0]

def init_map():
    global game_map, player_pos
    # 初始化空白地图
    game_map = [[0 for _ in range(MAP_SIZE)] for _ in range(MAP_SIZE)]
    
    # 随机放置障碍物
    obstacles = 0
    while obstacles < OBSTACLE_COUNT:
        x = random.randint(0, MAP_SIZE-1)
        y = random.randint(0, MAP_SIZE-1)
        if game_map[y][x] == 0:
            game_map[y][x] = 1
            obstacles += 1
    
    # 随机放置玩家
    while True:
        x = random.randint(0, MAP_SIZE-1)
        y = random.randint(0, MAP_SIZE-1)
        if game_map[y][x] == 0:
            player_pos = [x, y]
            break

def get_valid_moves(pos):
    moves = []
    x, y = pos
    for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
        new_x, new_y = x + dx, y + dy
        if (0 <= new_x < MAP_SIZE and 
            0 <= new_y < MAP_SIZE and 
            game_map[new_y][new_x] == 0):
            moves.append((new_x, new_y))
    return moves

def game_loop():
    while True:
        # 获取可能的移动方向
        valid_moves = get_valid_moves(player_pos)
        if valid_moves:
            # 随机选择一个有效移动
            player_pos[0], player_pos[1] = random.choice(valid_moves)
        
        # 发送游戏状态给所有客户端
        socketio.emit('game_state', {
            'map': game_map,
            'player': player_pos
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
        'player': player_pos
    })

if __name__ == '__main__':
    init_map()
    # 启动游戏循环线程
    game_thread = threading.Thread(target=game_loop)
    game_thread.daemon = True
    game_thread.start()
    
    socketio.run(app, debug=True, host='0.0.0.0', port=5000) 