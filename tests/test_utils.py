from datetime import date
from unittest import TestCase

from app.utils import calculate_age


class CalculateAgeTests(TestCase):

    def test_calculate(self):
        birthday = date(year=2019, month=9, day=1)
        at_dates = [
            date(year=2020, month=9, day=1),
            date(year=2020, month=8, day=31),
        ]
        expected_ages = [
            1,
            0
        ]

        for at, expected_age in zip(at_dates, expected_ages):
            age = calculate_age(birthday, at)
            with self.subTest(birthday=birthday, at=at):
                self.assertEqual(age, expected_age)

    def test_calculate_with_invalid_at(self):
        birthday = date(year=2019, month=9, day=1)
        at = date(year=2019, month=8, day=31)
        self.assertRaises(ValueError, calculate_age, birthday, at)
