from apps.common.models import Blacklist, Group, Keyword, PublicBlackList, PublicGroup, PublicKeyword
from config.celery import app


@app.task
def load_customer_public_entities(new_customer_id: int):

    for public_group in PublicGroup.objects.all():
        group, _ = Group.objects.get_or_create(url=public_group.url, customer_id=new_customer_id)

    for public_keyword in PublicKeyword.objects.all():
        keyword, _ = Keyword.objects.get_or_create(name=public_keyword.name, customer_id=new_customer_id)

    for public_black_list in PublicBlackList.objects.all():
        black_list, _ = Blacklist.objects.get_or_create(name=public_black_list.name, customer_id=new_customer_id)
