#!/usr/bin/env bash
# Convert manim-rendered PNG frames into a looping, transparent-background GIF.
#
# Usage:
#   ./make_gif.sh <frames_dir> [output.gif]
#
# Why PNG frames instead of mp4?
#   H.264/mp4 has no usable alpha channel, so a transparent background
#   would be lost when converting mp4 -> gif. Rendering --format png keeps
#   per-frame alpha, which palettegen/paletteuse preserve below.
#
# Optional mp4 preview (opaque background):
#   ffmpeg -y -framerate 30 -pattern_type glob -i "<dir>/*.png" \
#     -vf "scale=1584:396" -c:v libx264 -pix_fmt yuv420p preview.mp4

set -euo pipefail

if [[ $# -lt 1 ]]; then
  echo "usage: $0 <frames_dir> [output.gif]" >&2
  exit 1
fi

FRAMES_DIR="$1"
OUT="${2:-assets/herb-banner.gif}"
FPS=30

ffmpeg -y -framerate "$FPS" -pattern_type glob -i "$FRAMES_DIR/*.png" \
  -vf "fps=${FPS},split[a][b];[a]palettegen=reserve_transparent=1:max_colors=64[p];[b][p]paletteuse=dither=none:alpha_threshold=127" \
  -loop 0 "$OUT"

echo "wrote $OUT ($(du -h "$OUT" | cut -f1))"
