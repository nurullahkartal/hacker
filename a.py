#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Hacker Taklidi Son Rötuş Betiği
- manifest.json içindeki "2026'den" ifadesini "2026'dan" olarak düzeltir.
- index.htm içindeki agr.js ve link.js script etiketlerini siler.
- Mail adresine (denem@deneme.com) dokunmaz.
"""

import os
import json
import re
import shutil

def backup_file(filepath):
    """Dosyanın yedeğini .bak uzantısıyla al."""
    backup_path = filepath + ".bak"
    if not os.path.exists(backup_path):
        shutil.copy2(filepath, backup_path)
        print(f"✅ Yedek alındı: {backup_path}")
    else:
        print(f"⚠️ Yedek zaten var: {backup_path}")

def fix_manifest(base_dir):
    """manifest.json dosyasında '2026'den' -> '2026'dan' düzeltmesi yapar."""
    manifest_path = os.path.join(base_dir, "manifest.json")
    if not os.path.exists(manifest_path):
        print("❌ manifest.json bulunamadı.")
        return

    backup_file(manifest_path)

    with open(manifest_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    if "name" in data and "2026'den" in data["name"]:
        data["name"] = data["name"].replace("2026'den", "2026'dan")
        with open(manifest_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print("✅ manifest.json düzeltildi: '2026'den' -> '2026'dan'")
    else:
        print("ℹ️ manifest.json zaten düzgün veya ifade bulunamadı.")

def remove_scripts_from_index(base_dir):
    """index.htm içindeki agr.js ve link.js script satırlarını siler."""
    index_path = os.path.join(base_dir, "index.htm")
    if not os.path.exists(index_path):
        print("❌ index.htm bulunamadı.")
        return

    backup_file(index_path)

    with open(index_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Kaldırılacak iki script satırını regex ile bul (boşluklara duyarsız)
    # agr.js satırı
    pattern_agr = r'\s*<script\s+async=""\s+defer=""\s+data-country="true"\s+data-device="true"\s+data-referrer="true"\s+data-site-id="[^"]*"\s+src="agr.js">\s*</script>\s*'
    # link.js satırı
    pattern_link = r'\s*<script\s+async=""\s+defer=""\s+src="static/link.js">\s*</script>\s*'

    content = re.sub(pattern_agr, '', content, flags=re.IGNORECASE)
    content = re.sub(pattern_link, '', content, flags=re.IGNORECASE)

    with open(index_path, 'w', encoding='utf-8') as f:
        f.write(content)

    print("✅ index.htm içinden agr.js ve link.js script etiketleri kaldırıldı.")

def main():
    # Betik hangi klasörde çalışıyorsa orayı ana dizin kabul et
    base_dir = os.getcwd()
    print(f"📁 İşlem klasörü: {base_dir}")

    fix_manifest(base_dir)
    remove_scripts_from_index(base_dir)

    print("\n🎉 Tüm işlemler tamam. Şimdi siteyi sunucuya yükleyebilirsin.")

if __name__ == "__main__":
    main()