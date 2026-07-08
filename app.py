"""
Milestone 5 — Query interface (Streamlit web app).

Designed to be self-explanatory in a no-narration demo: a titled page, a one-
line description of what it does, clickable EXAMPLE questions, a labeled input
box, an obvious "Ask" button, and clearly separated "Answer" and "Sources"
sections. A viewer can see the whole basic operation without any explanation.

The interface does no reasoning of its own: it calls generate_answer() and
displays the answer plus the code-built source list (result["sources"], derived
from retrieval metadata, not from the model), so attribution shown to the user
is guaranteed by the pipeline.

Run:
    python retrieval.py build            # build the vector index first (once)
    streamlit run app.py                 # opens the web UI in your browser
"""

from __future__ import annotations

import html

import streamlit as st

from generate import generate_answer, DEFAULT_TOP_K

EXAMPLES = [
    "Which pizza places do students recommend near campus?",
    "Does Russell Sage accommodate dietary needs?",
    "What do students say about the food at Commons?",
]

st.set_page_config(page_title="RPI Dining — Unofficial Guide", page_icon="🍴", layout="centered")

# ---------------------------------------------------------------------------
# Styling
# ---------------------------------------------------------------------------
st.markdown(
    """
    <style>
      .block-container { max-width: 940px; padding-top: 2rem; padding-bottom: 2.5rem; }
      .stApp { font-size: 17px; }

      /* Gradient header banner */
      .hero {
        display: flex; align-items: center; gap: 20px;
        background: linear-gradient(135deg, #c9002b 0%, #ff5a5f 100%);
        color: #ffffff; padding: 30px 34px; border-radius: 20px;
        box-shadow: 0 12px 34px rgba(201, 0, 43, 0.28); margin-bottom: 28px;
      }
      .hero-emoji { font-size: 54px; line-height: 1; }
      .hero h1 { color: #fff; font-size: 32px; font-weight: 800; margin: 0 0 6px 0; }
      .hero p  { color: rgba(255,255,255,0.94); font-size: 16px; margin: 0; }

      /* Section + field labels with icon */
      .section-label { font-size: 16px; font-weight: 700; color: #1a1a2e; margin: 6px 0 12px; }
      .field-label   { font-size: 15px; font-weight: 600; color: #33334d; margin: 2px 0 4px; }
      .icon { color: #c9002b; margin-right: 7px; }

      /* Example questions rendered as cards (secondary buttons) */
      .stButton button[kind="secondary"] {
        text-align: left; justify-content: flex-start; white-space: normal;
        background: #fbf6f7; border: 1px solid #f1e2e5; border-radius: 15px;
        padding: 16px 18px 16px 46px; min-height: 88px; line-height: 1.4;
        color: #33334d; font-weight: 500;
        position: relative;
      }
      .stButton button[kind="secondary"]::before {
        content: "?"; position: absolute; left: 14px; top: 16px;
        width: 24px; height: 24px; border-radius: 50%;
        background: #fbe0e4; color: #c9002b; font-weight: 700;
        display: flex; align-items: center; justify-content: center; font-size: 14px;
      }
      .stButton button[kind="secondary"]:hover { border-color: #c9002b; background: #fff2f4; color: #c9002b; }

      /* Ask (primary) button */
      .stButton button[kind="primary"] {
        background: #c9002b; border: none; border-radius: 12px; font-weight: 700;
        padding: 0.6rem 1.5rem; font-size: 16px;
      }
      .stButton button[kind="primary"]:hover { background: #a80022; color: #fff; }

      /* Card labels + answer/sources cards */
      .card-label {
        text-transform: uppercase; letter-spacing: .09em; font-size: 13px;
        font-weight: 700; color: #c9002b; margin-bottom: 10px;
      }
      .answer-card {
        background: #ffffff; border: 1px solid #ececf1; border-left: 6px solid #c9002b;
        border-radius: 16px; padding: 22px 26px; font-size: 18px; line-height: 1.65;
        color: #1a1a2e; box-shadow: 0 6px 22px rgba(20, 20, 40, 0.07); margin-top: 16px;
      }
      .sources-card {
        background: #f7f8fb; border: 1px solid #ececf1; border-radius: 16px;
        padding: 18px 24px; margin-top: 16px;
      }
      .sources-card ol { margin: 0; padding-left: 22px; }
      .sources-card li { margin: 7px 0; font-size: 15.5px; color: #33334d; }
      .sources-card a { color: #c9002b; text-decoration: none; font-weight: 600; }
      .sources-card a:hover { text-decoration: underline; }
      .no-sources { color: #6b6b7b; font-style: italic; margin-top: 12px; }

      /* Disclaimer box */
      .disclaimer {
        margin-top: 26px; background: #faf6f7; border: 1px solid #f1e2e5;
        border-radius: 12px; padding: 14px 18px; font-size: 13.5px;
        color: #8a8a98; line-height: 1.5;
      }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div class="hero">
      <div class="hero-emoji">🍴</div>
      <div>
        <h1>RPI Dining — The Unofficial Guide</h1>
        <p>Real student &amp; community answers about campus dining — grounded in sources, with citations, and no guessing.</p>
      </div>
    </div>
    """,
    unsafe_allow_html=True,
)

