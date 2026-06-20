#!/usr/bin/env python3
"""
Instagram контент төлөвлөгч
===========================
Постын санаа, хуваарийг нэг газар хадгалж, удирдах энгийн хэрэгсэл.
Мэдээлэл нь tools/content.json файлд хадгалагдана.

Ашиглах заавар (терминалд):
    python3 tools/content_planner.py add "Постын санаа" 2026-06-25
    python3 tools/content_planner.py list
    python3 tools/content_planner.py done 1
    python3 tools/content_planner.py remove 1
"""

import json
import sys
from datetime import date
from pathlib import Path

DATA_FILE = Path(__file__).parent / "content.json"


def load():
    if DATA_FILE.exists():
        return json.loads(DATA_FILE.read_text(encoding="utf-8"))
    return []


def save(items):
    DATA_FILE.write_text(json.dumps(items, ensure_ascii=False, indent=2), encoding="utf-8")


def add(idea, when=None):
    items = load()
    new_id = (max((it["id"] for it in items), default=0)) + 1
    items.append({
        "id": new_id,
        "idea": idea,
        "date": when or str(date.today()),
        "done": False,
    })
    save(items)
    print(f"✅ Нэмэгдлээ (#{new_id}): {idea} — {when or str(date.today())}")


def list_items():
    items = sorted(load(), key=lambda it: it["date"])
    if not items:
        print("📭 Одоогоор постын санаа алга. 'add' командаар нэмнэ үү.")
        return
    print("\n📅 Контент хуваарь:\n" + "-" * 40)
    for it in items:
        mark = "✔" if it["done"] else "○"
        print(f"  {mark} #{it['id']:<3} {it['date']}  {it['idea']}")
    print("-" * 40)
    pending = sum(1 for it in items if not it["done"])
    print(f"  Нийт: {len(items)} | Үлдсэн: {pending}\n")


def mark_done(item_id):
    items = load()
    for it in items:
        if it["id"] == item_id:
            it["done"] = True
            save(items)
            print(f"✔ #{item_id} дууссан гэж тэмдэглэлээ.")
            return
    print(f"⚠ #{item_id} олдсонгүй.")


def remove(item_id):
    items = load()
    new_items = [it for it in items if it["id"] != item_id]
    if len(new_items) == len(items):
        print(f"⚠ #{item_id} олдсонгүй.")
        return
    save(new_items)
    print(f"🗑 #{item_id} устгалаа.")


def usage():
    print(__doc__)


def main():
    args = sys.argv[1:]
    if not args:
        usage()
        return
    cmd = args[0]
    if cmd == "add" and len(args) >= 2:
        add(args[1], args[2] if len(args) >= 3 else None)
    elif cmd == "list":
        list_items()
    elif cmd == "done" and len(args) >= 2:
        mark_done(int(args[1]))
    elif cmd == "remove" and len(args) >= 2:
        remove(int(args[1]))
    else:
        usage()


if __name__ == "__main__":
    main()
