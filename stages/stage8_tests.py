"""
Stage 8: Unit Testing
=====================
Concepts: pytest, unit testing, test fixtures, assertions

To test your work:
    uv run pytest stages/stage8_tests.py -v

Your Task:
----------
Write comprehensive unit tests for the functions you implemented in previous stages.

Learning Objectives:
- Write unit tests using pytest
- Use test fixtures for shared setup
- Test edge cases and error conditions
- Use assertions effectively
- Understand test coverage
"""

import pytest
from pathlib import Path

import sys
sys.path.insert(0, str(Path(__file__).parent.parent))

from stages.stage1_parsing import parse_ingredients
from stages.stage2_ingredient import Ingredient, create_unknown_ingredient
from stages.stage3_database import IngredientDatabase
from stages.stage5_scoring import calculate_overall_score, get_score_label, count_by_category


class TestStage1Parsing:
    """Tests for Stage 1: Ingredient Parsing"""

    def test_basic_parsing(self):
        """Test basic comma-separated parsing."""
        assert parse_ingredients("Water, Sugar, Salt") == ["water", "sugar", "salt"]

    def test_whitespace_handling(self):
        assert parse_ingredients("  Flour  ,  SUGAR,salt  ") == ["flour", "sugar", "salt"]

    def test_empty_string(self):
        """Test that empty string returns empty list."""
        assert parse_ingredients("") == []

    def test_parenthetical_removal(self):
        """Test that parenthetical content is removed."""
        assert parse_ingredients("Red 40 (for color), Sugar") == ["red 40", "sugar"]

    def test_single_ingredient(self):
        assert parse_ingredients("Water") == ["water"]


class TestStage2Ingredient:
    """Tests for Stage 2: Ingredient Dataclass"""

    def test_ingredient_creation_minimal(self):
        """Test creating an Ingredient with just the name."""
        ing = Ingredient(name="sugar")
        assert ing.category == "unknown"
        assert ing.health_score == 5
        assert ing.found_in_database == False

    def test_ingredient_creation_full(self):
        """Test creating an Ingredient with all fields."""
        ing = Ingredient(name="water", category="healthy", health_score=10,
                         description="Essential", found_in_database=True)
        assert ing.name == "water"
        assert ing.category == "healthy"
        assert ing.health_score == 10
        assert ing.description == "Essential"
        assert ing.found_in_database == True

    def test_create_unknown_ingredient(self):
        """Test the create_unknown_ingredient factory function."""
        ing = create_unknown_ingredient("mystery")
        assert ing.name == "mystery"
        assert ing.category == "unknown"
        assert ing.found_in_database == False

class TestStage3Database:
    """Tests for Stage 3: Ingredient Database"""

    @pytest.fixture
    def database(self):
        """Fixture to provide a loaded database for tests."""
        db_path = Path(__file__).parent.parent / "data" / "ingredients_db.json"
        return IngredientDatabase(str(db_path))

    def test_database_loads(self, database):
        """Test that the database loads successfully."""
        assert len(database) > 0


    def test_lookup_existing_ingredient(self, database):
        """Test looking up an ingredient that exists."""
        result = database.lookup("sugar")
        assert result is not None
        assert "category" in result
        assert "health_score" in result

    def test_lookup_case_insensitive(self, database):
        """Test that lookup is case-insensitive."""
        assert database.lookup("SUGAR") == database.lookup("sugar")

    def test_lookup_nonexistent(self, database):
        """Test looking up an ingredient that doesn't exist."""
        assert database.lookup("unicorn tears") is None

    def test_contains_operator(self, database):
        """Test the 'in' operator with the database."""
        assert "water" in database
        assert "unicorn tears" not in database

class TestStage5Scoring:
    """Tests for Stage 5: Health Scoring"""

    @pytest.fixture
    def sample_ingredients(self):
        """Fixture providing sample ingredients for testing."""
        return [
            Ingredient(name="water", category="healthy", health_score=10,
                      description="Good", found_in_database=True),
            Ingredient(name="sugar", category="harmful", health_score=2,
                      description="Bad", found_in_database=True),
        ]

    def test_calculate_score_empty_list(self):
        """Test score calculation with empty list returns 5.0."""
        assert calculate_overall_score([]) == 5.0



    def test_calculate_score_basic(self, sample_ingredients):
        """Test basic score calculation."""
        assert calculate_overall_score(sample_ingredients) == 6.0


    def test_score_label_excellent(self):
        """Test that scores 8-10 return 'Excellent'."""
        assert get_score_label(8.0) == "Excellent"
        assert get_score_label(9.0) == "Excellent"
        assert get_score_label(10.0) == "Excellent"


    def test_score_label_poor(self):
        """Test that scores 0-3.9 return 'Poor'."""
        assert get_score_label(0.0) == "Poor"
        assert get_score_label(2.0) == "Poor"
        assert get_score_label(3.9) == "Poor"


    def test_count_by_category(self, sample_ingredients):
        """Test counting ingredients by category."""
        counts = count_by_category(sample_ingredients)
        assert counts == {"healthy": 1, "harmful": 1}


def is_implemented() -> bool:
    """Check if this stage is implemented by running a subset of tests."""
    import inspect
    source = inspect.getsource(TestStage1Parsing.test_basic_parsing)
    return "assert" in source and "pass" not in source.split("assert")[0]


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
