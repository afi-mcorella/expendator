"""Expense model and business logic. Amounts are integer cents."""

import datetime
import json
from dataclasses import dataclass
from pathlib import Path


@dataclass
class Expense:
    date: datetime.date
    category: str
    amount: int  # cents
    description: str


def load(path):
    """Read the expenses stored in a JSON file."""
    with open(path, encoding="utf-8") as f:
        data = json.load(f)
    return [
        Expense(
            date=datetime.date.fromisoformat(item["date"]),
            category=item["category"],
            amount=item["amount"],
            description=item["description"],
        )
        for item in data
    ]


def save(path, expenses):
    """Write the expenses to a JSON file."""
    data = [
        {
            "date": e.date.isoformat(),
            "category": e.category,
            "amount": e.amount,
            "description": e.description,
        }
        for e in expenses
    ]
    Path(path).write_text(
        json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8"
    )


def add(expenses, expense):
    """Append an expense to the list."""
    expenses.append(expense)


def filter_by_category(expenses, category):
    """Return the expenses whose category matches exactly."""
    return [e for e in expenses if e.category == category]


def total(expenses):
    """Sum of the amounts, in cents."""
    return sum(e.amount for e in expenses)


def format_amount(cents):
    """Format cents as a string such as '12,05 €'."""
    euros, rest = divmod(cents, 100)
    return f"{euros},{rest:02d} €"
