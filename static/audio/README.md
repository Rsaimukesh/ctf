# Challenge Writeup — Emoji Variation Selector Decoding 🧩

## Summary ✅
This writeup documents how the challenge was solved: a sequence of Unicode Variation Selector codepoints (U+E0100–U+E01EF) was used to hide a flag. By normalizing the values, interpreting them as bytes, and applying a single-byte XOR, the final flag was recovered.

---

## Files / Artifacts
- Source of the values: a list of Variation Selector codepoints found in the payload (see 'Variation Selectors' below).
- Decoding work performed with small Python snippets (included below).

---

## Steps to reproduce 🔁

1) Given the Variation Selector codepoints (example):

```
0xe0146 0xe0151 0xe0165 0xe015c 0xe0164 0xe016b 0xe0163 0xe0120
0xe015d 0xe0123 0xe0164 0xe0158 0xe0159 0xe015e 0xe0157 0xe014f
0xe0153 0xe0120 0xe015e 0xe0156 0xe0165 0xe0163 0xe0159 0xe015e
0xe0157 0xe014f 0xe0158 0xe0123 0xe0162 0xe0123 0xe016d
```

2) Convert them into raw byte values by subtracting the Variation Selector base (BASE = 0xE0100):

```python
codepoints = [0xe0146, 0xe0151, 0xe0165, ...]
BASE = 0xE0100
vals = [v - BASE for v in codepoints]
print(vals)
# -> [70, 81, 101, 92, 100, ...]
```

3) Inspect ASCII interpretation — it's not plaintext:

```python
print(''.join(chr(b) for b in vals))
# -> FQe\dkc ]#dXY^WO S ^VecY^WOX#b#m
```

4) Try single-byte XOR brute-force (common obfuscation):

```python
for k in range(256):
    out = bytes(b ^ k for b in vals)
    try:
        s = out.decode()
        if '{' in s and '}' in s:  # look for flag markers
            print(k, s)
    except Exception:
        pass
# -> prints: 16 VAuLt{s0M3tHING_C0NFusING_H3r3}
```

5) Apply the found key (0x10) to decode the flag:

```python
decoded = ''.join(chr(b ^ 0x10) for b in vals)
print(decoded)
# -> VAuLt{s0M3tHING_C0NFusING_H3r3}
```

---

## Explanation & Notes 💡
- The values were Variation Selectors (U+E0100–U+E01EF). Subtracting the `BASE = 0xE0100` yields small integers (0..255) that represent obfuscated bytes.
- The presence of `'{...}'` is a helpful hint that the decoded text is a flag; brute-forcing single-byte XOR is a common technique.
- The XOR key was `0x10` (decimal 16), which produced the readable flag.

---

## Final Flag 🏁
**VAuLt{s0M3tHING_C0NFusING_H3r3}**

---

## Reproducible one-liner
You can reproduce the entire process in a short Python snippet:

```python
codepoints = [0xe0146,0xe0151,0xe0165,0xe015c,0xe0164,0xe016b,0xe0163,0xe0120,0xe015d,0xe0123,0xe0164,0xe0158,0xe0159,0xe015e,0xe0157,0xe014f,0xe0153,0xe0120,0xe015e,0xe0156,0xe0165,0xe0163,0xe0159,0xe015e,0xe0157,0xe014f,0xe0158,0xe0123,0xe0162,0xe0123,0xe016d]
BASE = 0xE0100
vals = [v - BASE for v in codepoints]
flag = ''.join(chr(b ^ 0x10) for b in vals)
print(flag)
```

---

## Credits & Footnote ✍️
- Author: challenge solver / writeup by you
- Tip: when encountering unusual Unicode codepoints, consider the Unicode blocks they belong to — they often hide numeric offsets that can be converted to meaningful bytes.

If you want, I can also add a short script `tools/decode_variation_selectors.py` to run automatically and include test vectors. Want me to add that? 🚀