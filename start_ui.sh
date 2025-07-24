#!/bin/bash

echo "🚀 Starting AI Test Agent Web UI..."
echo "This will start both backend and frontend servers"
echo ""

# Make scripts executable
chmod +x start_backend.sh
chmod +x start_frontend.sh

# Check if tmux is available for running both servers
if command -v tmux &> /dev/null; then
    echo "📱 Using tmux to run both servers..."
    
    # Create a new tmux session
    tmux new-session -d -s ai-test-agent
    
    # Split the window
    tmux split-window -h
    
    # Run backend in left pane
    tmux send-keys -t ai-test-agent:0.0 './start_backend.sh' Enter
    
    # Run frontend in right pane  
    tmux send-keys -t ai-test-agent:0.1 'sleep 5 && ./start_frontend.sh' Enter
    
    # Attach to the session
    echo "✨ Both servers starting in tmux session 'ai-test-agent'"
    echo "📖 Use 'tmux attach -t ai-test-agent' to view both servers"
    echo "📖 Use Ctrl+B then D to detach from tmux"
    echo "📖 Use 'tmux kill-session -t ai-test-agent' to stop both servers"
    echo ""
    echo "🌐 Frontend: http://localhost:3000"
    echo "🔗 Backend API: http://localhost:8000"
    echo "📖 API Docs: http://localhost:8000/docs"
    echo ""
    
    tmux attach -t ai-test-agent
    
elif command -v gnome-terminal &> /dev/null; then
    echo "📱 Using gnome-terminal to run both servers..."
    
    # Start backend in new terminal
    gnome-terminal --title="AI Test Agent Backend" -- bash -c './start_backend.sh; exec bash'
    
    # Wait a moment for backend to start
    sleep 3
    
    # Start frontend in another terminal
    gnome-terminal --title="AI Test Agent Frontend" -- bash -c './start_frontend.sh; exec bash'
    
    echo "✨ Both servers starting in separate terminals"
    echo "🌐 Frontend: http://localhost:3000"
    echo "🔗 Backend API: http://localhost:8000"
    echo ""

elif command -v xterm &> /dev/null; then
    echo "📱 Using xterm to run both servers..."
    
    # Start backend in new terminal
    xterm -title "AI Test Agent Backend" -e './start_backend.sh' &
    
    # Wait a moment for backend to start
    sleep 3
    
    # Start frontend in another terminal
    xterm -title "AI Test Agent Frontend" -e './start_frontend.sh' &
    
    echo "✨ Both servers starting in separate terminals"
    echo "🌐 Frontend: http://localhost:3000"
    echo "🔗 Backend API: http://localhost:8000"
    echo ""

else
    echo "📱 No terminal multiplexer found. Please run manually:"
    echo ""
    echo "Terminal 1: ./start_backend.sh"
    echo "Terminal 2: ./start_frontend.sh"
    echo ""
    echo "Or install tmux: sudo apt install tmux (Linux) / brew install tmux (macOS)"
    echo ""
    
    # Start backend in background
    echo "🔧 Starting backend in background..."
    ./start_backend.sh &
    BACKEND_PID=$!
    
    # Wait for backend to start
    sleep 5
    
    # Start frontend
    echo "🌐 Starting frontend..."
    ./start_frontend.sh
    
    # Clean up background process when frontend exits
    kill $BACKEND_PID 2>/dev/null
fi