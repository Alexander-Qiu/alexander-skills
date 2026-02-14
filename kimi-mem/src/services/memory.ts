import { getDatabase } from '../db/connection.js';
import { ProjectService } from './project.js';

export type MemoryType = 
    | 'observation'   // 一般观察
    | 'decision'      // 重要决策
    | 'bugfix'        // Bug 修复
    | 'feature'       // 功能实现
    | 'learning'      // 学习/发现
    | 'summary'       // 会话总结
    | 'architecture'  // 架构决策
    | 'refactor';     // 重构

export interface Memory {
    id: number;
    session_id: number | null;
    project_id: number;
    title: string;
    content: string;
    type: MemoryType;
    importance: number;
    tags: string[];
    metadata: Record<string, any>;
    files: string[];
    created_at: number;
    updated_at: number;
    access_count: number;
    last_accessed: number | null;
}

export interface MemoryInput {
    title: string;
    content: string;
    type?: MemoryType;
    importance?: number;  // 1-5
    tags?: string[];
    metadata?: Record<string, any>;
    files?: string[];
    projectName?: string;  // 如不指定则使用当前项目
}

export interface SearchOptions {
    query?: string;
    projectName?: string;
    type?: MemoryType | MemoryType[];
    tags?: string[];
    importance?: number;  // 最小重要性
    dateStart?: number;   // 时间戳
    dateEnd?: number;
    limit?: number;
    offset?: number;
}

export interface SearchResult {
    memories: Memory[];
    total: number;
    hasMore: boolean;
}

/**
 * 记忆管理服务
 */
export class MemoryService {
    private db = getDatabase();
    private projectService = new ProjectService();

    /**
     * 保存记忆
     */
    save(input: MemoryInput): Memory {
        // 获取项目
        let project;
        if (input.projectName) {
            project = this.projectService.getOrCreate(input.projectName);
        } else {
            project = this.projectService.getCurrent();
        }

        // 准备数据
        const type = input.type || 'observation';
        const importance = Math.max(1, Math.min(5, input.importance || 3));
        const tags = JSON.stringify(input.tags || []);
        const metadata = JSON.stringify(input.metadata || {});
        const files = JSON.stringify(input.files || []);
        const now = Date.now();

        // 插入数据
        const result = this.db.prepare(
            `INSERT INTO memories 
             (project_id, title, content, type, importance, tags, metadata, files, created_at, updated_at)
             VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)`
        ).run(
            project.id,
            input.title,
            input.content,
            type,
            importance,
            tags,
            metadata,
            files,
            now,
            now
        );

        return this.findById(result.lastInsertRowid as number)!;
    }

    /**
     * 根据 ID 查找记忆
     */
    findById(id: number): Memory | undefined {
        const row = this.db.prepare('SELECT * FROM memories WHERE id = ?').get(id) as any;
        if (!row) return undefined;
        return this.parseRow(row);
    }

    /**
     * 根据 ID 批量获取记忆
     */
    findByIds(ids: number[]): Memory[] {
        if (ids.length === 0) return [];
        
        const placeholders = ids.map(() => '?').join(',');
        const rows = this.db.prepare(
            `SELECT * FROM memories WHERE id IN (${placeholders}) ORDER BY created_at DESC`
        ).all(...ids) as any[];

        // 更新访问统计
        if (ids.length > 0) {
            this.db.prepare(
                `UPDATE memories SET access_count = access_count + 1, last_accessed = ? 
                 WHERE id IN (${placeholders})`
            ).run(Date.now(), ...ids);
        }

        return rows.map(row => this.parseRow(row));
    }

    /**
     * 全文搜索记忆
     */
    search(options: SearchOptions = {}): SearchResult {
        const {
            query,
            projectName,
            type,
            tags,
            importance,
            dateStart,
            dateEnd,
            limit = 20,
            offset = 0
        } = options;

        let sql: string;
        let params: any[] = [];
        let countSql: string;
        let countParams: any[] = [];

        // 如果有搜索词，使用 FTS5
        if (query && query.trim()) {
            sql = `
                SELECT m.* FROM memories m
                JOIN memories_fts fts ON m.id = fts.rowid
                WHERE memories_fts MATCH ?
            `;
            params.push(query);
            
            countSql = `SELECT COUNT(*) as count FROM memories_fts WHERE memories_fts MATCH ?`;
            countParams.push(query);
        } else {
            sql = `SELECT m.* FROM memories m WHERE 1=1`;
            countSql = `SELECT COUNT(*) as count FROM memories m WHERE 1=1`;
        }

        // 项目过滤
        if (projectName) {
            const project = this.projectService.findByName(projectName);
            if (project) {
                sql += ` AND m.project_id = ?`;
                params.push(project.id);
                countSql += ` AND project_id = ?`;
                countParams.push(project.id);
            }
        }

        // 类型过滤
        if (type) {
            const types = Array.isArray(type) ? type : [type];
            const placeholders = types.map(() => '?').join(',');
            sql += ` AND m.type IN (${placeholders})`;
            params.push(...types);
            countSql += ` AND type IN (${placeholders})`;
            countParams.push(...types);
        }

        // 重要性过滤
        if (importance !== undefined) {
            sql += ` AND m.importance >= ?`;
            params.push(importance);
            countSql += ` AND importance >= ?`;
            countParams.push(importance);
        }

        // 时间范围
        if (dateStart) {
            sql += ` AND m.created_at >= ?`;
            params.push(dateStart);
            countSql += ` AND created_at >= ?`;
            countParams.push(dateStart);
        }
        if (dateEnd) {
            sql += ` AND m.created_at <= ?`;
            params.push(dateEnd);
            countSql += ` AND created_at <= ?`;
            countParams.push(dateEnd);
        }

        // 标签过滤（使用 JSON 提取，简化版）
        if (tags && tags.length > 0) {
            // SQLite JSON 支持有限，这里简化处理
            // 实际使用中可以更复杂的查询
            tags.forEach(tag => {
                sql += ` AND m.tags LIKE ?`;
                params.push(`%"${tag}"%`);
                countSql += ` AND tags LIKE ?`;
                countParams.push(`%"${tag}"%`);
            });
        }

        // 排序和分页
        sql += ` ORDER BY m.created_at DESC LIMIT ? OFFSET ?`;
        params.push(limit, offset);

        // 执行查询
        const rows = this.db.prepare(sql).all(...params) as any[];
        const countRow = this.db.prepare(countSql).get(...countParams) as { count: number };
        const total = countRow?.count || 0;

        // 更新访问统计
        const ids = rows.map(r => r.id);
        if (ids.length > 0) {
            const placeholders = ids.map(() => '?').join(',');
            this.db.prepare(
                `UPDATE memories SET access_count = access_count + 1, last_accessed = ? 
                 WHERE id IN (${placeholders})`
            ).run(Date.now(), ...ids);
        }

        return {
            memories: rows.map(row => this.parseRow(row)),
            total,
            hasMore: offset + rows.length < total
        };
    }

