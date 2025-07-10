#!/bin/sh

CONFIG_FILE="/opt/xray/config.json"
KEY_DIR="/opt/xray"
PUB_KEY="$KEY_DIR/public.key"
PVT_KEY="$KEY_DIR/private.key"

generate_keys() {
    echo "Generating x25519 keys.."
    
    output=$(/usr/bin/xray x25519)
    private=$(echo "$output" | grep 'Private key:' | cut -d' ' -f3)
    public=$(echo "$output" | grep 'Public key:' | cut -d' ' -f3)

    echo "$private" > "$PVT_KEY"
    echo "$public" > "$PUB_KEY"
    echo "Keys saved to $PVT_KEY and $PUB_KEY"
}

start_xray() {
    echo "Starting xray.."
    /usr/bin/xray run -c $CONFIG_FILE & XRAY_PID=$!
}

restart_xray() {
    echo "Reloading xray config.."
    kill $XRAY_PID
    start_xray
}

if [[ ! -f "$PVT_FILE" || ! -f "$PUB_KEY" ]]; then
    generate_keys
else
    echo "Keys already exist, skipping generation.."
fi

start_xray

inotifywait -m -e modify "$CONFIG_FILE" | while read path action file; do
    restart_xray
done
