// 创建 src/types/index.ts 文件内容
// 这个文件应该放在项目的 src/types/index.ts 路径下

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