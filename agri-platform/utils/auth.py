import pandas as pd

def load_users():
    return pd.read_csv("data/users.csv")

def login(email, password):
    users = load_users()
    user = users[
        (users["email"] == email) &
        (users["password"].astype(str) == str(password))
    ]
    if len(user) == 1:
        return user.iloc[0].to_dict()
    return None
