#!/usr/bin/env python3
"""Flag the source-visible tells of agent-generated UI.

Usage: slop-scan.py PATH [PATH ...]

Scans HTML, CSS, JSX/TSX, Vue, Svelte, Markdown, and JS/TS files (directories
are walked, skipping node_modules, dist, build, and dot-directories). Prints
one line per hit as `file:line  rule  excerpt` and exits 1 when anything is
found, 0 when clean, 2 on usage errors or when no supported file was given.

A line containing `slop-ok:` is skipped. The comment must say which exception
in SKILL.md applies; the scanner only checks that the marker is present.

Rules come in three scopes so code does not drown the report:
- style: raw source lines, for CSS properties, Tailwind classes, and colours.
- text: words a reader sees. Markup text outside <style>/<script>, JSX text
  between tags, string literals in scripts, and Markdown outside code.
- file: whole-file properties of standalone HTML pages.
"""

import os
import re
import sys

MARKUP = {".html", ".htm", ".vue", ".svelte"}
JSX = {".jsx", ".tsx", ".mdx"}
SCRIPT = {".js", ".mjs", ".ts"}
STYLE = {".css", ".scss", ".sass", ".less"}
MARKDOWN = {".md", ".markdown"}
ALL = MARKUP | JSX | SCRIPT | STYLE | MARKDOWN
SKIP_DIRS = {"node_modules", "dist", "build", "out", "coverage", "vendor"}

I = re.IGNORECASE

# (rule id, pattern, flags, scopes). Scopes: "style" lines or "text" segments.
RULES = [
    # Separator glyphs standing in for hierarchy.
    ("middot", r"·|•|&middot;|&#183;|&#xb7;|&bull;|\\u00b7|\\u2022", I, {"style", "text"}),
    ("separator-glyph", r"\S\s+[|/]\s+\S", 0, {"text"}),
    ("em-dash", r"—|&mdash;|&#8212;|\\u2014", 0, {"text"}),
    ("arrow-cta", r"→|›|»|&rarr;|&raquo;|&rsaquo;|\\u2192", 0, {"text"}),
    ("emoji", "[\U0001F300-\U0001FAFF\u2600-\u2712\u2719-\u27BF\u2B50\u2B06\u2194-\u21AA]", 0, {"text"}),
    # Copy formulas.
    ("hype-word", r"\b(reimagined|supercharge\w*|unlock\w*|seamless(ly)?|effortless(ly)?|blazing(ly)?|next-gen|game.?chang\w+|elevate\w*|empower\w*|revolutioni[sz]\w*|world.class|cutting.edge|built for|everything you need|meet the|powerful)\b", I, {"text"}),
    ("staccato-tagline", r"\b[A-Z][a-z]+\.\s+[A-Z][a-z]+\.\s+[A-Z][a-z]+\.", 0, {"text"}),
    ("invented-number", r"\b\d+(\.\d+)?\s?[x×]\s+(faster|better|more|less|cheaper)\b|\b\d+(\.\d+)?\s?%|\b\d+(\.\d+)?[kKmM]\+", 0, {"text"}),
    ("header-count", r"\b[A-Z][A-Za-z ]{2,30}\s\(\d+\)", 0, {"text"}),
    ("meta-disclaimer", r"\b(simulation only|simulated|for illustration|illustrative|stand-in|mock(ed)? data|not the real|design study|this (mockup|prototype|wireframe)|demo only|sample data)\b", I, {"text"}),
    ("placeholder-content", r"lorem ipsum|\bacme\b|\b(john|jane) (doe|smith)\b|\bproject (alpha|phoenix)\b|\bfoo corp\b", I, {"text"}),
    # Visual tells in styles.
    ("eyebrow-uppercase", r"text-transform:\s*uppercase|(class(Name)?=|[\"'`\s])uppercase\b", I, {"style"}),
    ("wide-tracking", r"letter-spacing:\s*((0?\.0[2-9]|0?\.[1-9]\d*|[1-9]\d*(\.\d+)?)(em|rem)|(0?\.[3-9]\d*|[1-9]\d*(\.\d+)?)px)|\btracking-(wide|wider|widest|\[0?\.\d+em\])\b", I, {"style"}),
    ("pill", r"border-radius:\s*(\d{3,}px|9{2,}\w*|calc\(infinity)|^(?=.*\bpx-)(?=.*\brounded-full\b)|\b(badge|pill|chip)s?\b[^\"'`]*[\"'`]|[\"'`\s](badge|pill|chip)s?[\s\"'`]", I, {"style"}),
    ("gradient", r"(linear|radial|conic)-gradient|\bbg-gradient-|\bbg-linear-|background-clip:\s*text|\bbg-clip-text\b", I, {"style"}),
    ("glass-blur", r"backdrop-filter|\bbackdrop-blur|filter:\s*blur|\bblur-(xl|2xl|3xl)\b", I, {"style"}),
    ("big-shadow", r"\bshadow-(lg|xl|2xl)\b|box-shadow:[^;]*\b(1[2-9]|[2-9]\d|\d{3,})px", I, {"style"}),
    ("big-radius", r"\brounded-(xl|2xl|3xl)\b|border-radius:\s*(1[2-9]|[2-9]\d)px|border-radius:\s*(0?\.[89]|[1-9](\.\d+)?)rem", I, {"style"}),
    ("accent-left-border", r"border-left:\s*[2-8]px\s+solid|border-inline-start:\s*[2-8]px\s+solid|\bborder-l-[2-8]\b", I, {"style"}),
    ("ai-palette", r"#(6366f1|4f46e5|818cf8|8b5cf6|7c3aed|a855f7|9333ea|a78bfa|c084fc|d946ef|ec4899|6d28d9|5b21b6)\b|\b(indigo|violet|purple|fuchsia)-\d{2,3}\b", I, {"style"}),
    ("neon-on-dark", r"#(00ff\w{2}|39ff14|0ff\b|00ffff|22d3ee|4ade80|a3e635)\b|\b(cyan|lime|emerald)-(300|400)\b", I, {"style"}),
    ("terracotta", r"#(c2410c|ea580c|b45309|c4622d|d97757|cc785c|c96442|b85c38|a0522d|e07a5f)\b|\b(orange|amber)-(600|700)\b", I, {"style"}),
    ("mono-metadata", r"font-family:[^;]*\bmono|\bfont-mono\b|var\(--mono\)|ui-monospace", I, {"style"}),
    ("flavour-font", r"Space Grotesk|Instrument Serif|Fraunces|Playfair|DM Serif|Syne\b|Clash|Cabinet Grotesk|Outfit|Sora\b|Plus Jakarta|Newsreader|Bricolage", I, {"style", "text"}),
    ("italic-serif", r"font-style:\s*italic|(?<!not-)\bitalic\b", I, {"style"}),
    ("decorative-motion", r"translateY\(\s*-|hover:-?translate-y|hover:scale|scale\(1\.0[1-9]|\banimate-(pulse|ping|bounce|spin)\b|@keyframes\s+\w*(pulse|shimmer|glow|float|shine|gradient)", I, {"style"}),
    ("fake-chrome", r"#(ff5f57|febc2e|28c840|ff5f56|ffbd2e|27c93f)\b|traffic-?light", I, {"style"}),
    ("tiny-text", r"font-size:\s*(\d|10)(\.\d+)?px|\btext-\[(\d|10)(\.\d+)?px\]|font-size:\s*0?\.[0-6]\d*rem", I, {"style"}),
    ("kbd-hint", r"<kbd\b", I, {"style"}),
    ("theme-toggle", r"theme-?toggle|toggleTheme|setTheme\(|data-theme=|<button[^>]*>\s*(Dark|Light) (theme|mode)", I, {"style"}),
]
COMPILED = [(rid, re.compile(p, f), scopes) for rid, p, f, scopes in RULES]

