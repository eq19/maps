#!/bin/bash
set -e

FT=/home/runner/venv/bin/freqtrade

DATA_FLAG="$DATA_DIR/.data_ready"
TMP_PAIRS="$DATA_DIR/pairs.json"
CONFIG_BACKUP="$EXCHANGE_CONFIG.bak"

echo "[INFO] Mode: $RUN_MODE"
echo "[INFO] Data dir: $DATA_DIR"

# === STEP 1: Generate dynamic pairlist ===
echo "[INFO] Generating dynamic pairlist..."

#$FT test-pairlist \
  #--config "$CONFIG_FILE" \
  #--quote IDR \
  #--print-json > "$TMP_PAIRS"

#PAIRS=$(cat "$TMP_PAIRS")

#if [ -z "$PAIRS" ] || [ "$PAIRS" = "[]" ]; then
  #echo "[ERROR] Pairlist is empty!"
  #exit 1
#fi

PAIRS=gh variable get PAIRS
echo "[INFO] Pairlist:"
echo "$PAIRS"

# === STEP 2: Backup config ===
echo "[INFO] Backing up exchange config..."
cp "$EXCHANGE_CONFIG" "$CONFIG_BACKUP"

# === STEP 3: Inject pair_whitelist ===
echo "[INFO] Injecting pair_whitelist into exchange config..."

jq --argjson pairs "$PAIRS" \
  '.exchange.pair_whitelist = $pairs' \
  "$CONFIG_BACKUP" > "$EXCHANGE_CONFIG"

# === STEP 4: Download data ===
#if [ ! -f "$DATA_FLAG" ]; then
  #echo "[INFO] Downloading data..."
  #$FT download-data \
    #--config "$EXCHANGE_CONFIG" \
    #--userdir "$DATA_DIR" \
    #--timeframes "15m 1h" \
    #--days 30 \
    #--log-file "$DATA_DIR/logs/freqtrade.log
  #touch "$DATA_FLAG"
#else
  #echo "[INFO] Data already downloaded. Skipping..."
#fi

# === STEP 5: Restore config ===
#echo "[INFO] Restoring original exchange config..."
#mv "$CONFIG_BACKUP" "$EXCHANGE_CONFIG"

# === STEP 6: Start trading ===
#echo "[INFO] Starting freqtrade..."

#exec $FT trade -v \
  #--config "$CONFIG_FILE" \
  #--userdir "$DATA_DIR" \
  #--freqaimodel "$FREQAI_MODEL" \
  #--log-file "$DATA_DIR/logs/freqtrade.log"
