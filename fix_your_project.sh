#!/bin/bash
# 在你的项目目录 /Users/q/Downloads/ai-xiutu-main 2/ 中运行此脚本

echo "开始修复 ai-xiutu-main 项目的 TypeScript 错误..."

# 1. 安装缺失的类型包
echo "1. 安装类型包..."
npm install --save-dev @types/better-sqlite3 @types/node

# 2. 创建缺失的类型声明文件
echo "2. 创建类型声明文件..."

# 创建 src/types/index.ts
cat > src/types/index.ts << 'EOF'
// API 相关类型
export interface ApiRequest {
  method: string;
  url: string;
  headers?: Record<string, string>;
  body?: any;
}

export interface ApiResponse {
  success: boolean;
  data?: any;
  error?: string;
}

export interface ApiConfig {
  name: string;
  provider: string;
  apiKey: string;
  baseUrl: string;
  timeout?: number;
  enabled?: boolean;
}

// 任务相关类型
export interface Task {
  id: string;
  status: 'pending' | 'processing' | 'completed' | 'failed';
  inputFile: string;
  outputFile?: string;
  template?: Template;
  error?: string;
  progress: number;
  createdAt: Date;
  updatedAt: Date;
}

// 模板相关类型
export interface Template {
  id: string;
  name: string;
  type: string;
  config: Record<string, any>;
  createdAt: Date;
  updatedAt: Date;
}

// 缓存相关类型
export interface CacheEntry {
  key: string;
  value: any;
  createdAt: Date;
  expiresAt?: Date;
}

export interface CacheStats {
  hits: number;
  misses: number;
  total: number;
}

// 日志相关类型
export interface LogEntry {
  level: 'info' | 'warn' | 'error' | 'debug';
  message: string;
  timestamp: Date;
  metadata?: Record<string, any>;
}

// 应用配置类型
export interface AppConfig {
  api: {
    defaultProvider: string;
    timeout: number;
    retryCount: number;
  };
  cache: {
    enabled: boolean;
    maxSize: number;
    ttl: number;
  };
  hotFolder: {
    enabled: boolean;
    path: string;
    recursive: boolean;
  };
  logging: {
    level: string;
    file: boolean;
    console: boolean;
  };
}
EOF

echo "类型声明文件已创建：src/types/index.ts"

# 3. 修复具体的代码错误
echo "3. 修复代码错误..."

# 修复 TaskWorker.ts
echo "修复 TaskWorker.ts..."
cat > TaskWorker_fix.ts << 'EOF'
import { Task, ApiRequest, Template } from '../../src/types/index.js';
import { Logger } from './Logger.js';
import { mkdirSync } from 'fs';
import path from 'path';

// 修复 Logger 构造函数调用
// 原来的代码: this.logger = new Logger();
// 修复后:
this.logger = new Logger(userDataPath);

// 修复 mkdirSync 导入
// 在文件顶部添加: import { mkdirSync } from 'fs';
EOF

echo "修复脚本已完成！"
echo "接下来请手动修复以下文件中的具体错误："
echo "1. electron/main/main.ts - 添加 event 参数类型"
echo "2. 所有 services/*.ts 文件 - 修复错误参数类型"
echo "3. TaskWorker.ts - 添加缺失的导入"