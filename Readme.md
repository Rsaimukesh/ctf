# Challenge Writeup — Emoji / Variation Selector (Step-by-step) 🧩

## Overview ✅
This challenge hides a flag inside a sequence of Unicode Variation Selector codepoints (U+E0100–U+E01EF). The high-level steps are:
1. Extract the variation selector codepoints from the emoji payload.  
2. Subtract the Variation Selector base (0xE0100) to get raw byte values.  
3. Detect and remove a single-byte XOR obfuscation to reveal the flag.

---

## Where to look 🔎
- Visit the web page for the challenge (sub-route: `/test`) and inspect the page source; the emoji/variation selectors are embedded there.
- The challenge emoji may include a visible glyph (e.g., 🐿) and invisible variation selectors; the visible glyph can be ignored.

---

## Given values (example)
Variation Selectors found in the payload:

```
0xe0146 0xe0151 0xe0165 0xe015c 0xe0164 0xe016b 0xe0163 0xe0120
0xe015d 0xe0123 0xe0164 0xe0158 0xe0159 0xe015e 0xe0157 0xe014f
0xe0153 0xe0120 0xe015e 0xe0156 0xe0165 0xe0163 0xe0159 0xe015e
0xe0157 0xe014f 0xe0158 0xe0123 0xe0162 0xe0123 0xe016d
```

All of these are in the Unicode block U+E0100..U+E01EF (the Variation Selectors block).

---

## Step 1 — Normalize to bytes 🧮
Variation Selectors are high codepoints; convert them into bytes by subtracting the block base (BASE = 0xE0100):

```python
BASE = 0xE0100
vals = [v - BASE for v in codepoints]
# vals -> [70, 81, 101, 92, 100, ...]
```

This yields the byte array:

```
[70, 81, 101, 92, 100, 107, 99, 32,
 93, 35, 100, 88, 89, 94, 87, 79,
 83, 32, 94, 86, 101, 99, 89, 94,
 87, 79, 88, 35, 98, 35, 109]
```

When interpreted directly as ASCII you get:
```
FQe\dkc ]#dXY^WOS ^VecY^WOX#b#m
```
This is not readable plaintext, so another obfuscation layer remains.

---

## Step 2 — Detect XOR obfuscation 🔐
A common second layer is a single-byte XOR. Brute-force all 256 possible XOR keys and look for readable outputs (e.g., strings containing `{` and `}`):

```python
for k in range(256):
    out = bytes(b ^ k for b in vals)
    try:
        s = out.decode()
        if '{' in s and '}' in s:
            print(k, s)
    except:
        pass
```

The bruteforce reveals the key `0x10` and the decoded text:

```
0x10 -> VAuLt{s0M3tHING_C0NFusING_H3r3}
```

---

## Final Step — Decode and verify 🎯
Apply XOR with `0x10` to every byte and join into a string:

```python
decoded = ''.join(chr(b ^ 0x10) for b in vals)
print(decoded)
# -> VAuLt{s0M3tHING_C0NFusING_H3r3}
```

**Final Flag (case-sensitive):**  **VAuLt{s0M3tHING_C0NFusING_H3r3}**

---

## Reproducible commands & tools 🧪
- Use the included `solve.py` to automate these steps. Examples:

```
# Default (uses example codepoints from README)
./solve.py

# Provide hex codepoints explicitly
./solve.py 0xe0146 0xe0151 0xe0165 ...

# Provide a file containing the hex codepoints
./solve.py -f codepoints.txt

# Provide an emoji string (extracts variation selectors automatically)
./solve.py -e "<emoji-string-containing-variation-selectors>"

# Or pipe an emoji-containing file/string into the tool
echo -n "<emoji-string>" | ./solve.py
```

---

## Notes & tips 💡
- Variation Selectors are often invisible in rendered text; inspect the page source or copy-paste into a hex viewer / text editor that shows codepoints.
- If you see unexpected high codepoints, check the Unicode block — they may be encoding byte values via subtraction.
- Single-byte XOR is a common simple obfuscation; look for braces `{}` and typical flag markers when bruteforcing.

---

If you'd like, I can:
- add `tools/decode_variation_selectors.py` to the repo to decode arbitrary inputs, or
- include a quick test (`tools/test_solve.sh`) to validate the solution automatically.

Would you like me to add those? 🚀