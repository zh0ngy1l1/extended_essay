#!/usr/bin/env python3
"""
tex_wordcount.py

Approximate word count for .tex files in the current directory.
Heuristics: strip comments, many math environments ($...$, $$...$$, \[...\], \(..\), equation/align blocks),
remove common braced commands (\footnote{}, \caption{}, \section{}, \subsection{}, \title{}, \author{}, \cite{}, \bibliography{}),
remove thebibliography and titlepage environments, then count remaining alphabetic words.

Simple and intentionally heuristic — won't be perfect but should be reasonably close for prose.
"""
import os
import re
import glob
import sys

def read_file(path):
    for enc in ('utf-8', 'latin-1'):
        try:
            with open(path, 'r', encoding=enc) as f:
                return f.read()
        except Exception:
            continue
    return ''


def remove_regex_patterns(text):
    # Remove LaTeX comments (naive: % to end of line unless escaped)
    text = re.sub(r'(?<!\\)%.*', '', text)

    # Remove display math: $$...$$, \[...\], \begin{equation}...\end{equation}, align, gather, etc.
    text = re.sub(r'\$\$.*?\$\$', ' ', text, flags=re.DOTALL)
    text = re.sub(r'\\\[.*?\\\]', ' ', text, flags=re.DOTALL)
    text = re.sub(r'\\\(.*?\\\)', ' ', text, flags=re.DOTALL)  # although this is inline, remove anyway
    text = re.sub(r'\$.*?\$', ' ', text, flags=re.DOTALL)  # inline math (greedy-ish)
    # common math-like environments to drop wholesale
    math_envs = [
        'equation', 'equation\*', 'align', 'align\*', 'gather', 'gather\*',
        'multline', 'multline\*', 'eqnarray', 'displaymath'
    ]
    for env in math_envs:
        pattern = r'\\begin\{' + env + r'\}.*?\\end\{' + env + r'\}'
        text = re.sub(pattern, ' ', text, flags=re.DOTALL)

    # remove thebibliography and titlepage environments completely
    text = re.sub(r'\\begin\{thebibliography\}.*?\\end\{thebibliography\}', ' ', text, flags=re.DOTALL)
    text = re.sub(r'\\begin\{titlepage\}.*?\\end\{titlepage\}', ' ', text, flags=re.DOTALL)

    return text


def remove_commands_with_braces(text, commands):
    """
    Remove occurrences of \cmd{...} including nested braces for listed commands.
    This is iterative and removes the whole \cmd{...} span.
    """
    for cmd in commands:
        # pattern to find \cmd{
        pat = re.compile(r'\\' + re.escape(cmd) + r'\s*\{', flags=re.IGNORECASE)
        while True:
            m = pat.search(text)
            if not m:
                break
            start = m.start()
            # find matching closing brace for the first '{' after m
            i = m.end() - 1  # position of '{'
            depth = 0
            end = None
            for j in range(i, len(text)):
                if text[j] == '{':
                    depth += 1
                elif text[j] == '}':
                    depth -= 1
                    if depth == 0:
                        end = j
                        break
            if end is None:
                # no matching brace: remove from start to end of line as fallback
                nl = text.find('\n', m.end())
                if nl == -1:
                    nl = len(text)
                text = text[:start] + ' ' + text[nl:]
            else:
                text = text[:start] + ' ' + text[end+1:]
    return text


def strip_other_commands(text):
    # Remove \begin{...} and \end{...} residuals (safe)
    text = re.sub(r'\\begin\{[^\}]*\}', ' ', text)
    text = re.sub(r'\\end\{[^\}]*\}', ' ', text)

    # Remove command names like \emph, \textbf, \item, \label etc.
    # We already removed many braced args; drop remaining backslash-words
    text = re.sub(r'\\[A-Za-z@]+', ' ', text)

    # Remove any remaining curly braces
    text = text.replace('{', ' ').replace('}', ' ')

    # Remove LaTeX special chars that aren't words
    text = re.sub(r'[_^&%#~]', ' ', text)

    return text


def approx_word_count_from_text(text):
    text = remove_regex_patterns(text)

    # remove some specific braced commands entirely
    braced_cmds = [
        'footnote', 'caption', 'section', 'subsection', 'subsubsection',
        'chapter', 'title', 'author', 'date', 'cite', 'bibliography', 'label', 'ref', 'pageref'
    ]
    text = remove_commands_with_braces(text, braced_cmds)

    text = strip_other_commands(text)

    # collapse multiple spaces
    text = re.sub(r'\s+', ' ', text)

    # Count tokens consisting of letters (allow accented letters and apostrophes)
    tokens = re.findall(r"[A-Za-zÀ-ÖØ-öø-ÿ'’]+", text)
    # filter tokens that have at least one alphabetic character
    words = [t for t in tokens if re.search(r'[A-Za-zÀ-ÖØ-öø-ÿ]', t)]
    return len(words)


def main():
    cwd = os.getcwd()
    tex_files = sorted(glob.glob("*.tex"))
    n = len(tex_files)
    print(f"scanned {cwd} and found {n} file (s).")
    print()
    if n == 0:
        print("No .tex files found in the current directory.")
        return
    for name in tex_files:
        text = read_file(name)
        wc = approx_word_count_from_text(text)
        print(f"word count of {name}: {wc}")

if __name__ == "__main__":
    main()
