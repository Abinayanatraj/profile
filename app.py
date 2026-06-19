# app.py

import streamlit as st

from src.classifier import classify_persona
from src.rag_pipeline import RAGPipeline
from src.generator import generate_response
from src.escalator import (
    needs_escalation,
    generate_handoff
)

st.set_page_config(
    page_title="Persona Support Agent",
    layout="wide"
)

st.title(
    "🤖 Persona Adaptive Customer Support Agent"
)

rag = RAGPipeline()

user_query = st.text_area(
    "Enter your support request"
)

if st.button("Submit"):

    persona_result = classify_persona(
        user_query
    )

    persona = persona_result["persona"]

    docs = rag.retrieve(
        user_query,
        top_k=3
    )

    st.subheader("Detected Persona")

    st.write(persona)

    st.subheader("Retrieved Sources")

    for d in docs:

        st.write(
            f"{d['source']} | Score: {d['score']:.2f}"
        )

    if needs_escalation(
        user_query,
        docs
    ):

        st.error(
            "Escalated to Human Agent"
        )

        st.json(
            generate_handoff(
                persona,
                user_query,
                docs
            )
        )

    else:

        answer = generate_response(
            user_query,
            persona,
            docs
        )

        st.success("Response")

        st.write(answer)