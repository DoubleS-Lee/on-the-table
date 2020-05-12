import random
from django.core.management.base import BaseCommand
from django_seed import Seed
from reviews import models as review_models
from users import models as user_models
from contents import models as content_models

# 허수의 reviews들을 자동으로 생성하게 해주는 코드


class Command(BaseCommand):
    help = "This command creates reviews"

    def add_arguments(self, parser):
        parser.add_argument(
            "--number",
            default=1,
            type=int,
            help="How many reviews do you want to create?",
        )

    def handle(self, *args, **options):
        number = options.get("number")
        seeder = Seed.seeder()
        users = user_models.User.objects.all()
        contents = content_models.Content.objects.all()
        seeder.add_entity(
            review_models.Review,
            number,
            {
                "content": lambda x: random.choice(contents),
                "user": lambda x: random.choice(users),
            },
        )
        seeder.execute()
        self.stdout.write(self.style.SUCCESS(f"{number} reviews created!"))

        # 위의 코드를 작성한 뒤 TERMINAL 창에서
        # python manage.py seed_reviews --number 10 를 입력해줘야한다(10명을 만들고 싶은 경우)

        # 이 방법을 사용하면 관리자페이지에서 일일히 입력해주지 않아도 한번에 일괄적으로 입력이 가능하다