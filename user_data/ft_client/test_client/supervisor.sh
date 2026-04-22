#!/bin/bash
set -e

# === FIX: Load environment ===
source /home/runner/venv/bin/activate

CONFIG_SRC="$EXCHANGE_CONFIG"
DOWNLOAD_CFG="$DATA_DIR/download_config.json"
DATA_FLAG="$DATA_DIR/.data_ready"

echo "[INFO] Mode: $RUN_MODE"
echo "[INFO] Data dir: $DATA_DIR"

echo "[INFO] Using freqtrade: $(which freqtrade)"

# === Generate config ===
jq '{exchange:{name:.exchange.name},pair_whitelist:((.exchange.core_whitelist//[])+(.exchange.pair_reserved//[])|unique)}' "$CONFIG_SRC" > "$DOWNLOAD_CFG"

if [ ! -s "$DOWNLOAD_CFG" ]; then
  echo "[ERROR] download_config.json is empty!"
  exit 1
fi

# === Download data ===
if [ ! -f "$DATA_FLAG" ]; then
  echo "[INFO] Downloading data..."
  freqtrade download-data \
    --config "$DOWNLOAD_CFG" \
    --userdir "$DATA_DIR" \
    --timeframes "15m 1h" \
    --days 30
  touch "$DATA_FLAG"
else
  echo "[INFO] Data already downloaded."
fi

# === Start trading ===
exec freqtrade trade -v \
  --config "$CONFIG_FILE" \
  --userdir "$DATA_DIR" \
  --freqaimodel "$FREQAI_MODEL" \
  --log-file "$DATA_DIR/logs/freqtrade.log"
