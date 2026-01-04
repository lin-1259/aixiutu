#!/bin/bash
# 检查所有可用的 Ant Design Icons

echo "检查 @ant-design/icons 包中所有可用的图标..."
echo "查找包含 'Color' 或 'Palette' 的图标："

node -e "
try {
  const icons = require('@ant-design/icons');
  const allIcons = Object.keys(icons);
  console.log('所有图标总数:', allIcons.length);
  console.log('\n包含 Color 的图标:');
  allIcons.filter(icon => icon.toLowerCase().includes('color')).forEach(icon => console.log('  - ' + icon));
  console.log('\n包含 Palette 的图标:');
  allIcons.filter(icon => icon.toLowerCase().includes('palette')).forEach(icon => console.log('  - ' + icon));
  console.log('\n包含 Paint 的图标:');
  allIcons.filter(icon => icon.toLowerCase().includes('paint')).forEach(icon => console.log('  - ' + icon));
} catch (e) {
  console.log('错误: 无法加载 @ant-design/icons');
  console.log('请先安装: npm install @ant-design/icons');
}
"