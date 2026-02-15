-- kimi-mem 数据库结构
-- SQLite + FTS5

-- 项目表
CREATE TABLE IF NOT EXISTS projects (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE,
    path TEXT,
    description TEXT,
    created_at INTEGER NOT NULL DEFAULT (unixepoch() * 1000),
    updated_at INTEGER NOT NULL DEFAULT (unixepoch() * 1000),
    access_count INTEGER DEFAULT 0
);

-- 会话表（跟踪使用 kimi-mem 的会话）
CREATE TABLE IF NOT EXISTS sessions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    session_id TEXT NOT NULL UNIQUE,
    project_id INTEGER,
    started_at INTEGER NOT NULL DEFAULT (unixepoch() * 1000),
    ended_at INTEGER,
    summary TEXT,
    FOREIGN KEY (project_id) REFERENCES projects(id) ON DELETE SET NULL
);

-- 记忆/观察表（核心）
CREATE TABLE IF NOT EXISTS memories (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    session_id INTEGER,
    project_id INTEGER NOT NULL,
    
    -- 内容
    title TEXT NOT NULL,
    content TEXT NOT NULL,
    
    -- 分类
    type TEXT DEFAULT 'observation',  -- observation, decision, bugfix, feature, learning, summary
    importance INTEGER DEFAULT 3,      -- 1-5, 5 最重要
    
    -- 元数据
    tags TEXT,                         -- JSON 数组 ["tag1", "tag2"]
    metadata TEXT,                     -- JSON 对象 {key: value}
    
    -- 文件关联
    files TEXT,                        -- JSON 数组 ["path/to/file1", "path/to/file2"]
    
    -- 时间戳
    created_at INTEGER NOT NULL DEFAULT (unixepoch() * 1000),
    updated_at INTEGER NOT NULL DEFAULT (unixepoch() * 1000),
    
    -- 访问统计
    access_count INTEGER DEFAULT 0,
    last_accessed INTEGER,
    
    FOREIGN KEY (session_id) REFERENCES sessions(id) ON DELETE SET NULL,
    FOREIGN KEY (project_id) REFERENCES projects(id) ON DELETE CASCADE
);

-- FTS5 虚拟表（全文搜索）
CREATE VIRTUAL TABLE IF NOT EXISTS memories_fts USING fts5(
    title,
    content,
    content='memories',
    content_rowid='id'
);

-- 触发器：自动同步 FTS 索引
CREATE TRIGGER IF NOT EXISTS memories_fts_insert AFTER INSERT ON memories BEGIN
    INSERT INTO memories_fts(rowid, title, content)
    VALUES (new.id, new.title, new.content);
END;

CREATE TRIGGER IF NOT EXISTS memories_fts_update AFTER UPDATE ON memories BEGIN
    DELETE FROM memories_fts WHERE rowid = old.id;
    INSERT INTO memories_fts(rowid, title, content)
    VALUES (new.id, new.title, new.content);
END;

CREATE TRIGGER IF NOT EXISTS memories_fts_delete AFTER DELETE ON memories BEGIN
    DELETE FROM memories_fts WHERE rowid = old.id;
END;

-- 索引
CREATE INDEX IF NOT EXISTS idx_memories_project ON memories(project_id);
CREATE INDEX IF NOT EXISTS idx_memories_session ON memories(session_id);
CREATE INDEX IF NOT EXISTS idx_memories_type ON memories(type);
CREATE INDEX IF NOT EXISTS idx_memories_created ON memories(created_at);
CREATE INDEX IF NOT EXISTS idx_memories_importance ON memories(importance);

CREATE INDEX IF NOT EXISTS idx_sessions_project ON sessions(project_id);
CREATE INDEX IF NOT EXISTS idx_sessions_started ON sessions(started_at);

-- 初始化默认项目
INSERT OR IGNORE INTO projects (name, description) 
VALUES ('default', 'Default project for memories without specific project association');
