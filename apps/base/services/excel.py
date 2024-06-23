import pandas as pd

from apps.common.models import Category, Group, Keyword
from apps.customers.models import Customer


def import_keyword_from_excel(file, is_import_to_all: bool = True, customer_id: int | None = None):
    df = pd.read_excel(file)
    for index, row in df.iterrows():
        keyword_name = row["KeyWord"]
        category = row["Category"]

        category = Category.objects.get_or_create(name=category)

        if is_import_to_all:
            customers = Customer.objects.all()
            for customer in customers:
                Keyword.objects.get_or_create(name=keyword_name, customer=customer, defaults={"category": category})

        else:
            Group.objects.get_or_create(name=keyword_name, customer_id=customer_id, defaults={"category": category})


def import_group_from_excel(file, is_import_to_all: bool = True, customer_id: int | None = None):
    df = pd.read_excel(file)
    for index, row in df.iterrows():
        group_url = row["Group"]
        category = row["Category"]

        category = Category.objects.get_or_create(name=category)

        if is_import_to_all:
            customers = Customer.objects.all()
            for customer in customers:
                Group.objects.get_or_create(url=group_url, customer=customer, defaults={"category": category})

        else:
            Group.objects.get_or_create(url=group_url, customer_id=customer_id, defaults={"category": category})


def get_excel_file_not_contains_columns(file, columns: list[str]) -> list[str]:
    df = pd.read_excel(file)
    return [column for column in columns if column not in df.columns]
