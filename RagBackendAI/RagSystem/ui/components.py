# ui/components.py — Reusable HTML Components
# ─────────────────────────────────────────────────────────────


def app_header(name: str, subtitle: str, icon: str = "🐟") -> str:
    return f"""
<div class="app-header">
  <span style="font-size:2.2rem;">{icon}</span>
  <div>
    <h1>{name}</h1>
    <p>{subtitle}</p>
  </div>
</div>"""


def welcome_box() -> str:
    return """
<div class="welcome-box">
  <h2>HOW CAN I HELP YOU TODAY?</h2>
  <p>
    Ask me about pond management, fish species selection, water quality, or disease control.
    I'll provide expert guidance backed by our <strong style="color:#4db6ac;">Aquafarming Knowledge Base</strong>.
  </p>
  <div class="feature-row">
    <span class="feature-chip">🌊 Water Quality</span>
    <span class="feature-chip">🐟 Species Expert</span>
    <span class="feature-chip rag">📖 RAG-backed Answers</span>
    <span class="feature-chip">⚖️ Feeding Guide</span>
    <span class="feature-chip">🚨 Crisis Management</span>
    <span class="feature-chip">🚜 Agriculture Tech</span>
  </div>
</div>"""


def emergency_banner(message: str = "") -> str:
    body = message or (
        "Critical situation detected! Check Dissolved Oxygen (DO) levels immediately and ensure aeration is active. "
        "Consult a fisheries expert if mass mortality occurs."
    )
    return f"""
<div class="emergency-wrap">
  <h3>🚨 CRITICAL ALERT</h3>
  <p>{body}</p>
</div>"""


def user_message(content: str) -> str:
    return f"""
<div class="msg-wrap">
  <div class="msg-user">
    <div class="msg-label lbl-user">👤 FARMER</div>
    {content}
  </div>
</div>"""


def ai_message(content: str, rag_used: bool = False) -> str:
    badge = '<span class="rag-badge">📖 KNOWLEDGE BASE</span>' if rag_used else ""
    return f"""
<div class="msg-wrap">
  <div class="msg-ai">
    <div class="msg-label lbl-ai">🐟 AQUA EXPERT {badge}</div>
    {content}
  </div>
</div>"""


def emergency_message(content: str) -> str:
    clean = content.replace("[EMERGENCY]", "").strip()
    return f"""
<div class="emergency-wrap">
  <h3>🚨 CRITICAL ACTION REQUIRED</h3>
  <p>{clean}</p>
</div>"""


def stg_sources_panel(rag_results: list) -> str:
    """
    Shows the Knowledge Base references used for the last response.
    """
    if not rag_results:
        return ""

    refs = ""
    for i, r in enumerate(rag_results, 1):
        excerpt = r.get("text", "")[:180].strip() + "..."
        score   = r.get("score", 0)
        page    = r.get("page", "?")
        refs += f"""
<div class="stg-ref">
  <div class="stg-meta">Reference {i} &nbsp;·&nbsp; Page {page} &nbsp;·&nbsp; {score:.0%} match</div>
  {excerpt}
</div>"""

    return f"""
<div class="stg-panel">
  <div class="stg-panel-title">📖 Knowledge Base Sources Used</div>
  {refs}
</div>"""


def rag_status_box(status: dict) -> str:
    """Renders the RAG status in the sidebar."""
    if not status:
        return ""
    msg = status.get("message", "")
    src = status.get("source", "error")
    chunks = status.get("chunks", 0)

    if status.get("success"):
        source_label = "Cached index" if src == "cache" else "Built from Files"
        return f"""
<div class="rag-status-ok">
  ✅ Knowledge Base Ready<br>
  <span style="font-size:0.65rem;opacity:0.8;">{chunks} knowledge chunks · {source_label}</span>
</div>"""
    elif src == "building":
        return '<div class="rag-building">⏳ Building Knowledge Index... (first time only)</div>'
    else:
        return f'<div class="rag-status-err">⚠️ {msg}</div>'


def rag_not_loaded_warning() -> str:
    return """
<div class="rag-status-warn">
  ⚠️ <strong>Knowledge Base not loaded.</strong><br>
  Place your PDF documents in the <code>data/FishAquafarming/PDF</code> folder and restart.
</div>"""


def stage_badge(label: str, is_emergency: bool = False) -> str:
    cls = "stage-badge emergency" if is_emergency else "stage-badge"
    return f'<div class="{cls}">{label}</div>'


def status_dot(connected: bool) -> str:
    if connected:
        return '<span class="dot dot-on"></span>Connected'
    return '<span class="dot dot-off"></span>Enter API key to start'


def memory_tags(items: list, tag_class: str) -> str:
    return "".join(f'<span class="tag {tag_class}">{i}</span>' for i in items)


def sidebar_disclaimer() -> str:
    return """
<div style="font-size:0.72rem; color:#4a6080; line-height:1.65; margin-top:1rem;">
  ⚠️ <strong style="color:#64748b;">Disclaimer:</strong> This AI provides
  guidance for aquaculture management. Field conditions vary; always consult
  with local fisheries officers or specialists.
  <br><br>
  🆓 Free Groq API key:<br>
  <a href="https://console.groq.com" target="_blank" style="color:#00d4ff;">console.groq.com</a>
</div>"""


def input_hint() -> str:
    return (
        '<p style="color:#4a6080; font-size:0.73rem; text-align:right; margin-top:4px;">'
        'Click SEND to submit &nbsp;•&nbsp; Monitor water quality regularly</p>'
    )
