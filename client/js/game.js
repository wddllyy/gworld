const socket = io('http://localhost:5000');
const canvas = document.getElementById('gameCanvas');
const ctx = canvas.getContext('2d');

// 设置画布大小
const CELL_SIZE = 40;
const MAP_WIDTH = 40;
const MAP_HEIGHT = 30;
canvas.width = MAP_WIDTH * CELL_SIZE;
canvas.height = MAP_HEIGHT * CELL_SIZE;

// 缓存上一次的玩家位置
let lastPlayerPos = null;
// 存储所有游戏对象
let gameObjects = [];
// 当前选中的对象
let selectedObject = null;

// 绘制单个单元格
function drawCell(x, y, type) {
    ctx.fillStyle = type === 1 ? '#666' : '#eee';
    ctx.fillRect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE);
    
    // if (type === 1) {
    //     ctx.fillStyle = '#000';
    //     ctx.fillText('█', x * CELL_SIZE + 12, y * CELL_SIZE + 28);
    // }
}

// 绘制游戏对象
function drawGameObjects() {
    gameObjects.forEach(obj => {
        const { x, y, emoji } = obj;
        
        // 绘制对象emoji
        ctx.fillText(emoji, x * CELL_SIZE, y * CELL_SIZE + 32);
        
        // 如果是选中的对象，绘制高亮边框
        if (selectedObject && selectedObject.x === x && selectedObject.y === y) {
            ctx.strokeStyle = '#ff0000';
            ctx.lineWidth = 3;
            ctx.strokeRect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE);
        }
    });
}

// 绘制玩家
function drawPlayer(playerData) {
    const { x, y, emoji } = playerData;
    
    // 清除上一次的玩家位置
    if (lastPlayerPos) {
        drawCell(lastPlayerPos[0], lastPlayerPos[1], 0);
    }
    
    
    // 绘制玩家emoji
    ctx.fillText(emoji, x * CELL_SIZE, y * CELL_SIZE + 32);
    
    // 如果是选中的玩家，绘制高亮边框
    if (selectedObject && selectedObject.x === x && selectedObject.y === y) {
        ctx.strokeStyle = '#ff0000';
        ctx.lineWidth = 3;
        ctx.strokeRect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE);
    }
    
    lastPlayerPos = [x, y];
}

// 初始化地图
function initMap(map) {
    for (let y = 0; y < MAP_HEIGHT; y++) {
        for (let x = 0; x < MAP_WIDTH; x++) {
            drawCell(x, y, map[y][x]);
        }
    }
    // 绘制游戏对象
    drawGameObjects();
}

// 设置字体
ctx.font = '32px monospace';

// 鼠标点击检测
canvas.addEventListener('click', function(event) {
    const rect = canvas.getBoundingClientRect();
    const x = Math.floor((event.clientX - rect.left) / CELL_SIZE);
    const y = Math.floor((event.clientY - rect.top) / CELL_SIZE);
    
    // 检查是否点击了游戏对象
    const clickedObject = gameObjects.find(obj => obj.x === x && obj.y === y);
    if (clickedObject) {
        selectedObject = clickedObject;
        showObjectInfo(clickedObject);
        return;
    }
    
    // 检查是否点击了玩家
    if (lastPlayerPos && lastPlayerPos[0] === x && lastPlayerPos[1] === y) {
        selectedObject = { x: x, y: y, emoji: '🧍🏻‍♂️', type: 'player' };
        showObjectInfo(selectedObject);
        return;
    }
    
    // 点击空白区域，取消选择
    selectedObject = null;
    showObjectInfo(null);
});

// 显示物体信息
function showObjectInfo(obj) {
    const infoDiv = document.getElementById('object-info');
    
    if (!obj) {
        infoDiv.innerHTML = '<div class="no-selection">点击地图上的物体查看详细信息</div>';
        return;
    }
    
    let infoHtml = '<div class="object-info">';
    infoHtml += `<h3>${obj.emoji} ${getObjectTypeName(obj.type)}</h3>`;
    infoHtml += `<p><strong>位置:</strong> (${obj.x}, ${obj.y})</p>`;
    infoHtml += `<p><strong>类型:</strong> ${getObjectTypeName(obj.type)}</p>`;
    
    // 根据类型添加特定信息
    if (obj.type === 'tree') {
        infoHtml += '<p><strong>描述:</strong> 一棵大树，可以砍伐获得木材</p>';
    } else if (obj.type === 'stone') {
        infoHtml += '<p><strong>描述:</strong> 一块石头，可以开采获得石材</p>';
    } else if (obj.type === 'player') {
        infoHtml += '<p><strong>描述:</strong> 游戏玩家角色</p>';
    }
    
    infoHtml += '</div>';
    infoDiv.innerHTML = infoHtml;
}

// 获取物体类型的中文名称
function getObjectTypeName(type) {
    const typeNames = {
        'tree': '树',
        'stone': '石头',
        'player': '玩家'
    };
    return typeNames[type] || type;
}

socket.on('game_state', function(data) {
    // 如果是第一次收到数据，初始化地图
    if (!lastPlayerPos) {
        gameObjects = data.objects || [];
        initMap(data.map);
    } else {
        // 更新游戏对象
        gameObjects = data.objects || [];
    }
    
    // 重新绘制整个地图
    for (let y = 0; y < MAP_HEIGHT; y++) {
        for (let x = 0; x < MAP_WIDTH; x++) {
            drawCell(x, y, data.map[y][x]);
        }
    }
    
    // 绘制游戏对象
    drawGameObjects();
    
    // 更新玩家位置
    drawPlayer(data.player);
}); 