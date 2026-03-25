"""
Stage 7: Exception Handling
===========================
Concepts: try/except blocks, custom exceptions, input validation

To test your work:
    uv run python stages/stage7_exceptions.py
    uv run python -m stages.stage7_exceptions

Your Task:
----------
Create custom exceptions and add robust error handling to the application.

Learning Objectives:
- Create custom exception classes
- Use try/except/finally blocks
- Validate inputs and raise appropriate exceptions
- Handle different types of errors gracefully
"""
import time
from typing import Optional


class NutrientScannerError(Exception):
    """Base exception for all Nutrient Scanner errors."""

    pass


class InvalidIngredientError(NutrientScannerError):
    """
    Raised when an ingredient name is invalid.

    An ingredient name is invalid if it:
    - Is empty or only whitespace
    - Contains only numbers
    - Is longer than 100 characters
    """
    def __init__(self, ingredient_name: str):
        self.ingredient_name = ingredient_name
        cleaned = ingredient_name.strip()

        if not cleaned:
            reason = "empty or whitespace only"
        elif len(cleaned) > 100:
            reason = "exceeds 100 characters"
        elif cleaned.isdigit():
            reason = "contains only numbers"
        else:
            reason = "must contain at least one letter"

        super().__init__(f"Invalid ingredient name: '{ingredient_name}' ({reason})")


class DatabaseNotFoundError(NutrientScannerError):
    """
    Raised when the ingredient database file cannot be found.
    """

    def __init__(self, path: str):
        self.path = path
        super().__init__(f"Ingredient database not found at: {path}")


class APIError(NutrientScannerError):
    """
    Raised when there's an error with the Gemini API.
    """
    def __init__(self, message: str, status_code: Optional[int] = None, original_error: Optional[Exception] = None):
        self.status_code = status_code
        self.original_error = original_error
        if status_code:
            message = f"API Error: {message} (status code: {status_code})"
        else:
            message = f"API Error: {message}"
        super().__init__(message)


class ImageProcessingError(NutrientScannerError):
    """
    Raised when there's an error processing an image.
    """

    def __init__(self, message: str, image_size: Optional[int] = None):
        self.image_size = image_size
        if image_size:
            message = f"{message} (image size: {image_size} bytes)"
        super().__init__(message)


def validate_ingredient_name(name: str) -> str:
    """
    Validate and clean an ingredient name.

    Args:
        name: The ingredient name to validate

    Returns:
        The cleaned ingredient name (stripped and lowercased)

    Raises:
        InvalidIngredientError: If the name is invalid

    Validation rules:
    1. Name cannot be empty or whitespace only
    2. Name cannot be only numbers
    3. Name cannot be longer than 100 characters
    4. Name must contain at least one letter

    Example:
        >>> validate_ingredient_name("  Sugar  ")
        'sugar'

        >>> validate_ingredient_name("")
        Raises InvalidIngredientError

        >>> validate_ingredient_name("12345")
        Raises InvalidIngredientError
    """
    cleaned = name.strip()
    if not cleaned:
        raise InvalidIngredientError(name)
    if len(cleaned) > 100:
        raise InvalidIngredientError(name)
    if cleaned.isdigit():
        raise InvalidIngredientError(name)
    if not any(c.isalpha() for c in cleaned):
        raise InvalidIngredientError(name)
    return cleaned.lower()


def safe_parse_ingredients(raw_text: str) -> tuple[list[str], list[str]]:
    """
    Safely parse ingredients, collecting any errors encountered.

    This function attempts to parse and validate each ingredient,
    returning both the valid ingredients and any error messages.

    Args:
        raw_text: Raw comma-separated ingredients text

    Returns:
        A tuple of (valid_ingredients, error_messages)
        - valid_ingredients: List of successfully validated ingredient names
        - error_messages: List of error messages for invalid ingredients

    Example:
        >>> valid, errors = safe_parse_ingredients("Sugar, , 12345, Water")
        >>> valid
        ['sugar', 'water']
        >>> errors
        ["Invalid ingredient: '' - empty or whitespace only",
         "Invalid ingredient: '12345' - contains only numbers"]
    """
    valid_ingredients = []
    error_messages = []
    for item in raw_text.split(","):
        try:
            valid_ingredients.append(validate_ingredient_name(item))
        except InvalidIngredientError as e:
            error_messages.append(str(e))
    return valid_ingredients, error_messages

def safe_api_call(func, *args, max_retries: int = 3, **kwargs):
    """
    Wrapper function to safely call API functions with retry logic.

    Args:
        func: The function to call
        *args: Positional arguments to pass to the function
        max_retries: Maximum number of retry attempts (default 3)
        **kwargs: Keyword arguments to pass to the function

    Returns:
        The result of the function call

    Raises:
        APIError: If all retries fail

    Example:
        >>> result = safe_api_call(extract_text_from_image, image_bytes, max_retries=3)
    """
    last_error = None
    for attempt in range(max_retries):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            last_error = e
            if attempt < max_retries - 1:
                time.sleep(1)
    raise APIError(f"All {max_retries} retries failed", original_error=last_error)


def is_implemented() -> bool:
    """Check if this stage is implemented."""
    try:
        valid, errors = safe_parse_ingredients("Sugar, , Water")
        return len(valid) > 0 or len(errors) > 0
    except Exception:
        return False


if __name__ == "__main__":
    print("Stage 8: Exception Handling")
    print("=" * 40)

    print("\nTesting validate_ingredient_name()...")
    test_cases = [
        ("  Sugar  ", True),
        ("", False),
        ("   ", False),
        ("12345", False),
        ("a" * 101, False),
        ("Red 40", True),
    ]

    for name, should_pass in test_cases:
        try:
            result = validate_ingredient_name(name)
            status = "✓" if should_pass else "✗ (should have raised)"
            print(f"  {status} '{name}' -> '{result}'")
        except InvalidIngredientError as e:
            status = "✓" if not should_pass else "✗ (unexpected error)"
            print(f"  {status} '{name}' -> Error: {e}")

    print("\nTesting safe_parse_ingredients()...")
    raw = "Sugar, , Water, 12345, Salt, " + "a" * 101
    valid, errors = safe_parse_ingredients(raw)
    print(f"  Input: '{raw[:50]}...'")
    print(f"  Valid ingredients: {valid}")
    print(f"  Errors: {errors}")

    print("\nTesting custom exceptions...")
    try:
        raise DatabaseNotFoundError("/path/to/db.json")
    except NutrientScannerError as e:
        print(f"  Caught: {type(e).__name__}: {e}")

    try:
        raise ImageProcessingError("Image too large", image_size=10_000_000)
    except NutrientScannerError as e:
        print(f"  Caught: {type(e).__name__}: {e}")
