import pandas as pd

from apps.customers.models.categories import Category
from apps.customers.models.groups import Group
from apps.customers.models.keywords import Keyword


def import_group_from_excel(file):
    df = pd.read_excel(file)
    for index, row in df.iterrows():
        group_url = row["Group"]
        category_name = row["Tag"]
        category, created = Category.objects.get_or_create(name=category_name)
        Group.objects.get_or_create(url=group_url, defaults={"category": category})


def import_keyword_from_excel(file):
    df = pd.read_excel(file)
    for index, row in df.iterrows():
        keyword_name = row["KeyWord"]
        category_name = row["Tag"]
        category, created = Category.objects.get_or_create(name=category_name)
        Keyword.objects.get_or_create(name=keyword_name, defaults={"category": category})
