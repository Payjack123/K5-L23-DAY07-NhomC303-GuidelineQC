"""Sinh JSON Ä‘á»ƒ dÃ¡n vÃ o CVAT (Project -> Labels -> tab Raw) tá»« submission/taxonomy.json.

    python scripts/make_cvat_labels.py

Ghi ra cvat/labels_generated.json vÃ  in ra mÃ n hÃ¬nh. Má»—i láº§n Ä‘á»•i taxonomy.json thÃ¬ cháº¡y láº¡i
vÃ  dÃ¡n láº¡i vÃ o CVAT Ä‘á»ƒ má»i ngÆ°á»i dÃ¹ng Ä‘Ãºng cÃ¹ng má»™t bá»™ lá»›p/thuá»™c tÃ­nh.
"""
from __future__ import annotations

import argparse
import json

from common import ROOT, final_taxonomy_path, load_taxonomy, rel

COLORS = ["#e6194b", "#3cb44b", "#4363d8", "#f58231", "#911eb4", "#46c8c8", "#f032e6", "#9a6324",
          "#808000", "#008080", "#800000", "#000075"]


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--final", action="store_true", help="Sinh cáº¥u hÃ¬nh cho taxonomy sau calibration.")
    args = parser.parse_args()
    tax = load_taxonomy(final_taxonomy_path()) if args.final else load_taxonomy()
    labels = []
    for i, name in enumerate(tax.classes):
        attrs = []
        if name != tax.ignore:
            for a in tax.attrs.values():
                attrs.append({
                    "name": a["name"],
                    "mutable": False,
                    "input_type": a["type"],
                    "default_value": str(a.get("default", "")),
                    "values": [str(v) for v in a.get("values", [])] if a["type"] == "select" else ["false", "true"],
                })
        labels.append({"name": name, "color": "#808080" if name == tax.ignore else COLORS[i % len(COLORS)],
                       "attributes": attrs})
    text = json.dumps(labels, ensure_ascii=False, indent=2)
    out = ROOT / "cvat" / ("labels_final.json" if args.final else "labels_generated.json")
    out.parent.mkdir(exist_ok=True)
    out.write_text(text + "\n", encoding="utf8")
    print(text)
    print(f"\n# ÄÃ£ ghi {rel(out)} (taxonomy {tax.version}). DÃ¡n ná»™i dung vÃ o CVAT: Project -> Labels -> Raw -> Done.")


if __name__ == "__main__":
    main()

