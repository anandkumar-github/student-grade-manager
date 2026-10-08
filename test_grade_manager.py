import pytest

from grade_manager import Student, calculate_average, determine_grade, format_results


def test_calculate_average():
    assert calculate_average([90, 85, 88]) == 87.67


def test_determine_grade():
    assert determine_grade(95) == "A"
    assert determine_grade(82) == "B"
    assert determine_grade(70) == "C"
    assert determine_grade(58) == "D"
    assert determine_grade(40) == "F"


def test_format_results():
    student = Student("Alice", [90, 85, 88])
    output = format_results([student])
    assert "Alice" in output
    assert "87.67" in output
    assert "B" in output


def test_invalid_mark_rejected():
    with pytest.raises(ValueError):
        Student("Bob", [80, -5, 90])


def test_invalid_name_rejected():
    with pytest.raises(ValueError):
        Student("", [90, 80, 70])
