# 案例 1: API 设计 - 快速模式

## 用户请求
> "帮我设计一个用户认证的 API"

## 复杂度评估
```
任务类型: API 设计
预估代码量: < 100 行
依赖数量: 2-3 个 (HTTP框架, JWT库, 数据库)
复杂度评分: 2/10

建议模式: 【快速模式】
预计时间: 5 分钟
```

## Phase 0: 模式确认
**Agent**: 
```
这是一个标准的 API 设计任务，建议使用【快速模式】。

预计时间: 5 分钟
包含: 
- 2 个关键问题确认
- 可行性快速评估
- API 接口设计
- 对接 writing-plans

确认开始？[Y/n]: Y
```

## Phase 1: 动态问题生成
**Agent**:
```
基于"用户认证 API"，我需要了解：

【关键问题 1/2】
使用什么认证机制？
- A: JWT (无状态，适合分布式)
- B: Session (有状态，传统方式)
- C: OAuth2 (第三方集成)

用户选择: A

【关键问题 2/2】
需要支持多设备同时登录吗？
- A: 是 (需要设备管理)
- B: 否 (单点登录)

用户选择: A
```

## Phase 2: 调度 Brainstorming
**Brainstorming Skill**:
```
## 探索方案

基于 JWT + 多设备支持的认证 API，有 2 个主要方案：

### 方案 1: 标准 JWT
- Access Token (15分钟) + Refresh Token (7天)
- 每个设备独立 Token
- 黑名单机制处理登出

### 方案 2: 短 Token + 滑动会话
- Access Token (5分钟) + 自动续期
- 更好的安全性
- 实现复杂度稍高

推荐: 方案 1 (平衡安全性和实现复杂度)
```

## Phase 3: 加载子代理
**加载**: `feasibility_agent`

**子代理分析**:
```json
{
  "overall_feasibility": "high",
  "dimensions": {
    "technical": {"score": 9, "blocking_issues": []},
    "resource": {"score": 9, "blocking_issues": []},
    "schedule": {"score": 9, "blocking_issues": []}
  },
  "recommendations": ["使用成熟的 JWT 库如 PyJWT"]
}
```

## Phase 4: 关键决策
**Agent**:
```
基于分析，关键决策：

1. 【Token 存储】
   - 推荐: Redis 存储 Refresh Token 黑名单
   - 理由: 支持快速登出和设备管理

2. 【密码安全】
   - 推荐: bcrypt 加密
   - 理由: 行业标准的密码哈希
```

用户确认以上决策。

## Phase 5: 对接 Writing-Plans
**Writing-Plans Skill** 生成:

```markdown
# API 设计实现计划

## 接口定义

### POST /auth/register
注册新用户

```python
@app.post("/auth/register")
async def register(email: str, password: str):
    # 1. 验证邮箱格式
    # 2. bcrypt 加密密码
    # 3. 存入数据库
    # 4. 返回成功
```

### POST /auth/login
用户登录

```python
@app.post("/auth/login")
async def login(email: str, password: str, device_id: str):
    # 1. 验证用户存在
    # 2. 比对密码
    # 3. 生成 JWT (access + refresh)
    # 4. 记录设备信息
    # 5. 返回 tokens
```

### POST /auth/logout
用户登出

```python
@app.post("/auth/logout")
async def logout(token: str):
    # 1. 验证 token
    # 2. 加入黑名单
    # 3. 返回成功
```

## 任务分解

| 任务 | 预计时间 | 依赖 |
|------|----------|------|
| 1. 搭建 FastAPI 项目结构 | 10分钟 | - |
| 2. 实现用户模型 | 15分钟 | 1 |
| 3. 实现 JWT 工具类 | 20分钟 | - |
| 4. 实现注册接口 | 15分钟 | 2, 3 |
| 5. 实现登录接口 | 15分钟 | 2, 3 |
| 6. 实现登出接口 | 10分钟 | 3 |
| 7. 编写单元测试 | 20分钟 | 4, 5, 6 |

总计: ~2 小时
```

## 总结

- **分析时间**: 5 分钟
- **输出物**: API 设计 + 实现计划
- **后续**: 可以直接开始编码实现
