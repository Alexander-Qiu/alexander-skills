#!/usr/bin/env node

import { Server } from '@modelcontextprotocol/sdk/server/index.js';
import { StdioServerTransport } from '@modelcontextprotocol/sdk/server/stdio.js';
import {
    CallToolRequestSchema,
    ListToolsRequestSchema,
} from '@modelcontextprotocol/sdk/types.js';
import { memoryService, MemoryInput, MemoryType } from '../services/memory.js';
import { projectService } from '../services/project.js';
import { closeDatabase } from '../db/connection.js';

// 工具定义
const TOOLS = [
    {
        name: 'memory_save',
        description: '保存一条记忆/观察。用于记录重要发现、决策、bug修复等。',
        inputSchema: {
            type: 'object',
            properties: {
                title: {
                    type: 'string',
                    description: '记忆的标题（简短，1-2句话）'
                },
                content: {
                    type: 'string',
                    description: '记忆的详细内容'
                },
                type: {
                    type: 'string',
                    enum: ['observation', 'decision', 'bugfix', 'feature', 'learning', 'summary', 'architecture', 'refactor'],
                    description: '记忆类型'
                },
                importance: {
                    type: 'number',
                    minimum: 1,
                    maximum: 5,
                    description: '重要程度（1-5，5最重要）'
                },
                tags: {
                    type: 'array',
                    items: { type: 'string' },
                    description: '标签数组，如 ["bug", "auth", "performance"]'
                },
                files: {
                    type: 'array',
                    items: { type: 'string' },
                    description: '相关文件路径'
                },
                projectName: {
                    type: 'string',
                    description: '项目名称（如不指定则使用当前项目）'
                }
            },
            required: ['title', 'content']
        }
    },
    {
        name: 'memory_search',
        description: '搜索历史记忆。支持全文搜索、项目过滤、类型过滤等。',
        inputSchema: {
            type: 'object',
            properties: {
                query: {
                    type: 'string',
                    description: '搜索关键词'
                },
                projectName: {
                    type: 'string',
                    description: '项目名称过滤'
                },
                type: {
                    type: 'string',
                    description: '类型过滤（如 bugfix, decision）'
                },
                tags: {
                    type: 'array',
                    items: { type: 'string' },
                    description: '标签过滤'
                },
                importance: {
                    type: 'number',
                    description: '最小重要程度（1-5）'
                },
                limit: {
                    type: 'number',
                    default: 10,
                    description: '返回结果数量'
                }
            }
        }
    },
    {
        name: 'memory_get',
        description: '根据 ID 获取记忆的完整详情。',
        inputSchema: {
            type: 'object',
            properties: {
                id: {
                    type: 'number',
                    description: '记忆 ID'
                }
            },
            required: ['id']
        }
    },
    {
        name: 'memory_get_batch',
        description: '批量获取多条记忆的详情。',
        inputSchema: {
            type: 'object',
            properties: {
                ids: {
                    type: 'array',
                    items: { type: 'number' },
                    description: '记忆 ID 数组'
                }
            },
            required: ['ids']
        }
    },
    {
        name: 'memory_recent',
        description: '获取最近的记忆。',
        inputSchema: {
            type: 'object',
            properties: {
                limit: {
                    type: 'number',
                    default: 10,
                    description: '返回数量'
                },
                projectName: {
                    type: 'string',
                    description: '项目名称过滤'
                }
            }
        }
    },
    {
        name: 'memory_delete',
        description: '删除一条记忆。',
        inputSchema: {
            type: 'object',
            properties: {
                id: {
                    type: 'number',
                    description: '记忆 ID'
                }
            },
            required: ['id']
        }
    },
    {
        name: 'project_list',
        description: '列出所有项目。',
        inputSchema: {
            type: 'object',
            properties: {
                limit: {
                    type: 'number',
                    default: 50,
                    description: '返回数量'
                }
            }
        }
    },
    {
        name: 'project_get_current',
        description: '获取当前项目（自动检测）。',
        inputSchema: {
            type: 'object',
            properties: {}
        }
    },
    {
        name: 'stats_get',
        description: '获取记忆统计信息。',
        inputSchema: {
            type: 'object',
            properties: {
                projectName: {
                    type: 'string',
                    description: '项目名称（如不指定则统计所有）'
                }
            }
        }
    }
];

