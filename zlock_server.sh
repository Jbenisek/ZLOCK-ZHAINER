#!/bin/bash

# ZLOCK Web Server Control Script
# Port: 4243
# Directory: ~/webhosting/zlock/wwwroot

PORT=4243
DIR=~/webhosting/zlock/wwwroot
PID_FILE=/tmp/zlock_server.pid

case "$1" in
    start)
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
        
        echo "Opening firewall port $PORT..."
        sudo ufw allow $PORT/tcp 2>/dev/null
        
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
        if [ ! -f $PID_FILE ]; then
            echo "No PID file found. Checking for running Python servers on port $PORT..."
            # Find and kill any Python process using the port
            PYTHON_PID=$(lsof -ti:$PORT 2>/dev/null)
            if [ ! -z "$PYTHON_PID" ]; then
                echo "Found Python server on port $PORT (PID: $PYTHON_PID)"
                kill -9 $PYTHON_PID
                echo "✅ Server forcefully stopped."
            else
                echo "No server found running on port $PORT"
            fi
            exit 0
        fi
        
        PID=$(cat $PID_FILE)
        echo "Stopping ZLOCK web server (PID: $PID)..."
        
        # Try graceful shutdown first
        if ps -p $PID > /dev/null 2>&1; then
            kill $PID 2>/dev/null
            sleep 1
            
            # Check if still running, force kill if needed
            if ps -p $PID > /dev/null 2>&1; then
                echo "Process still running, forcing shutdown..."
                kill -9 $PID 2>/dev/null
                sleep 1
            fi
        fi
        
        # Also check if port is still in use and clean it up
        PORT_PID=$(lsof -ti:$PORT 2>/dev/null)
        if [ ! -z "$PORT_PID" ]; then
            echo "Cleaning up process still using port $PORT (PID: $PORT_PID)..."
            kill -9 $PORT_PID 2>/dev/null
            sleep 1
        fi
        
        rm -f $PID_FILE
        echo "✅ Server stopped."
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
