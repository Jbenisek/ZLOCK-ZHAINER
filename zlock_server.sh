#!/bin/bash

# ZLOCK Web Server Control Script
# Port: 4243
# Directory: ~/webhosting/zlock/wwwroot

PORT=4243
DIR=~/webhosting/zlock/wwwroot
PID_FILE=/tmp/zlock_server.pid

case "$1" in
    start)
        # Check and install pip3 if not present
        if ! command -v pip3 &> /dev/null; then
            echo "Installing pip3..."
            sudo apt-get update
            sudo apt-get install -y python3-pip
        fi
        
        # Check and install websockets module if not present
        if ! python3 -c "import websockets" 2>/dev/null; then
            echo "Installing websockets module..."
            sudo pip3 install websockets
        fi
        
        # Check if port is already in use BEFORE trying to start
        PORT_PID=$(lsof -ti:$PORT 2>/dev/null)
        if [ ! -z "$PORT_PID" ]; then
            echo "❌ ERROR: Port $PORT is already in use by PID $PORT_PID"
            echo "Killing existing process..."
            sudo kill -9 $PORT_PID
            sleep 1
        fi
        
        if [ -f $PID_FILE ]; then
            PID=$(cat $PID_FILE)
            if ps -p $PID > /dev/null 2>&1; then
                echo "Server already running on port $PORT (PID: $PID)"
                exit 1
            else
                echo "Removing stale PID file..."
                rm $PID_FILE
            fi
        fi
        
        echo "Opening firewall ports $PORT and 8765..."
        sudo ufw allow $PORT/tcp 2>/dev/null
        sudo ufw allow 8765/tcp 2>/dev/null
        
        echo "Starting ZLOCK web server on port $PORT..."
        cd $DIR
        # Use custom Python server with proper MIME types for GLB files
        nohup python3 zlock_server.py > /tmp/zlock_server.log 2>&1 &
        SERVER_PID=$!
        echo $SERVER_PID > $PID_FILE
        
        # Wait 2 seconds and verify it's still running
        sleep 2
        if ps -p $SERVER_PID > /dev/null 2>&1; then
            echo "✅ Server started successfully (PID: $SERVER_PID)"
            echo "Access at: http://$(hostname -I | awk '{print $1}'):$PORT/zlock_consensus.html"
            echo "Logs at: /tmp/zlock_server.log"
        else
            echo "❌ ERROR: Server failed to start. Check logs:"
            cat /tmp/zlock_server.log
            rm $PID_FILE
            exit 1
        fi
        ;;
        
    stop)
        echo "Stopping ZLOCK servers..."
        
        # Kill any process on HTTP port 4243
        PORT_PID=$(sudo lsof -ti:$PORT 2>/dev/null)
        if [ ! -z "$PORT_PID" ]; then
            echo "Killing HTTP server on port $PORT (PID: $PORT_PID)..."
            sudo kill -9 $PORT_PID 2>/dev/null
        fi
        
        # Kill any process on WebSocket port 8765
        WS_PID=$(sudo lsof -ti:8765 2>/dev/null)
        if [ ! -z "$WS_PID" ]; then
            echo "Killing WebSocket server on port 8765 (PID: $WS_PID)..."
            sudo kill -9 $WS_PID 2>/dev/null
        fi
        
        # Also kill by PID file if it exists
        if [ -f $PID_FILE ]; then
            PID=$(cat $PID_FILE)
            if ps -p $PID > /dev/null 2>&1; then
                echo "Killing process from PID file (PID: $PID)..."
                sudo kill -9 $PID 2>/dev/null
            fi
            rm -f $PID_FILE
        fi
        
        # Wait and verify
        sleep 1
        
        # Double-check both ports are free
        STILL_RUNNING=""
        if sudo lsof -ti:$PORT &>/dev/null; then
            STILL_RUNNING="$STILL_RUNNING port $PORT"
        fi
        if sudo lsof -ti:8765 &>/dev/null; then
            STILL_RUNNING="$STILL_RUNNING port 8765"
        fi
        
        if [ -z "$STILL_RUNNING" ]; then
            echo "✅ All servers stopped."
        else
            echo "⚠️  Warning: Still have processes on$STILL_RUNNING"
            echo "Try: sudo lsof -ti:4243,8765 | xargs sudo kill -9"
        fi
        ;;
        
    restart)
        $0 stop
        sleep 2
        $0 start
        ;;
        
    status)
        if [ -f $PID_FILE ]; then
            PID=$(cat $PID_FILE)
            if ps -p $PID > /dev/null 2>&1; then
                echo "✅ Server is running (PID: $PID)"
                echo "Access at: http://$(hostname -I | awk '{print $1}'):$PORT/zlock_consensus.html"
                echo "Logs at: /tmp/zlock_server.log"
            else
                echo "❌ Server is not running (stale PID file)"
                rm -f $PID_FILE
            fi
        else
            PORT_PID=$(lsof -ti:$PORT 2>/dev/null)
            if [ ! -z "$PORT_PID" ]; then
                echo "⚠️  Port $PORT is in use by PID $PORT_PID (no PID file)"
            else
                echo "❌ Server is not running"
            fi
        fi
        ;;
        
    *)
        echo "Usage: $0 {start|stop|restart|status}"
        exit 1
        ;;
esac

exit 0
