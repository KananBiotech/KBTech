# app.py — AquaExpert AI (RAG Edition) | Entry Point
# ─────────────────────────────────────────────────────────────

import streamlit as st

# Use relative imports to avoid conflicts with global 'config' package
from .config        import (APP_NAME, APP_ICON, APP_SUBTITLE, APP_LAYOUT,
                            SIDEBAR_DEFAULT, DEFAULT_MODEL, STAGES,
                            DIAGNOSIS_TURN_THRESHOLD, CSS_FILE)
from .memory        import default_memory, extract_entities, update_memory, is_emergency
from .llm           import create_client, get_response
from .rag.pipeline  import RAGPipeline
from .prompt_builder import build_api_messages
from .ui.sidebar    import render_sidebar
from .ui.chat       import render_chat
from .ui.components import (app_header, welcome_box, emergency_banner, input_hint)


# ─── PAGE CONFIG ─────────────────────────────────────────────
if hasattr(st, 'set_page_config'):
    st.set_page_config(
        page_title=APP_NAME, page_icon=APP_ICON,
        layout=APP_LAYOUT, initial_sidebar_state=SIDEBAR_DEFAULT,
    )


# ─── LOAD CSS ────────────────────────────────────────────────
def load_css(path: str) -> None:
    # Ensure path is handled correctly if relative to this file
    import os
    if not os.path.isabs(path):
        base_dir = os.path.dirname(__file__)
        path = os.path.join(base_dir, path)

    with open(path, "r") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


# ─── SESSION INIT ─────────────────────────────────────────────
def init_session() -> None:
    defaults = {
        "messages"         : [],
        "memory"           : default_memory(),
        "stage"            : "INITIAL",
        "emergency"        : False,
        "turn"             : 0,
        "api_key"          : "",
        "model"            : DEFAULT_MODEL,
        "client"           : None,
        "last_error"       : "",
        # RAG state
        "rag_pipeline"     : None,
        "rag_ready"        : False,
        "rag_status"       : None,
        "rag_chunk_count"  : 0,
        "rag_log"          : [],       # List of RAG results per AI turn
        "last_rag_results" : [],
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v


# ─── RAG INIT ────────────────────────────────────────────────
def init_rag() -> None:
    if st.session_state.rag_pipeline is not None:
        return   # Already initialized this session

    pipeline = RAGPipeline()

    with st.spinner("📖 Loading Aquaculture Knowledge Base..."):
        status = pipeline.initialize()

    st.session_state.rag_pipeline    = pipeline
    st.session_state.rag_ready       = status["success"]
    st.session_state.rag_status      = status
    st.session_state.rag_chunk_count = status.get("chunks", 0)


# ─── STAGE LOGIC ─────────────────────────────────────────────
def current_stage_label() -> str:
    if st.session_state.emergency: return STAGES["EMERGENCY"]
    if st.session_state.turn == 0: return STAGES["INITIAL"]
    if st.session_state.turn < DIAGNOSIS_TURN_THRESHOLD: return STAGES["QUESTIONING"]
    return STAGES["DIAGNOSED"]


def advance_stage() -> None:
    if st.session_state.emergency:
        st.session_state.stage = "EMERGENCY"
    elif st.session_state.turn == 0:
        st.session_state.stage = "INITIAL"
    elif st.session_state.turn < DIAGNOSIS_TURN_THRESHOLD:
        st.session_state.stage = "QUESTIONING"
    else:
        st.session_state.stage = "DIAGNOSED"


# ─── SEND MESSAGE ─────────────────────────────────────────────
def handle_send(user_input: str) -> None:
    st.session_state.last_error = ""

    # Check for critical situations
    if is_emergency(user_input):
        st.session_state.emergency = True

    st.session_state.messages.append({"role": "user", "content": user_input})

    # Update memory
    entities = extract_entities(user_input, st.session_state.client)
    if entities:
        st.session_state.memory = update_memory(st.session_state.memory, entities)

    # ── RAG Retrieval ─────────────────────────────────────────
    rag_results = []
    pipeline    = st.session_state.get("rag_pipeline")

    if pipeline and pipeline.is_ready():
        # Build a search query from current input
        rag_query   = user_input
        rag_results = pipeline.query(rag_query)
        st.session_state.last_rag_results = rag_results

    # ── LLM Call ──────────────────────────────────────────────
    reply, error = get_response(
        client      = st.session_state.client,
        conversation= st.session_state.messages,
        rag_results = rag_results,
        model       = st.session_state.model,
    )

    if error:
        st.session_state.last_error = error
        st.session_state.messages.pop()
        return

    st.session_state.messages.append({"role": "assistant", "content": reply})

    # Log which RAG results were used for this AI turn
    st.session_state.rag_log.append(rag_results)

    st.session_state.turn += 1
    advance_stage()


# ─── MAIN ─────────────────────────────────────────────────────
def main() -> None:
    init_session()
    load_css(CSS_FILE)
    init_rag()

    st.markdown(app_header(APP_NAME, APP_SUBTITLE, APP_ICON), unsafe_allow_html=True)

    if st.session_state.emergency:
        st.markdown(emergency_banner(), unsafe_allow_html=True)

    render_sidebar(
        stage_label  = current_stage_label(),
        is_emergency = st.session_state.emergency,
    )

    if not st.session_state.messages:
        st.markdown(welcome_box(), unsafe_allow_html=True)

    render_chat(st.session_state.messages, st.session_state.rag_log)

    st.markdown("<br>", unsafe_allow_html=True)

    if st.session_state.last_error:
        st.error(st.session_state.last_error)

    col_text, col_btn = st.columns([5, 1])
    with col_text:
        user_input = st.text_area(
            "message",
            placeholder="Ask about your fish farm or pond conditions...",
            height=95,
            label_visibility="collapsed",
            key="input_box",
        )
    with col_btn:
        st.markdown("<div style='height:0.45rem'></div>", unsafe_allow_html=True)
        send = st.button("SEND →", use_container_width=True)

    if send and user_input.strip():
        if not st.session_state.client:
            st.warning("⚠️  Please enter your Groq API key in the sidebar first.")
        else:
            with st.spinner("🐟 Consulting aquaculture knowledge base..."):
                handle_send(user_input.strip())
            st.rerun()

    st.markdown(input_hint(), unsafe_allow_html=True)


if __name__ == "__main__":
    main()
