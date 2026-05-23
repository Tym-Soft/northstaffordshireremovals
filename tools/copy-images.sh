#!/usr/bin/env bash
# One-shot: copy source images from ~/Desktop/Moving Photos for websites/
# into images/ with descriptive SEO names, resize to 1600px max, compress
# to ~70 quality so every file lands ≤200 KB (audit Rule 21).

set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
SRC="/Users/markwillis/Desktop/Moving Photos for websites"
DST="$ROOT/images"
mkdir -p "$DST"

declare -a MAP=(
  "Packing Eletronics Safely.jpg|packing-electronics-safely-removal.jpg"
  "pexels-anete-lusina-4792548.jpg|moving-day-packing-checklist.jpg"
  "pexels-blue-bird-7210487.jpg|couple-unpacking-boxes-new-home.jpg"
  "pexels-blue-bird-7217766.jpg|smiling-woman-with-dog-moving-day.jpg"
  "pexels-blue-bird-7217807.jpg|woman-packing-bedroom-floor.jpg"
  "pexels-blue-bird-7217807 (1).jpg|woman-packing-bedroom-floor-alt.jpg"
  "pexels-blue-bird-7217903.jpg|couple-wrapping-furniture-protection.jpg"
  "pexels-cottonbro-studio-4554234.jpg|packing-kitchenware-cardboard-box.jpg"
  "pexels-cottonbro-studio-4554234 (1).jpg|packing-kitchenware-cardboard-box-alt.jpg"
  "pexels-cottonbro-studio-4554237.jpg|labelling-moving-boxes-kitchen.jpg"
  "pexels-cottonbro-studio-4554242.jpg|loading-cardboard-removal-boxes.jpg"
  "pexels-cottonbro-studio-4554351.jpg|sealing-cardboard-moving-box.jpg"
  "pexels-cottonbro-studio-4554353.jpg|couple-packing-living-room.jpg"
  "pexels-cottonbro-studio-4554384.jpg|wrapping-fragile-items-paper.jpg"
  "pexels-cottonbro-studio-4554387.jpg|packing-glassware-bubble-wrap.jpg"
  "pexels-cottonbro-studio-4554415.jpg|unpacking-bedroom-boxes.jpg"
  "pexels-cottonbro-studio-4568710.jpg|moving-day-living-room-boxes.jpg"
  "pexels-cottonbro-studio-4569369.jpg|man-carrying-cardboard-box-home.jpg"
  "pexels-cottonbro-studio-6063692.jpg|couple-new-home-cardboard-box.jpg"
  "pexels-karolina-grabowska-4498142.jpg|hands-holding-cardboard-moving-box.jpg"
  "pexels-karolina-grabowska-4506260.jpg|man-yellow-tshirt-with-moving-box.jpg"
  "pexels-karolina-grabowska-4506262.jpg|labelling-kitchen-box-marker.jpg"
  "pexels-ketut-subiyanto-4246059.jpg|kitchen-removal-box-bedroom-stack.jpg"
  "pexels-ketut-subiyanto-4246091.jpg|stacked-cardboard-boxes-empty-room.jpg"
  "pexels-ketut-subiyanto-4246117.jpg|woman-unpacking-large-cardboard-box.jpg"
  "pexels-ketut-subiyanto-4246120.jpg|unpacking-cardboard-removal-boxes.jpg"
  "pexels-ketut-subiyanto-4246242.jpg|packing-table-removal-day.jpg"
  "pexels-ketut-subiyanto-4247728.jpg|sealing-cardboard-removal-box-floor.jpg"
  "pexels-ketut-subiyanto-4247759.jpg|writing-moving-inventory-list.jpg"
  "pexels-kindel-media-7578899.jpg|estate-agent-handing-house-keys.jpg"
  "pexels-kindel-media-7578984.jpg|holding-house-keys-new-home.jpg"
  "pexels-mart-production-7414957.jpg|family-moving-house-boxes-celebration.jpg"
  "pexels-mart-production-7415049.jpg|family-celebrating-keys-new-home.jpg"
  "pexels-rodnae-productions-7464367.jpg|couple-with-removal-boxes-new-home.jpg"
  "pexels-rodnae-productions-7464463.jpg|woman-unpacking-kitchenware.jpg"
  "pexels-rodnae-productions-7464701.jpg|man-packing-living-room-cardboard-box.jpg"
  "pexels-ron-lach-9594415.jpg|opening-removal-box-room.jpg"
  "pexels-ron-lach-9853466.jpg|couple-unpacking-photo-frames-memories.jpg"
  "pexels-shvets-production-7203699.jpg|stacked-removal-boxes-hallway.jpg"
  "pexels-shvets-production-7203772.jpg|man-stacking-cardboard-removal-boxes.jpg"
  "pexels-shvets-production-7203779.jpg|woman-checking-removal-boxes.jpg"
  "pexels-shvets-production-7203785.jpg|empty-room-moving-boxes-ready.jpg"
  "pexels-timur-weber-9186011.jpg|woman-folding-clothes-suitcase-packing.jpg"
  "shutterstock_1378547738.jpg|professional-removal-team-lorry.jpg"
  "shutterstock_1443249299.jpg|removal-lorry-loading-furniture.jpg"
  "shutterstock_180958814.jpg|cardboard-boxes-storage-warehouse.jpg"
)

# Also pull the "house purchase.jpg" from Pictures if it exists
EXTRA_SRC="/Users/markwillis/Pictures/house purchase.jpg"

count=0
for entry in "${MAP[@]}"; do
  src_name="${entry%%|*}"
  dst_name="${entry##*|}"
  src_path="$SRC/$src_name"
  dst_path="$DST/$dst_name"
  if [[ -f "$src_path" ]]; then
    cp "$src_path" "$dst_path"
    # Resize to max 1600px on long edge, then re-encode at quality 60.
    sips --resampleHeightWidthMax 1600 "$dst_path" >/dev/null 2>&1 || true
    sips -s formatOptions 60 "$dst_path" >/dev/null 2>&1 || true
    # If still > 200K, drop quality further
    sz=$(stat -f%z "$dst_path")
    if (( sz > 200*1024 )); then
      sips -s formatOptions 45 "$dst_path" >/dev/null 2>&1 || true
    fi
    sz=$(stat -f%z "$dst_path")
    if (( sz > 200*1024 )); then
      sips --resampleHeightWidthMax 1200 "$dst_path" >/dev/null 2>&1 || true
      sips -s formatOptions 50 "$dst_path" >/dev/null 2>&1 || true
    fi
    count=$((count+1))
  else
    echo "MISSING: $src_path"
  fi
done

if [[ -f "$EXTRA_SRC" ]]; then
  cp "$EXTRA_SRC" "$DST/keys-handover-house-purchase.jpg"
  sips --resampleHeightWidthMax 1600 "$DST/keys-handover-house-purchase.jpg" >/dev/null 2>&1 || true
  sips -s formatOptions 60 "$DST/keys-handover-house-purchase.jpg" >/dev/null 2>&1 || true
  count=$((count+1))
fi

echo "Copied + compressed $count images to $DST"
echo "---"
ls -lhS "$DST" | head -8
echo "---"
# Verify all ≤200K
big=$(find "$DST" -type f -size +200k | wc -l | tr -d ' ')
echo "Images over 200KB after compression: $big"
if [[ "$big" != "0" ]]; then
  find "$DST" -type f -size +200k -exec ls -lh {} \;
fi
