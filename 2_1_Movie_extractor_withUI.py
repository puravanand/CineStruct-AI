import streamlit as st

from dotenv import load_dotenv
load_dotenv()

from langchain_groq import ChatGroq

llm = ChatGroq(model="openai/gpt-oss-20b")

from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field
from typing import List, Optional


# ============================================================
# YOUR ORIGINAL CORE CODE — UNCHANGED
# ============================================================

class Structure_data(BaseModel):
    Name: str = Field(description="Name of the Movie")
    cast: List[str]
    release_year: Optional[int]
    Director: str
    Actress: List[str]
    Total_cost: int
    Total_Earn: int
    Language: str
    genre: List[str]


prompts = ChatPromptTemplate.from_messages([
    {
        "role": "system",
        "content": "You are the Novie Extractor Data Agent, you have to extract the Movie details from the given input"
    },
    {
        "role": "user",
        "content": "{question}"
    }
])


# ============================================================
# STREAMLIT PAGE
# ============================================================

st.set_page_config(
    page_title="CineStruct AI",
    page_icon="🎬",
    layout="wide"
)


# ============================================================
# CUSTOM UI
# ============================================================

st.markdown("""
<style>

.stApp {
    background: #f7f8fc;
}

/* ================= HEADER ================= */

.main-title {
    text-align: center;
    font-size: 48px;
    font-weight: 800;
    color: #111827;
    margin-top: 15px;
    margin-bottom: 5px;
}

.subtitle {
    text-align: center;
    font-size: 17px;
    color: #64748b;
    margin-bottom: 40px;
}


/* ================= SECTION TITLE ================= */

.section-title {
    font-size: 25px;
    font-weight: 750;
    color: #111827;
    margin-top: 20px;
    margin-bottom: 15px;
}


/* ================= INPUT ================= */

.stTextArea textarea {
    background-color: #ffffff !important;
    color: #111827 !important;

    border: 1px solid #d9dee8 !important;
    border-radius: 14px !important;

    font-size: 16px !important;
    line-height: 1.6 !important;

    padding: 18px !important;

    box-sizing: border-box !important;

    width: 100% !important;
    max-width: 100% !important;

    overflow-wrap: anywhere !important;
    word-break: break-word !important;
}

.stTextArea textarea:focus {
    border: 1px solid #7c3aed !important;
    box-shadow: 0 0 0 1px #7c3aed !important;
}


/* ================= BUTTON ================= */

.stButton > button {
    border-radius: 12px !important;
    height: 52px !important;

    font-size: 16px !important;
    font-weight: 700 !important;

    width: 100% !important;
}


/* ================= RESULT CARDS ================= */

.result-card {
    background: #ffffff;

    padding: 21px;

    border-radius: 15px;

    border: 1px solid #e2e6ee;

    box-shadow: 0 5px 20px rgba(15, 23, 42, 0.05);

    width: 100%;
    max-width: 100%;

    box-sizing: border-box;

    overflow-wrap: anywhere;
    word-break: break-word;

    margin-bottom: 18px;
}


/* ================= TOP FIELD ================= */

.field-title {
    font-size: 12px;

    color: #64748b;

    font-weight: 700;

    text-transform: uppercase;

    letter-spacing: 0.7px;

    margin-bottom: 8px;
}

.field-value {
    font-size: 21px;

    color: #111827;

    font-weight: 750;

    line-height: 1.35;

    overflow-wrap: anywhere;
    word-break: break-word;
}


/* ================= LIST CARD ================= */

.list-card {
    background: #ffffff;

    padding: 22px;

    border-radius: 15px;

    border: 1px solid #e2e6ee;

    box-shadow: 0 5px 20px rgba(15, 23, 42, 0.05);

    width: 100%;
    max-width: 100%;

    box-sizing: border-box;

    min-height: 220px;

    overflow-wrap: anywhere;
    word-break: break-word;
}

.list-title {
    font-size: 20px;

    font-weight: 750;

    color: #111827;

    margin-bottom: 16px;
}

.list-item {
    font-size: 15px;

    color: #374151;

    line-height: 1.65;

    margin-bottom: 6px;

    overflow-wrap: anywhere;
    word-break: break-word;
}


/* ================= JSON ================= */

[data-testid="stJson"] {
    width: 100% !important;
    max-width: 100% !important;

    box-sizing: border-box !important;
}


/* ================= FOOTER ================= */

.footer {
    text-align: center;

    color: #64748b;

    font-size: 14px;

    margin-top: 50px;

    padding-top: 22px;

    border-top: 1px solid #e2e6ee;

    line-height: 1.8;
}

.footer-name {
    color: #111827;

    font-weight: 700;
}


/* ================= RESPONSIVE ================= */

@media (max-width: 900px) {

    .main-title {
        font-size: 38px;
    }

    .subtitle {
        font-size: 15px;
    }

    .field-value {
        font-size: 18px;
    }

}

</style>
""", unsafe_allow_html=True)


# ============================================================
# HEADER
# ============================================================

st.markdown(
    '<div class="main-title">🎬 CineStruct AI</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">'
    'Intelligent Movie Information Extraction & Structured Data'
    '</div>',
    unsafe_allow_html=True
)


# ============================================================
# INPUT
# ============================================================