// 创建 MCP 服务器
const server = new Server(
    {
        name: 'kimi-mem',
        version: '0.1.0',
    },
    {
        capabilities: {
            tools: {},
        },
    }
);

// 注册工具列表处理器
server.setRequestHandler(ListToolsRequestSchema, async () => {
    return {
        tools: TOOLS
    };
});

// 注册工具调用处理器
server.setRequestHandler(CallToolRequestSchema, async (request) => {
    const { name, arguments: args } = request.params;

    try {
        switch (name) {
            case 'memory_save': {
                const input: MemoryInput = {
                    title: args.title as string,
                    content: args.content as string,
                    type: args.type as MemoryType,
                    importance: args.importance as number,
                    tags: args.tags as string[],
                    files: args.files as string[],
                    projectName: args.projectName as string
                };
                
                const memory = memoryService.save(input);
                
                return {
                    content: [{
                        type: 'text',
                        text: `✅ 记忆已保存 (ID: ${memory.id})\n\n标题: ${memory.title}\n类型: ${memory.type}\n项目: ${projectService.findById(memory.project_id)?.name || 'unknown'}`
                    }]
                };
            }

            case 'memory_search': {
                const result = memoryService.search({
                    query: args.query as string,
                    projectName: args.projectName as string,
                    type: args.type as MemoryType,
                    tags: args.tags as string[],
                    importance: args.importance as number,
                    limit: args.limit as number || 10
                });

                if (result.memories.length === 0) {
                    return {
                        content: [{
                            type: 'text',
                            text: '未找到匹配的记忆。'
                        }]
                    };
                }

                const lines = result.memories.map(m => {
                    const date = new Date(m.created_at).toLocaleString('zh-CN');
                    const typeEmoji = getTypeEmoji(m.type);
                    return `[${m.id}] ${typeEmoji} ${m.title} (${date})`;
                });

                return {
                    content: [{
                        type: 'text',
                        text: `找到 ${result.total} 条记忆（显示 ${result.memories.length} 条）：\n\n${lines.join('\n')}${result.hasMore ? '\n\n... 还有更多结果' : ''}`
                    }]
                };
            }

            case 'memory_get': {
                const memory = memoryService.findById(args.id as number);
                
                if (!memory) {
                    return {
                        content: [{
                            type: 'text',
                            text: `未找到 ID 为 ${args.id} 的记忆。`
                        }],
                        isError: true
                    };
                }

                const project = projectService.findById(memory.project_id);
                const date = new Date(memory.created_at).toLocaleString('zh-CN');
                const typeEmoji = getTypeEmoji(memory.type);

                let text = `${typeEmoji} **${memory.title}**\n\n`;
                text += `ID: ${memory.id}\n`;
                text += `类型: ${memory.type}\n`;
                text += `项目: ${project?.name || 'unknown'}\n`;
                text += `时间: ${date}\n`;
                text += `重要度: ${'★'.repeat(memory.importance)}${'☆'.repeat(5 - memory.importance)}\n`;
                
                if (memory.tags.length > 0) {
                    text += `标签: ${memory.tags.join(', ')}\n`;
                }
                
                if (memory.files.length > 0) {
                    text += `文件: ${memory.files.join(', ')}\n`;
                }
                
                text += `\n---\n\n${memory.content}`;

                return {
                    content: [{ type: 'text', text }]
                };
            }

            case 'memory_get_batch': {
                const ids = args.ids as number[];
                
                if (!ids || ids.length === 0) {
                    return {
                        content: [{
                            type: 'text',
                            text: '请提供至少一个 ID。'
                        }],
                        isError: true
                    };
                }

                const memories = memoryService.findByIds(ids);
                
                if (memories.length === 0) {
                    return {
                        content: [{
                            type: 'text',
                            text: '未找到指定的记忆。'
                        }]
                    };
                }

                const parts = memories.map(m => {
                    const date = new Date(m.created_at).toLocaleDateString('zh-CN');
                    const typeEmoji = getTypeEmoji(m.type);
                    return `[${m.id}] ${typeEmoji} **${m.title}** (${date})\n\n${m.content}\n`;
                });

                return {
                    content: [{
                        type: 'text',
                        text: parts.join('\n---\n\n')
                    }]
                };
            }

            case 'memory_recent': {
                const memories = memoryService.getRecent(
                    args.limit as number || 10,
                    args.projectName as string
                );

                if (memories.length === 0) {
                    return {
                        content: [{
                            type: 'text',
                            text: '暂无记忆。'
                        }]
                    };
                }

                const lines = memories.map(m => {
                    const date = new Date(m.created_at).toLocaleString('zh-CN');
                    const typeEmoji = getTypeEmoji(m.type);
                    return `[${m.id}] ${typeEmoji} ${m.title} (${date})`;
                });

                return {
                    content: [{
                        type: 'text',
                        text: `最近的 ${memories.length} 条记忆：\n\n${lines.join('\n')}`
                    }]
                };
            }

            case 'memory_delete': {
                const success = memoryService.delete(args.id as number);
                
                return {
                    content: [{
                        type: 'text',
                        text: success ? `✅ 记忆 ${args.id} 已删除。` : `❌ 未找到记忆 ${args.id}。`
                    }]
                };
            }

            case 'project_list': {
                const projects = projectService.listAll(args.limit as number || 50);
                
                if (projects.length === 0) {
                    return {
                        content: [{
                            type: 'text',
                            text: '暂无项目。'
                        }]
                    };
                }

                const lines = projects.map(p => {
                    const lastAccess = new Date(p.updated_at).toLocaleDateString('zh-CN');
                    return `- **${p.name}** (${p.access_count} 次访问, 最后: ${lastAccess})`;
                });

                return {
                    content: [{
                        type: 'text',
                        text: `项目列表：\n\n${lines.join('\n')}`
                    }]
                };
            }

            case 'project_get_current': {
                const project = projectService.getCurrent();
                
                return {
                    content: [{
                        type: 'text',
                        text: `当前项目: **${project.name}**\n路径: ${project.path || 'N/A'}\n描述: ${project.description || 'N/A'}`
                    }]
                };
            }

            case 'stats_get': {
                const stats = memoryService.getStats(args.projectName as string);
                
                let text = `📊 记忆统计`;
                if (args.projectName) {
                    text += ` (${args.projectName})`;
                }
                text += `\n\n`;
                
                text += `总计: ${stats.total} 条记忆\n`;
                text += `最近7天: ${stats.recentCount} 条\n\n`;
                
                if (Object.keys(stats.byType).length > 0) {
                    text += '按类型分布:\n';
                    for (const [type, count] of Object.entries(stats.byType)) {
                        text += `  ${getTypeEmoji(type as MemoryType)} ${type}: ${count}\n`;
                    }
                }

                return {
                    content: [{ type: 'text', text }]
                };
            }

            default:
                return {
                    content: [{
                        type: 'text',
                        text: `未知工具: ${name}`
                    }],
                    isError: true
                };
        }
    } catch (error) {
        return {
            content: [{
                type: 'text',
                text: `错误: ${error instanceof Error ? error.message : String(error)}`
            }],
            isError: true
        };
    }
});

// 类型表情映射
function getTypeEmoji(type: MemoryType): string {
    const emojiMap: Record<MemoryType, string> = {
        observation: '👁️',
        decision: '⚡',
        bugfix: '🐛',
        feature: '✨',
        learning: '📚',
        summary: '📝',
        architecture: '🏗️',
        refactor: '♻️'
    };
    return emojiMap[type] || '📌';
}

// 清理处理
async function cleanup() {
    closeDatabase();
    process.exit(0);
}

process.on('SIGINT', cleanup);
process.on('SIGTERM', cleanup);

// 启动服务器
async function main() {
    const transport = new StdioServerTransport();
    await server.connect(transport);
    
    // 静默启动，不输出到 stdout（避免干扰 MCP 协议）
    console.error('kimi-mem MCP server started');
}

main().catch((error) => {
    console.error('Fatal error:', error);
    process.exit(1);
});
