"""
Stage 1: Parsing Ingredients
============================
Concepts: String manipulation (split, strip, lower)

To test your work:
    uv run python stages/stage1_parsing.py

Your Task:
----------
Implement the `parse_ingredients` function that takes a raw text string
containing ingredients (typically comma-separated) and returns a clean list.

Learning Objectives:
- Use string methods: split(), strip(), lower()
- Filter out empty strings from a list
- Handle edge cases in text processing
"""

def parse_ingredients(raw_text: str) -> list[str]:
    """
    Parse a raw ingredients text into a clean list of ingredient names.

    Requirements:
    1. Split the text by commas
    2. Remove leading/trailing whitespace from each ingredient
    3. Convert all ingredients to lowercase
    4. Remove any empty strings from the result
    5. Remove any parenthetical content like "(for color)" from ingredients

    Args:
        raw_text: A string containing ingredients, typically comma-separated
                  Example: "Water, Sugar, Salt, Natural Flavors (soy)"

    Returns:
        A list of cleaned ingredient names
        Example: ["water", "sugar", "salt", "natural flavors"]

    Examples:
        >>> parse_ingredients("Water, Sugar, Salt")
        ['water', 'sugar', 'salt']

        >>> parse_ingredients("  Flour  ,  SUGAR,salt  ")
        ['flour', 'sugar', 'salt']

        >>> parse_ingredients("Red 40 (for color), Sugar")
        ['red 40', 'sugar']

        >>> parse_ingredients("")
        []
    """
    ingredients = raw_text.split(",")
    result = []
    for ingredient in ingredients:
        cleaned = ingredient.strip().lower()

        # Remove parenthetical content using string indexing
        if "(" in cleaned:
            cleaned = cleaned[:cleaned.index("(")] #stop before (

        cleaned = cleaned.strip()
        if cleaned:
            result.append(cleaned)
    return result


def is_implemented() -> bool:
    """Check if this stage is implemented by testing with sample input."""
    result = parse_ingredients("Water, Sugar, Salt")
    return result != ["__NOT_IMPLEMENTED__"] and len(result) == 3


if __name__ == "__main__":
    test_cases = [
        ("Water, Sugar, Salt", ["water", "sugar", "salt"]),
        ("  Flour  ,  SUGAR,salt  ", ["flour", "sugar", "salt"]),
        ("Red 40 (for color), Sugar", ["red 40", "sugar"]),
        ("", []),
        ("Single", ["single"]),
    ]

    print("Testing parse_ingredients()...")
    for input_text, expected in test_cases:
        result = parse_ingredients(input_text)
        status = "✓" if result == expected else "✗"
        print(f"{status} Input: {repr(input_text)}")
        print(f"  Expected: {expected}")
        print(f"  Got:      {result}")
        print()
