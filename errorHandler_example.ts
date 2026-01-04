// utils/errorHandler.ts
// 创建一个通用的错误处理函数文件

/**
 * 将未知类型错误转换为字符串
 */
export function handleError(error: unknown): string {
  if (error instanceof Error) {
    return error.message;
  }
  return String(error || '未知错误');
}

/**
 * 安全的错误日志记录
 */
export function safeLogError(logger: any, message: string, error: unknown) {
  logger.error(message, handleError(error));
}