"""
Nutrient Scanner - Streamlit Application
========================================

A mobile-friendly app to scan food ingredients and analyze their health impact.

To run:
    uv run streamlit run streamlit_app.py

For mobile testing:
    uv run streamlit run streamlit_app.py --server.address 0.0.0.0

Then access from your phone using your computer's IP address.
"""

import os
from pathlib import Path

import streamlit as st

st.set_page_config(
    page_title="Nutrient Scanner",
    page_icon="🥗",
    layout="centered",
    initial_sidebar_state="expanded",
)

st.markdown(
    """
    <style>
    .stApp {
        max-width: 800px;
        margin: 0 auto;
    }
    .stage-complete {
        color: #28a745;
        font-weight: bold;
    }
    .stage-pending {
        color: #6c757d;
    }
    .health-score {
        font-size: 3rem;
        font-weight: bold;
        text-align: center;
        padding: 1rem;
        border-radius: 1rem;
    }
    .score-excellent { background-color: #d4edda; color: #155724; }
    .score-good { background-color: #cce5ff; color: #004085; }
    .score-fair { background-color: #fff3cd; color: #856404; }
    .score-poor { background-color: #f8d7da; color: #721c24; }
    </style>
    """,
    unsafe_allow_html=True,
)

from stages import check_stage_implementation, get_completion_status

DATA_DIR = Path(__file__).parent / "data"
DB_PATH = DATA_DIR / "ingredients_db.json"
README_PATH = Path(__file__).parent / "README.md"


@st.dialog("Assignment Guide", width="large")
def show_assignment_guide():
    """Display the README in a dialog."""
    if README_PATH.exists():
        st.markdown(README_PATH.read_text())
    else:
        st.error("README.md not found")


def show_progress_sidebar():
    """Display assignment progress in the sidebar."""
    with st.sidebar:
        st.header("📊 Assignment Progress")
        status = get_completion_status()

        st.progress(status["percentage"] / 100)
        st.caption(f"{status['completed']}/{status['total']} stages completed")

        st.divider()

        for stage in status["stages"]:
            if stage.is_implemented:
                st.markdown(f"✅ **Stage {stage.number}**: {stage.name}")
            else:
                st.markdown(f"⬜ Stage {stage.number}: {stage.name}")
            st.caption(f"   {stage.concepts}")

        st.divider()
        if st.button("📖 Assignment Guide", use_container_width=True):
            show_assignment_guide()


def get_sample_ingredients() -> str:
    """Return sample ingredients for testing."""
    return """Water, High Fructose Corn Syrup, Sugar, Contains 2% or Less of:
    Citric Acid, Natural Flavors, Salt, Sodium Benzoate (Preservative),
    Red 40, Blue 1"""


def main():
    show_progress_sidebar()

    st.title("🥗 Nutrient Scanner")
    st.markdown("*Scan food ingredients and discover what you're really eating*")

    st.divider()

    input_tab, camera_tab, results_tab = st.tabs(
        ["📝 Enter Text", "📸 Camera/Upload", "📊 Results"]
    )

    st.session_state.setdefault("ingredients_text", "")
    st.session_state.setdefault("analyzed_ingredients", [])
    st.session_state.setdefault("analysis_complete", False)

    with input_tab:
        st.subheader("Enter Ingredients")

        col1, col2 = st.columns([3, 1])
        with col2:
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("📋 Use Sample", use_container_width=True):
                st.session_state.text_input = get_sample_ingredients()
                st.rerun()
            if st.button("🗑️ Clear", use_container_width=True):
                st.session_state.text_input = ""
                st.session_state.analysis_complete = False
                st.rerun()
        with col1:
            ingredients_text = st.text_area(
                "Paste ingredients list here:",
                height=150,
                placeholder="e.g., Water, Sugar, Salt, Natural Flavors...",
                key="text_input",
            )

        if st.button(
            "🔍 Analyze Ingredients", type="primary", use_container_width=True
        ):
            analyze_ingredients_text(st.session_state.get("text_input", ""))

    with camera_tab:
        st.subheader("Take a Photo or Upload")

        st.info(
            "📱 **Mobile Tip:** On your phone, the camera option will open your device camera!"
        )

        input_method = st.radio(
            "Choose input method:",
            ["📷 Camera", "📁 Upload File"],
            horizontal=True,
            label_visibility="collapsed",
        )

        if input_method == "📷 Camera":
            camera_image = st.camera_input(
                "Take a photo of the ingredients list",
                help="Point your camera at the ingredients label",
            )
            if camera_image is not None:
                process_image(camera_image.getvalue())

        else:
            uploaded_file = st.file_uploader(
                "Upload an image of ingredients",
                type=["jpg", "jpeg", "png", "webp"],
                help="Supported formats: JPG, PNG, WebP",
            )
            if uploaded_file is not None:
                st.image(
                    uploaded_file, caption="Uploaded image", use_container_width=True
                )
                process_image(uploaded_file.getvalue())

    with results_tab:
        show_results()