    /**
     * 获取最近记忆
     */
    getRecent(limit: number = 10, projectName?: string): Memory[] {
        let sql = `SELECT * FROM memories`;
        const params: any[] = [];

        if (projectName) {
            const project = this.projectService.findByName(projectName);
            if (project) {
                sql += ` WHERE project_id = ?`;
                params.push(project.id);
            }
        }

        sql += ` ORDER BY created_at DESC LIMIT ?`;
        params.push(limit);

        const rows = this.db.prepare(sql).all(...params) as any[];
        return rows.map(row => this.parseRow(row));
    }

    /**
     * 更新记忆
     */
    update(id: number, updates: Partial<MemoryInput>): boolean {
        const existing = this.findById(id);
        if (!existing) return false;

        const sets: string[] = [];
        const params: any[] = [];

        if (updates.title !== undefined) {
            sets.push('title = ?');
            params.push(updates.title);
        }
        if (updates.content !== undefined) {
            sets.push('content = ?');
            params.push(updates.content);
        }
        if (updates.type !== undefined) {
            sets.push('type = ?');
            params.push(updates.type);
        }
        if (updates.importance !== undefined) {
            sets.push('importance = ?');
            params.push(Math.max(1, Math.min(5, updates.importance)));
        }
        if (updates.tags !== undefined) {
            sets.push('tags = ?');
            params.push(JSON.stringify(updates.tags));
        }
        if (updates.metadata !== undefined) {
            sets.push('metadata = ?');
            params.push(JSON.stringify(updates.metadata));
        }
        if (updates.files !== undefined) {
            sets.push('files = ?');
            params.push(JSON.stringify(updates.files));
        }

        if (sets.length === 0) return false;

        sets.push('updated_at = ?');
        params.push(Date.now());
        params.push(id);

        const result = this.db.prepare(
            `UPDATE memories SET ${sets.join(', ')} WHERE id = ?`
        ).run(...params);

        return result.changes > 0;
    }

    /**
     * 删除记忆
     */
    delete(id: number): boolean {
        const result = this.db.prepare('DELETE FROM memories WHERE id = ?').run(id);
        return result.changes > 0;
    }

    /**
     * 获取统计信息
     */
    getStats(projectName?: string): {
        total: number;
        byType: Record<string, number>;
        recentCount: number;
    } {
        let whereClause = '';
        const params: any[] = [];

        if (projectName) {
            const project = this.projectService.findByName(projectName);
            if (project) {
                whereClause = 'WHERE project_id = ?';
                params.push(project.id);
            }
        }

        const total = (this.db.prepare(`SELECT COUNT(*) as count FROM memories ${whereClause}`).get(...params) as any)?.count || 0;
        
        const byTypeRows = this.db.prepare(
            `SELECT type, COUNT(*) as count FROM memories ${whereClause} GROUP BY type`
        ).all(...params) as any[];
        
        const byType: Record<string, number> = {};
        byTypeRows.forEach(row => {
            byType[row.type] = row.count;
        });

        const recentWhere = whereClause ? `${whereClause} AND created_at > ?` : 'WHERE created_at > ?';
        const recentParams = projectName ? [params[0], Date.now() - 7 * 24 * 60 * 60 * 1000] : [Date.now() - 7 * 24 * 60 * 60 * 1000];
        const recentCount = (this.db.prepare(
            `SELECT COUNT(*) as count FROM memories ${recentWhere}`
        ).get(...recentParams) as any)?.count || 0;

        return { total, byType, recentCount };
    }

    /**
     * 解析数据库行
     */
    private parseRow(row: any): Memory {
        return {
            ...row,
            tags: JSON.parse(row.tags || '[]'),
            metadata: JSON.parse(row.metadata || '{}'),
            files: JSON.parse(row.files || '[]')
        };
    }
}

// 导出单例
export const memoryService = new MemoryService();
