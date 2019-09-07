from datetime import date
from unittest import TestCase
from unittest.mock import patch

from freezegun import freeze_time
from requests import HTTPError

from app.models import User


class MockResponse:
    def json(self):
        return dict(
            prefecture='東京都',
            city='品川区西五反田'
        )


class UserTests(TestCase):

    def setUp(self):
        self.user = User(
            first_name='takayuki',
            last_name='hirayama',
            zip_code='141-0031',
            birthday=date(2019, 9, 1),
        )

    def test_first_name(self):
        self.assertEqual(self.user.first_name, 'Takayuki')

    def test_last_name(self):
        self.assertEqual(self.user.last_name, 'Hirayama')

    def test_full_name(self):
        self.assertEqual(self.user.full_name, 'Takayuki Hirayama')

    def test_age(self):
        at_dates = [
            date(year=2020, month=9, day=1),
            date(year=2020, month=8, day=31),
        ]
        expected_ages = [
            1,
            0
        ]
        for at, expected_age in zip(at_dates, expected_ages):
            with self.subTest(birthday=self.user.birthday, at=at):
                self.assertEqual(self.user.age(at=at), expected_age)

    @freeze_time('2020-09-01')
    def test_age_at_today(self):
        self.assertEqual(self.user.age(), 1)

    @patch('requests.get', return_value=MockResponse())
    def test_address(self, mock_get):
        self.assertTupleEqual(
            self.user.address,
            ('東京都', '品川区西五反田'),
        )

    @patch('requests.get', side_effect=HTTPError)
    def test_address_with_error(self, mock_get):
        with self.assertRaises(HTTPError):
            address = self.user.address
        self.assertEqual(mock_get.call_count, 3)
