from datetime import date

import requests
from retry import retry

from app.utils import calculate_age


class User:
    def __init__(self, first_name, last_name, zip_code, birthday):
        """
        :param first_name: ファーストネーム
        :param last_name: ラストネーム
        :param zip_code: 郵便番号
        :param birthday: 生年月日
        """
        self.first_name = first_name.title()
        self.last_name = last_name.title()
        self.zip_code = zip_code
        self.birthday = birthday

    @property
    def full_name(self):
        """
        フルネームを取得する

        :return: "ファーストネーム ラストネーム"の文字列
        """
        return '{} {}'.format(self.first_name, self.last_name)

    @property
    @retry(exceptions=requests.HTTPError, tries=3)
    def address(self):
        """
        APIを利用して郵便番号から都道府県と市区町村を取得する
        エラーが発生した場合は3回までリトライする

        :return: (都道府県, 市区町村)のタプル
        """
        response = requests.get(url='http://localhost', params={
            'zip_code': self.zip_code,
        })
        results = response.json()
        return results['prefecture'], results['city']

    def age(self, at=None):
        """
        atで指定した日付を基準にした年齢を取得する
        atが指定されない場合はdatetime.date.todayを基準日とする

        :param at: 年齢計算の基準日
        :return: 年齢
        """
        if at is None:
            at = date.today()
        return calculate_age(self.birthday, at)
