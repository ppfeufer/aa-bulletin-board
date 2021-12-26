"""
Test bulletins
"""

# Third Party
from faker import Faker

# Django
from django.contrib.auth.models import Group
from django.contrib.messages import get_messages
from django.test import TestCase
from django.urls import reverse

from ..models import Bulletin
from .utils import create_fake_user

fake = Faker()


class TestBulletins(TestCase):
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

    def test_should_remove_bulletin(self):
        """
        Test if a bulletin should be removed
        :return:
        :rtype:
        """

        # given
        bulletin_title = fake.sentence()
        bulletin = Bulletin.objects.create(
            title=bulletin_title,
            content=f"<p>{fake.sentence()}</p>",
            created_by=self.user_1001,
        )

        self.client.force_login(self.user_1003)

        # when
        response = self.client.get(
            reverse("aa_bulletin_board:remove_bulletin", args=[bulletin.slug])
        )
        messages = list(get_messages(response.wsgi_request))

        # then
        self.assertRedirects(response, "/bulletin-board/")
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), f'Bulletin "{bulletin_title}" deleted.')

    def test_should_raise_does_not_exist_exception_when_delete_bulletin_not_found(self):
        """
        Test if a bulletin that doesn't exist should be removed
        :return:
        :rtype:
        """

        # given
        bulletin = Bulletin.objects.create(
            title=fake.sentence(),
            content=f"<p>{fake.sentence()}</p>",
            created_by=self.user_1001,
        )
        self.client.force_login(self.user_1003)

        # when
        response = self.client.get(
            reverse("aa_bulletin_board:remove_bulletin", args=["foobarsson"])
        )
        messages = list(get_messages(response.wsgi_request))

        self.assertRaises(bulletin.DoesNotExist)
        self.assertEqual(len(messages), 1)
        self.assertEqual(
            str(messages[0]),
            "The bulletin you are trying to delete for does not exist.",
        )
