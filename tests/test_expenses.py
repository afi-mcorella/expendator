import datetime

from expendator import expenses as ex
from expendator.cli import main


def make_expense(category="food", amount=1250, description="Lunch", day=14):
    return ex.Expense(datetime.date(2025, 3, day), category, amount, description)


# --- logic -----------------------------------------------------------------


def test_add_appends_expense_to_list():
    expenses = []
    ex.add(expenses, make_expense())
    assert len(expenses) == 1


def test_filter_by_category_keeps_only_matching_expenses():
    expenses = [make_expense("food"), make_expense("travel"), make_expense("food")]
    result = ex.filter_by_category(expenses, "food")
    assert [e.category for e in result] == ["food", "food"]


def test_filter_by_category_with_no_match_returns_empty_list():
    assert ex.filter_by_category([make_expense("food")], "travel") == []


def test_total_sums_amounts_in_cents():
    expenses = [make_expense(amount=1250), make_expense(amount=1999)]
    assert ex.total(expenses) == 3249


def test_total_of_empty_list_is_zero():
    assert ex.total([]) == 0


def test_format_amount_with_euros_and_cents():
    assert ex.format_amount(1205) == "12,05 €"


def test_format_amount_with_two_digit_cents():
    assert ex.format_amount(1250) == "12,50 €"


def test_save_then_load_returns_same_expenses(tmp_path):
    path = tmp_path / "data.json"
    expenses = [make_expense("food", 1250), make_expense("travel", 4599, "Train")]
    ex.save(path, expenses)
    assert ex.load(path) == expenses


def test_load_of_missing_file_returns_empty_list(tmp_path):
    assert ex.load(tmp_path / "missing.json") == []


# --- command line ----------------------------------------------------------


def run(path, *args):
    return main(["--file", str(path), *args])


def test_cli_add_stores_expense_in_file(tmp_path):
    path = tmp_path / "data.json"
    ex.save(path, [])
    run(path, "add", "food", "12,50", "Lunch", "--date", "2025-03-14")
    stored = ex.load(path)
    assert stored == [make_expense("food", 1250, "Lunch")]


def test_cli_list_shows_stored_expenses(tmp_path, capsys):
    path = tmp_path / "data.json"
    ex.save(path, [make_expense("food", 1250, "Lunch")])
    run(path, "list")
    out = capsys.readouterr().out
    assert "Lunch" in out and "12,50 €" in out


def test_cli_total_filters_by_category(tmp_path, capsys):
    path = tmp_path / "data.json"
    ex.save(path, [make_expense("food", 1250), make_expense("travel", 4599)])
    run(path, "total", "--category", "food")
    assert "Total: 12,50 €" in capsys.readouterr().out
