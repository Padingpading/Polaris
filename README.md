# Polaris Admin

前后端分离的用户管理与 RBAC 权限控制示例项目。

- **后端**：FastAPI（同步 `def` 路由）+ SQLAlchemy 2.0 + PyMySQL + JWT + 分层架构
- **前端**：Vue 3 + TypeScript + Pinia + Vue Router + Element Plus

## 架构分层

```text
backend/app
├── api/v1          # 路由层（只做参数接收与响应封装）
├── schemas         # Pydantic DTO
├── services        # 业务逻辑层
├── repositories    # 数据访问层
├── models          # ORM 模型
├── core            # 配置、安全、依赖注入、异常、统一响应
└── db              # 引擎、会话、初始化数据

frontend/src
├── api             # 接口封装
├── stores          # Pinia 状态
├── router          # 路由与权限守卫
├── views           # 页面
├── layouts         # 布局
├── directives      # v-permission
└── types           # 类型定义
```

## 数据库

当前使用 **MySQL**（SQLAlchemy 2.0 + PyMySQL 同步 ORM）：

```text
DATABASE_URL=mysql+pymysql://user:password@host:3306/polaris?charset=utf8mb4
```

应用启动时会自动：
1. `CREATE DATABASE IF NOT EXISTS polaris`
2. `create_all` 建表
3. 写入默认账号与权限数据

## 快速启动

### 1. 后端

```bash
# 在项目根目录 Polaris 创建/使用虚拟环境
python -m venv .venv

# Windows
.venv\Scripts\activate

# macOS / Linux
# source .venv/bin/activate

pip install -r backend/requirements.txt
cd backend
python main.py
```

接口文档：http://127.0.0.1:8000/docs

### 2. 前端

```bash
cd frontend
npm install
npm run dev
```

访问：http://127.0.0.1:5173

## 默认账号

| 账号 | 密码 | 说明 |
|------|------|------|
| admin | Admin@123 | 超级管理员，拥有全部权限 |
| viewer | Viewer@123 | 只读账号，仅 list/read |

## 权限码

- `user:list` / `user:read` / `user:create` / `user:update` / `user:delete`
- `role:list` / `role:create` / `role:update` / `role:delete`

## 主要 API

| Method | Path | 说明 |
|--------|------|------|
| POST | `/api/v1/auth/login` | 登录 |
| POST | `/api/v1/auth/logout` | 登出 |
| GET | `/api/v1/auth/me` | 当前用户 |
| GET/POST | `/api/v1/users` | 用户列表 / 创建 |
| GET/PUT/DELETE | `/api/v1/users/{id}` | 用户详情 / 更新 / 删除 |
| GET/POST | `/api/v1/roles` | 角色列表 / 创建 |
| PUT/DELETE | `/api/v1/roles/{id}` | 角色更新 / 删除 |
| GET | `/api/v1/roles/permissions` | 权限列表 |

## 统一响应格式

```json
{
  "code": 0,
  "message": "ok",
  "data": {}
}
```
