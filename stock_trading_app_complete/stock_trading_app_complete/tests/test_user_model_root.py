from models.user_model import Users


def test_generate_hashed_password_unique():
    """
    test that hashing the same password twice produces different salts and hashes.

    this ensures that the _generate_hashed_password method generates a unique
    salt each time, even for the same input password, which is important for
    password security.

    asserts:
        - that two generated salts are different.
        - that two generated hashes are different.
    """
    salt1, hash1 = Users._generate_hashed_password("pass")
    salt2, hash2 = Users._generate_hashed_password("pass")
    assert salt1 != salt2
    assert hash1 != hash2

def test_verify_password():
    """
    test that verify_password correctly identifies an incorrect password.

    this test creates a user with a known password hash and verifies that
    an incorrect password fails the verification check.

    asserts:
        - that verify_password returns False for an incorrect password.
    """
    user = Users(username="test", salt="abcd"*8, password="")
    user.password = Users._generate_hashed_password("pass")[1]
    assert not user.verify_password("wrong")
