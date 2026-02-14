import Database from 'better-sqlite3';
import { existsSync, mkdirSync } from 'fs';
import { dirname, join } from 'path';
import { homedir } from 'os';

// 配置路径
const KIMI_MEM_DIR = join(homedir(), '.kimi-mem');
const DB_PATH = join(KIMI_MEM_DIR, 'kimi-mem.db');

let db: Database.Database | null = null;

/**
 * 获取数据库连接（单例）
 */
export function getDatabase(): Database.Database {
    if (db) return db;

    // 确保目录存在
    if (!existsSync(KIMI_MEM_DIR)) {
        mkdirSync(KIMI_MEM_DIR, { recursive: true });
    }

    // 创建连接
    db = new Database(DB_PATH);
    
    // 启用 WAL 模式提高性能
    db.pragma('journal_mode = WAL');
    db.pragma('foreign_keys = ON');

    // 初始化表结构
    initializeSchema();

    return db;
}

/**
 * 初始化数据库表结构
 */
function initializeSchema(): void {
    const db = getDatabase();
    
    // 读取并执行 schema.sql
    const schemaPath = new URL('schema.sql', import.meta.url);
    // 注意：实际运行时 schema.sql 需要复制到 dist 目录
    // 这里使用内嵌 SQL 避免文件路径问题
    
    const schema = `
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

-- 会话表
CREATE TABLE IF NOT EXISTS sessions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    session_id TEXT NOT NULL UNIQUE,
    project_id INTEGER,
    started_at INTEGER NOT NULL DEFAULT (unixepoch() * 1000),
    ended_at INTEGER,
    summary TEXT,
    FOREIGN KEY (project_id) REFERENCES projects(id) ON DELETE SET NULL
);

-- 记忆表
CREATE TABLE IF NOT EXISTS memories (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    session_id INTEGER,
    project_id INTEGER NOT NULL,
    title TEXT NOT NULL,
    content TEXT NOT NULL,
    type TEXT DEFAULT 'observation',
    importance INTEGER DEFAULT 3,
    tags TEXT,
    metadata TEXT,
    files TEXT,
    created_at INTEGER NOT NULL DEFAULT (unixepoch() * 1000),
    updated_at INTEGER NOT NULL DEFAULT (unixepoch() * 1000),
    access_count INTEGER DEFAULT 0,
    last_accessed INTEGER,
    FOREIGN KEY (session_id) REFERENCES sessions(id) ON DELETE SET NULL,
    FOREIGN KEY (project_id) REFERENCES projects(id) ON DELETE CASCADE
);

-- FTS5 虚拟表
CREATE VIRTUAL TABLE IF NOT EXISTS memories_fts USING fts5(
    title, content, content='memories', content_rowid='id'
);

-- 触发器
CREATE TRIGGER IF NOT EXISTS memories_fts_insert AFTER INSERT ON memories BEGIN
    INSERT INTO memories_fts(rowid, title, content) VALUES (new.id, new.title, new.content);
END;

CREATE TRIGGER IF NOT EXISTS memories_fts_update AFTER UPDATE ON memories BEGIN
    DELETE FROM memories_fts WHERE rowid = old.id;
    INSERT INTO memories_fts(rowid, title, content) VALUES (new.id, new.title, new.content);
END;

CREATE TRIGGER IF NOT EXISTS memories_fts_delete AFTER DELETE ON memories BEGIN
    DELETE FROM memories_fts WHERE rowid = old.id;
END;

-- 索引
CREATE INDEX IF NOT EXISTS idx_memories_project ON memories(project_id);
CREATE INDEX IF NOT EXISTS idx_memories_type ON memories(type);
CREATE INDEX IF NOT EXISTS idx_memories_created ON memories(created_at);

-- 默认项目
INSERT OR IGNORE INTO projects (name, description) 
VALUES ('default', 'Default project');
    `;

    db.exec(schema);
}

/**
 * 关闭数据库连接
 */
export function closeDatabase(): void {
    if (db) {
        db.close();
        db = null;
    }
}

/**
 * 获取数据库路径
 */
export function getDatabasePath(): string {
    return DB_PATH;
}

/**
 * 获取数据目录
 */
export function getDataDir(): string {
    return KIMI_MEM_DIR;
}
