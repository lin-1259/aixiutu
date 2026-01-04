#!/bin/bash
# TypeScript 错误快速修复脚本

echo "开始修复 TypeScript 编译错误..."

# 1. 安装缺失的类型包
echo "1. 安装 @types/better-sqlite3..."
npm install --save-dev @types/better-sqlite3

# 2. 检查并创建 types 目录
echo "2. 检查 types 目录..."
if [ ! -d "src/types" ]; then
  mkdir -p src/types
  echo "创建 src/types 目录"
fi

# 3. 检查是否需要安装其他类型包
echo "3. 检查其他可能需要的类型包..."
# 你可能还需要这些包：
# npm install --save-dev @types/node

echo "修复完成！请根据 typescript_fix_guide.md 继续手动修复具体的代码问题。"