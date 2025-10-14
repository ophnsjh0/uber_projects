#!/bin/bash  # 또는 #!/bin/zsh

PORT=$(ls -t /dev/tty.usb* 2>/dev/null | head -n 1)

if [[ -z "$PORT" ]]; then
  echo "❌ No USB serial device found."
  exit 1
fi

echo "✅ Connecting to $PORT..."
sleep 1
exec screen "$PORT" 9600
