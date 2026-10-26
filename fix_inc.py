# По логу сборки находит "'dir/file.h' file not found" и кладёт ссылку на заголовок из нового SDK
# в external/hl2sdk-cs2/public/<dir>/<file.h> (public уже в путях поиска). Код возврата 1 — нечего чинить.
import os, re, sys

sdk = "external/hl2sdk-cs2"
log = open(sys.argv[1], errors="replace").read()
missing = sorted(set(re.findall(r"fatal error: '([^']+)' file not found", log)))
if not missing:
    sys.exit(1)
index = {}
for dp, _, fs in os.walk(sdk):
    for f in fs:
        index.setdefault(f, os.path.join(dp, f))
fixed = 0
for inc in missing:
    found = index.get(os.path.basename(inc))
    if not found:
        print("НЕ НАЙДЕН:", inc)
        continue
    dst = os.path.join(sdk, "public", inc)
    if os.path.exists(dst):
        continue
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    os.symlink(os.path.realpath(found), dst)
    print("link", inc, "->", found)
    fixed += 1
sys.exit(0 if fixed else 1)
