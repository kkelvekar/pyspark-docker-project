#!/bin/bash
# This script will execute the Python debugger and pass along all arguments
# that it receives (like the name of your script, app.py).
exec python -m debugpy --listen 0.0.0.0:5678 --wait-for-client "$@"