def analyze_ingredients_text(text: str):
    """Analyze the ingredients from text input."""
    if not text.strip():
        st.warning("Please enter some ingredients first!")
        return

    stage1_ok = check_stage_implementation(1)
    stage2_ok = check_stage_implementation(2)
    stage3_ok = check_stage_implementation(3)
    stage4_ok = check_stage_implementation(4)

    if not stage1_ok:
        st.error("⚠️ **Stage 1 not implemented!**")
        st.info(
            "Implement `parse_ingredients()` in `stages/stage1_parsing.py` to continue."
        )
        with st.expander("Preview: What this stage does"):
            st.code(f'Input: "{text[:50]}..."')
            st.code('Output: ["ingredient1", "ingredient2", ...]')
        return

    from stages.stage1_parsing import parse_ingredients

    with st.spinner("Parsing ingredients..."):
        parsed = parse_ingredients(text)

    st.success(f"✅ Parsed {len(parsed)} ingredients")

    with st.expander("Parsed ingredients", expanded=True):
        st.write(parsed)

    if not stage2_ok:
        st.warning("⚠️ **Stage 2 not implemented** - Cannot create Ingredient objects")
        st.info("Implement the `Ingredient` dataclass in `stages/stage2_ingredient.py`")
        return

    if not stage3_ok:
        st.warning("⚠️ **Stage 3 not implemented** - Cannot load ingredient database")
        st.info("Implement `IngredientDatabase` in `stages/stage3_database.py`")
        return

    if not stage4_ok:
        st.warning("⚠️ **Stage 4 not implemented** - Cannot analyze ingredients")
        st.info("Implement `analyze_ingredients()` in `stages/stage4_analyzer.py`")
        return

    from stages.stage3_database import IngredientDatabase
    from stages.stage4_analyzer import analyze_ingredients

    with st.spinner("Analyzing ingredients..."):
        db = IngredientDatabase(str(DB_PATH))
        analyzed = analyze_ingredients(parsed, db)

    st.session_state.analyzed_ingredients = analyzed
    st.session_state.analysis_complete = True

    st.success("✅ Analysis complete! Check the **Results** tab.")
    st.balloons()


def process_image(image_bytes: bytes):
    """Process an uploaded or captured image using Gemini API."""
    try:
        from google import genai
        from google.genai import types
    except ImportError:
        st.error("Google Gen AI package not installed.")
        st.code("uv add google-genai")
        return

    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        api_key = st.text_input(
            "Enter your Gemini API key:",
            type="password",
            help="Get one from https://aistudio.google.com/apikey",
        )
        if not api_key:
            st.warning("Please enter your Gemini API key to extract text from images.")
            with st.expander("How to get a Gemini API key"):
                st.markdown("""
                1. Go to [Google AI Studio](https://aistudio.google.com/apikey)
                2. Sign in with your Google account
                3. Click "Create API Key"
                4. Copy the key and paste it above

                **Tip:** Set `GEMINI_API_KEY` environment variable to avoid entering it each time.
                """)
            return

    with st.spinner("Extracting text from image..."):
        try:
            import base64

            client = genai.Client(api_key=api_key)

            encoded = base64.b64encode(image_bytes).decode("utf-8")
            image_part = types.Part.from_bytes(data=image_bytes, mime_type="image/jpeg")

            prompt = """Look at this image of a food product's ingredients list.
            Extract ONLY the ingredient names as a comma-separated list.
            Do not include any other text, explanations, or formatting.
            Example output: water, sugar, salt, natural flavors"""

            response = client.models.generate_content(
                model="gemini-2.0-flash",
                contents=[prompt, image_part],
            )
            extracted_text = response.text.strip()
        except Exception as e:
            st.error(f"Error extracting text: {e}")
            return

    st.success("✅ Text extracted successfully!")

    with st.expander("Extracted text", expanded=True):
        st.text(extracted_text)

    st.session_state.text_input = extracted_text

    if st.button(
        "🔍 Analyze These Ingredients", type="primary", use_container_width=True
    ):
        analyze_ingredients_text(extracted_text)


