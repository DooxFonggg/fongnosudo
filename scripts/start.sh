#!/bin/bash

echo "🚀 Starting Fongnosudo Blog..."

# Start services
docker-compose up -d

echo "✅ Services started!"
echo "📊 Backend: http://127.0.0.1/api/"
echo "🌐 Frontend: http://127.0.0.1/"
echo ""
echo "Run 'docker-compose logs -f' to see logs"