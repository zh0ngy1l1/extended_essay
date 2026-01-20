import re
from pathlib import Path

# --- Directories ---
input_dir = Path("ggb_exports")
output_dir = Path("src")
output_dir.mkdir(exist_ok=True)

# --- Find exactly one .txt file ---
txt_files = list(input_dir.glob("*.txt"))
if len(txt_files) == 0:
    raise FileNotFoundError(f"No .txt files found in {input_dir}")
elif len(txt_files) > 1:
    raise FileExistsError(f"Multiple .txt files found in {input_dir}: {txt_files}")

input_file = txt_files[0]
output_file = output_dir / (input_file.stem + ".tex")

# --- Read ---
content = input_file.read_text(encoding="utf-8")

# --- Extract tikzpicture ---
m = re.search(r"\\begin{tikzpicture}.*?\\end{tikzpicture}", content, flags=re.DOTALL)
if not m:
    raise ValueError("No tikzpicture environment found.")
tikz = m.group(0)

# Delete original
input_file.unlink()

XMIN, XMAX = -10.82, 10.82
YMIN, YMAX = -7.41, 7.41

# ----------------------------------------------------
# Remove \clip(...) ...; (pgfplots axis clipping will handle this)
# ----------------------------------------------------
tikz = re.sub(r"\\clip\s*\(.*?\)\s*rectangle\s*\(.*?\)\s*;", "", tikz, flags=re.DOTALL)

# --- Replace fill and color with black ---
tikz = re.sub(r"fill\s*=\s*[^,\]]+", "fill=black", tikz)
tikz = re.sub(r"color\s*=\s*[^,\]]+", "color=black", tikz)

# --- Remove line width=... and redundant color=black ---
def clean_options(m):
    parts = [p.strip() for p in m.group(1).split(",")]
    parts = [p for p in parts if not p.startswith("line width=") and p != "color=black"]
    return "[" + ", ".join(parts) + "]" if parts else ""

tikz = re.sub(r"\[(.*?)\]", clean_options, tikz)

# --- Adjust circle size: only 2.5pt → 2pt ---
tikz = re.sub(r"circle\s*\(\s*2\.5pt\s*\)", "circle (2pt)", tikz)

# --- Remove scriptsize ---
tikz = re.sub(r"\\begin{scriptsize}", "", tikz)
tikz = re.sub(r"\\end{scriptsize}", "", tikz)

# --- Remove x=1cm,y=1cm ---
tikz = re.sub(r"x\s*=\s*1cm\s*,?", "", tikz)
tikz = re.sub(r"y\s*=\s*1cm\s*,?", "", tikz)

# ----------------------------------------------------
# Replace dash pattern with dashed (preserving other options)
# ----------------------------------------------------
def replace_dash(match):
    opts = match.group(1)
    parts = [p.strip() for p in opts.split(",") if "dash pattern=" not in p]
    parts.append("dashed")
    return r"\draw [" + ", ".join(parts) + "]"

tikz = re.sub(r"\\draw\s*\[([^\]]*dash pattern=[^\]]*)\]", replace_dash, tikz)

# Cleanup commas
tikz = re.sub(r",\s*,", ",", tikz)
tikz = re.sub(r",\s*\]", "]", tikz)

# ----------------------------------------------------
# Wrap node labels in math mode: node {...} → node {$...$}
# ----------------------------------------------------
tikz = re.sub(
    r"node\s*{\s*([^${}][^}]*)\s*}",
    r"node {$\1$}",
    tikz
)

def convert_shifted_param_arc(m):
    draw_opts = ((m.group("draw_opts") or "") + (m.group("draw_opts_tail") or "")).strip()
    sx, sy = m.group("sx").strip(), m.group("sy").strip()
    plot_opts = (m.group("plot_opts") or "").strip()
    R = m.group("R").strip()

    parts = [p.strip() for p in draw_opts.split(",") if p.strip()]
    # shift is already removed by construction; just de-dupe
    merged = parts + [p.strip() for p in plot_opts.split(",") if p.strip()]

    def norm(s): return re.sub(r"\s+", "", s)
    seen, final = set(), []
    for p in merged:
        k = norm(p)
        if k not in seen:
            seen.add(k)
            final.append(p)

    final_opts = ", ".join(final)

    return (
        rf"\addplot[{final_opts}] "
        rf"({{{sx} + {R}*cos(\t r)}},"
        rf"{{{sy} + {R}*sin(\t r)}});"
    )

tikz = re.sub(
    r"""
    \\draw\s*\[
        (?P<draw_opts>[^\]]*?)
        shift=\{\(\s*(?P<sx>[^,]+)\s*,\s*(?P<sy>[^\)]+)\s*\)\}
        (?P<draw_opts_tail>[^\]]*?)
    \]\s*
    plot\s*\[
        (?P<plot_opts>[^\]]*?)
    \]\s*
    \(
        \s*\{[^}]*?(?P<R>[0-9.+-Ee]+)\*cos\(\s*\\t\s*r\)[^}]*\}\s*,
        \s*\{[^}]*?(?P=R)\*sin\(\s*\\t\s*r\)[^}]*\}\s*
    \)\s*;
    """,
    convert_shifted_param_arc,
    tikz,
    flags=re.VERBOSE | re.DOTALL,
)

# ----------------------------------------------------
# Convert TikZ function plots:
#   \draw[...] plot(\x,{expr});
#   \draw[...] plot [..] (\x,{expr});
# into pgfplots:
#   \addplot[...] {expr};
# ----------------------------------------------------
def convert_plot(match):
    draw_opts = (match.group("draw_opts") or "").strip()
    plot_opts = (match.group("plot_opts") or "").strip()
    expr = (match.group("expr") or "").strip()

    merged_raw = ",".join([draw_opts, plot_opts]).strip(",")
    parts = [p.strip() for p in merged_raw.split(",") if p.strip()]

    def norm(s: str) -> str:
        return re.sub(r"\s+", "", s)

    # remove domain/samples/variable if present; we’ll force them
    remove_prefixes = ["domain=", "samples=", "variable="]
    cleaned = []
    for p in parts:
        p_n = norm(p)
        if any(p_n.startswith(norm(pref)) for pref in remove_prefixes):
            continue
        cleaned.append(p)

    # force per-plot domain
    cleaned.append(f"domain={XMIN}:{XMAX}")

    # de-dupe
    seen = set()
    final_parts = []
    for p in cleaned:
        key = norm(p)
        if key not in seen:
            seen.add(key)
            final_parts.append(p)

    expr = expr.replace(r"\x", "x")
    final_opts = ", ".join(final_parts)
    return rf"\addplot[{final_opts}] {{{expr}}};"

tikz = re.sub(
    r"""
    \\draw
    (?:\s*\[(?P<draw_opts>[^\]]*)\])?
    \s*
    plot
    (?:\s*\[(?P<plot_opts>[^\]]*)\])?
    \s*
    \(
        \s*\\x\s*,\s*{(?P<expr>[^}]*)}\s*
    \)
    \s*;
    """,
    convert_plot,
    tikz,
    flags=re.VERBOSE,
)

# Final cleanup
tikz = re.sub(r",\s*,", ", ", tikz)
tikz = re.sub(r"\[\s*,", "[", tikz)
tikz = re.sub(r",\s*\]", "]", tikz)

# --- Save ---
output_file.write_text(tikz, encoding="utf-8")
print(f"TikZ code written to {output_file}")
