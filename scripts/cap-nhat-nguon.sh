#!/usr/bin/env bash
# Lấy bản mới nhất của 41 skill trong tong-hop/ từ repo gốc (MIT, Corey Haines).
# KHÔNG đụng tới cua-doan/. Xem `git diff` trước khi commit.
set -euo pipefail

GOC="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
NGUON="https://github.com/coreyhaines31/marketingskills.git"
TAM="$(mktemp -d)"
trap 'rm -rf "$TAM"' EXIT

CHON=(offers pricing copywriting copy-editing content-strategy emails cold-email
      lead-magnets launch social video community-marketing marketing-psychology
      customer-research competitors competitor-profiling cro ab-testing analytics
      ads ad-creative marketing-plan marketing-ideas marketing-loops marketing-council
      referrals influencer-marketing co-marketing public-relations events onboarding
      sales-enablement prospecting seo-audit ai-seo image free-tools product-marketing
      attribution popups churn-prevention)

echo "→ tải bản mới nhất từ $NGUON"
git clone --depth 1 -q "$NGUON" "$TAM/nguon"

cd "$TAM/nguon"
echo "   phiên bản: $(python3 -c "import json;print(json.load(open('.claude-plugin/marketplace.json'))['metadata']['version'])" 2>/dev/null || echo '?')"

thieu=0
for s in "${CHON[@]}"; do
  if [ ! -d "$TAM/nguon/skills/$s" ]; then
    echo "   ⚠️  nguồn KHÔNG CÒN skill '$s' — bỏ qua, giữ bản cũ"
    thieu=$((thieu+1)); continue
  fi
  rm -rf "$GOC/tong-hop/skills/$s"
  cp -R "$TAM/nguon/skills/$s" "$GOC/tong-hop/skills/"
done

cp "$TAM/nguon/LICENSE" "$GOC/tong-hop/LICENSE-marketingskills"
find "$GOC/tong-hop/skills" -type d -name evals -exec rm -rf {} + 2>/dev/null || true

echo "✅ xong — $(( ${#CHON[@]} - thieu ))/${#CHON[@]} skill đã cập nhật"
echo "   soát lại:  git -C \"$GOC\" diff --stat"
