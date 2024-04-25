import logging

from django.core.management import BaseCommand

from apps.customers.models.categories import Category
from apps.customers.models.keywords import Keyword

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "Load groups from CSV file"

    def handle(self, *args, **kwargs):
        text = """פרסום;אלון משה
קהל;אלון משה
יועץ;אלון משה
המלצות;אלון משה
Marketing;אלון משה
קמפיינר;אלון משה
שיווק;אלון משה
מומחה;אלון משה
המלצה;אלון משה
מודעות;אלון משה
מכירות;אלון משה
Leads;אלון משה
ecommerce;אלון משה
סוכנות;אלון משה
קידום;אלון משה
טיקטוק;אלון משה
למכירה;אלון משה
פייסבוק;אלון משה
סושיאל;אלון משה
לידים;אלון משה
קמפיינים;אלון משה
אינסטגרם;אלון משה
תותח;אלון משה
גוגל;אלון משה
איקומרס;אלון משה
קמפיין;אלון משה
פדיקור עם לק;לק ג'ל
לק גל;לק ג'ל
לק ג'ל;לק ג'ל
לק ג'ל בידיים;לק ג'ל
מניקור;לק ג'ל
ציפורניים;לק ג'ל
פדיקור;לק ג'ל
תור לפדיקור;לק ג'ל
תור ללק ג'ל;לק ג'ל
מחפשת לק ג'ל;לק ג'ל
ציפורנים;לק ג'ל
בניין;משה שעיה
קוטג;משה שעיה
מגורים;משה שעיה
חניה;משה שעיה
צריך המלצה לעורך דין;משה שעיה
וילה;משה שעיה
מחפש לקנות בית;משה שעיה
דירת חדרים;משה שעיה
ניהול נכס;משה שעיה
מרוהט תיווך;משה שעיה
תמ"א 38;משה שעיה
נדל"ן;משה שעיה
למכירה;משה שעיה
דרוש עורך דין;משה שעיה
קונה;משה שעיה
מחפש מתכנת;משה שעיה
ללא תיווך;משה שעיה
מחפש יועץ נדלן;משה שעיה
מחפש להשכיר;משה שעיה
נכס;משה שעיה
פרויקט נדל"ן;משה שעיה
צריך מעצב;משה שעיה
פנטהאוז;משה שעיה
תכנון עירוני;משה שעיה
דירה;משה שעיה
דירת גן;משה שעיה
מוכר;משה שעיה
להשכרה;משה שעיה
לאן להשקיע;משה שעיה
שוק הנדל"ן;משה שעיה
דירת מגורים ריהוט;משה שעיה
ללא תיווך;משה שעיה
גג;משה שעיה
סטודיו;משה שעיה"""
        rows = text.split("\n")
        for row in rows:
            cols = row.split(";")
            url = cols[0].strip()
            category_name = cols[1].strip()

            category, created = Category.objects.get_or_create(name=category_name)
            group, created = Keyword.objects.get_or_create(name=url, defaults={"category": category})
