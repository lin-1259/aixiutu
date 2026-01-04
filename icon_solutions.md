# Ant Design Icons PaletteOutlined 导入错误解决方案

## 问题分析
错误信息显示："PaletteOutlined" is not exported by "node_modules/@ant-design/icons/es/index.js"

## 解决方案

### 方案A: 使用替代图标名称
PaletteOutlined 可能不存在，尝试以下替代图标：

```tsx
// 原来的导入
import { PaletteOutlined } from '@ant-design/icons';

// 替代方案1: 使用 ColorsOutlined (颜色相关)
import { ColorsOutlined } from '@ant-design/icons';

// 替代方案2: 使用 FormatPainterOutlined (格式画家)
import { FormatPainterOutlined } from '@ant-design/icons';

// 替代方案3: 使用 PictureOutlined (图片相关)
import { PictureOutlined } from '@ant-design/icons';

// 替代方案4: 使用 AppstoreOutlined (应用商店)
import { AppstoreOutlined } from '@ant-design/icons';
```

### 方案B: 检查可用的所有图标
运行以下命令查看所有可用的图标：

```bash
node -e "console.log(Object.keys(require('@ant-design/icons')).filter(k => k.includes('Palette')).join('\n'))"
```

### 方案C: 更新到最新版本
```bash
npm update @ant-design/icons
```

### 方案D: 直接修复 TemplateSelector.tsx
将 PaletteOutlined 替换为可用的图标：

```tsx
// 修复前
import {
  FileTextOutlined, 
  CloudOutlined,
  PaletteOutlined,  // 这行有问题
  PlusOutlined,
  EditOutlined
} from '@ant-design/icons';

// 修复后 - 选择一个替代图标
import {
  FileTextOutlined, 
  CloudOutlined,
  FormatPainterOutlined,  // 或者 ColorsOutlined
  PlusOutlined,
  EditOutlined
} from '@ant-design/icons';
```

### 方案E: 检查图标名称的正确拼写
Ant Design Icons 中的图标命名规范：
- 所有图标都以 "Outlined"、"Filled" 或 "TwoTone" 结尾
- 颜色相关的图标可能是：
  - ColorsOutlined
  - FormatPainterOutlined
  - PictureOutlined
  - AppstoreOutlined

### 验证修复
修复后重新运行构建命令：
```bash
npm run build
```

## 推荐解决方案
1. 首先尝试方案D，直接替换 PaletteOutlined 为 FormatPainterOutlined 或 ColorsOutlined
2. 如果问题仍然存在，运行方案B查看所有可用的图标
3. 最后考虑更新到最新版本（方案C）