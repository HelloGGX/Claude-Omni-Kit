#!/bin/bash

# Confluence页面创建器运行示例
# 请先修改config.yaml中的配置

echo "🚀 Confluence页面创建器 - 运行示例"
echo "=================================="

# 检查Python版本
python_version=$(python --version 2>&1)
echo "📦 Python版本: $python_version"

# 检查依赖安装
echo "🔍 检查依赖安装..."
if ! python -c "import playwright, yaml" 2>/dev/null; then
    echo "❌ 缺少必要依赖，请运行: pip install -r requirements.txt"
    exit 1
fi

echo "✅ 依赖检查通过"

# 检查配置文件
if [ ! -f "config.yaml" ]; then
    echo "📋 未找到config.yaml，复制示例配置..."
    cp config-example.yaml config.yaml
    echo "⚠️  请编辑config.yaml文件，填入您的实际配置"
    exit 1
fi

echo "✅ 配置文件检查通过"

# 运行技能
echo "🎯 开始执行技能..."
python main.py config.yaml

echo "✅ 执行完成！"