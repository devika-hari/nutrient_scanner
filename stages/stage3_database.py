"""
Stage 3: Ingredient Database
============================
Concepts: Dictionaries, JSON, file handling, data structures

To test your work:
    uv run python stages/stage3_database.py

Your Task:
----------
Create an IngredientDatabase class that loads ingredient data from a JSON file
and provides lookup methods.

Learning Objectives:
- Load and parse JSON files
- Work with nested dictionaries
- Implement class methods for data access
- Use the .get() method for safe dictionary access
"""

import json
from pathlib import Path
from typing import Optional


class IngredientDatabase:
    """
    A database of ingredients loaded from a JSON file.

    The JSON file has this structure:
    {
        "ingredients": {
            "sugar": {
                "category": "harmful",
                "health_score": 2,
                "description": "Added sugars contribute to obesity"
            },
            ...
        },
        "categories": {
            "healthy": {"color": "green", "description": "...", "score_range": [7, 10]},
            ...
        }
    }

    Example usage:
        >>> db = IngredientDatabase("data/ingredients_db.json")
        >>> db.lookup("sugar")
        {'category': 'harmful', 'health_score': 2, 'description': '...'}
        >>> db.lookup("unknown_item")
        None
        >>> db.get_all_ingredients()
        ['sugar', 'water', 'salt', ...]
    """

    def __init__(self, json_path: str):
        """
        Initialize the database by loading data from a JSON file.

        Args:
            json_path: Path to the JSON file containing ingredient data

        Raises:
            FileNotFoundError: If the JSON file doesn't exist
            json.JSONDecodeError: If the JSON is invalid
        """
        try:
            with open(json_path, 'r') as f:
                data = json.load(f)
        except FileNotFoundError:
            raise FileNotFoundError(f"Database file not found: {json_path}")
        except json.JSONDecodeError as e:
            raise json.JSONDecodeError(f"Invalid JSON in database file: {json_path}", e.doc, e.pos)

        self._ingredients:dict = data["ingredients"]
        self._categories:dict = data["categories"]

    def lookup(self, ingredient_name: str) -> Optional[dict]:
        """
        Look up an ingredient by name.

        Args:
            ingredient_name: The name of the ingredient to look up (case-insensitive)

        Returns:
            A dictionary with 'category', 'health_score', and 'description' keys,
            or None if the ingredient is not found.

        Example:
            >>> db.lookup("Sugar")  # Note: case-insensitive
            {'category': 'harmful', 'health_score': 2, 'description': '...'}
        """

        return self._ingredients.get(ingredient_name.lower())

    def get_all_ingredients(self) -> list[str]:
        """
        Get a list of all ingredient names in the database.

        Returns:
            A sorted list of all ingredient names.

        Example:
            >>> db.get_all_ingredients()[:3]
            ['almonds', 'apple', 'apple cider vinegar']
        """
        return sorted(self._ingredients.keys())

    def get_category_info(self, category: str) -> Optional[dict]:
        """
        Get information about a category.

        Args:
            category: The category name ("healthy", "moderate", or "harmful")

        Returns:
            A dictionary with 'color', 'description', and 'score_range' keys,
            or None if the category doesn't exist.
        """
        return self._categories.get(category)

    def __len__(self) -> int:
        """Return the number of ingredients in the database."""
        return len(self._ingredients)

    def __contains__(self, ingredient_name: str) -> bool:
        """Check if an ingredient is in the database (case-insensitive)."""
        return ingredient_name.lower() in self._ingredients


def is_implemented() -> bool:
    """Check if this stage is implemented."""
    try:
        db_path = Path(__file__).parent.parent / "data" / "ingredients_db.json"
        db = IngredientDatabase(str(db_path))
        return not getattr(db, "_not_implemented", False) and len(db) > 0
    except Exception:
        return False


if __name__ == "__main__":
    db_path = Path(__file__).parent.parent / "data" / "ingredients_db.json"

    print(f"Loading database from: {db_path}")
    db = IngredientDatabase(str(db_path))

    print(f"\nDatabase contains {len(db)} ingredients")
    print(f"\nFirst 5 ingredients: {db.get_all_ingredients()[:5]}")

    print("\nLooking up 'sugar':")
    result = db.lookup("sugar")
    print(f"  {result}")

    print("\nLooking up 'Sugar' (uppercase):")
    result = db.lookup("Sugar")
    print(f"  {result}")

    print("\nLooking up 'unknown_ingredient':")
    result = db.lookup("unknown_ingredient")
    print(f"  {result}")

    print("\nCategory info for 'healthy':")
    print(f"  {db.get_category_info('healthy')}")

    print("\nUsing 'in' operator:")
    print(f"  'water' in db: {'water' in db}")
    print(f"  'unicorn tears' in db: {'unicorn tears' in db}")
