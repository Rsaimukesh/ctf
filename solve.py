s = "🐿󠅦󠅑󠅥󠅜󠅤󠅫󠅣󠄠󠅝󠄣󠅤󠅘󠅙󠅞󠅗󠅏󠅓󠄠󠅞󠅖󠅥󠅣󠅙󠅞󠅗󠅏󠅘󠄣󠅢󠄣󠅭"

# extract VS bytes
data = []
for c in s:
    o = ord(c)
    if 0xE0100 <= o <= 0xE01EF:
        data.append(o - 0xE0100)

raw = bytes(data)
print("[+] Raw bytes:", raw)

print("\n[+] XOR brute force results:\n")
for k in range(256):
    out = bytes(b ^ k for b in raw)
    try:
        txt = out.decode()
        if all(32 <= ord(c) <= 126 for c in txt):
            if "{" in txt or "flag" in txt.lower() or "0x" in txt:
                print(f"key={k}: {txt}")
    except:
        pass