HEX = re.compile(r"#([0-9a-fA-F]{6}|[0-9a-fA-F]{3})\b")
STRING = re.compile(r"\"((?:[^\"\\]|\\.)*)\"|'((?:[^'\\]|\\.)*)'|`((?:[^`\\]|\\.)*)`")
JSX_TEXT = re.compile(r">([^<>{}]+)<")
URL = re.compile(r"https?://\S+|\b[\w.-]+/[\w./-]+\.\w+\b")
INLINE_CODE = re.compile(r"`[^`]*`")
TAG = re.compile(r"<[^>]*>")
INLINE_HTML_CODE = re.compile(r"<(code|kbd|samp)\b[^>]*>.*?</\1>", re.IGNORECASE)
COMMENT = re.compile(r"\s*(//|/\*|\*(\s|/|$)|<!--|\{/\*)")
TEMPLATE_EXPR = re.compile(r"\$\{(?:[^{}]|\{[^{}]*\})*\}")


def warm_paper(hex_value):
    """True for warm off-white backgrounds: the cream-paper default."""
    h = hex_value if len(hex_value) == 6 else "".join(c * 2 for c in hex_value)
    r, g, b = (int(h[i:i + 2], 16) for i in (0, 2, 4))
    return r >= 0xEE and g >= 0xE4 and r - b >= 8 and b <= g <= r


def looks_like_code(s):
    return bool(re.search(r"[;{}()=]|=>|\w\.\w+\(|^\s*(import|export|const|let|var|return)\b", s))


