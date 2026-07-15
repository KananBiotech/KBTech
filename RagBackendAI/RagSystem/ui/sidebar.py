# ui/sidebar.py — Sidebar Rendering
# ─────────────────────────────────────────────────────────────

import streamlit as st
from ..config import AVAILABLE_MODELS
from ..llm import create_client
from ..memory import memory_has_data
from .components import (
    status_dot, stage_badge, memory_tags,
    sidebar_disclaimer, rag_status_box, rag_not_loaded_warning
)


def render_sidebar(stage_label: str, is_emergency: bool) -> None:
    with st.sidebar:

        # ── Setup ────────────────────────────────────────────
        st.markdown("### ⚙️  Setup")
        key_input = st.text_input(
            "Groq API Key", type="password",
            placeholder="gsk_...",
            value=st.session_state.api_key,
            help="Free key at console.groq.com",
        )
        if key_input != st.session_state.api_key:
            st.session_state.api_key = key_input
            st.session_state.client  = create_client(key_input)
        elif key_input and st.session_state.client is None:
            st.session_state.client  = create_client(key_input)

        st.markdown(status_dot(st.session_state.client is not None), unsafe_allow_html=True)

        model_keys   = list(AVAILABLE_MODELS.keys())
        model_labels = list(AVAILABLE_MODELS.values())
        current_idx  = model_keys.index(st.session_state.model) if st.session_state.model in model_keys else 0
        selected     = st.selectbox("Model", model_labels, index=current_idx)
        st.session_state.model = model_keys[model_labels.index(selected)]

        st.markdown("---")

        # ── Knowledge Base Status ────────────────────────────
        st.markdown("### 📖  Knowledge Base")

        rag_status = st.session_state.get("rag_status", None)
        rag_ready  = st.session_state.get("rag_ready", False)

        if rag_status:
            st.markdown(rag_status_box(rag_status), unsafe_allow_html=True)
        else:
            st.markdown(rag_not_loaded_warning(), unsafe_allow_html=True)

        if rag_ready:
            last_rag = st.session_state.get("last_rag_results", [])
            if last_rag:
                st.markdown(f"**Last query:** `{len(last_rag)}` chunks retrieved")

        # Rebuild button
        if st.button("🔄  Rebuild Index", use_container_width=True):
            import os
            from ..config import FAISS_INDEX_FILE, CHUNKS_FILE
            for f in [FAISS_INDEX_FILE, CHUNKS_FILE]:
                if os.path.exists(f): os.remove(f)
            st.session_state.rag_ready  = False
            st.session_state.rag_status = None
            st.session_state.rag_pipeline = None
            st.rerun()

        st.markdown("---")

        # ── Consultation Status ───────────────────────────────
        st.markdown("### 📊  Session Status")
        st.markdown(stage_badge(stage_label, is_emergency), unsafe_allow_html=True)
        st.markdown(f"**Turns:** `{st.session_state.turn}`")

        st.markdown("---")

        # ── Aquaculture Data ──────────────────────────────────
        st.markdown("### 🧠  Pond & Fish Data")
        _render_memory()

        st.markdown("---")

        # ── Actions ───────────────────────────────────────────
        if st.button("🆕  New Session", use_container_width=True):
            rag_pipeline = st.session_state.get("rag_pipeline")
            rag_status   = st.session_state.get("rag_status")
            rag_ready    = st.session_state.get("rag_ready")
            api_key      = st.session_state.get("api_key")
            model        = st.session_state.get("model")
            client       = st.session_state.get("client")

            st.session_state.clear()

            st.session_state.rag_pipeline = rag_pipeline
            st.session_state.rag_status   = rag_status
            st.session_state.rag_ready    = rag_ready
            st.session_state.api_key      = api_key
            st.session_state.model        = model
            st.session_state.client       = client
            st.rerun()

        st.markdown(sidebar_disclaimer(), unsafe_allow_html=True)


def _render_memory() -> None:
    mem = st.session_state.get("memory", {})
    if not mem or not memory_has_data(mem):
        st.markdown('<p style="color:#4a6080;font-size:0.82rem;">No data yet. Start describing your farm.</p>', unsafe_allow_html=True)
        return

    if mem.get("species"):
        st.markdown("**Species:**")
        st.markdown(memory_tags(mem["species"], "tag tag-symptom"), unsafe_allow_html=True) # reuse symptom styling for species
    if mem.get("symptoms"):
        st.markdown("**Symptoms/Observations:**")
        st.markdown(memory_tags(mem["symptoms"], "tag tag-info"), unsafe_allow_html=True)
    if mem.get("water_parameters"):
        params = {k: v for k, v in mem["water_parameters"].items() if v}
        if params:
            st.markdown("**Water Quality:**")
            st.markdown("`" + " | ".join(f"{k.upper()}: {v}" for k, v in params.items()) + "`")
    if mem.get("pond_type"):
        st.markdown(f"**Pond Type:** `{mem['pond_type']}`")
    if mem.get("duration"):
        st.markdown(f"**Duration:** `{mem['duration']}`")
    if mem.get("location"):
        st.markdown(f"**Location:** `{mem['location']}`")
    if mem.get("treatments_applied"):
        st.markdown("**Treatments:**")
        st.markdown(memory_tags(mem["treatments_applied"], "tag tag-med"), unsafe_allow_html=True)