def show_results():
    """Display analysis results."""
    if not st.session_state.analysis_complete:
        st.info(
            "No analysis results yet. Enter ingredients or take a photo to get started!"
        )
        return

    analyzed = st.session_state.analyzed_ingredients
    if not analyzed:
        st.warning("No ingredients were analyzed.")
        return

    stage5_ok = check_stage_implementation(5)
    stage6_ok = check_stage_implementation(6)

    st.subheader("Analysis Results")

    if stage5_ok:
        from stages.stage5_scoring import (
            calculate_overall_score,
            count_by_category,
            generate_recommendations,
            get_score_label,
        )

        score = calculate_overall_score(analyzed)
        label = get_score_label(score)
        counts = count_by_category(analyzed)

        score_class = {
            "Excellent": "score-excellent",
            "Good": "score-good",
            "Fair": "score-fair",
            "Poor": "score-poor",
        }.get(label, "")

        st.markdown(
            f'<div class="health-score {score_class}">{score:.1f}/10 - {label}</div>',
            unsafe_allow_html=True,
        )

        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Total", len(analyzed))
        col2.metric("Healthy", counts.get("healthy", 0), delta=None)
        col3.metric("Moderate", counts.get("moderate", 0), delta=None)
        col4.metric("Harmful", counts.get("harmful", 0), delta=None)

        st.divider()

        st.subheader("💡 Recommendations")
        recommendations = generate_recommendations(analyzed)
        for rec in recommendations:
            st.markdown(f"- {rec}")

    else:
        st.warning("⚠️ **Stage 5 not implemented** - Scoring unavailable")
        st.info("Implement scoring functions in `stages/stage5_scoring.py`")

    st.divider()

    st.subheader("📋 Ingredient Details")

    if stage6_ok:
        from stages.stage6_dataframes import ingredients_to_dataframe

        df = ingredients_to_dataframe(analyzed)
        display_df = df[["name", "category", "health_score", "description"]]

        category_filter = st.multiselect(
            "Filter by category:",
            ["healthy", "moderate", "harmful", "unknown"],
            default=["healthy", "moderate", "harmful", "unknown"],
        )

        filtered_df = display_df[display_df["category"].isin(category_filter)]

        sort_by = st.selectbox("Sort by:", ["health_score", "name", "category"])
        ascending = st.checkbox("Ascending order", value=False)

        sorted_df = filtered_df.sort_values(sort_by, ascending=ascending)

        st.dataframe(sorted_df, use_container_width=True, hide_index=True)

    else:
        st.warning("⚠️ **Stage 6 not implemented** - DataFrame display unavailable")
        st.info("Implement DataFrame functions in `stages/stage6_dataframes.py`")

        for ing in analyzed:
            with st.container(border=True):
                col1, col2 = st.columns([3, 1])
                with col1:
                    st.markdown(f"**{ing.name}**")
                    st.caption(getattr(ing, "description", "No description"))
                with col2:
                    category = getattr(ing, "category", "unknown")
                    score = getattr(ing, "health_score", 5)
                    emoji = {"healthy": "🟢", "moderate": "🟡", "harmful": "🔴"}.get(
                        category, "⚪"
                    )
                    st.markdown(f"{emoji} {score}/10")


if __name__ == "__main__":
    main()
