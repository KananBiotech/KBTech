# ui/chat.py — Chat Window Rendering
# ─────────────────────────────────────────────────────────────
# Renders conversation messages and STG source panels.
# Each AI message shows which STG chunks were used (if any).
# ─────────────────────────────────────────────────────────────

import streamlit as st
from ui.components import (
    user_message, ai_message,
    emergency_message, stg_sources_panel
)


def render_chat(messages: list, rag_log: list) -> None:
    """
    Renders the full conversation.

    rag_log is a parallel list to messages — each entry is the list
    of STG results used when generating the corresponding AI message.
    Index: rag_log[i] corresponds to the i-th assistant message.
    """
    ai_turn = 0   # Track which AI message we're on

    for msg in messages:
        if msg["role"] == "user":
            st.markdown(user_message(msg["content"]), unsafe_allow_html=True)
        else:
            rag_results = []
            if rag_log and ai_turn < len(rag_log):
                rag_results = rag_log[ai_turn]
            ai_turn += 1

            _render_ai_message(msg["content"], rag_results)


def _render_ai_message(content: str, rag_results: list) -> None:
    """Renders AI response + optional STG sources panel below it."""
    rag_used = bool(rag_results)

    if "[EMERGENCY]" in content:
        st.markdown(emergency_message(content), unsafe_allow_html=True)
    else:
        st.markdown(ai_message(content, rag_used), unsafe_allow_html=True)

    # Show STG sources if they were used
    if rag_used:
        with st.expander(f"📖 View {len(rag_results)} STG source(s) used", expanded=False):
            st.markdown(stg_sources_panel(rag_results), unsafe_allow_html=True)
