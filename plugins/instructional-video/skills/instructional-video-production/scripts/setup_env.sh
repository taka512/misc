#!/usr/bin/env bash
# 説明動画制作に必要なツールを確認し、不足していれば導入する。
#
#   setup_env.sh           不足分を導入する
#   setup_env.sh --check   確認のみ（不足があれば終了コード 1）
#
# Python ライブラリは専用の仮想環境に入れる（既定: ~/.cache/instructional-video/venv）。
# 場所は環境変数 VIDEO_VENV で変更できる。導入後は "$VIDEO_VENV/bin/python" を使う。

set -euo pipefail

VENV="${VIDEO_VENV:-${XDG_CACHE_HOME:-$HOME/.cache}/instructional-video/venv}"
PY_PACKAGES=(pillow numpy edge-tts)
CHECK_ONLY=false
[[ "${1:-}" == "--check" ]] && CHECK_ONLY=true

missing=0
ok()   { printf '  [OK]   %s\n' "$1"; }
ng()   { printf '  [不足] %s\n' "$1"; missing=1; }

check_all() {
  missing=0
  echo "== 環境確認 =="
  for cmd in ffmpeg ffprobe; do
    if command -v "$cmd" >/dev/null 2>&1; then ok "$cmd"; else ng "$cmd"; fi
  done
  if [[ -x "$VENV/bin/python" ]] && "$VENV/bin/python" -c 'import PIL, numpy, edge_tts' 2>/dev/null; then
    ok "Python venv ($VENV): pillow numpy edge-tts"
  else
    ng "Python venv ($VENV): pillow numpy edge-tts"
  fi
  if [[ -x "$VENV/bin/edge-tts" ]]; then ok "edge-tts CLI"; else ng "edge-tts CLI"; fi
}

install_ffmpeg() {
  command -v ffmpeg >/dev/null 2>&1 && command -v ffprobe >/dev/null 2>&1 && return
  echo "== FFmpeg を導入 =="
  if command -v brew >/dev/null 2>&1; then
    brew install ffmpeg
  elif command -v apt-get >/dev/null 2>&1; then
    echo "apt で導入します（sudo が必要）"
    sudo apt-get update && sudo apt-get install -y ffmpeg
  else
    echo "FFmpeg を自動導入できません。手動で導入してください: https://ffmpeg.org/download.html" >&2
    exit 1
  fi
}

install_python() {
  "$VENV/bin/python" -c 'import PIL, numpy, edge_tts' 2>/dev/null && return
  echo "== Python 仮想環境を作成: $VENV =="
  mkdir -p "$(dirname "$VENV")"
  if command -v uv >/dev/null 2>&1; then
    [[ -x "$VENV/bin/python" ]] || uv venv -q "$VENV"
    uv pip install -q --python "$VENV/bin/python" "${PY_PACKAGES[@]}"
  else
    [[ -x "$VENV/bin/python" ]] || python3 -m venv "$VENV"
    "$VENV/bin/python" -m pip install -q --upgrade pip
    "$VENV/bin/python" -m pip install -q "${PY_PACKAGES[@]}"
  fi
}

check_all
if $CHECK_ONLY; then
  exit "$missing"
fi
if [[ "$missing" -eq 0 ]]; then
  echo "すべて導入済みです。Python: $VENV/bin/python"
  exit 0
fi

install_ffmpeg
install_python
check_all
if [[ "$missing" -ne 0 ]]; then
  echo "導入に失敗したツールがあります。上の出力を確認してください。" >&2
  exit 1
fi
echo "準備完了。Python: $VENV/bin/python / edge-tts: $VENV/bin/edge-tts"
