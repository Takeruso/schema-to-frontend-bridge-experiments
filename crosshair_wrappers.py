from types import SimpleNamespace

from benchmark.level_5.case_1 import UserModel as L5c1
from benchmark.level_5.case_3 import UserModel as L5c3
from benchmark.level_5.case_4 import Square as L5c4
from benchmark.level_5.case_5 import Organization as L5c5, User as L5c5User


def l5c1(username: str, password: str, password_repeat: str) -> object:
    m = L5c1.model_construct(username=username, password=password, password_repeat=password_repeat)
    return m.check_passwords_match()


def l5c3(password: str, password_repeat: str) -> object:
    return L5c3.check_passwords_match(password_repeat, SimpleNamespace(data={"password": password}))


def l5c4(width: float, height: float) -> object:
    return L5c4.model_construct(width=width, height=height).verify_square()


def l5c5(forbidden_passwords: list[str], passwords: list[str]) -> object:
    users = [L5c5User.model_construct(username="u", password=p) for p in passwords]
    return L5c5.model_construct(forbidden_passwords=forbidden_passwords, users=users).validate_user_passwords()