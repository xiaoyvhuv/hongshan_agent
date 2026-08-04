# 红山游伴 · 动态路线后端 MVP

这是独立于现有移动端原型的后端工程，覆盖文档中的模块二“游前动态路线规划”和模块三“游中动态调整”。不会修改上级目录中的 `src/`、`package.json` 或任何原型文件。

## 技术闭环

- FastAPI：HTTP API 层
- Python Orchestrator：确定性状态机，决定调用哪个 Agent
- Intent Agent：将自然语言转成结构化游玩偏好
- Route Agent：NetworkX/Dijkstra 计算带坡度、树荫、拥挤、福利约束的通行成本
- Dynamic Adjust Agent：根据疲劳、饥饿、拥挤、提前离园、动物活跃事件做局部重规划
- SQLite：可选持久化；默认使用内存 Session，便于比赛演示
- Qwen：预留 `QWEN_API_KEY`，没有 Key 时使用本地规则解析，不影响 Demo 运行

## 启动

```powershell
cd route_ai_backend
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

打开 `http://127.0.0.1:8000/docs` 查看 Swagger。

## API

### `POST /api/route/plan`

```json
{
  "natural_language": "我带着3岁孩子，只有2小时，怕晒，不想爬山，今天很想去熊猫馆",
  "preferences": {
    "duration_minutes": 120,
    "pace": "slow",
    "avoid_climbing": true,
    "avoid_sun": true,
    "with_child": true,
    "preferred_animals": ["大熊猫"]
  }
}
```

### `POST /api/session/start`

传入 `route_id` 创建本次游览 Session。返回 `session_id`、当前节点、剩余路线和状态。

### `POST /api/session/event`

事件类型：`fatigue`、`hungry`、`crowd`、`leave_early`、`stay_longer`、`animal_active`、`off_route`、`weather_change`。每个事件由 Orchestrator 判断是否需要局部重规划，并返回“发生了什么 / 影响 / 可选方案 / 推荐方案 / 成本差异”。

### `POST /api/route/replan`

直接根据 Session 状态重算剩余路线，保留已访问节点、用户明确保留的必去点和离园约束。

## Qwen 接入

默认不要求密钥。接入千问时配置：

```powershell
$env:QWEN_API_KEY="你的百炼 API Key"
$env:QWEN_MODEL="qwen-plus"
```

`IntentAgent` 保留了 `QwenProvider` 接口；Qwen 只负责理解、结构化提取和解释，绝不直接编造路线。所有路线必须经过 `route_engine` 的约束校验。

## 当前 Mock 范围

园区节点、道路、坡度、遮阴、客流、场馆开放状态、动物活跃度均为可替换的演示数据；地图和 GPS 没有接入真实服务。正式接入时替换 `app/park_data.py` 与 `app/providers.py`，不需要改 API 契约。
