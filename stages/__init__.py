"""
Stages Package
==============

This module provides stage detection and completion tracking for the
Nutrient Scanner assignment.
"""

from typing import NamedTuple


class StageInfo(NamedTuple):
    """Information about a stage."""
    number: int
    name: str
    concepts: str
    module_name: str
    is_implemented: bool


def check_stage_implementation(stage_number: int) -> bool:
    """
    Check if a specific stage is implemented.

    Args:
        stage_number: The stage number (1-8)

    Returns:
        True if the stage is implemented, False otherwise.
    """
    try:
        if stage_number == 1:
            from stages.stage1_parsing import is_implemented
            return is_implemented()
        elif stage_number == 2:
            from stages.stage2_ingredient import is_implemented
            return is_implemented()
        elif stage_number == 3:
            from stages.stage3_database import is_implemented
            return is_implemented()
        elif stage_number == 4:
            from stages.stage4_analyzer import is_implemented
            return is_implemented()
        elif stage_number == 5:
            from stages.stage5_scoring import is_implemented
            return is_implemented()
        elif stage_number == 6:
            from stages.stage6_dataframes import is_implemented
            return is_implemented()
        elif stage_number == 7:
            from stages.stage7_exceptions import is_implemented
            return is_implemented()
        elif stage_number == 8:
            from stages.stage8_tests import is_implemented
            return is_implemented()
        else:
            return False
    except Exception:
        return False


def get_all_stages() -> list[StageInfo]:
    """
    Get information about all stages.

    Returns:
        A list of StageInfo namedtuples with stage details.
    """
    stages = [
        (1, "Parsing", "String manipulation", "stage1_parsing"),
        (2, "Ingredient", "Classes & types", "stage2_ingredient"),
        (3, "Database", "Dictionaries & JSON", "stage3_database"),
        (4, "Analyzer", "Loops & list comprehensions", "stage4_analyzer"),
        (5, "Scoring", "Functions & aggregation", "stage5_scoring"),
        (6, "DataFrames", "Pandas DataFrames", "stage6_dataframes"),
        (7, "Exceptions", "Error handling", "stage7_exceptions"),
        (8, "Tests", "Unit testing", "stage8_tests"),
    ]

    return [
        StageInfo(
            number=num,
            name=name,
            concepts=concepts,
            module_name=module,
            is_implemented=check_stage_implementation(num),
        )
        for num, name, concepts, module in stages
    ]


def get_completion_status() -> dict:
    """
    Get a summary of completion status.

    Returns:
        A dictionary with:
        - completed: Number of completed stages
        - total: Total number of stages
        - percentage: Completion percentage
        - stages: List of StageInfo objects
    """
    stages = get_all_stages()
    completed = sum(1 for s in stages if s.is_implemented)
    total = len(stages)

    return {
        "completed": completed,
        "total": total,
        "percentage": (completed / total) * 100 if total > 0 else 0,
        "stages": stages,
    }


def print_status():
    """Print a formatted status report."""
    status = get_completion_status()

    print("\n" + "=" * 50)
    print("Nutrient Scanner - Assignment Progress")
    print("=" * 50)

    for stage in status["stages"]:
        icon = "✓" if stage.is_implemented else "○"
        print(f"  {icon} Stage {stage.number}: {stage.name}")
        print(f"      Concepts: {stage.concepts}")

    print("-" * 50)
    print(f"Progress: {status['completed']}/{status['total']} stages ({status['percentage']:.0f}%)")
    print("=" * 50 + "\n")


if __name__ == "__main__":
    print_status()
