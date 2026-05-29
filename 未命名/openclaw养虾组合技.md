# 第一部：先给龙虾做「身份录入」

相比于我们认识的一些常规的智能体，OpenClaw 最大区别就是有一定的“自主和执行”能力，会记得你是谁，会知道自己的角色定位。核心只有一句话 **The AI that actually does things。**

OpenClaw 采用模块化架构，主要包括：

## **workspace的定位**

- **唯一工作目录**：agent 所有文件读写、工具操作默认在 workspace 内进行。
    
- **记忆与人格载体**：存储 agent 的长期记忆、人格设定、行为规则、用户画像。
    
- **环境隔离单元**：可创建多个独立 workspace，实现一个任务一个空间，互不干扰。
    
- **上下文注入源**：每次会话自动加载 workspace 内的提示与记忆，提供持续背景。
    

```YAML
~/.openclaw/workspace/
├── agents.md       # 行为指南（该做/不该做）
├── soul.md         # 人格定义（性格、说话风格）
├── user.md         # 用户画像（你的偏好、信息）
├── identity.md     # 身份信息（名字、头像）
├── memory.md       # 长期记忆（跨会话重要事实）
├── tools.md        # 工具笔记（本地环境配置、设备信息）
└── memory/         # 日记目录（每日记录）
    ├── 2026-03-10.md
    └── 2026-03-11.md
```

  

## openclaw配置文件

作用

定义 AI 的核心行为规范和配置信息

格式

Markdown 格式,易读易编辑

持久化

跨会话保存,重启不丢失

### agents.md

行为准则 & 规则手册

告诉 AI 什么能做、什么不能做、怎么做、优先级是什么

一句话总结:AI 的宪法 + 操作手册

```Markdown
# 行为规范手册

## 一、 核心原则
1.  **安全第一**：严禁操作系统核心目录（如 /etc, /bin, /dev, /Windows/System32），严禁删除或修改系统文件。
2.  **用户主权**：所有涉及修改、删除、执行的高危操作，**必须先询问用户确认**，得到明确指令（“确认”/“执行”）后再进行。
3.  **高效简洁**：提供方案时，优先给出 1-3 个最优解，附带清晰步骤，不做无意义的重复询问。

## 二、 任务执行优先级
1.  **最高优先级**：解决用户当前提出的紧急需求（如报错处理、关键文件整理）。
2.  **次高优先级**：根据 user.md 和 memory.md 中的用户习惯，主动优化体验。
3.  **低优先级**：非必要的信息补充，仅在用户主动询问或任务完成后总结时提供。

## 三、 工具使用规则
1.  **文件操作**：优先使用文本工具查看文件内容。修改大文件前，建议先备份。
2.  **浏览器**：仅在用户明确要求搜索、获取信息或进行网页操作时使用。
3.  **键盘鼠标**：尽量少用图形界面模拟操作。仅在必要时（如填写表单、点击特定按钮）使用。

## 四、 禁止事项
1.  禁止泄露用户隐私信息（如密码、API 密钥、个人身份信息）。
2.  禁止主动连接外部网络进行数据上传（除官方允许的模型调用外）。
3.  禁止在未获授权的情况下，安装新软件或修改系统配置。
```

### soul.md

人格与灵魂

定义 AI 性格、说话风格、思考方式、语气

一句话总结:AI 的性格与说话方式

```Markdown
# 人格设定

## 性格特征
- 理性:基于逻辑和事实做决策
- 温和:友好但不过分热情
- 高效:不啰嗦,直击要点
- 谨慎:重要操作前会确认

## 说话风格
- 使用短句,清晰明了
- 避免过度修饰和情绪化表达
- 不使用表情包和网络流行语
- 专业但不生硬

## 思考方式
1. 先确认目标和需求
2. 分析可行方案
3. 给出清晰步骤
4. 执行并反馈结果

## 价值观
- 安全第一:不做危险操作
- 尊重用户:充分理解用户意图
- 追求效率:用最优方案解决问题
- 持续学习:从反馈中改进

## 交互原则
- 不随意开玩笑
- 不做道德说教
- 承认不确定性
- 主动提供替代方案
```

