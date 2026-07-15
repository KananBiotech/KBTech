"""
doctor_agent.py - The brain of the medical assistant.

Uses Groq (llama-3.1-70b) for:
  1. Extracting structured clinical data from free-text patient input
  2. Asking intelligent follow-up questions (like a doctor)
  3. Detecting emergencies
  4. Generating diagnosis summary + medicine recommendations (RAG-enhanced)
"""

import json
import re
import os
from typing import Dict, Any, Tuple
from groq import Groq
from memory import PatientMemory
from rag_engine import MedicalRAG

# ── Prompts ────────────────────────────────────────────────────────────────

SYSTEM_PROMPT = """You are Dr. MedAssist, an experienced, empathetic medical AI assistant.
Your role:
1. Extract clinical information from patient messages (symptoms, duration, severity, age, gender, vitals, history).
2. Ask targeted follow-up questions like a real doctor — one or two at a time, not a flood.
3. Detect emergencies immediately and give clear guidance.
4. Once you have enough data, generate a differential diagnosis and recommend medicines (both affordable and premium options).
5. ONLY answer medical/health questions. For any non-medical question, politely decline and redirect.

CRITICAL RULES:
- Never diagnose definitively — always say "likely" or "possibly" and recommend seeing a doctor for confirmation.
- Always ask about: age, gender, symptom duration, severity, allergies, current meds if not provided.
- Emergency red flags: chest pain + shortness of breath, stroke symptoms (FAST), severe head injury, anaphylaxis, uncontrolled bleeding, unconsciousness.
- Be warm, professional, and easy to understand.
- Use simple language, avoid medical jargon unless explaining it.
"""

EXTRACTION_PROMPT = """Extract ALL medical/clinical information from the patient's message.
Return ONLY valid JSON with these keys (use null if not mentioned):
{{
  "symptoms": ["list", "of", "symptoms"],
  "duration": "how long symptoms have been present",
  "severity": "mild/moderate/severe or null",
  "age": "patient age",
  "gender": "male/female/other",
  "temperature": "body temperature if mentioned",
  "medical_history": ["past conditions or null"],
  "allergies": ["known allergies"],
  "current_medications": ["current medications"],
  "additional_notes": ["any other medically relevant info"],
  "is_emergency": true/false
}}

Patient message: "{message}"
Previous context: {context}
"""

DOCTOR_CONVERSATION_PROMPT = """You are Dr. MedAssist. 
Current patient data collected so far:
{clinical_summary}

Conversation stage: {stage}
Questions asked so far: {questions_asked}
Follow-up questions remaining: {follow_up_remaining}

Guidelines:
- Stage "greeting": Warmly greet and ask what's bothering them.
- Stage "collecting_symptoms": Extract symptoms, ask about duration and severity.
- Stage "clarifying": Ask 1-2 targeted clarifying questions (age, gender, fever temp, associated symptoms).
  * If follow_up_remaining == 0, move to diagnosis regardless.
- Stage "diagnosis": Summarize findings, give likely diagnosis.
- Stage "recommending": Recommend medicines with dosage. Include both cheap generic and branded options.
- Stage "closed": Offer to answer follow-up questions.

RAG context from Standard Treatment Guidelines:
{rag_context}

IMPORTANT: 
- If is_emergency=True, IMMEDIATELY provide emergency guidance and emergency contacts.
- Only answer health/medical questions. For others: "I can only assist with medical questions."
- Recommend doctor visit for confirmation.
"""