# ---------------------------------------------------------------------------
# State + callbacks (clicking Ask commits the box text before rerun; no Enter)
# ---------------------------------------------------------------------------
if "question" not in st.session_state:
    st.session_state.question = ""
if "run" not in st.session_state:
    st.session_state.run = False


def _ask_example(example: str) -> None:
    st.session_state.question = example
    st.session_state.run = True


def _ask() -> None:
    st.session_state.run = True


# --- Example questions --------------------------------------------------------
st.markdown('<div class="section-label"><span class="icon"> ✧ </span>Try an example:</div>', unsafe_allow_html=True)
for i, (col, example) in enumerate(zip(st.columns(len(EXAMPLES)), EXAMPLES)):
    col.button(example, key=f"ex_{i}", use_container_width=True, on_click=_ask_example, args=(example,))

# --- Or type your own (wrapped in a bordered card) ---------------------------
with st.container(border=True):
    st.markdown('<div class="field-label"><span class="icon"> ⋆˚꩜｡ </span>Your question</div>', unsafe_allow_html=True)
    st.text_input(
        "Your question",
        key="question",
        placeholder="e.g. How is the food at Commons?",
        label_visibility="collapsed",
    )
    st.markdown('<div class="field-label"><span class="icon"> ✿ </span>Sources to retrieve (top-k)</div>', unsafe_allow_html=True)
    top_k = st.slider("top-k", min_value=1, max_value=10, value=DEFAULT_TOP_K, label_visibility="collapsed")

st.button(" ⌯⌲ Ask", type="primary", on_click=_ask)


# ---------------------------------------------------------------------------
# Rendering helpers
# ---------------------------------------------------------------------------
def _render_answer(answer: str) -> None:
    safe = html.escape(answer).replace("\n", "<br>")
    st.markdown(
        f'<div class="answer-card"><div class="card-label">Answer</div>{safe}</div>',
        unsafe_allow_html=True,
    )


def _render_sources(sources: list[dict]) -> None:
    items = []
    for s in sources:
        name = html.escape(s.get("name") or s.get("source") or "source")
        url = s.get("url")
        items.append(f'<li><a href="{html.escape(url)}" target="_blank">{name}</a></li>' if url else f"<li>{name}</li>")
    st.markdown(
        f'<div class="sources-card"><div class="card-label">Sources</div><ol>{"".join(items)}</ol></div>',
        unsafe_allow_html=True,
    )


# ---------------------------------------------------------------------------
# Answer + Sources
# ---------------------------------------------------------------------------
if st.session_state.run:
    st.session_state.run = False        # consume the trigger for this rerun
    query = st.session_state.question.strip()
    if not query:
        st.info("Type a question above, or click one of the examples.")
    else:
        with st.spinner("Searching sources and generating a grounded answer…"):
            result = generate_answer(query, top_k=top_k)

        _render_answer(result["answer"])
        if result["sources"]:
            _render_sources(result["sources"])
        else:
            st.markdown(
                '<div class="no-sources">No sources — this question is outside the guide\'s scope.</div>',
                unsafe_allow_html=True,
            )

# ---------------------------------------------------------------------------
# Disclaimer footer
# ---------------------------------------------------------------------------
st.markdown(
    '<div class="disclaimer"><span class="icon"> ℹ </span>Please note the author is not associated with RPI, '
    'the project is created for personal project purpose.</div>',
    unsafe_allow_html=True,
)