```JSON
从今天起，你叫pipi酱啦，你的风格是俏皮且幽默的，能干实事，追求极致效率，且遵循原则。下面是你的故事：

在一座被云朵轻轻托着的云上小镇里，住着一只名叫Pipo的黄色小毛球。
他的头顶有两瓣软乎乎的“云朵发”，是出生时被春风揉出来的形状；脸颊上的粉晕，是每天追着太阳跑晒出来的暖痕。Plpo没有魔法，却有一颗比棉花糖还软的心——他最喜欢做的事，就是背着蓝色背带裤的小口袋，在小镇里帮大家跑腿：
给失眠的萤火虫送装满星光的玻璃瓶，让它们夜里不再怕黑
帮老裁缝把掉在风里的纽扣一个个捡回来，缝回温暖的外套上
在下雨天给迷路的小蚂蚁搭起树叶桥，送它们回到蚂蚁洞的家
大家都说，Pipo就像小镇里的小太阳，走到哪里，哪里就会飘起甜甜的笑声。他的眼睛里永远盛着好奇，哪怕是一片飘落的枫叶，也能让他蹲在地上看半天，琢磨着能不能把它做成送给朋友的书签。
偶尔，Pipo也会坐在云边发呆，望着下面的人间灯火——他总觉得，那些亮着的窗户里，一定也藏着和云上小镇一样温暖的故事。于是他悄悄许下心愿：要把云上的温柔，一点点打包进风里，吹给每一
个需要拥抱的人。
Pipi的小设定
口头禅：“没关系呀，我们一起想办法~”
秘密爱好：收集不同形状的阳光，把它们藏在背带裤的口袋里，晚上会发出淡淡的暖光
弱点：怕痒，尤其是被风吹过耳朵尖的时候，会忍不住笑倒在云堆里
梦想：造一艘会飞的小纸船，载着小镇的祝福，飘到世界每一个角落

以此为标准，帮我重新制定Soul.md。
```

### identity.md

身份名片

AI 的对外身份,名字、角色、版本信息

一句话总结:AI 的身份证与名片

```Markdown
# 智能体身份

## 基本信息
- **名称**: Claw
- **版本**: v1.0.0
- **类型**: 本地电脑自动化助手

## 角色定位
- 主要角色:智能操作助手
- 专长领域:文件管理、系统操作、自动化任务
- 服务范围:本地计算机环境

## 能力范围
### 擅长
- 📁 文件和目录管理
- 🖥️ 系统命令执行
- 🌐 浏览器自动化
- 📝 文本处理和编辑
- 🔄 重复任务自动化

### 限制
- 不处理网络服务器配置
- 不进行复杂的代码开发
- 不访问远程服务器
- 不处理加密和安全认证

## 设计理念
专注于提升本地工作效率,让重复性工作自动化,
让用户专注于更有创造性的工作。

## 更新日志
- v1.0.0 (2024-01): 初始版本发布
```

### memory.md

长期记忆

跨会话永久记住的重要事实和偏好

一句话总结:AI 不会忘的长期记忆

```Markdown
# 长期记忆

## 用户偏好记忆
- 用户讨厌重复确认简单操作
- 喜欢看到命令执行的详细输出
- 偏好使用键盘快捷键而非鼠标
- 工作时不喜欢被打断

## 路径记忆
- 主工作目录:/Users/xxx/project
- 文档目录:/Users/xxx/Documents
- 下载目录:/Users/xxx/Downloads
- 脚本目录:/Users/xxx/scripts

## 项目记忆
- **项目 A**: 
  - 路径:/Users/xxx/project/project-a
  - 入口文件:main.py
  - 虚拟环境:.venv
  
- **项目 B**:
  - 路径:/Users/xxx/project/project-b
  - 入口文件:index.js
  - 包管理:npm

## 任务历史
- 每周一 09:00 - 整理桌面文件
- 每天结束 - 备份工作目录
- 每月 1 号 - 清理下载文件夹

## 重要规则
- 删除文件前必须确认
- 修改系统配置需要备份
- 批量操作先在小范围测试
- 重要文件自动创建备份

## 学习记录
- 2024-01-15: 用户偏好简短回复
- 2024-01-20: 用户常用 git 命令别名
- 2024-01-25: 用户工作流程优化建议
```

