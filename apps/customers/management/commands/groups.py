import logging

from django.core.management import BaseCommand

from apps.customers.models.categories import Category
from apps.customers.models.groups import Group

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "Load groups from CSV file"

    def handle(self, *args, **kwargs):
        text = """https://www.facebook.com/groups/chashdanistim;יזמות
        https://www.facebook.com/groups/216219708071114;יזמות
        https://www.facebook.com/groups/yazamutIsrael/;יזמות
        https://www.facebook.com/groups/1598771583735880;יזמות
        https://www.facebook.com/groups/buybystore;יזמות
        https://www.facebook.com/groups/864908790226104/;משה שעיה
        https://www.facebook.com/groups/1637994659811132/permalink/3566466890297223/;משה שעיה
        https://www.facebook.com/groups/279135451973/permalink/10161216242241974;משה שעיה
        https://www.facebook.com/groups/227042837307326/;משה שעיה
        https://www.facebook.com/groups/322313854934686/;משה שעיה
        https://www.facebook.com/groups/864908790226104/;משה שעיה
        https://www.facebook.com/groups/167457006612972/;משה שעיה
        https://www.facebook.com/groups/526817150689303/;משה שעיה
        https://www.facebook.com/groups/661709787239277/;משה שעיה
        https://www.facebook.com/groups/1730789290457027/;משה שעיה
        https://www.facebook.com/groups/322313854934686/;משה שעיה
        https://www.facebook.com/groups/136273756449416/;משה שעיה
        https://www.facebook.com/groups/2302505389980235/;משה שעיה
        https://www.facebook.com/groups/5516147018443257/;משה שעיה
        https://www.facebook.com/groups/beers7beyachad/;משה שעיה
        https://www.facebook.com/groups/322313854934686/;משה שעיה
        https://www.facebook.com/groups/3081467598789404/;משה שעיה
        https://www.facebook.com/groups/2302505389980235;משה שעיה
        https://www.facebook.com/groups/2302505389980235/;משה שעיה
        https://www.facebook.com/groups/167457006612972/;משה שעיה
        https://www.facebook.com/groups/340927103032618/;משה שעיה
        https://www.facebook.com/groups/1141748329196416/?ref=share&mibextid=NSMWBT;משה שעיה
        https://www.facebook.com/groups/796604540779210/?ref=share&mibextid=NSMWBT;משה שעיה
        https://www.facebook.com/groups/170744879507/permalink/10160660029399508/?mibextid=Nif5oz;משה שעיה
        https://www.facebook.com/groups/1637994659811132/permalink/3566466890297223/?mibextid=Nif5oz;משה שעיה
        https://www.facebook.com/groups/213195335405493/;משה שעיה
        https://www.facebook.com/groups/441237999359320;לק ג'ל
        https://www.facebook.com/groups/2216916078544026/;לק ג'ל
        https://www.facebook.com/groups/195010292187642/;לק ג'ל
        https://www.facebook.com/groups/152709495385468/;לק ג'ל
        https://www.facebook.com/groups/iLoveOfakim/;לק ג'ל
        https://www.facebook.com/groups/674766306318402/;לק ג'ל
        https://www.facebook.com/groups/OfakimMyCity/;לק ג'ל
        https://www.facebook.com/groups/667831133646900/;לק ג'ל
        https://www.facebook.com/groups/214978525204547/;לק ג'ל
        https://www.facebook.com/groups/2879124088973031/;לק ג'ל
        https://www.facebook.com/groups/666189103808522/;לק ג'ל
        https://www.facebook.com/groups/2987586461490764/;לק ג'ל
        https://www.facebook.com/groups/416121589750001/;לק ג'ל
        https://www.facebook.com/groups/1442412065866172/;לק ג'ל
        https://www.facebook.com/groups/iLoveNetivot/;לק ג'ל
        https://www.facebook.com/groups/731849637716743/;לק ג'ל
        https://www.facebook.com/groups/267503181058734/;לק ג'ל
        https://www.facebook.com/groups/353992781670203/;לק ג'ל
        https://www.facebook.com/groups/ofakimofficial/;לק ג'ל
        https://www.facebook.com/groups/216268915819168/;לק ג'ל
        https://www.facebook.com/groups/441237999359320/;לק ג'ל
        https://www.facebook.com/groups/1756637371219138;אלון משה
        https://www.facebook.com/groups/IsraeliBusinessFlorida;אלון משה
        https://www.facebook.com/groups/1779102489007154;אלון משה
        https://www.facebook.com/groups/126274368006898;אלון משה
        https://www.facebook.com/groups/2051199548445008/;אלון משה
        https://www.facebook.com/groups/IsraelisNewYork/;אלון משה
        https://www.facebook.com/groups/131398024099344/;אלון משה
        https://www.facebook.com/groups/217217060143103/;אלון משה
        https://www.facebook.com/groups/1514612552137495/;אלון משה
        https://www.facebook.com/groups/2215912328473960/;אלון משה
        https://www.facebook.com/groups/1755925284657506/;אלון משה
        https://www.facebook.com/groups/560997350685946/;אלון משה
        https://www.facebook.com/groups/36927955925/;אלון משה
        https://www.facebook.com/groups/417198565886935/;אלון משה
        https://www.facebook.com/groups/IsraelisLosAngeles/;אלון משה
        https://www.facebook.com/groups/185654615241203;אלון משה
        https://www.facebook.com/groups/1821545751489585/;אלון משה
        https://www.facebook.com/groups/217680319818/;אלון משה
        https://www.facebook.com/groups/386198811739945/;אלון משה
        https://www.facebook.com/groups/1453382448315287;אלון משה
        https://www.facebook.com/groups/344731389257060;אלון משה
        https://www.facebook.com/groups/1415043375475323/;אלון משה
        https://www.facebook.com/groups/280841712027616/;אלון משה
        https://www.facebook.com/groups/1779102489007154/;אלון משה
        https://www.facebook.com/groups/1095580407240110;אלון משה"""

        rows = text.split("\n")
        for row in rows:
            cols = row.split(";")
            url = cols[0].strip()
            category_name = cols[1].strip()

            category, created = Category.objects.get_or_create(name=category_name)
            group, created = Group.objects.get_or_create(url=url, defaults={"category": category})
