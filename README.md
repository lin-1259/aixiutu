# AI 批量图片修改工具

一个基于 PyQt6 的 AI 批量图片编辑工具，支持豆包修图模型和 Banana 风格模型。

## 功能特性

- **双模型支持**：豆包修图模型（人像精修、画质增强）和 Banana 风格模型（风格转换）
- **批量处理**：支持同时处理多张图片，最大并发数为 5
- **实时预览**：左右分栏布局，实时显示原图和处理后效果图
- **灵活配置**：可视化 API 配置界面，支持即时修改无需重启
- **进度追踪**：实时显示处理进度条和任务状态
- **异常处理**：完善的错误处理机制，确保程序稳定运行

## 系统要求

- Python 3.9+
- Windows 10+ / macOS 12+ / Ubuntu 20.04+
- 网络连接（用于访问 AI 模型 API）

## 安装

1. 克隆或下载本项目

2. 安装依赖：
```bash
pip install -r requirements.txt
```

3. 配置 API：
   - 复制 `.env.example` 文件为 `.env`
   - 填写您的 API 配置信息
   - 或在程序运行时点击"API 配置"按钮进行配置

```bash
cp .env.example .env
```

编辑 `.env` 文件，填入您的 API 信息：
```env
DOUBAO_API_URL=your_doubao_api_url
DOUBAO_API_KEY=your_doubao_api_key
BANANA_API_URL=your_banana_api_url
BANANA_API_KEY=your_banana_api_key
BANANA_MODEL_KEY=your_banana_model_key
```

## 使用方法

1. **启动程序**：
```bash
python main.py
```

2. **配置 API**：
   - 点击左上角"API 配置"按钮
   - 填写豆包和 Banana 的 API 信息
   - 点击"确认"保存配置

3. **导入图片**：
   - 点击"导入图片"按钮
   - 选择一张或多张图片（支持 JPG/PNG/WebP 格式）
   - 图片会显示在左侧列表中

4. **选择模型和参数**：
   - 在"模型选择"下拉框中选择模型
   - 根据选择的模型配置相应参数：
     - **豆包修图模型**：选择修图类型（人像精修/画质增强），设置磨皮和美白强度
     - **Banana 风格模型**：输入风格描述 Prompt

5. **选择输出目录**：
   - 点击"选择输出目录"按钮
   - 选择处理后图片的保存位置（默认为 ./output）

6. **开始处理**：
   - 点击"启动批量处理"按钮
   - 等待处理完成，进度条会显示实时进度
   - 处理完成后会在右侧预览区显示效果图
   - 处理完成的图片会保存到指定的输出目录

## 项目结构

```
.
├── main.py                 # 程序入口
├── config_manager.py       # 配置管理模块
├── api_clients.py          # API 客户端模块
├── worker_threads.py       # 任务调度和工作线程模块
├── ui_components.py        # UI 组件模块
├── requirements.txt        # Python 依赖列表
├── .env.example           # 环境变量示例文件
└── README.md              # 项目说明文档
```

## 模块说明

### config_manager.py
负责 API 配置的加载、保存和管理，支持从 `.env` 文件读取配置。

### api_clients.py
实现与 AI 模型 API 的通信：
- `DoubaoClient`：豆包修图模型客户端
- `BananaClient`：Banana 风格模型客户端
- 图片 Base64 编码/解码工具

### worker_threads.py
实现任务调度和并发处理：
- `TaskManager`：管理任务队列和工作者线程
- `ProcessingTask`：表示单个图片处理任务
- `WorkerThread`：执行图片处理的工作线程
- 支持最大 5 个并发任务

### ui_components.py
实现 PyQt6 用户界面：
- `MainWindow`：主窗口
- `ConfigPanel`：左侧配置面板
- `PreviewPanel`：右侧预览面板
- `ApiConfigDialog`：API 配置对话框

## 性能指标

- 单张图片处理响应时间：≤ 60s
- 支持批量处理：≥ 50 张图片
- 单张图片大小限制：≤ 5MB
- 最大并发任务数：5

## 注意事项

1. **API 配置**：使用前必须正确配置 API 信息，否则无法调用 AI 模型
2. **网络连接**：程序需要网络连接来访问 AI 模型 API
3. **图片格式**：导入的图片会统一转换为 PNG 格式进行处理
4. **输出目录**：确保输出目录有足够的磁盘空间
5. **并发控制**：最大并发数为 5，可防止 API 过载

## 故障排除

### 无法加载图片
- 检查图片格式是否为 JPG/PNG/WebP
- 检查图片文件是否损坏

### API 调用失败
- 检查 API 配置是否正确
- 检查网络连接是否正常
- 检查 API Key 是否有效
- 查看控制台日志了解详细错误信息

### 处理速度慢
- 检查网络连接质量
- 减少同时处理的图片数量
- 检查 API 服务端状态

## 开发者信息

- 技术栈：Python + PyQt6 + Requests + Pillow
- API 模型：豆包修图模型、Banana 风格模型
- 许可证：请根据项目实际情况添加

## 更新日志

### v1.0.0
- 初始版本发布
- 支持豆包修图模型和 Banana 风格模型
- 实现批量图片处理功能
- 添加实时预览和进度追踪
