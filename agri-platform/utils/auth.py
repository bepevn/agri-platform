import pandas as pd
from pathlib import Path


# 프로젝트의 기준 폴더
BASE_DIR = Path(__file__).resolve().parent.parent

# users.csv 위치
USERS_FILE = BASE_DIR / "data" / "users.csv"


def load_users():
    return pd.read_csv(USERS_FILE)


def login(email, password):
    users = load_users()

    user = users[
        (users["email"].astype(str) == str(email)) &
        (users["password"].astype(str) == str(password))
    ]

    if len(user) == 1:
        return user.iloc[0].to_dict()

    return None