st.markdown(
    '<div class="section-title">📝 Movie Information</div>',
    unsafe_allow_html=True
)

query = st.text_area(
    "Movie Information",
    placeholder=(
        "Enter movie information here...\n\n"
        "Example: The movie Dangal is a Hindi sports drama "
        "directed by Nitesh Tiwari and released in 2016..."
    ),
    height=230,
    label_visibility="collapsed"
)


# ============================================================
# BUTTON
# ============================================================

st.write("")

button_col1, button_col2, button_col3 = st.columns(
    [1, 1.15, 1],
    gap="large"
)

with button_col2:

    extract = st.button(
        "🎬  Extract Movie Details",
        use_container_width=True,
        type="primary"
    )


# ============================================================
# YOUR ORIGINAL PROCESS
# ============================================================

if extract:

    if not query.strip():

        st.warning("Please enter movie information first.")

    else:

        with st.spinner("Extracting movie information..."):

            final_promts = prompts.invoke({
                "question": query
            })

            structure_llm = llm.with_structured_output(
                Structure_data
            )

            res = structure_llm.invoke(
                final_promts
            )


        # ====================================================
        # RESULT
        # ====================================================

        st.markdown(
            '<div class="section-title">✨ Movie Details</div>',
            unsafe_allow_html=True
        )


        # ====================================================
        # BASIC INFORMATION
        # ====================================================

        col1, col2, col3, col4 = st.columns(
            4,
            gap="large",
            vertical_alignment="top"
        )


        with col1:

            st.markdown(
                '<div class="result-card">'
                '<div class="field-title">Movie</div>'
                f'<div class="field-value">{res.Name}</div>'
                '</div>',
                unsafe_allow_html=True
            )


        with col2:

            st.markdown(
                '<div class="result-card">'
                '<div class="field-title">Release Year</div>'
                f'<div class="field-value">{res.release_year}</div>'
                '</div>',
                unsafe_allow_html=True
            )


        with col3:

            st.markdown(
                '<div class="result-card">'
                '<div class="field-title">Director</div>'
                f'<div class="field-value">{res.Director}</div>'
                '</div>',
                unsafe_allow_html=True
            )


        with col4:

            st.markdown(
                '<div class="result-card">'
                '<div class="field-title">Language</div>'
                f'<div class="field-value">{res.Language}</div>'
                '</div>',
                unsafe_allow_html=True
            )


        # ====================================================
        # CAST / ACTRESS / GENRE
        # ====================================================

        st.markdown(
            '<div class="section-title">🎭 Cast & Classification</div>',
            unsafe_allow_html=True
        )


        col1, col2, col3 = st.columns(
            3,
            gap="large",
            vertical_alignment="top"
        )


        # ----------------------------------------------------
        # CAST
        # ----------------------------------------------------

        with col1:

            cast_items = ""

            for person in res.cast:
                cast_items += (
                    f'<div class="list-item">• {person}</div>'
                )

            st.markdown(
                '<div class="list-card">'
                '<div class="list-title">🎭 Cast</div>'
                f'{cast_items}'
                '</div>',
                unsafe_allow_html=True
            )


        # ----------------------------------------------------
        # ACTRESS
        # ----------------------------------------------------

        with col2:

            actress_items = ""

            for person in res.Actress:
                actress_items += (
                    f'<div class="list-item">• {person}</div>'
                )

            st.markdown(
                '<div class="list-card">'
                '<div class="list-title">👩 Actress</div>'
                f'{actress_items}'
                '</div>',
                unsafe_allow_html=True
            )


        # ----------------------------------------------------
        # GENRE
        # ----------------------------------------------------

        with col3:

            genre_items = ""

            for genre in res.genre:
                genre_items += (
                    f'<div class="list-item">• {genre}</div>'
                )

            st.markdown(
                '<div class="list-card">'
                '<div class="list-title">🎞️ Genre</div>'
                f'{genre_items}'
                '</div>',
                unsafe_allow_html=True
            )


        # ====================================================
        # FINANCIAL INFORMATION
        # ====================================================

        st.markdown(
            '<div class="section-title">💰 Financial Information</div>',
            unsafe_allow_html=True
        )


        col1, col2 = st.columns(
            2,
            gap="large",
            vertical_alignment="top"
        )


        with col1:

            st.markdown(
                '<div class="result-card">'
                '<div class="field-title">Total Cost</div>'
                f'<div class="field-value">₹ {res.Total_cost} Crore</div>'
                '</div>',
                unsafe_allow_html=True
            )


        with col2:

            st.markdown(
                '<div class="result-card">'
                '<div class="field-title">Total Earnings</div>'
                f'<div class="field-value">₹ {res.Total_Earn} Crore</div>'
                '</div>',
                unsafe_allow_html=True
            )


        # ====================================================
        # STRUCTURED JSON
        # ====================================================

        st.markdown(
            '<div class="section-title">📦 Structured Data</div>',
            unsafe_allow_html=True
        )


        st.json(
            res.model_dump(),
            expanded=True
        )


# ============================================================
# FOOTER
# ============================================================

st.markdown(
    '<div class="footer">'
    '<span class="footer-name">Made by Purav Anand</span>'
    '<br>'
    'Powered by Groq LLM • GenAI • Pydantic'
    '</div>',
    unsafe_allow_html=True
)