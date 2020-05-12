import random
from django.core.management.base import BaseCommand
from django.contrib.admin.utils import flatten
from django_seed import Seed
from contents import models as content_models
from users import models as user_models

# 허수의 contents들을 자동으로 생성하게 해주는 코드


class Command(BaseCommand):
    help = "This command creates many contents"

    def add_arguments(self, parser):
        parser.add_argument(
            "--number",
            default=1,
            type=int,
            help="How many users do you want to create?",
        )

    def handle(self, *args, **options):
        number = options.get("number")
        seeder = Seed.seeder()
        # 생성해놓은 users 정보를 가져오는 코드
        # content을 생성하려면 user가 반드시 있어야하기 때문에 user와 room을 매칭시켜주는 작업이 필요하다
        all_users = user_models.User.objects.all()
        # 기본 add_entity에 content 안에 random으로 user를 집어넣는 람다함수를 만든다
        seeder.add_entity(
            content_models.Content,
            number,
            {
                "title": lambda x: seeder.faker.job(),
                "description": lambda x: seeder.faker.sentence(),
                "dish": lambda x: seeder.faker.company(),
                "cooking_ingredients": lambda x: seeder.faker.color_name(),
                "cuisine": lambda x: seeder.faker.address(),
                "user": lambda x: random.choice(all_users),
            },
        )
        created_photos = seeder.execute()
        # 이상한 모양 정리
        created_clean = flatten(list(created_photos.values()))
        cooking_utensils = content_models.CookingUtensil.objects.all()
        for pk in created_clean:
            # 생성된 모든 content를 Primary key로 그 content를 찾고
            # content의 instance를 받기 위함
            content = content_models.Content.objects.get(pk=pk)

            # 최소 1, 최대 1이나 2까지 사진을 만들고
            for i in range(1, random.randint(2, 3)):
                content_models.Photo.objects.create(
                    caption=seeder.faker.sentence(),
                    content=content,
                    # 생성된 content에게 파일을 준다
                    file=f"content_photos/{random.randint(1,16)}.jpg",
                )

            for a in cooking_utensils:
                magic_number = random.randint(0, 3)
                if magic_number % 2 == 0:
                    content.cooking_utensils.add(a)

        self.stdout.write(self.style.SUCCESS(f"{number} contents created!"))

        # 위의 코드를 작성한 뒤 TERMINAL 창에서
        # python manage.py seed_contents --number 10 를 입력해줘야한다(10명을 만들고 싶은 경우)

        # 이 방법을 사용하면 관리자페이지에서 일일히 입력해주지 않아도 한번에 일괄적으로 입력이 가능하다