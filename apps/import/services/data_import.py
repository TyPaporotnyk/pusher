import pandas as pd

from apps.common.models import Blacklist, Category, Group, Keyword, PublicBlackList, PublicGroup, PublicKeyword
from apps.customers.models import Customer


def import_keyword_from_excel(file, is_import_to_all: bool, customer_id: int | None = None):
    df = pd.read_excel(file)
    for index, row in df.iterrows():
        keyword_name = row["Keyword"]
        category = row["Category"]

        category, _ = Category.objects.get_or_create(name=category)

        if is_import_to_all:
            customers = Customer.objects.all()
            for customer in customers:
                Keyword.objects.get_or_create(name=keyword_name, customer=customer, defaults={"category": category})

        else:
            Keyword.objects.get_or_create(name=keyword_name, customer_id=customer_id, defaults={"category": category})


def import_group_from_excel(file, is_import_to_all: bool = True, customer_id: int | None = None):
    df = pd.read_excel(file)
    for index, row in df.iterrows():
        group_url = row["Group"]
        category = row["Category"]

        category, _ = Category.objects.get_or_create(name=category)

        if is_import_to_all:
            customers = Customer.objects.all()
            for customer in customers:
                Group.objects.get_or_create(url=group_url, customer=customer, defaults={"category": category})

        else:
            Group.objects.get_or_create(url=group_url, customer_id=customer_id, defaults={"category": category})


def import_black_list_from_excel(file, is_import_to_all: bool = True, customer_id: int | None = None):
    df = pd.read_excel(file)
    for index, row in df.iterrows():
        black_list_name = row["BlackList"]
        category = row["Category"]

        category, _ = Category.objects.get_or_create(name=category)

        if is_import_to_all:
            customers = Customer.objects.all()
            for customer in customers:
                Blacklist.objects.get_or_create(
                    name=black_list_name, customer=customer, defaults={"category": category}
                )

        else:
            Blacklist.objects.get_or_create(
                name=black_list_name, customer_id=customer_id, defaults={"category": category}
            )


def import_public_groups_from_excel(file):
    df = pd.read_excel(file)
    for index, row in df.iterrows():
        group_url = row["Group"]
        PublicGroup.objects.get_or_create(url=group_url)


def import_public_keywords_from_excel(file):
    df = pd.read_excel(file)
    for index, row in df.iterrows():
        keyword_name = row["Keyword"]
        PublicKeyword.objects.get_or_create(name=keyword_name)


def import_public_black_lists_from_excel(file):
    df = pd.read_excel(file)
    for index, row in df.iterrows():
        black_list_name = row["BlackList"]
        PublicBlackList.objects.get_or_create(name=black_list_name)
