# Electron TypeScript 编译错误修复方案

## 错误分析

构建现在在 TypeScript 编译阶段失败，主要有以下几个问题：

1. **缺少类型声明文件**: `../../src/types/index.js`
2. **类型错误**: `unknown` 类型不能分配给 `string | undefined`
3. **模块缺失**: `better-sqlite3` 缺少类型声明
4. **参数缺失**: Logger 构造函数参数缺失
5. **函数未导入**: `mkdirSync` 函数未导入

## 修复方案

### 1. 创建缺失的类型声明文件

创建 `/src/types/index.ts` 文件：

```typescript
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
```

### 2. 修复 Logger 类型错误

在 Logger 构造函数中处理未知类型错误：

```typescript
// 修复前
this.logger.error('错误信息', error);

// 修复后
this.logger.error('错误信息', error instanceof Error ? error.message : String(error));
```

### 3. 修复 better-sqlite3 类型问题

```bash
npm install --save-dev @types/better-sqlite3
```

### 4. 修复 import 问题

```typescript
// 添加缺失的导入
import { mkdirSync } from 'fs';
import path from 'path';
```

## 快速修复脚本

运行以下命令进行快速修复：

```bash
# 1. 安装缺失的类型包
npm install --save-dev @types/better-sqlite3

# 2. 创建类型声明文件（见上面的代码）
# 3. 修复各个文件的类型错误
```

## 批量修复类型错误

对于所有的 `unknown` 类型错误，可以这样处理：

```typescript
// 通用错误处理函数
function handleError(error: unknown): string {
  if (error instanceof Error) {
    return error.message;
  }
  return String(error || '未知错误');
}

// 使用示例
this.logger.error('错误信息', handleError(error));
```

## 推荐的修复顺序

1. **立即修复**: 安装 @types/better-sqlite3
2. **创建类型文件**: 创建 `/src/types/index.ts`
3. **修复类型错误**: 处理所有的 `unknown` 类型错误
4. **添加缺失导入**: 添加 `mkdirSync` 等缺失的导入
5. **验证修复**: 重新运行构建命令