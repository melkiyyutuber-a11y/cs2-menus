# Подгоняет новый s2sdk под старые пути в AMBuildScript Pisex:
# .cpp, которых нет на прежнем месте, ищутся по имени (симлинк), иначе — пустая заглушка.
import os, re

sdk = "external/hl2sdk-cs2"
src = open("AMBuildScript").read()
index = {}
for dp, _, fs in os.walk(sdk):
    for f in fs:
        index.setdefault(f, os.path.join(dp, f))
for m in re.finditer(r"os\.path\.join\(sdk\['path'\],\s*((?:'[^']+',?\s*)+)\)", src):
    parts = re.findall(r"'([^']+)'", m.group(1))
    want = os.path.join(sdk, *parts)
    if not want.endswith((".cpp", ".cc")) or os.path.exists(want):
        continue
    os.makedirs(os.path.dirname(want), exist_ok=True)
    found = index.get(parts[-1])
    if found:
        os.symlink(os.path.realpath(found), want)
        print("link", want, "->", found)
    else:
        open(want, "w").write("// stub\n")
        print("stub", want)
