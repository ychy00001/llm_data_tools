#!/bin/bash
CURRENT_DIR=$(cd $(dirname $0); pwd)
$CURRENT_DIR/venv/bin/pip install -r requirements.txt
nohup $CURRENT_DIR/venv/bin/python $CURRENT_DIR/app.py &
