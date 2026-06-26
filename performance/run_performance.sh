#!/bin/bash

# 用法：sh run_perf.sh locustfile_httpbingo.py
# 或者：sh run_perf.sh locustfile_ecommerce.py 100 10 60s

SCRIPT_FILE="${1:-locustfile_httpbingo.py}"   # 第1个参数，默认值 locustfile_httpbingo.py
USERS="${2:-50}"                                # 第2个参数，默认值 50
RATE="${3:-5}"                                  # 第3个参数，默认值 5
TIME="${4:-120s}"                               # 第4个参数，默认值 120s

SCRIPT_NAME=$(basename "$SCRIPT_FILE" .py)

mkdir -p ./reports

locust -f "$SCRIPT_FILE" \
  --headless -u "$USERS" -r "$RATE" -t "$TIME" \
  --html="./reports/${SCRIPT_NAME}_$(date +%Y%m%d_%H%M%S)_u${USERS}_r${RATE}_t${TIME}.html"