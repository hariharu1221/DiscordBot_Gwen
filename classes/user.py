from typing import Union, Optional

import discord

from utils.sqlite_class import Seta_sqlite
from utils import level_design

db = Seta_sqlite('db/userdata.db')


class User:
    user: Optional[discord.User] = None  # 디스코드의 유저 객체
    id: int = 0  # 유저 아이디
    name: str = '알 수 없는 유저'  # 유저 이름

    _money: int = 0  # 보유한 돈
    _exp: int = 0  # 경험치 (레벨은 경험치에 따라 자동 조정되며, 공격, 방어 등의 스탯은 레벨에 따라 자동 조정 됩니다.)
    items: list = []  # 아이템 목록

    realname: Optional[str] = None

    def __init__(self, user: Union[discord.User, int]):
        if isinstance(user, int):
            self.id = user
        else:
            self.user = user
            self.id = user.id
            self.realname = user.name.replace("'", '').replace("\"", '')

        try:
            self.load()
        except NotExistUser:
            self.name = self.realname if self.realname is not None else user.name
            db.insert_sql(
                'users', 'id, name, hp, mp',
                f"{self.id}, '{self.name}', {level_design.level_to_maxhp(1)}, {level_design.level_to_maxmp(1)}"
                )
            self.load()

        if self.realname is not None:
            if self.realname != self.name:
                db.update_sql('users', f"name='{self.name}'", f"id={self.id}")
            self.name = self.realname

    def load(self):
        '''데이터에서 값을 다시 불러옵니다'''
        data = self._load_data()
        if data == []:
            raise NotExistUser

        data = data[0]
        self.name = str(data[0])
        self._money = int(data[1])
        self._exp = int(data[2])
        self._hp = int(data[3])
        self._mp = int(data[4])
        self._is_gaming = bool(data[5])
        return data

    def _load_data(self):
        return db.select_sql(
            'users',
            'name, money, exp, hp, mp, is_gaming',
            f'WHERE id={self.id}'
            )

# --------- Getter/Setter --------- #

    @property
    def money(self):
        '''int: 유저의 돈'''
        return db.select_sql('users', 'money', f'WHERE id={self.id}')[0][0]

    @money.setter
    def money(self, value: int):
        db.update_sql('users', f'money={int(value)}', f'WHERE id={self.id}')
        self._money = int(value)

    def add_money(self, value: int):
        db.update_sql('users', f'money=money+{int(value)}', f'WHERE id={self.id}')
        self._money += int(value)

    @property
    def exp(self):
        '''int: 유저의 경험치'''
        return db.select_sql('users', 'exp', f'WHERE id={self.id}')[0][0]

    @exp.setter
    def exp(self, value: int):
        db.update_sql('users', f'exp={int(value)}', f'WHERE id={self.id}')
        self._exp = int(value)

    def add_exp(self, value: int):
        db.update_sql('users', f'exp=exp+{int(value)}', f'WHERE id={self.id}')
        self._exp += int(value)

    @property
    def level(self):
        '''int: 유저의 레벨'''
        return level_design.exp_to_level(self.exp)

class NotExistUser(Exception):
    def __init__(self):
        super().__init__('존재하지 않는 유저입니다')
