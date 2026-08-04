# 山野游伴 · 完整产品工程

这是“山野游伴”的完整可运行工程目录，独立于上级原型工程。它包含：

- `src/`：移动端高保真产品前端
- `backend/`：FastAPI 动态路线与游中调整后端
- `backend/app/`：Intent Agent、Route Agent、Orchestrator、Session 与 Mock 园区数据

## 启动后端

```powershell
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

## 启动前端

另开终端：

```powershell
npm install
npm run dev
```

前端默认调用 `http://127.0.0.1:8000`。如需修改：

```powershell
$env:VITE_API_BASE="http://127.0.0.1:8000"
```

## 完整产品能力

1. 游伴测试 / 盲盒领养
2. 3D 动物搭子
3. 游玩条件与“今天最想去哪里”合并规划
4. 园区地图与路线结果
5. 路线驱动的侦探 / 森林 / 动物来信故事
6. 到达节点后的线索收集
7. NPC 任务、节点盖章、成长值
8. 场馆讲解与语音 / 文字问答
9. 疲劳、饥饿、拥挤、动物活跃等游中事件
10. 成长等级、印章册与纪念品兑换演示

路线规划页会优先调用 `src/services/backendApi.ts` 的 `/api/route/plan`；后端不可用时自动回退到本地演示流程。真实 Qwen、地图、GPS、客流和园区运营数据均有明确替换位置，当前不写入任何 API Key。
