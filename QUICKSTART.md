# 快速开始指南

## 环境准备

### 1. 安装 Python 依赖

```bash
pip install -r requirements.txt
```

### 2. 配置 API

复制环境变量模板：
```bash
cp .env.example .env
```

编辑 `.env` 文件，填入您的 API 信息：
```env
# 豆包 API 配置
DOUBAO_API_URL=https://your-api-endpoint.com/doubao
DOUBAO_API_KEY=your_doubao_api_key_here

# Banana API 配置
BANANA_API_URL=https://your-api-endpoint.com/banana
BANANA_API_KEY=your_banana_api_key_here
BANANA_MODEL_KEY=your_banana_model_key_here
```

## 运行程序

```bash
python main.py
```

## 使用流程

1. **配置 API**
   - 点击左上角"API 配置"按钮
   - 填写豆包和 Banana 的 API 信息
   - 点击"确认"保存

2. **导入图片**
   - 点击"导入图片"按钮
   - 选择一张或多张图片（JPG/PNG/WebP）
   - 图片会显示在列表中

3. **选择模型**
   - 在"模型选择"下拉框中选择：
     - **豆包修图模型**：人像精修或画质增强
     - **Banana 风格模型**：自定义风格描述

4. **配置参数**
   - 豆包模型：设置磨皮强度（0-1）和美白强度（0-1）
   - Banana 模型：输入风格描述 Prompt

5. **选择输出目录**
   - 点击"选择输出目录"
   - 选择图片保存位置

6. **开始处理**
   - 点击"启动批量处理"
   - 等待处理完成
   - 查看右侧预览区的效果图

## 功能说明

### 豆包修图模型参数

- **修图类型**：
  - `retouch`：人像精修，包括磨皮、美白等
  - `enhance`：画质增强，提升图片清晰度

- **磨皮强度**（smooth）：
  - 范围：0-1
  - 默认值：0.8
  - 值越大，磨皮效果越明显

- **美白强度**（whiten）：
  - 范围：0-1
  - 默认值：0.6
  - 值越大，美白效果越明显

### Banana 风格模型参数

- **风格描述 Prompt**：
  - 默认值：`convert to anime style, high detail`
  - 可以自定义描述，例如：
    - `oil painting style, vibrant colors`
    - `watercolor painting, soft edges`
    - `pencil sketch, black and white`

## 常见问题

### Q: 程序无法启动？
A: 确保已安装所有依赖：`pip install -r requirements.txt`

### Q: API 调用失败？
A: 检查以下内容：
1. API 配置是否正确填写
2. 网络连接是否正常
3. API Key 是否有效
4. 查看 控制台日志 了解详细错误

### Q: 图片处理很慢？
A: 
1. 检查网络连接质量
2. 图片文件可能较大，建议单张不超过 5MB
3. API 服务端可能响应较慢

### Q: 批量处理失败？
A:
1. 检查是否有足够的磁盘空间
2. 确保输出目录有写入权限
3. 查看 处理完成提示 中的失败数量

## 技术支持

- 查看 README.md 了解详细功能说明
- 查看 代码注释 了解实现细节
- 查看日志文件了解错误信息
