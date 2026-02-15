#!/usr/bin/env node

/**
 * kimi-mem CLI
 * 
 * 提供命令行方式操作记忆，便于脚本和手动管理
 */

import { memoryService } from '../services/memory.js';
import { projectService } from '../services/project.js';
import { closeDatabase } from '../db/connection.js';

function printHelp() {
    console.log(`
🧠 kimi-mem CLI

Usage:
  kimi-mem <command> [options]

Commands:
  save [options]         保存记忆
  search [options]       搜索记忆
  recent [options]       查看最近记忆
  show <id>              查看记忆详情
  delete <id>            删除记忆
  projects               列出项目
  current                显示当前项目
  stats                  显示统计

Options for save:
  -t, --title <title>       标题（必填）
  -c, --content <content>   内容（必填）
  --type <type>            类型（默认: observation）
  --importance <1-5>       重要程度（默认: 3）
  --tags <tag1,tag2>       标签
  --project <name>         项目名

Options for search:
  -q, --query <text>       搜索词
  --type <type>           类型过滤
  --project <name>        项目过滤
  -n, --limit <num>       结果数量（默认: 10）

Options for recent:
  -n, --limit <num>       数量（默认: 10）
  --project <name>        项目过滤

Examples:
  kimi-mem save -t "修复登录Bug" -c "详细描述..." --type bugfix --tags auth,bug
  kimi-mem search -q "authentication" --limit 5
  kimi-mem recent -n 5
  kimi-mem stats
`);
}

function parseArgs(args: string[]): Record<string, any> {
    const options: Record<string, any> = {};
    for (let i = 0; i < args.length; i++) {
        const arg = args[i];
        if (arg.startsWith('--')) {
            const key = arg.slice(2);
            const nextArg = args[i + 1];
            if (nextArg && !nextArg.startsWith('-')) {
                options[key] = nextArg;
                i++;
            } else {
                options[key] = true;
            }
        } else if (arg.startsWith('-')) {
            const key = arg.slice(1);
            const nextArg = args[i + 1];
            if (nextArg && !nextArg.startsWith('-')) {
                options[key] = nextArg;
                i++;
            }
        } else {
            options._args = options._args || [];
            options._args.push(arg);
        }
    }
    return options;
}

async function main() {
    const args = process.argv.slice(2);
    const command = args[0];
    const options = parseArgs(args.slice(1));

    try {
        switch (command) {
            case 'save':
            case 's': {
                if (!options.title && !options.t) {
                    console.error('❌ Title is required. Use -t or --title');
                    process.exit(1);
                }
                if (!options.content && !options.c) {
                    console.error('❌ Content is required. Use -c or --content');
                    process.exit(1);
                }

                const memory = memoryService.save({
                    title: options.title || options.t,
                    content: options.content || options.c,
                    type: options.type || 'observation',
                    importance: parseInt(options.importance) || 3,
                    tags: options.tags ? options.tags.split(',') : undefined,
                    projectName: options.project
                });

                console.log(`✅ Memory saved (ID: ${memory.id})`);
                break;
            }

            case 'search':
            case 'find': {
                const result = memoryService.search({
                    query: options.query || options.q,
                    projectName: options.project,
                    type: options.type,
                    limit: parseInt(options.limit || options.n) || 10
                });

                if (result.memories.length === 0) {
                    console.log('No memories found.');
                    break;
                }

                console.log(`Found ${result.total} memories:\n`);
                for (const m of result.memories) {
                    const date = new Date(m.created_at).toLocaleDateString();
                    console.log(`[${m.id}] ${m.type}: ${m.title} (${date})`);
                }
                break;
            }

            case 'recent':
            case 'r': {
                const memories = memoryService.getRecent(
                    parseInt(options.limit || options.n) || 10,
                    options.project
                );

                if (memories.length === 0) {
                    console.log('No memories yet.');
                    break;
                }

                for (const m of memories) {
                    const date = new Date(m.created_at).toLocaleDateString();
                    console.log(`[${m.id}] ${m.type}: ${m.title} (${date})`);
                }
                break;
            }

            case 'show':
            case 'view': {
                const id = parseInt(options._args?.[0]);
                if (!id) {
                    console.error('❌ Memory ID required');
                    process.exit(1);
                }

                const memory = memoryService.findById(id);
                if (!memory) {
                    console.error(`❌ Memory ${id} not found`);
                    process.exit(1);
                }

                const project = projectService.findById(memory.project_id);
                const date = new Date(memory.created_at).toLocaleString();

                console.log(`\n${memory.title}`);
                console.log(`ID: ${memory.id}`);
                console.log(`Type: ${memory.type}`);
                console.log(`Project: ${project?.name || 'unknown'}`);
                console.log(`Date: ${date}`);
                console.log(`Importance: ${'★'.repeat(memory.importance)}${'☆'.repeat(5 - memory.importance)}`);
                if (memory.tags.length) console.log(`Tags: ${memory.tags.join(', ')}`);
                console.log(`\n${memory.content}`);
                break;
            }

            case 'delete':
            case 'rm': {
                const id = parseInt(options._args?.[0]);
                if (!id) {
                    console.error('❌ Memory ID required');
                    process.exit(1);
                }

                const success = memoryService.delete(id);
                console.log(success ? `✅ Memory ${id} deleted` : `❌ Memory ${id} not found`);
                break;
            }

            case 'projects':
            case 'p': {
                const projects = projectService.listAll();
                if (projects.length === 0) {
                    console.log('No projects yet.');
                    break;
                }

                for (const p of projects) {
                    console.log(`${p.name} (${p.access_count} memories)`);
                }
                break;
            }

            case 'current':
            case 'cwd': {
                const project = projectService.getCurrent();
                console.log(`Current project: ${project.name}`);
                if (project.path) console.log(`Path: ${project.path}`);
                break;
            }

            case 'stats': {
                const stats = memoryService.getStats(options.project);
                console.log(`Total memories: ${stats.total}`);
                console.log(`Recent (7d): ${stats.recentCount}`);
                if (Object.keys(stats.byType).length > 0) {
                    console.log('\nBy type:');
                    for (const [type, count] of Object.entries(stats.byType)) {
                        console.log(`  ${type}: ${count}`);
                    }
                }
                break;
            }

            case 'help':
            case '-h':
            case '--help':
            default:
                printHelp();
                break;
        }
    } catch (error) {
        console.error('Error:', error instanceof Error ? error.message : error);
        process.exit(1);
    } finally {
        closeDatabase();
    }
}

main();