class DoctorAgent:
    def __init__(self, groq_api_key: str, rag: MedicalRAG = None):
        self.client = Groq(api_key=groq_api_key)
        self.rag = rag or MedicalRAG()  # works even without PDF
        self.model = "llama-3.1-70b-versatile"   # best free Groq model

    def _call_groq(self, messages: list, temperature: float = 0.3, max_tokens: int = 1024) -> str:
        """Call Groq API."""
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens,
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            return f"⚠️ API error: {str(e)}. Please check your GROQ_API_KEY."

    def extract_clinical_data(self, user_message: str, memory: PatientMemory) -> Dict[str, Any]:
        """Extract structured clinical data from the user's message."""
        prompt = EXTRACTION_PROMPT.format(
            message=user_message,
            context=memory.get_clinical_summary()
        )
        messages = [
            {"role": "system", "content": "You are a medical data extractor. Return ONLY valid JSON."},
            {"role": "user", "content": prompt}
        ]
        raw = self._call_groq(messages, temperature=0.1, max_tokens=512)
        
        # Parse JSON from response
        try:
            # find JSON block
            match = re.search(r'\{.*\}', raw, re.DOTALL)
            if match:
                return json.loads(match.group())
        except (json.JSONDecodeError, AttributeError):
            pass
        return {}

    def update_memory(self, extracted: Dict[str, Any], memory: PatientMemory):
        """Merge extracted data into memory (additive, never overwrites with None)."""
        if extracted.get("symptoms"):
            new_syms = [s for s in extracted["symptoms"] if s not in memory.symptoms]
            memory.symptoms.extend(new_syms)
        for field in ["duration", "severity", "age", "gender", "temperature"]:
            val = extracted.get(field)
            if val and val != "null":
                setattr(memory, field, val)
        for list_field in ["medical_history", "allergies", "current_medications", "additional_notes"]:
            items = extracted.get(list_field) or []
            existing = getattr(memory, list_field)
            for item in items:
                if item and item not in existing:
                    existing.append(item)
        if extracted.get("is_emergency"):
            memory.is_emergency = True

    def decide_next_stage(self, memory: PatientMemory) -> str:
        """State machine to advance the conversation stage."""
        if memory.is_emergency:
            return "emergency"
        if memory.stage == "greeting":
            if memory.symptoms:
                return "clarifying"
            return "greeting"
        if memory.stage in ("collecting_symptoms", "clarifying"):
            # Enough info to diagnose?
            has_basics = bool(memory.symptoms and memory.duration)
            ran_out_of_questions = memory.follow_up_questions_remaining <= 0
            if has_basics or ran_out_of_questions:
                return "diagnosis"
            return "clarifying"
        if memory.stage == "diagnosis":
            return "recommending"
        if memory.stage == "recommending":
            return "closed"
        return memory.stage

    def generate_response(self, user_message: str, memory: PatientMemory) -> Tuple[str, str]:
        """
        Main entry point.
        Returns (assistant_response, new_stage)
        """
        # 1. Extract clinical data
        extracted = self.extract_clinical_data(user_message, memory)
        self.update_memory(extracted, memory)

        # 2. Decide stage
        new_stage = self.decide_next_stage(memory)
        memory.stage = new_stage

        # 3. Retrieve RAG context
        rag_query = " ".join(memory.symptoms[:5]) if memory.symptoms else user_message
        rag_context = self.rag.retrieve(rag_query)
        if not rag_context:
            rag_context = "No specific guideline retrieved. Use general medical knowledge."

        # 4. Build LLM messages
        system = SYSTEM_PROMPT + "\n\n" + DOCTOR_CONVERSATION_PROMPT.format(
            clinical_summary=memory.get_clinical_summary(),
            stage=new_stage,
            questions_asked=memory.questions_asked,
            follow_up_remaining=memory.follow_up_questions_remaining,
            rag_context=rag_context[:1500],   # cap to avoid token overflow
        )

        llm_messages = [{"role": "system", "content": system}]
        llm_messages += memory.get_history_for_llm()
        llm_messages.append({"role": "user", "content": user_message})

        # 5. Call LLM
        response = self._call_groq(llm_messages, temperature=0.4, max_tokens=1024)

        # 6. Update memory
        memory.add_message("user", user_message)
        memory.add_message("assistant", response)
        memory.questions_asked += 1
        if new_stage == "clarifying":
            memory.follow_up_questions_remaining = max(0, memory.follow_up_questions_remaining - 1)

        # Save summaries when available
        if new_stage in ("diagnosis", "recommending", "closed"):
            if not memory.diagnosis_summary:
                memory.diagnosis_summary = response
            else:
                memory.recommended_medicines = response

        return response, new_stage

    def check_non_medical(self, user_message: str) -> bool:
        """Quick check if user is asking something non-medical."""
        non_medical_keywords = [
            "weather", "news", "sports", "movie", "song", "recipe", "math",
            "code", "programming", "politics", "stock", "crypto", "game",
            "translate", "history", "geography", "celebrity"
        ]
        msg_lower = user_message.lower()
        return any(kw in msg_lower for kw in non_medical_keywords)
