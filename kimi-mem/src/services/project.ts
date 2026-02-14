import { getDatabase } from '../db/connection.js';
import { existsSync, statSync } from 'fs';
import { execSync } from 'child_process';

export interface Project {
    id: number;
    name: string;
    path: string | null;
    description: string | null;
    created_at: number;
    updated_at: number;
    access_count: number;
}

export interface ProjectInput {
    name: string;
    path?: string;
    description?: string;
}

/**
 * 项目管理服务
 */
export class ProjectService {
    private db = getDatabase();

    /**
     * 获取或创建项目
     */
    getOrCreate(name: string, path?: string): Project {
        // 先尝试查找
        let project = this.findByName(name);
        
        if (project) {
            // 更新访问统计
            this.db.prepare(
                'UPDATE projects SET access_count = access_count + 1, updated_at = ? WHERE id = ?'
            ).run(Date.now(), project.id);
            return project;
        }

        // 创建新项目
        const result = this.db.prepare(
            'INSERT INTO projects (name, path, description, created_at, updated_at) VALUES (?, ?, ?, ?, ?)'
        ).run(name, path || null, null, Date.now(), Date.now());

        return {
            id: result.lastInsertRowid as number,
            name,
            path: path || null,
            description: null,
            created_at: Date.now(),
            updated_at: Date.now(),
            access_count: 0
        };
    }

    /**
     * 根据名称查找项目
     */
    findByName(name: string): Project | undefined {
        return this.db.prepare('SELECT * FROM projects WHERE name = ?').get(name) as Project | undefined;
    }

    /**
     * 根据 ID 查找项目
     */
    findById(id: number): Project | undefined {
        return this.db.prepare('SELECT * FROM projects WHERE id = ?').get(id) as Project | undefined;
    }

    /**
     * 列出所有项目
     */
    listAll(limit: number = 50): Project[] {
        return this.db.prepare(
            'SELECT * FROM projects ORDER BY access_count DESC, updated_at DESC LIMIT ?'
        ).all(limit) as Project[];
    }

    /**
     * 更新项目描述
     */
    updateDescription(id: number, description: string): void {
        this.db.prepare(
            'UPDATE projects SET description = ?, updated_at = ? WHERE id = ?'
        ).run(description, Date.now(), id);
    }

    /**
     * 删除项目（会级联删除相关记忆）
     */
    delete(id: number): boolean {
        const result = this.db.prepare('DELETE FROM projects WHERE id = ?').run(id);
        return result.changes > 0;
    }

    /**
     * 自动检测当前项目
     * 
     * 策略：
     * 1. 如果有 package.json，使用 name 字段
     * 2. 如果是 git 仓库，使用仓库名
     * 3. 使用目录名
     */
    detectFromPath(cwd: string = process.cwd()): { name: string; path: string } {
        const path = require('path');
        
        // 尝试读取 package.json
        const pkgPath = path.join(cwd, 'package.json');
        if (existsSync(pkgPath)) {
            try {
                const pkg = JSON.parse(require('fs').readFileSync(pkgPath, 'utf-8'));
                if (pkg.name && pkg.name !== '.') {
                    return { name: pkg.name, path: cwd };
                }
            } catch {}
        }

        // 尝试 git 仓库名
        try {
            const gitRemote = execSync('git remote get-url origin', { 
                cwd, 
                encoding: 'utf-8',
                timeout: 5000 
            }).trim();
            const match = gitRemote.match(/\/([^\/]+?)(?:\.git)?$/);
            if (match) {
                return { name: match[1], path: cwd };
            }
        } catch {}

        // 使用目录名
        return { 
            name: path.basename(cwd), 
            path: cwd 
        };
    }

    /**
     * 获取当前项目（自动检测或默认）
     */
    getCurrent(cwd?: string): Project {
        const detected = this.detectFromPath(cwd);
        return this.getOrCreate(detected.name, detected.path);
    }
}

// 导出单例
export const projectService = new ProjectService();
