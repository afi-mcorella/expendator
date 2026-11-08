"""Command-line interface (argparse)."""

import argparse
import datetime
from decimal import Decimal, InvalidOperation

from . import expenses as ex

DEFAULT_FILE = "expenses.json"


def parse_amount(text):
    """Convert text such as '12,05' or '12.05' (euros) into cents."""
    try:
        value = Decimal(text.replace(",", "."))
    except InvalidOperation:
        raise argparse.ArgumentTypeError(f"importe no válido: {text!r}")
    return int(value * 100)


def build_parser():
    parser = argparse.ArgumentParser(
        prog="expendator", description="Gestor de gastos personales."
    )
    parser.add_argument(
        "--file", default=DEFAULT_FILE, help="archivo JSON de gastos"
    )
    sub = parser.add_subparsers(dest="command", required=True)

    p_add = sub.add_parser("add", help="añadir un gasto")
    p_add.add_argument("category", help="categoría del gasto")
    p_add.add_argument("amount", type=parse_amount, help="importe en euros")
    p_add.add_argument("description", help="descripción del gasto")
    p_add.add_argument(
        "--date",
        type=datetime.date.fromisoformat,
        default=None,
        help="fecha AAAA-MM-DD (por defecto, hoy)",
    )

    p_list = sub.add_parser("list", help="listar los gastos")
    p_list.add_argument("--category", help="filtrar por categoría")

    p_total = sub.add_parser("total", help="mostrar el total")
    p_total.add_argument("--category", help="filtrar por categoría")
    return parser


def main(argv=None):
    args = build_parser().parse_args(argv)
    expenses = ex.load(args.file)

    if args.command == "add":
        expense = ex.Expense(
            date=args.date or datetime.date.today(),
            category=args.category,
            amount=args.amount,
            description=args.description,
        )
        ex.add(expenses, expense)
        ex.save(args.file, expenses)
        print(f"Gasto añadido: {ex.format_amount(expense.amount)} en {expense.category}.")
        return 0

    if args.category:
        expenses = ex.filter_by_category(expenses, args.category)

    if args.command == "list":
        if not expenses:
            print("No hay gastos.")
        for e in expenses:
            print(
                f"{e.date.isoformat()}  {e.category:<12} "
                f"{ex.format_amount(e.amount):>10}  {e.description}"
            )
        return 0

    print(f"Total: {ex.format_amount(ex.total(expenses))}")
    return 0
