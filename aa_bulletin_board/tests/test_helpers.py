"""
Test our helper functions
"""

# Third Party
from faker import Faker

# Django
from django.contrib.auth.models import Group
from django.test import TestCase

from ..models import Bulletin
from .utils import create_fake_user

fake = Faker()


class TestHelpers(TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        """
        Set up groups and users
        """

        super().setUpClass()
        cls.group = Group.objects.create(name="Superhero")

        # User cannot access bulletins
        cls.user_1001 = create_fake_user(1001, "Peter Parker")

        # User can access bulletins
        cls.user_1002 = create_fake_user(
            1002, "Bruce Wayne", permissions=["aa_bulletin_board.basic_access"]
        )

        # User can manage bulletins
        cls.user_1003 = create_fake_user(
            1003,
            "Clark Kent",
            permissions=[
                "aa_bulletin_board.basic_access",
                "aa_bulletin_board.manage_bulletins",
            ],
        )

    def test_should_translate_russian_letters_in_slug(self):
        """
        Test that russian letters in a slug are translated
        :return:
        :rtype:
        """

        bulletin = Bulletin.objects.create(
            title="дрифтерке, рорки в док",
            content=f"<p>{fake.sentence()}</p>",
            created_by=self.user_1001,
        )

        self.assertTrue(bulletin.slug, "drifterke-rorki-v-dok")