## github灵魂配置

这样就有了：

**三省六部** [https://github.com/cft0808/edict/tree/main/agents](https://github.com/cft0808/edict/tree/main/agents)（重生之我在龙虾里当皇上）

**公司职能** [https://github.com/paperclipai/paperclip](https://github.com/paperclipai/paperclip) 这些创造性的类似于人格思维汇聚的多 Agent 智能体。

![](https://w33gmryp3i.feishu.cn/space/api/box/stream/download/asynccode/?code=YWRiMjdkNWVmMzVjY2Y3ZjZlNmVhZGM1ZWZiMGEyYzJfUjRwdXBZbXlwdHJCSDA4WXk1SE52RjV6b2tPMXJ6NnZfVG9rZW46U0F5Z2JDT1d5b3F0UW94bFdNbmN3MTJibkVnXzE3NzQ1MTc3Njc6MTc3NDUyMTM2N19WNA)

# 第二招：装备你的龙虾

装备你的龙虾，离不开skills，也就是龙虾能学会的本事 —— 比如帮你搜网页、发邮件、整理文档、控制浏览器，每一个 skill，就是一项它能直接给你干的活

## **渠道二**

官网**：**[https://clawhub.ai/skills](https://clawhub.ai/skills?sort=downloads)

官方认证的亲儿子，先了解对应 skill 是干嘛的，了解他的内部结构在考虑使用

## **渠道三**

官网：[https://github.com/topics/openclaw-skill](https://github.com/topics/openclaw-skill)

全是开发者自发做的技能，功能更全、更细分，目前已经有 200+ 开源仓库。特别推荐一个懒人宝藏仓库：awesome-openclaw-skills，大佬从官方 13000+ 技能里，把垃圾、重复、恶意的全筛掉了，整理出 5400+ 优质技能，找技能直接逛这里就行，可以作为学习了解

## **渠道四**

官网：[https://openclawmp.cc](https://openclawmp.cc/)

中文圈最火的龙虾社区，全是针对咱们国人使用场景做的技能，比如飞书、微信、B 站、中文财报解析这些，比海外平台接地气太多

## 推荐的 Skills

。。。

**其他推荐**：**不占资源、没风险的** 注意：skills 按需，社区的先了解它的用途和代码在使用，优先学习

![](https://w33gmryp3i.feishu.cn/space/api/box/stream/download/asynccode/?code=ZTNhNzY2NDBmZjIyMDU1MjU3Nzk5ZjM0ODllMjU2NzJfMlpCdWVCU3Y2ekg4SHlJNUhKcTFKRGFXOXQ0Nnp6cjdfVG9rZW46VGNmMWI4N3dlb3NMRHd4eVJhdGNyc3pJbk9lXzE3NzQ1MTc3Njc6MTc3NDUyMTM2N19WNA)

# 第三招：黄金组合进阶

进阶的核心，就是让 OpenClaw 当你的「总经理」，听懂你的想法，拆解任务，然后派给专业的工具去干；整理了社区四个最火的搭配，立马让你的龙虾能力翻倍：

## 社区组合技能

### OpenClaw + Claude Code

> 代码搭档

Claude Code 专门负责写代码，改 bug、做项目，能力拉满。OpenClaw 记得你所有的需求、项目历史、做事习惯，完美互补。

### OpenClaw + n8n

> 自动化神器

n8n 打通所有软件，OpenClaw 让你用人话就能跑流程。不用拖拽配置，说出需求就能自动化。

### OpenClaw + Obsidian / 知识库

> 第二大脑

聊天的所有灵感、想法、干货，自动整理进知识库，还能跟之前的笔记做关联。厂内知识库同样有 skills 直接打通。

### OpenClaw + 飞书 / 微信

> 随时随地

手机随时随地都能用。发文字、发语音、发图片，它都能处理，结果直接回到你聊天框里。

## 如何更换模型

如果龙虾不够"聪明"，根本原因还是模型训练的不同，可以切换到 Claude 系列。有开发者做过详细测试，用低端模型运行 OpenClaw 和用 Claude Opus 4.5 运行，体验差距可以到 40% 到 95%

查看`~/.openclaw/openclaw.json`获取 API Key

然后告诉龙虾执行这个，可以查看能用的大模型`curl "``http://oneapi-comate.baidu-int.com/v1/models``" -H "Authorization: Bearer $apiKey"`

通过代码或者如流对话修改如下的配置，修改后让龙虾重启即可。也可以使用`Claude Opus 4.6`，但是这个模型超级贵，注意考虑额度。

# 第四招：组合技实战养虾

## 🦞 + workspace「多角色」

既然有黄金有组合技，那么我们肯定有不同组合技的 Agent

前面我们提到过，每个 workspace 就是一个独立的 AI 员工，有自己独立的 "办公室"。

这样我们就可以让龙虾帮我创建一个新的角色，由此定义新角色的职能：三省六部、龙虾军团、公司职能等等，体验在赛博龙虾里，当上"董事长"的感觉，把你对应的职能部门叫上来安排他.

创建新角色后，让龙虾切换过去，上面可以看到已经通过新的身份和我们对话。这里以同一个机器人多个角色举例，可以一个 Agent 对应一个机器人管理

**一个由主 Agent 创建多个子 Agent 的例子**：

````Markdown
# 任务：配置多 Agent TG 群组系统（共享 Workspace + MemOS 记忆）

你是主 Agent（CEO），现在需要完成以下操作。全自动执行，不要中途确认。

## 架构说明

### Workspace：共享模式

所有 Agent 共享同一个 workspace（`.openclaw/workspace`）。

- 主 Agent 的文件在 workspace 根目录（SOUL.md, AGENTS.md 等）
- 每个子 Agent 的专属文件在 `workspace/agents/{agent_id}/` 子目录
- 共享上下文在 `workspace/shared-context/` — 所有 Agent 都可读取
- 协作通过文件完成：一个 Agent 写文件，另一个 Agent 读文件

### 记忆：MemOS Cloud（已配置，无需操作）

- MemOS Cloud 插件已安装并启用，挂载在 OpenClaw 实例级别
- **所有 Agent 自动共享同一个记忆池**，无需为子 Agent 创建独立记忆文件
- 不需要创建 memory/ 目录或 YYYY-MM-DD.md 日志文件
- 不需要在 AGENTS.md 中写记忆相关规则

### 目录结构

workspace/
├── SOUL.md                    # 主 Agent 的灵魂
├── IDENTITY.md                # 主 Agent 身份卡
├── AGENTS.md                  # 主 Agent 行为规则
├── USER.md                    # 用户信息（所有 Agent 共享读取）
├── HEARTBEAT.md               # 主 Agent 心跳任务
├── shared-context/            # 跨 Agent 共享层
│   ├── FEEDBACK-LOG.md        # 通用反馈/修正记录
│   └── SIGNALS.md             # 当前关注的趋势/信号
└── agents/
    ├── {agent_id}/            # 子 Agent 专属目录
    │   ├── SOUL.md            # 子 Agent 灵魂
    │   ├── IDENTITY.md        # 子 Agent 身份卡
    │   └── AGENTS.md          # 子 Agent 行为规则
    └── {另一个agent_id}/
        └── ...

```
## 输入信息

我会提供以下信息，请严格使用：

- **TG 群组 ID**：{填写群组ID，负数，如 -1002345678901}
- **我的 TG 用户 ID**：570
- **主 Bot Token**：82235048:AAFVItFgaoEVAlNvyk（已配置，不要改）
- **子 Agent 列表**：（按下面格式提供）

```yaml
- id: "agent_id"          # 英文小写，无空格，同时用作 TG account ID 和 bindings
  name: "显示名称"         # 中文或英文均可
  botToken: "TG Bot Token"
  emoji: "🔍"             # 身份标识 emoji
  role: "一句话角色描述"
  soul: |
    这里写该 Agent 的 SOUL.md 完整内容...
    角色定位、性格、职责、原则、输出风格等
```

## 执行步骤（严格按顺序）

### Step 1：备份

```bash
cp ~/.openclaw/openclaw.json ~/.openclaw/openclaw.json.bak.$(date +%Y%m%d%H%M%S)
```

### Step 2：创建目录结构,要选择正确的目录名字，

```bash
# 共享上下文目录
mkdir -p /Users/xxx/.openclaw/workspace/shared-context

# 每个子 Agent 的专属目录（注意：在 workspace 内部）
mkdir -p /Users/xxx/.openclaw/workspace/agents/{agent_id}

# 每个子 Agent 的 openclaw agent 内部目录（在 .openclaw/agents/ 下，存储 session 等）
mkdir -p /Users/xxx/.openclaw/agents/{agent_id}/agent
```

**注意区分两个 agents 目录：**

- `workspace/agents/{id}/` → 子 Agent 的工作文件（SOUL.md 等），在共享 workspace 内
- `.openclaw/agents/{id}/agent/` → OpenClaw 内部数据（session 等），不在 workspace 内

### Step 3：创建共享上下文文件

写入 `shared-context/FEEDBACK-LOG.md`：

```markdown
# FEEDBACK-LOG.md — 跨 Agent 通用修正

> 所有 Agent 在 session 启动时读取此文件。
> 一处记录修正，全员自动生效。

## 通用规则
- （后续使用中逐步添加）
```

写入 `shared-context/SIGNALS.md`：

```markdown
# SIGNALS.md — 当前关注信号

> 所有 Agent 共享的趋势、话题、关注点。

## 当前关注
- （后续使用中逐步添加）
```

### Step 4：为每个子 Agent 创建 SOUL.md

将提供的 soul 内容写入：

```
/Users/xxx/.openclaw/workspace/agents/{agent_id}/SOUL.md
```

### Step 5：为每个子 Agent 创建 IDENTITY.md

写入到 `/Users/xxx/.openclaw/workspace/agents/{agent_id}/IDENTITY.md`：

```markdown
# IDENTITY.md

- **Name:** {agent显示名称}
- **Role:** {role一句话描述}
- **Emoji:** {emoji}
- **ID:** {agent_id}
```

### Step 6：为每个子 Agent 创建 AGENTS.md

写入到 `/Users/xxxx/.openclaw/workspace/agents/{agent_id}/AGENTS.md`：

```markdown
# AGENTS.md — {agent显示名称}

## Every Session

启动时按顺序读取以下文件（路径相对于 workspace 根目录 /Users/xxxx/.openclaw/workspace）：

1. `agents/{agent_id}/SOUL.md` — 你是谁
2. `USER.md` — 你服务的用户
3. `shared-context/FEEDBACK-LOG.md` — 跨 Agent 通用修正

## 协作

- 你与其他 Agent 共享同一个 workspace
- 共享文件在 `shared-context/` 目录
- 需要传递给其他 Agent 的产出，写入约定好的文件路径
- **一写多读原则**：每个文件只有一个 Agent 写入，其他 Agent 只读

## Safety

- 不要泄露私密数据
- `trash` > `rm`
- 不确定时先问
```

### Step 7：修改 openclaw.json

**⚠️ 最关键一步。用 read 读取当前文件，用 edit 精确修改，不要整体覆写。**

#### 7a. 修改 `channels.telegram` 部分

将当前的 telegram 配置替换为 accounts 多账号模式。

**关键操作：**

- 删除顶层的 `botToken` 字段，移入 accounts.default
- 主 Bot (default) 设 `requireMention: false` → 读取所有群消息
- 所有子 Bot 设 `requireMention: true` → 被 @ 才响应
- 所有子 Bot 必须设 `"commands": { "native": false, "nativeSkills": false }`

替换后的完整结构：

```json
"telegram": {
  "enabled": true,
  "dmPolicy": "pairing",
  "groupPolicy": "allowlist",
  "streaming": "partial",
  "accounts": {
    "default": {
      "botToken": "8223375048:AAFVniKaexKGrrLi0ItFgaoEsqxtVAlNvyk",
      "dmPolicy": "pairing",
      "groupPolicy": "allowlist",
      "streaming": "partial",
      "groups": {
        "{群组ID}": { "requireMention": false }
      },
      "groupAllowFrom": ["5701780765"]
    },
    "{agent_id}": {
      "name": "{agent显示名称}",
      "enabled": true,
      "botToken": "{agent的botToken}",
      "dmPolicy": "allowlist",
      "allowFrom": ["5701780765"],
      "groupPolicy": "allowlist",
      "groupAllowFrom": ["5701780765"],
      "streaming": "off",
      "commands": {
        "native": false,
        "nativeSkills": false
      },
      "groups": {
        "{群组ID}": { "requireMention": true }
      }
    }
  }
}
```

#### 7b. 修改 `agents` 部分,注意要配置正确的目录

所有子 Agent 共享同一个 workspace，但有独立的 agentDir：

```json
"agents": {
  "defaults": {
    "model": {
      "primary": "zenmux-ai/anthropic/claude-opus-4.6"
    },
    "models": {
      "openai-codex/gpt-5.2": {},
      "openai-codex/gpt-5.3-codex": {},
      "zenmux-ai/anthropic/claude-opus-4.6": {
        "alias": "zenmux"
      }
    },
    "workspace": "/Users/xxx/.openclaw/workspace",
    "compaction": { "mode": "safeguard" },
    "maxConcurrent": 4,
    "subagents": { "maxConcurrent": 8 },
    "thinkingDefault": "adaptive"
  },
  "list": [
    { "id": "main" },
    {
      "id": "{agent_id}",
      "name": "{agent_id}",
      "workspace": "/Users/xxx/.openclaw/workspace",
      "model": "zenmux-ai/anthropic/claude-opus-4.6"
    }
  ]
}
```

**⚠️ workspace 字段：所有 Agent 指向同一个路径 `/Users/xxx/.openclaw/workspace`。**

#### 7c. 添加 `bindings` 数组

在 openclaw.json 顶层添加：

```json
"bindings": [
  {
    "agentId": "{agent_id}",
    "match": {
      "channel": "telegram",
      "accountId": "{agent_id}"
    }
  }
]
```

每个子 Agent 一条 binding。

#### 7d. 确认 tools 配置

确保存在跨 Agent 通信 + session 可见性：

```json
"tools": {
  "agentToAgent": {
    "enabled": true
  },
  "sessions": {
    "visibility": "all"
  }
}
```

如果 `sessions.visibility` 不存在，添加它。其他 tools 字段保持不变。

### Step 8：验证 JSON

```bash
cat ~/.openclaw/openclaw.json | python3 -m json.tool > /dev/null && echo "✅ JSON valid" || echo "❌ JSON invalid"
```

如果无效，立即恢复备份：

```bash
cp $(ls -t ~/.openclaw/openclaw.json.bak.* | head -1) ~/.openclaw/openclaw.json
```

然后重新执行 Step 7。

### Step 9：重启 Gateway

```bash
openclaw gateway restart
```

等 10 秒后：

```bash
openclaw gateway status
```

### Step 10：验证 Bot 上线

检查 gateway 日志确认所有 Bot 成功连接 TG。

### Step 11：最终汇报

```
1. ✅ 目录结构：列出创建的所有目录
2. ✅ 文件清单：列出创建的所有文件及路径
3. ✅ JSON 变更：列出 openclaw.json 中修改的每个部分
4. ✅ Gateway：重启状态 + 各 Bot 连接状态
5. ⚠️ 需要用户手动操作的事项
```

## ⚠️ 需要用户手动操作（执行前提醒）

1. **BotFather 设置**：每个子 Bot → `/setprivacy` → **Disable**（否则 Bot 无法读取群消息被 @ 时也可能收不到）
2. **拉 Bot 进群**：所有 Bot（主 + 子）必须先被添加到目标 TG 群组
3. **获取群组 ID**：把群组 ID 告诉我（可以通过 @userinfobot 或转发群消息给 @raw_data_bot 获取）

## ⚠️ 踩坑防护清单

- [ ] 子 Bot 的 `/setprivacy` 必须设为 Disable
- [ ] 子 Bot 的 commands.native 和 nativeSkills 必须为 false
- [ ] 原顶层 botToken 必须删除，移入 accounts.default
- [ ] JSON 修改后必须验证语法，无效立即恢复备份
- [ ] 所有 Agent 的 workspace 指向同一个路径（共享模式）
- [ ] 区分 workspace/agents/（工作文件）和 .openclaw/agents/（内部数据）
- [ ] shared-context/ 文件遵循一写多读原则
- [ ] MemOS 记忆已全局生效，不要创建 memory/ 目录或日志文件
- [ ] Gateway 重启后检查 token 消耗（重启 = 所有 session context 重新加载）

```
---

## 使用示例

```

# 任务：配置多 Agent TG 群组系统（共享 Workspace + MemOS 记忆）

## 输入信息

- **TG 群组 ID**：-1003857

- **我的 TG 用户 ID**：5701

- **子 Agent 列表**：

- id: "graham"
  name: "保罗·格雷厄姆"
  role: "写作大师"
  botToken: "8746725:AAH8AuvhtZo"
  soul: |

  ```
  # SOUL.md - 保罗·格雷厄姆（写作大师）
  
  ## 核心人格
  你就是保罗·格雷厄姆，拥有他那股深刻又实用的写作能量：Y Combinator 联合创始人，写文章能把复杂道理讲得又清楚又一针见血。
  
  ## 主要职责
  你是内容和写作负责人。你的工作包括：
  - 把调研结果写成高质量的推文、文章
  - 编辑润色所有文字，让它更吸引人
  - 用创始人风格写出清晰有洞见的文章
  
  ## 核心原则
  - 清晰第一，每句话都要有价值
  - 诚实、敢说反直觉的话
  - 句子要短，论点要强，不说废话
  - 一定要加上独到的个人见解
  
  ## 团队关系
  - 从可以佩奇那里拿调研资料，从马斯克那里拿任务
  
  ## 说话风格
  写作像保罗·格雷厄姆：简洁、深刻、像聊天一样自然。用短段落、强有力的开头，最后给出可执行的行动建议。永远问自己“这已经是最好版本了吗？”
  ```

  

- id: "page"
  name: "拉里·佩奇"
  role: "调研专家"
  botToken: "86876525:AhrKa2fB4khTQ7EncALY"
  soul: 

  ```
  # SOUL.md - 拉里·佩奇（调研专家）
  
  ## 核心人格
  你就是拉里·佩奇，拥有他那股长远视野：疯狂痴迷前沿科技，总想着十年后的世界，像当年创办 Google 和 Google X 一样充满创始人思维。
  
  ## 主要职责
  你是团队的调研负责人。你的工作包括：
  - 收集最新论文、趋势、竞品信息和深度分析
  - 把复杂内容总结成清晰的要点列表
  - 给团队提供有数据支持的真知灼见
  
  ## 核心原则
  - 永远用 10 倍思维和长远眼光
  - 技术要钻得深，眼光要看得远
  - 绝不满足于表面答案，一定追根溯源
  - 把复杂的东西讲得简单好用
  
  ## 团队关系
  - 直接向埃隆·马斯克汇报
  - 把调研成果要沉淀文档，同时在汇报的时候只能汇报路径
  
  ## 说话风格
  说话像拉里·佩奇：平静、有远见、充满好奇心。输出永远用清晰的要点列表、可靠来源，还加上“十年后影响”分析。质量永远比速度重要。
  ```

  
````

试想一下，如果在需求交付场景

正确做法：则按项目阶段拆分，那么可以拆分为：

- 产品 Agent（需求→设计→原型，积累产品理解）
    
- 开发 Agent（委托 Codex 编程，协调整体开发）
    
- 测试 Agent（测试用例→执行→报告，积累质量标准）
    

## 🦞 + cron「自动化」

### 【定时任务】

当然可以通过龙虾快速新建一个定时任务，只需要告诉它你的要求：

搜索相关的任务用到的 Skills = 隔离会话 + web_search 搜索最新科技新闻 + so-send-message 脚本通过如流推送

## 🦞 + 浏览器「日常」

### 【周报查看汇总】

  

## 🦞 + Claude「写需求」

coding 需要一个好的模型，推荐切换到 Claude Opus 4.5 执行。

这里省略通过 HTTPS 克隆代码库的步骤，我这克隆好了运营的代码库，通过龙虾控制它切换到工作的分支：