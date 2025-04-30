from models.user_model import Users


def test_generate_hashed_password_unique():
    salt1, hash1 = Users._generate_hashed_password("pass")
    salt2, hash2 = Users._generate_hashed_password("pass")
    assert salt1 != salt2
    assert hash1 != hash2

def test_verify_password():
    user = Users(username="test", salt="abcd"*8, password="")
    user.password = Users._generate_hashed_password("pass")[1]
    assert not user.verify_password("wrong")
