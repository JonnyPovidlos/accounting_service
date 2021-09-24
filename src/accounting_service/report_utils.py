from datetime import date
from typing import Optional

from fastapi import Query


class ReportRecord:
    def __init__(self, key):
        self.key = key
        self.children = {}
        self.amounts = {}
        self.total = 0

    def add_row(self, path, date, amount):
        self.amounts[date] = self.amounts.setdefault(date, 0) + amount
        self.total += amount
        if path:
            path_key = path.pop(0)
            child = self.children.setdefault(path_key, ReportRecord(path_key))
            child.add_row(path, date, amount)

    def make_amounts_per_date(self, time_points):
        for time_point in time_points:
            self.amounts.setdefault(time_point, 0)
        for child in self.children.values():
            child.make_amounts_per_date(time_points)

    def as_dict(self):
        date_list = [date for date in self.amounts.keys()]
        date_list.sort()
        result = {
            'name': self.key,
            'amounts': [self.amounts[date] for date in date_list],
            'total': self.total
        }
        if self.children:
            result.update({
                'children': [self.children[child].as_dict()
                             for child in self.children]})
        return result


def make_date_range(min_date, max_date):
    result = []
    current = min_date
    while current <= max_date:
        result.append(current)
        next_month = current.month + 1
        current = date(current.year + next_month // 12, (next_month - 1) % 12 + 1, 1)
    return result


def parse_list_shops(args: str = Query(None, alias='shops')) -> Optional[list[int]]:
    if args is None:
        return
    return [int(arg) for arg in args.split(',')]


def parse_list_categories(args: str = Query(None, alias='categories')) -> Optional[list[int]]:
    if args is None:
        return
    return [int(arg) for arg in args.split(',')]
