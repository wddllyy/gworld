const socket = io('http://localhost:5000');
const canvas = document.getElementById('gameCanvas');
const ctx = canvas.getContext('2d');

// 设置画布大小
const CELL_SIZE = 10;
const MAP_SIZE = 100;
canvas.width = MAP_SIZE * CELL_SIZE;
canvas.height = MAP_SIZE * CELL_SIZE;

// 缓存上一次的玩家位置
let lastPlayerPos = null;

// 绘制单个单元格
function drawCell(x, y, type) {
    ctx.fillStyle = type === 1 ? '#666' : '#fff';
    ctx.fillRect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE);
    
    if (type === 1) {
        ctx.fillStyle = '#000';
        ctx.fillText('█', x * CELL_SIZE + 2, y * CELL_SIZE + 8);
    }
}

// 绘制玩家
function drawPlayer(x, y) {
    // 清除上一次的玩家位置
    if (lastPlayerPos) {
        drawCell(lastPlayerPos[0], lastPlayerPos[1], 0);
    }
    
    // 绘制新的玩家位置
    ctx.fillStyle = '#f00';
    ctx.fillRect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE);
    ctx.fillStyle = '#fff';
    ctx.fillText('P', x * CELL_SIZE + 2, y * CELL_SIZE + 8);
    
    lastPlayerPos = [x, y];
}

// 初始化地图
function initMap(map) {
    for (let y = 0; y < MAP_SIZE; y++) {
        for (let x = 0; x < MAP_SIZE; x++) {
            drawCell(x, y, map[y][x]);
        }
    }
}

// 设置字体
ctx.font = '8px monospace';

socket.on('game_state', function(data) {
    // 如果是第一次收到数据，初始化地图
    if (!lastPlayerPos) {
        initMap(data.map);
    }
    
    // 只更新玩家位置
    drawPlayer(data.player[0], data.player[1]);
}); 