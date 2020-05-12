from django.core.management.base import BaseCommand
from contents.models import CookingUtensil

class Command(BaseCommand):
    help = "This command creates cooking utensils"
    def handle(self, *args, **options):
        cooking_utensils = [
            "냄비",
            "후라이팬",
            "전자레인지",
            "에어프라이기",
            "튀김기",
            "오븐",
            "가스레인지",
        ]

        # 위에서 미리 준비해놓은 Cooking utensils들을 object로 만들어서
        # 실제로 홈페이지에 연동시켜 Cooking utensils 항목들을 다 채우는 방법
        for a in cooking_utensils:
            CookingUtensil.objects.create(name=a)
        self.stdout.write(self.style.SUCCESS("Cooking utensils created!"))

        # 위의 코드를 작성한 뒤 TERMINAL 창에서
        # python manage.py seed_cooking_utensils를 입력해줘야한다

        # 이 방법을 사용하면 관리자페이지에서 일일히 입력해주지 않아도 한번에 일괄적으로 입력이 가능하다