def text_segments(ext, line, state):
    """Return reader-visible text on this line. `state` tracks blocks across lines."""
    if ext in MARKDOWN or ext == ".mdx":
        if line.lstrip().startswith(("```", "~~~")):
            state["fence"] = not state.get("fence")
            return []
        if state.get("fence") or line.lstrip().startswith("|"):
            return []
        line = INLINE_CODE.sub(" ", line)
        if ext in MARKDOWN:
            return [URL.sub(" ", line)]
    if ext in MARKUP:
        low = line.lower()
        for tag in ("style", "script", "pre", "textarea"):
            if re.search(r"<%s\b" % tag, low):
                state[tag] = True
            if "</%s" % tag in low:
                state[tag] = False
                return []
        if state.get("style") or state.get("pre") or state.get("textarea"):
            return []
        line = INLINE_HTML_CODE.sub(" ", line)
        if state.get("script"):
            return [s for s in string_literals(line)]
        stripped = TAG.sub(" ", line)
        stripped = re.sub(r"^[^<]*?>", " ", stripped) if "<" not in stripped and ">" in stripped else stripped
        stripped = re.sub(r"<[^>]*$", " ", stripped)
        return [URL.sub(" ", stripped)]
    if ext in JSX or ext in SCRIPT:
        segs = [m.group(1) for m in JSX_TEXT.finditer(line) if not looks_like_code(m.group(1))]
        return segs + string_literals(line)
    return []


def string_literals(line):
    out = []
    for m in STRING.finditer(line):
        s = next(g for g in m.groups() if g is not None)
        s = TEMPLATE_EXPR.sub(" ", s)
        tokens = s.split()
        # Class lists (Tailwind and friends) are style, not reader text.
        if tokens and sum(1 for t in tokens if re.search(r"[-:\[]", t)) * 2 >= len(tokens):
            continue
        # Skip identifiers, paths, selectors, class lists and imports.
        if " " not in s.strip() and not re.search(r"[·•—→]", s):
            continue
        if re.fullmatch(r"[\w\s:/\-\[\].#%()]+", s) and not re.search(r"[A-Z][a-z]+ [a-z]+", s):
            continue
        out.append(URL.sub(" ", s))
    return out


def scan_file(path):
    ext = os.path.splitext(path)[1].lower()
    try:
        with open(path, encoding="utf-8", errors="replace") as fh:
            lines = fh.read().splitlines()
    except OSError as err:
        print("%s: cannot read (%s)" % (path, err), file=sys.stderr)
        return []
    hits = []
    state = {}
    styled = ext in STYLE | MARKUP | JSX | SCRIPT
    for n, line in enumerate(lines, 1):
        segs = text_segments(ext, line, state)
        if "slop-ok:" in line or (ext not in MARKDOWN and COMMENT.match(line)):
            continue
        seen = set()
        for rid, rx, scopes in COMPILED:
            if "style" in scopes and styled and rx.search(line):
                hits.append((n, rid, line.strip()))
                seen.add(rid)
                continue
            if "text" in scopes and rid not in seen:
                for seg in segs:
                    if rx.search(seg):
                        hits.append((n, rid, seg.strip()))
                        break
        if styled and ext not in MARKDOWN:
            for m in HEX.finditer(line):
                if warm_paper(m.group(1)):
                    hits.append((n, "cream-paper", line.strip()))
                    break
    if ext in {".html", ".htm"}:
        body = "\n".join(lines)
        if re.search(r"<style|style=", body, I):
            if not re.search(r"prefers-color-scheme|color-scheme:\s*light\s+dark", body, I):
                hits.append((1, "no-system-theme", "standalone page ignores prefers-color-scheme"))
            if not re.search(r"max-width|max-inline-size", body, I):
                hits.append((1, "no-max-width", "standalone page has no max-width on content"))
    return hits


def walk(paths):
    for p in paths:
        if os.path.isdir(p):
            for root, dirs, files in os.walk(p):
                dirs[:] = [d for d in dirs if d not in SKIP_DIRS and not d.startswith(".")]
                for f in sorted(files):
                    if os.path.splitext(f)[1].lower() in ALL and not f.endswith(".min.js"):
                        yield os.path.join(root, f)
        elif os.path.isfile(p):
            if os.path.splitext(p)[1].lower() in ALL:
                yield p
            else:
                print("%s: not scanned (unsupported file type)" % p, file=sys.stderr)
        else:
            print("%s: no such file or directory" % p, file=sys.stderr)


def main(argv):
    if len(argv) < 2 or argv[1] in {"-h", "--help"}:
        print(__doc__.strip())
        return 2
    total = 0
    counts = {}
    scanned = 0
    for path in walk(argv[1:]):
        scanned += 1
        for n, rid, excerpt in scan_file(path):
            total += 1
            counts[rid] = counts.get(rid, 0) + 1
            print("%s:%d  %s  %s" % (path, n, rid, excerpt[:140]))
    if total:
        summary = ", ".join("%s %d" % (k, v) for k, v in sorted(counts.items(), key=lambda kv: -kv[1]))
        print("\n%d hits: %s" % (total, summary))
        return 1
    if not scanned:
        print("no supported files scanned", file=sys.stderr)
        return 2
    print("clean (%d files)" % scanned)
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main(sys.argv))
    except BrokenPipeError:
        sys.exit(1)
