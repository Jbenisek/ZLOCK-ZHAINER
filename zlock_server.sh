#!/bin/bash

# ZLOCK Web Server Control Script
# Port: 4243
# Directory: ~/webhosting/zlock/wwwroot

PORT=4243
DIR=~/webhosting/zlock/wwwroot
PID_FILE=/tmp/zlock_server.pid

case "$1" in
    start)
        if [ -f $PID_FILE ]; then
            PID=$(cat $PID_FILE)
            if ps -p $PID > /dev/null 2>&1; then
                echo "Server already running on port $PORT (PID: $PID)"
                exit 1
            fi
        fi
        
        echo "Opening firewall port $PORT..."
        sudo ufw allow $PORT/tcp
        
        echo "Starting ZLOCK web server on port $PORT..."
        cd $DIR
        # Use custom Python server with proper MIME types for GLB files
        nohup python3 zlock_server.py > /tmp/zlock_server.log 2>&1 &
        echo $! > $PID_FILE
        echo "Server started (PID: $!)"
        echo "Access at: http://$(hostname -I | awk '{print $1}'):$PORT/zlock_consensus.html"
        ;;
        
    stop)
        if [ ! -f $PID_FILE ]; then
            echo "No PID file found. Server may not be running."
            exit 1
        fi
        
        PID=$(cat $PID_FILE)
        if ps -p $PID > /dev/null 2>&1; then
            echo "Stopping ZLOCK web server (PID: $PID)..."
            kill $PID
            rm $PID_FILE
            echo "Server stopped."
        else
            echo "Server not running (stale PID file removed)"
            rm $PID_FILE
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
                echo "Server is running (PID: $PID)"
                echo "Access at: http://$(hostname -I | awk '{print $1}'):$PORT/zlock_consensus.html"
            else
                echo "Server is not running (stale PID file)"
            fi
        else
            echo "Server is not running"
        fi
        ;;
        
    *)
        echo "Usage: $0 {start|stop|restart|status}"
        exit 1
        ;;
esac

exit 0
