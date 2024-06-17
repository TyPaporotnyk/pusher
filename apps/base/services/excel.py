import pandas as pd

from apps.common.models import Category, Group, Keyword
from apps.customers.models import Customer


def import_keyword_from_excel(file):
    df = pd.read_excel(file)
    for index, row in df.iterrows():
        keyword_name = row["KeyWord"]
        category_name = row["Tag"]
        category, created = Category.objects.get_or_create(name=category_name)
        Keyword.objects.get_or_create(name=keyword_name, defaults={"category": category})


def import_group_from_excel(file):
    df = pd.read_excel(file)
    for index, row in df.iterrows():
        group_url = row["Group"]

        for user in Customer.objects.all():
            Group.objects.get_or_create(url=group_url, user=user)
