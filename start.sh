#!/bin/bash

echo "🚀 Starting Fongnosudo Blog..."

# Start services
docker-compose up -d

echo "✅ Services started!"
echo "📊 Backend: http://localhost:5000"
echo "🌐 Frontend: http://localhost"
echo ""
echo "Run 'docker-compose logs -f' to see logs"