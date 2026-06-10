import streamlit as st
import sys
import os
import time
from io import StringIO

# ── Page config ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="ResearchMind — Multi-Agent AI System",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── Global CSS ─────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');

*, *::before, *::after { box-sizing: border-box; }

html, body, [data-testid="stAppViewContainer"] {
    background: #06080d !important;
    color: #dce3ef !important;
    font-family: 'Inter', sans-serif !important;
}

[data-testid="stAppViewContainer"] > .main { background: #06080d !important; }
[data-testid="stHeader"]  { background: transparent !important; }
[data-testid="stSidebar"] { background: #0c0f18 !important; }

.block-container {
    padding: 0 3rem 5rem !important;
    max-width: 1120px !important;
    margin: 0 auto;
}

/* ─── Top nav bar ─────────────────────────────────────────────────────── */
.topbar {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 1.1rem 0 1.1rem;
    border-bottom: 1px solid #131929;
    margin-bottom: 0;
}
.topbar-logo {
    display: flex;
    align-items: center;
    gap: 0.6rem;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.82rem;
    font-weight: 500;
    color: #e2eaf4;
    letter-spacing: 0.08em;
    text-transform: uppercase;
}
.topbar-logo .dot-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 3px;
    width: 18px;
    height: 18px;
}
.topbar-logo .dot-grid span {
    width: 7px;
    height: 7px;
    border-radius: 50%;
    background: #3b9eff;
    display: block;
}
.topbar-logo .dot-grid span:nth-child(2) { background: #7c6af7; }
.topbar-logo .dot-grid span:nth-child(3) { background: #28c994; }
.topbar-logo .dot-grid span:nth-child(4) { background: #f5a623; }
.topbar-tag {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.68rem;
    letter-spacing: 0.14em;
    color: #3b9eff;
    background: rgba(59,158,255,0.08);
    border: 1px solid rgba(59,158,255,0.18);
    border-radius: 3px;
    padding: 3px 10px;
    text-transform: uppercase;
}

/* ─── Hero ────────────────────────────────────────────────────────────── */
.hero {
    padding: 4.5rem 0 3.5rem;
    text-align: center;
    width: 100%;
    display: flex;
    flex-direction: column;
    align-items: center;
}
.hero-eyebrow {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.7rem;
    letter-spacing: 0.22em;
    color: #5a6a85;
    text-transform: uppercase;
    margin-bottom: 1.2rem;
}
.hero h1 {
    font-size: 3.2rem !important;
    font-weight: 700 !important;
    letter-spacing: -0.04em;
    line-height: 1.1;
    color: #eaf0fa !important;
    margin: 0 0 0.75rem !important;
}
.hero h1 em {
    font-style: normal;
    background: linear-gradient(90deg, #3b9eff 0%, #7c6af7 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}
.hero-sub {
    font-size: 1.05rem;
    color: #4f6080;
    max-width: 580px;
    margin: 0 auto;
    line-height: 1.65;
    text-align: center;
    display: block;
}

/* ─── Agent architecture diagram ─────────────────────────────────────── */
.arch-row {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 0;
    margin: 2.5rem 0 3rem;
}
.arch-node {
    background: #0c0f18;
    border: 1px solid #192035;
    border-radius: 10px;
    padding: 1rem 1.35rem;
    min-width: 148px;
    text-align: center;
    position: relative;
    transition: border-color 0.2s;
}
.arch-node.active  { border-color: #3b9eff; box-shadow: 0 0 0 1px #3b9eff22; }
.arch-node.done    { border-color: #28c994; }
.arch-node.pending { opacity: 0.4; }
.arch-icon {
    width: 34px;
    height: 34px;
    border-radius: 8px;
    display: flex;
    align-items: center;
    justify-content: center;
    margin: 0 auto 0.5rem;
    font-size: 1rem;
}
.arch-icon.blue   { background: rgba(59,158,255,0.12);  color: #3b9eff; }
.arch-icon.purple { background: rgba(124,106,247,0.12); color: #7c6af7; }
.arch-icon.green  { background: rgba(40,201,148,0.12);  color: #28c994; }
.arch-icon.amber  { background: rgba(245,166,35,0.12);  color: #f5a623; }
.arch-icon.check  { background: rgba(40,201,148,0.15);  color: #28c994; }
.arch-label {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.6rem;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    margin-bottom: 3px;
}
.arch-label.blue   { color: #3b9eff; }
.arch-label.purple { color: #7c6af7; }
.arch-label.green  { color: #28c994; }
.arch-label.amber  { color: #f5a623; }
.arch-name  { font-size: 0.88rem; font-weight: 600; color: #dce3ef; margin-bottom: 2px; }
.arch-desc  { font-size: 0.74rem; color: #3d4f6a; line-height: 1.4; }
.arch-arrow {
    width: 40px;
    flex-shrink: 0;
    display: flex;
    align-items: center;
    justify-content: center;
    color: #1e2d47;
    font-size: 1rem;
}
.arch-arrow svg { width: 32px; height: 12px; }

/* ─── Input section ───────────────────────────────────────────────────── */
.input-wrap {
    background: #0c0f18;
    border: 1px solid #192035;
    border-radius: 12px;
    padding: 1.75rem 2rem;
    margin-bottom: 2.5rem;
}
.input-section-label {
    font-family: 'Inter', sans-serif;
    font-size: 0.72rem;
    font-weight: 600;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    color: #3b9eff;
}

[data-testid="stTextInput"] input {
    background: #080b12 !important;
    border: 1px solid #192035 !important;
    border-radius: 8px !important;
    color: #dce3ef !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 1rem !important;
    padding: 0.8rem 1.1rem !important;
    transition: border-color 0.15s, box-shadow 0.15s;
}
[data-testid="stTextInput"] input:focus {
    border-color: #3b9eff !important;
    box-shadow: 0 0 0 3px rgba(59,158,255,0.1) !important;
    outline: none !important;
}
[data-testid="stTextInput"] input::placeholder { color: #2a3a55 !important; }

[data-testid="stTextInput"] label {
    font-size: 0.73rem !important;
    font-weight: 600 !important;
    letter-spacing: 0.08em !important;
    text-transform: uppercase !important;
    color: #5a6a85 !important;
}

/* ─── Run button ──────────────────────────────────────────────────────── */
[data-testid="stButton"] > button {
    background: #3b9eff !important;
    color: #04070f !important;
    border: none !important;
    border-radius: 8px !important;
    font-family: 'Inter', sans-serif !important;
    font-weight: 700 !important;
    font-size: 0.88rem !important;
    letter-spacing: 0.03em;
    padding: 0.75rem 1.75rem !important;
    transition: background 0.15s, transform 0.1s;
}
[data-testid="stButton"] > button:hover  { background: #5aaeff !important; transform: translateY(-1px); }
[data-testid="stButton"] > button:active { transform: translateY(0); }

/* ─── Status bar ──────────────────────────────────────────────────────── */
.status-bar {
    display: flex;
    align-items: center;
    gap: 0.55rem;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.78rem;
    letter-spacing: 0.06em;
    padding: 0.65rem 1rem;
    background: #0c0f18;
    border: 1px solid #192035;
    border-radius: 8px;
    margin-bottom: 1.5rem;
}
.status-bar.running { color: #3b9eff; border-color: rgba(59,158,255,0.25); }
.status-bar.done    { color: #28c994; border-color: rgba(40,201,148,0.25); }
.pulse {
    width: 7px; height: 7px; border-radius: 50%;
    animation: pulse 1.1s ease-in-out infinite;
    flex-shrink: 0;
}
.pulse.blue  { background: #3b9eff; }
.pulse.green { background: #28c994; animation: none; opacity: 1; }
@keyframes pulse {
    0%, 100% { opacity: 1; transform: scale(1); }
    50%       { opacity: 0.25; transform: scale(0.65); }
}

/* ─── Stat strip ──────────────────────────────────────────────────────── */
.stat-strip {
    display: flex;
    gap: 0.75rem;
    flex-wrap: wrap;
    margin-bottom: 2rem;
}
.stat-chip {
    background: #0c0f18;
    border: 1px solid #192035;
    border-radius: 6px;
    padding: 0.5rem 0.95rem;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.74rem;
    color: #3d4f6a;
    display: flex;
    align-items: center;
    gap: 0.45rem;
}
.stat-chip .val { color: #3b9eff; font-weight: 500; }
.stat-chip.highlight { border-color: rgba(59,158,255,0.22); }
.stat-chip.highlight .val { color: #5aaeff; }

/* ─── Section heading ─────────────────────────────────────────────────── */
.section-head {
    display: flex;
    align-items: center;
    gap: 0.6rem;
    margin: 2.2rem 0 1rem;
}
.section-head-line {
    flex: 1;
    height: 1px;
    background: #131929;
}
.section-head-label {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.65rem;
    letter-spacing: 0.16em;
    text-transform: uppercase;
    color: #2a3a55;
    white-space: nowrap;
}

/* ─── Result cards ────────────────────────────────────────────────────── */
.result-card {
    background: #0c0f18;
    border: 1px solid #192035;
    border-radius: 12px;
    overflow: hidden;
    margin-bottom: 1.25rem;
}
.result-card-header {
    display: flex;
    align-items: center;
    gap: 0.65rem;
    padding: 0.85rem 1.25rem;
    border-bottom: 1px solid #131929;
    background: #090c14;
}
.result-card-header .accent-dot {
    width: 7px; height: 7px; border-radius: 50%; flex-shrink: 0;
}
.result-card-title {
    font-size: 0.72rem;
    font-weight: 600;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    color: #5a6a85;
    flex: 1;
}
.result-card-agent {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.65rem;
    color: #2a3a55;
    letter-spacing: 0.08em;
}
.result-card-body {
    padding: 1.5rem 1.75rem;
    font-size: 0.9rem;
    line-height: 1.8;
    color: #9aaec8;
    max-height: 480px;
    overflow-y: auto;
    word-break: break-word;
}
.result-card-body.mono {
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 0.8rem !important;
    color: #5a6a85 !important;
    white-space: pre-wrap;
    line-height: 1.7;
}

/* ── Styled markdown content inside cards ── */
.rmd h1, .rmd h2, .rmd h3, .rmd h4 {
    font-family: 'Inter', sans-serif;
    font-weight: 700;
    color: #dce3ef;
    margin: 1.5rem 0 0.5rem;
    line-height: 1.25;
    letter-spacing: -0.01em;
}
.rmd h1 { font-size: 1.25rem; border-bottom: 1px solid #192035; padding-bottom: 0.5rem; margin-top: 0; }
.rmd h2 { font-size: 1.05rem; color: #b0c4e0; margin-top: 1.6rem; }
.rmd h3 { font-size: 0.95rem; color: #7c96b8; font-weight: 600; }
.rmd h4 { font-size: 0.88rem; color: #5a6a85; font-weight: 600; text-transform: uppercase; letter-spacing: 0.06em; }
.rmd p  { margin: 0.6rem 0 0.9rem; color: #9aaec8; }
.rmd p:first-child { margin-top: 0; }
.rmd strong { color: #c8d8ee; font-weight: 600; }
.rmd em { color: #7c96b8; font-style: italic; }

.rmd ul, .rmd ol {
    margin: 0.5rem 0 1rem 0;
    padding-left: 0;
    list-style: none;
}
.rmd ul li {
    position: relative;
    padding: 0.35rem 0 0.35rem 1.4rem;
    color: #9aaec8;
    border-bottom: 1px solid #0f1420;
    font-size: 0.88rem;
    line-height: 1.65;
}
.rmd ul li:last-child { border-bottom: none; }
.rmd ul li::before {
    content: '';
    position: absolute;
    left: 0;
    top: 0.75rem;
    width: 5px;
    height: 5px;
    border-radius: 50%;
    background: #3b9eff;
    opacity: 0.6;
}
.rmd ol { counter-reset: ol-counter; }
.rmd ol li {
    position: relative;
    padding: 0.35rem 0 0.35rem 2rem;
    color: #9aaec8;
    border-bottom: 1px solid #0f1420;
    font-size: 0.88rem;
    line-height: 1.65;
    counter-increment: ol-counter;
}
.rmd ol li:last-child { border-bottom: none; }
.rmd ol li::before {
    content: counter(ol-counter);
    position: absolute;
    left: 0;
    top: 0.38rem;
    width: 20px;
    height: 20px;
    background: rgba(59,158,255,0.1);
    border: 1px solid rgba(59,158,255,0.2);
    border-radius: 4px;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.65rem;
    color: #3b9eff;
    display: flex;
    align-items: center;
    justify-content: center;
    text-align: center;
    line-height: 20px;
}
.rmd blockquote {
    border-left: 3px solid #3b9eff;
    margin: 1rem 0;
    padding: 0.6rem 1rem;
    background: rgba(59,158,255,0.04);
    border-radius: 0 6px 6px 0;
    color: #5a6a85;
    font-style: italic;
    font-size: 0.88rem;
}
.rmd code {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.8rem;
    background: #0a0d17;
    border: 1px solid #192035;
    border-radius: 4px;
    padding: 2px 7px;
    color: #7c6af7;
}
.rmd hr {
    border: none;
    border-top: 1px solid #192035;
    margin: 1.25rem 0;
}
/* Score badge (for critic output) */
.score-badge {
    display: inline-flex;
    align-items: center;
    gap: 0.5rem;
    background: rgba(59,158,255,0.08);
    border: 1px solid rgba(59,158,255,0.2);
    border-radius: 8px;
    padding: 0.6rem 1.1rem;
    margin: 0.5rem 0 1.25rem;
    font-family: 'JetBrains Mono', monospace;
}
.score-badge .score-num {
    font-size: 1.6rem;
    font-weight: 700;
    color: #3b9eff;
    line-height: 1;
}
.score-badge .score-label {
    font-size: 0.68rem;
    color: #3d4f6a;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    line-height: 1.3;
}

.result-card-body::-webkit-scrollbar { width: 4px; }
.result-card-body::-webkit-scrollbar-track { background: transparent; }
.result-card-body::-webkit-scrollbar-thumb { background: #192035; border-radius: 2px; }

/* ─── Divider ─────────────────────────────────────────────────────────── */
.divider { border: none; border-top: 1px solid #131929; margin: 2rem 0; }

/* ─── Expander ────────────────────────────────────────────────────────── */
[data-testid="stExpander"] {
    background: #0c0f18 !important;
    border: 1px solid #192035 !important;
    border-radius: 10px !important;
}
[data-testid="stExpander"] summary {
    font-size: 0.84rem !important;
    font-weight: 500 !important;
    color: #3d4f6a !important;
}

/* ─── Alert ───────────────────────────────────────────────────────────── */
[data-testid="stAlert"] {
    background: rgba(59,158,255,0.05) !important;
    border: 1px solid rgba(59,158,255,0.15) !important;
    border-radius: 8px !important;
    color: #5a6a85 !important;
}

/* ─── Download button ─────────────────────────────────────────────────── */
[data-testid="stDownloadButton"] > button {
    background: transparent !important;
    border: 1px solid #192035 !important;
    color: #3d4f6a !important;
    border-radius: 8px !important;
    font-size: 0.82rem !important;
    font-weight: 500 !important;
    padding: 0.5rem 1.2rem !important;
    transition: border-color 0.15s, color 0.15s;
}
[data-testid="stDownloadButton"] > button:hover {
    border-color: #3b9eff !important;
    color: #3b9eff !important;
    background: rgba(59,158,255,0.05) !important;
}

/* ─── Footer ──────────────────────────────────────────────────────────── */
.footer {
    text-align: center;
    padding: 2.5rem 0 1rem;
    font-size: 0.7rem;
    color: #1e2d47;
    font-family: 'JetBrains Mono', monospace;
    letter-spacing: 0.08em;
    border-top: 1px solid #131929;
    margin-top: 4rem;
}
.idle-hint {
    text-align: center;
    margin-top: 2rem;
    color: #1e2d47;
    font-size: 0.75rem;
    font-family: 'JetBrains Mono', monospace;
    letter-spacing: 0.1em;
    text-transform: uppercase;
}
</style>
""", unsafe_allow_html=True)

# ── Helpers ────────────────────────────────────────────────────────────────────

AGENTS = [
    {
        "icon": "🔍",
        "color_cls": "blue",
        "label": "Agent 01",
        "name": "Search Agent",
        "desc": "Queries the web for recent, reliable sources.",
    },
    {
        "icon": "📖",
        "color_cls": "purple",
        "label": "Agent 02",
        "name": "Reader Agent",
        "desc": "Scrapes the most relevant URL for deeper content.",
    },
    {
        "icon": "✍️",
        "color_cls": "green",
        "label": "Chain 03",
        "name": "Writer Chain",
        "desc": "Synthesises data into a structured report.",
    },
    {
        "icon": "🧐",
        "color_cls": "amber",
        "label": "Chain 04",
        "name": "Critic Chain",
        "desc": "Reviews the report for accuracy and depth.",
    },
]

ARROW_SVG = """<svg viewBox="0 0 32 12" fill="none" xmlns="http://www.w3.org/2000/svg">
  <line x1="0" y1="6" x2="26" y2="6" stroke="#192035" stroke-width="1.5"/>
  <polyline points="20,2 26,6 20,10" stroke="#192035" stroke-width="1.5" fill="none" stroke-linecap="round" stroke-linejoin="round"/>
</svg>"""


def render_arch(active_idx: int = -1, done_idxs: set = set()):
    """Render the agent architecture strip."""
    nodes_html = ""
    for i, ag in enumerate(AGENTS):
        if i in done_idxs:
            state = "done"
            icon_cls = "check"
            icon_char = "✓"
            label_cls = "green"
        elif i == active_idx:
            state = "active"
            icon_cls = ag["color_cls"]
            icon_char = ag["icon"]
            label_cls = ag["color_cls"]
        else:
            state = "pending"
            icon_cls = ag["color_cls"]
            icon_char = ag["icon"]
            label_cls = ag["color_cls"]

        nodes_html += f"""
        <div class="arch-node {state}">
            <div class="arch-icon {icon_cls}">{icon_char}</div>
            <div class="arch-label {label_cls}">{ag['label']}</div>
            <div class="arch-name">{ag['name']}</div>
            <div class="arch-desc">{ag['desc']}</div>
        </div>"""
        if i < len(AGENTS) - 1:
            nodes_html += f'<div class="arch-arrow">{ARROW_SVG}</div>'

    st.markdown(f'<div class="arch-row">{nodes_html}</div>', unsafe_allow_html=True)


def status_bar(text: str, done: bool = False):
    cls = "done" if done else "running"
    dot_cls = "green" if done else "blue"
    st.markdown(
        f'<div class="status-bar {cls}"><div class="pulse {dot_cls}"></div>{text}</div>',
        unsafe_allow_html=True,
    )


def parse_md_to_html(text: str) -> str:
    """Convert markdown-style text to styled HTML for result cards."""
    import re, html

    lines = text.split("\n")
    out = []
    in_ul = False
    in_ol = False

    def close_lists():
        nonlocal in_ul, in_ol
        if in_ul:
            out.append("</ul>")
            in_ul = False
        if in_ol:
            out.append("</ol>")
            in_ol = False

    def inline(s: str) -> str:
        s = html.escape(s)
        # bold
        s = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", s)
        s = re.sub(r"__(.+?)__",     r"<strong>\1</strong>", s)
        # italic
        s = re.sub(r"\*(.+?)\*",     r"<em>\1</em>", s)
        s = re.sub(r"_(.+?)_",       r"<em>\1</em>", s)
        # inline code
        s = re.sub(r"`(.+?)`",       r"<code>\1</code>", s)
        return s

    for line in lines:
        stripped = line.strip()

        # blank line
        if not stripped:
            close_lists()
            continue

        # headings
        if stripped.startswith("#### "):
            close_lists()
            out.append(f"<h4>{inline(stripped[5:])}</h4>")
        elif stripped.startswith("### "):
            close_lists()
            out.append(f"<h3>{inline(stripped[4:])}</h3>")
        elif stripped.startswith("## "):
            close_lists()
            out.append(f"<h2>{inline(stripped[3:])}</h2>")
        elif stripped.startswith("# "):
            close_lists()
            out.append(f"<h1>{inline(stripped[2:])}</h1>")

        # hr
        elif stripped in ("---", "***", "___"):
            close_lists()
            out.append("<hr>")

        # blockquote
        elif stripped.startswith("> "):
            close_lists()
            out.append(f"<blockquote>{inline(stripped[2:])}</blockquote>")

        # score line e.g. "Score: 8/10"
        elif re.match(r"^score\s*:\s*(\d+)/(\d+)", stripped, re.I):
            close_lists()
            m = re.match(r"^score\s*:\s*(\d+)/(\d+)", stripped, re.I)
            num, denom = m.group(1), m.group(2)
            out.append(f"""<div class="score-badge">
                <span class="score-num">{html.escape(num)}</span>
                <span class="score-label">out of {html.escape(denom)}<br>quality score</span>
            </div>""")

        # unordered list
        elif re.match(r"^[-*•]\s+", stripped):
            if not in_ul:
                close_lists()
                out.append("<ul>")
                in_ul = True
            item = re.sub(r"^[-*•]\s+", "", stripped)
            out.append(f"<li>{inline(item)}</li>")

        # ordered list
        elif re.match(r"^\d+\.\s+", stripped):
            if not in_ol:
                close_lists()
                out.append("<ol>")
                in_ol = True
            item = re.sub(r"^\d+\.\s+", "", stripped)
            out.append(f"<li>{inline(item)}</li>")

        # paragraph
        else:
            close_lists()
            out.append(f"<p>{inline(stripped)}</p>")

    close_lists()
    return "\n".join(out)


def result_card(title: str, agent_tag: str, dot_color: str, content: str, mono: bool = False):
    if mono:
        import html as _html
        body_html = f'<div class="result-card-body mono">{_html.escape(content)}</div>'
    else:
        rendered = parse_md_to_html(content)
        body_html = f'<div class="result-card-body"><div class="rmd">{rendered}</div></div>'

    st.markdown(f"""
    <div class="result-card">
        <div class="result-card-header">
            <div class="accent-dot" style="background:{dot_color}"></div>
            <span class="result-card-title">{title}</span>
            <span class="result-card-agent">{agent_tag}</span>
        </div>
        {body_html}
    </div>
    """, unsafe_allow_html=True)


def section_head(label: str):
    st.markdown(f"""
    <div class="section-head">
        <div class="section-head-line"></div>
        <div class="section-head-label">{label}</div>
        <div class="section-head-line"></div>
    </div>
    """, unsafe_allow_html=True)


# ── Top nav ────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="topbar">
    <div class="topbar-logo">
        <div class="dot-grid">
            <span></span><span></span><span></span><span></span>
        </div>
        ResearchMind
    </div>
    <div class="topbar-tag">Multi-Agent AI System</div>
</div>
""", unsafe_allow_html=True)

# ── Hero ───────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
    <div class="hero-eyebrow">Autonomous research intelligence</div>
    <h1>Four AI agents.<br><em>One verified report.</em></h1>
    <p class="hero-sub">
        Enter any research topic. The AI system autonomously retrieves live web data,
        extracts insights from primary sources, produces a structured report,
        and applies a built-in quality review — delivering reliable research in seconds.
    </p>
</div>
""", unsafe_allow_html=True)

# ── Input area ─────────────────────────────────────────────────────────────────
st.markdown('<div class="input-wrap">', unsafe_allow_html=True)
st.markdown("""
<div style="display:flex; align-items:center; justify-content:space-between; margin-bottom:0.75rem;">
    <div class="input-section-label">Research topic</div>
    <div style="font-family:'JetBrains Mono',monospace; font-size:0.65rem; color:#2a3a55; letter-spacing:0.1em;">
        SEARCH → READ → WRITE → REVIEW
    </div>
</div>
""", unsafe_allow_html=True)
col_inp, col_btn = st.columns([5, 1], vertical_alignment="bottom")
with col_inp:
    topic = st.text_input(
        "Topic",
        placeholder="e.g.  Large language models in healthcare — clinical applications 2025",
        help="Any topic — the AI system handles search, extraction, writing, and critique automatically.",
        label_visibility="collapsed",
    )
with col_btn:
    run_btn = st.button("Run System ›", use_container_width=True)
st.markdown("""
<div style="margin-top:0.65rem; font-size:0.74rem; color:#2a3a55; line-height:1.5;">
    The system runs four sequential AI agents. Average completion time is 30 – 90 seconds depending on topic complexity.
</div>
""", unsafe_allow_html=True)
st.markdown("</div>", unsafe_allow_html=True)

# ── Idle view ──────────────────────────────────────────────────────────────────
if not run_btn:
    render_arch()
    st.markdown(
        '<div class="idle-hint">System ready — enter a topic above to begin</div>',
        unsafe_allow_html=True,
    )

# ── Run ────────────────────────────────────────────────────────────────────────
if run_btn:
    if not topic.strip():
        st.warning("Please enter a research topic to get started.")
    else:
        try:
            sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
            from b_agents import build_search_agent, build_reader_agent, writer_chain, critic_chain
        except ImportError as e:
            st.error(
                f"Import error: `{e}`\n\n"
                "Make sure `b_agents.py`, `c_pipeline.py`, and `a_tools.py` are in the same folder as `d_app.py`."
            )
            st.stop()

        st.markdown('<hr class="divider">', unsafe_allow_html=True)

        arch_ph   = st.empty()
        status_ph = st.empty()
        done_set  = set()
        timing    = {}

        def upd(active_idx):
            with arch_ph.container():
                render_arch(active_idx=active_idx, done_idxs=done_set)

        # ── Agent 01: Search ────────────────────────────────────────────────
        upd(0)
        with status_ph.container():
            status_bar("Search agent is querying the web…")
        t0 = time.time()

        old_stdout = sys.stdout
        sys.stdout = StringIO()
        state = {}
        try:
            search_agent  = build_search_agent()
            search_result = search_agent.invoke({"messages": [("user", f"Find recent, reliable and detailed information about: {topic}")]})
            state["search_results"] = search_result["messages"][-1].content
        except Exception as e:
            sys.stdout = old_stdout
            st.error(f"Search agent failed: {e}")
            st.stop()

        timing["search"] = round(time.time() - t0, 1)
        done_set.add(0)
        upd(1)

        # ── Agent 02: Reader ────────────────────────────────────────────────
        with status_ph.container():
            status_bar("Reader agent is scraping top source…")
        t1 = time.time()

        try:
            reader_agent  = build_reader_agent()
            reader_result = reader_agent.invoke({
                "messages": [("user",
                    f"Based on the following search results about '{topic}', "
                    f"pick the most relevant URL and scrape it for deeper content.\n\n"
                    f"Search Results:\n{state['search_results'][:800]}"
                )]
            })
            state["scrapped_content"] = reader_result["messages"][-1].content
        except Exception as e:
            sys.stdout = old_stdout
            st.error(f"Reader agent failed: {e}")
            st.stop()

        timing["reader"] = round(time.time() - t1, 1)
        done_set.add(1)
        upd(2)

        # ── Chain 03: Writer ────────────────────────────────────────────────
        with status_ph.container():
            status_bar("Writer chain is drafting the report…")
        t2 = time.time()

        try:
            research_combined = (
                f"SEARCH RESULTS:\n{state['search_results']}\n\n"
                f"DETAILED SCRAPED CONTENT:\n{state['scrapped_content']}"
            )
            state["report"] = writer_chain.invoke({"topic": topic, "research": research_combined})
        except Exception as e:
            sys.stdout = old_stdout
            st.error(f"Writer chain failed: {e}")
            st.stop()

        timing["writer"] = round(time.time() - t2, 1)
        done_set.add(2)
        upd(3)

        # ── Chain 04: Critic ────────────────────────────────────────────────
        with status_ph.container():
            status_bar("Critic chain is reviewing the report…")
        t3 = time.time()

        try:
            state["feedback"] = critic_chain.invoke({"report": state["report"]})
        except Exception as e:
            sys.stdout = old_stdout
            st.error(f"Critic chain failed: {e}")
            st.stop()

        timing["critic"] = round(time.time() - t3, 1)
        done_set.add(3)
        sys.stdout = old_stdout

        # ── All done ────────────────────────────────────────────────────────
        with arch_ph.container():
            render_arch(active_idx=-1, done_idxs=done_set)
        with status_ph.container():
            status_bar("AI system complete — report ready.", done=True)

        # ── Stat strip ──────────────────────────────────────────────────────
        total_t = sum(timing.values())
        st.markdown(f"""
        <div class="stat-strip">
            <div class="stat-chip highlight">Total <span class="val">{total_t}s</span></div>
            <div class="stat-chip">Search <span class="val">{timing['search']}s</span></div>
            <div class="stat-chip">Reader <span class="val">{timing['reader']}s</span></div>
            <div class="stat-chip">Writer <span class="val">{timing['writer']}s</span></div>
            <div class="stat-chip">Critic <span class="val">{timing['critic']}s</span></div>
            <div class="stat-chip">Sources <span class="val">2</span></div>
        </div>
        """, unsafe_allow_html=True)

        # ── Extract content ─────────────────────────────────────────────────
        report_content = state.get("report", "")
        if hasattr(report_content, "content"):
            report_content = report_content.content

        feedback_content = state.get("feedback", "")
        if hasattr(feedback_content, "content"):
            feedback_content = feedback_content.content

        search_content  = state.get("search_results", "")
        scraped_content = state.get("scrapped_content", "")

        # ── Primary outputs ─────────────────────────────────────────────────
        section_head("Research Report")
        result_card(
            "Final report",
            "Writer chain · Agent 03",
            "#3b9eff",
            report_content,
        )

        section_head("Critic Review")
        result_card(
            "Quality assessment",
            "Critic chain · Agent 04",
            "#7c6af7",
            feedback_content,
        )

        # ── Raw outputs (expandable) ────────────────────────────────────────
        section_head("Raw Agent Outputs")
        with st.expander("🔍  Search results (raw)"):
            result_card("Search agent output", "Agent 01", "#3b9eff", search_content, mono=True)

        with st.expander("📖  Scraped content (raw)"):
            result_card("Reader agent output", "Agent 02", "#28c994", scraped_content, mono=True)

        # ── Download ────────────────────────────────────────────────────────
        st.markdown('<hr class="divider">', unsafe_allow_html=True)
        export_text = (
            f"RESEARCHMIND — MULTI-AGENT AI SYSTEM REPORT\n"
            f"Topic : {topic}\n"
            f"Time  : {total_t}s  |  Agents: 4\n"
            f"{'='*64}\n\n"
            f"RESEARCH REPORT\n{'-'*64}\n{report_content}\n\n"
            f"CRITIC FEEDBACK\n{'-'*64}\n{feedback_content}\n\n"
            f"SEARCH RESULTS (RAW)\n{'-'*64}\n{search_content}\n\n"
            f"SCRAPED CONTENT (RAW)\n{'-'*64}\n{scraped_content}\n"
        )
        st.download_button(
            label="⬇  Download full report (.txt)",
            data=export_text,
            file_name=f"researchmind_{topic[:40].replace(' ', '_')}.txt",
            mime="text/plain",
        )

# ── Footer ─────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="footer">
    ResearchMind · Multi-Agent AI System · LangChain + Mistral + Streamlit
</div>
""", unsafe_allow_html=True)