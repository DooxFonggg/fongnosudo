#!/bin/bash

echo "🔨 Building Fongnosudo Blog..."

# Build images
docker-compose build --no-cache

echo "✅ Build completed!"