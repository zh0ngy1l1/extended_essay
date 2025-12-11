import re
import os
from pathlib import Path

# --- Directories ---
input_dir = Path("ggb_exports")
output_dir = Path("src")
output_dir.mkdir(exist_ok=True)  # ensure src/ exists

# --- Find exactly one .txt file in ggb_exports ---
txt_files = list(input_dir.glob("*.txt"))
if len(txt_files) == 0:
    raise FileNotFoundError(f"No .txt files found in {input_dir}")
elif len(txt_files) > 1:
    raise FileExistsError(f"Multiple .txt files found in {input_dir}: {txt_files}")

input_file = txt_files[0]
output_file = output_dir / (input_file.stem + ".tex")  # e.g., fig1.tex

# --- Read input file ---
with input_file.open("r", encoding="utf-8") as f:
    content = f.read()

# --- Extract only the tikzpicture ---
match = re.search(
    r"\\begin{tikzpicture}.*?\\end{tikzpicture}",
    content,
    flags=re.DOTALL
)
if not match:
    raise ValueError("No tikzpicture environment found.")

tikz = match.group(0)

# --- Delete the original file ---
input_file.unlink()

# ----------------------------------------------------
# Replace any existing \clip(...) with a fixed clip
# restricting the xdomain and ydomain
# ----------------------------------------------------
tikz = re.sub(
    r"\\clip\s*\(.*?\)\s*rectangle\s*\(.*?\)\s*;",
    r"\\clip(-10.82,-7.41) rectangle (10.82,7.41);",
    tikz
)

# --- Replace fill=... and color=... with black ---
tikz = re.sub(r"fill\s*=\s*[^,\]]+", "fill=black", tikz)
tikz = re.sub(r"color\s*=\s*[^,\]]+", "color=black", tikz)

# --- Remove line width=... inside option lists and redundant color=black ---
tikz = re.sub(
    r"\[(.*?)\]",
    lambda m: "[" + ", ".join(
        p for p in (part.strip() for part in m.group(1).split(","))
        if not (p.startswith("line width=") or p == "color=black")
    ) + "]",
    tikz
)
# Remove empty brackets
tikz = re.sub(r"\[\s*\]", "", tikz)

# --- Adjust circle size ---
tikz = re.sub(r"circle\s*\(\s*2\.5pt\s*\)", "circle (2pt)", tikz)

# --- Remove scriptsize environment ---
tikz = re.sub(r"\\begin{scriptsize}", "", tikz)
tikz = re.sub(r"\\end{scriptsize}", "", tikz)

# --- Remove x=1cm and y=1cm from tikzpicture options ---
tikz = re.sub(r"x\s*=\s*1cm\s*,?\s*", "", tikz)
tikz = re.sub(r"y\s*=\s*1cm\s*,?\s*", "", tikz)

# ----------------------------------------------------
# Replace any \draw [...] containing "dash pattern=..." with [dashed], preserving other options
# Example: 
# \draw [shift={(-2.25,-0.38)}, dash pattern=on 1pt off 1pt] ...;
# -> 
# \draw [shift={(-2.25,-0.38)}, dashed] ...;
# ----------------------------------------------------
def replace_dash(match):
    options = match.group(1)
    # Remove dash pattern from the options
    parts = [p.strip() for p in options.split(",") if "dash pattern=" not in p]
    parts.append("dashed")  # add dashed at the end
    return r"\draw [" + ", ".join(parts) + "]"

tikz = re.sub(
    r"\\draw\s*\[([^\]]*dash pattern=[^\]]*)\]",
    replace_dash,
    tikz
)

# --- Clean up leftover double commas ---
tikz = re.sub(r",\s*,", ",", tikz)
tikz = re.sub(r"\[\s*,", "[", tikz)

# ----------------------------------------------------
# Enclose all node labels in $...$ if not already
# Example: \draw (x,y) node {A*}  -> \draw (x,y) node {$A*$}
# ----------------------------------------------------
tikz = re.sub(
    r"node\s*{\s*([^$][^}]*)\s*}",  # match node { ... } not starting with $
    r"node {$\1$}",                 # replace with node {$...$}
    tikz
)

# --- Write to output file ---
with output_file.open("w", encoding="utf-8") as f:
    f.write(tikz)

print(f"TikZ code written to {output_file}")
