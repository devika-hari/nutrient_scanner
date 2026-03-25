# Nutrient Scanner
_Redi Backend course, Spring 26, Mini project 1._

## Overview

Build a food ingredient analyzer that identifies healthy and harmful ingredients.

In this assignment, you'll implement the core functionality of a Streamlit app that:
- Parses ingredient lists from food labels
- Looks up ingredients in a database
- Analyzes and scores the healthiness of foods
- Displays results in an interactive dashboard

The app scaffolding and UI are provided. Your job is to implement the Python functions that power it.

## Getting Started

### Prerequisites
- Python 3.10 or higher
- [uv](https://docs.astral.sh/uv/) package manager

### Installation

```bash
# Clone or download this project
cd nutrient_scanner

# Install dependencies
uv sync
```

### Running the App

```bash
uv run streamlit run streamlit_app.py
```

The app will open at http://localhost:8501

### Mobile Testing

To test on your phone (great for camera features):

```bash
uv run streamlit run streamlit_app.py --server.address 0.0.0.0
```

Then open `http://<your-computer-ip>:8501` on your phone.

## Assignment Structure

The assignment is divided into **8 stages**. Complete them in order - each stage builds on the previous ones.

| Stage | File | Concepts | Description |
|-------|------|----------|-------------|
| 1 | `stages/stage1_parsing.py` | String manipulation | Parse comma-separated ingredients |
| 2 | `stages/stage2_ingredient.py` | Classes & dataclasses | Create an Ingredient data class |
| 3 | `stages/stage3_database.py` | Dictionaries & JSON | Load and query the ingredient database |
| 4 | `stages/stage4_analyzer.py` | Loops & list comprehensions | Analyze ingredient lists |
| 5 | `stages/stage5_scoring.py` | Functions & aggregation | Calculate health scores |
| 6 | `stages/stage6_dataframes.py` | Pandas DataFrames | Convert results for display |
| 7 | `stages/stage7_exceptions.py` | Exception handling | Add error handling |
| 8 | `stages/stage8_tests.py` | Unit testing | Write pytest tests |

## How to Work on Each Stage

1. **Open the stage file** (e.g., `stages/stage1_parsing.py`)
2. **Read the docstrings** - they explain what to implement
3. **Find the `TODO` comments** - that's where you write code
4. **Test your work** by running the file directly:
   ```bash
   uv run python stages/stage1_parsing.py
   ```
5. **Check the app** - your changes take effect immediately!

## Testing Your Progress

### Check a single stage:
```bash
uv run python stages/stage1_parsing.py
```

### Run the full test suite (after completing Stage 8):
```bash
uv run pytest stages/stage8_tests.py -v
```

### Check overall progress:
```bash
uv run python stages/__init__.py
```

Or just look at the sidebar in the Streamlit app!

## Tips

- **Start with Stage 1** - the app won't work until you complete it
- **Read the examples** in the docstrings carefully
- **Use the test cases** at the bottom of each file to verify your code
- **The app updates live** - save your file and refresh the browser
- **Check the sidebar** to see which stages are complete

## Using the Camera Feature

The app can extract ingredients from photos using Google's Gemini AI:

1. Get a free API key from [Google AI Studio](https://aistudio.google.com/apikey)
2. Either:
   - Enter it in the app when prompted, or
   - Set the environment variable: `export GEMINI_API_KEY="your-key"`

## Project Structure

```
nutrient_scanner/
├── streamlit_app.py          # Main app (provided)
├── pyproject.toml            # Dependencies
├── stages/                   # YOUR CODE GOES HERE
│   ├── stage1_parsing.py
│   ├── stage2_ingredient.py
│   ├── stage3_database.py
│   ├── stage4_analyzer.py
│   ├── stage5_scoring.py
│   ├── stage6_dataframes.py
│   ├── stage7_exceptions.py
│   └── stage8_tests.py
└── data/
    └── ingredients_db.json   # Ingredient database (100+ items)
```

## Need Help?

- Each stage file has detailed docstrings and examples
- Look at the `if __name__ == "__main__"` section for test cases
- The app shows helpful error messages when stages aren't complete

Good luck! 🥗
