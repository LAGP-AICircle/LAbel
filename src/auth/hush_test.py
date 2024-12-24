# hash_password.py
import streamlit_authenticator as stauth

def hash_passwords():
    # テスト用の単一パスワード
    password = "test"
    hasher = stauth.Hasher()
    hashed_password = hasher.hash(password)
    
    print(f"Original password: {password}")
    print(f"Hashed password: {hashed_password}")

    # 実際のユーザー用のパスワード
    users_passwords = {
        "t.miyamoto": "1234",
        "s.mori": "1234",
        # 他のユーザーも同様に
    }
    
    print("\nAll users hashed passwords:")
    for username, pwd in users_passwords.items():
        hashed = hasher.hash(pwd)
        print(f"\nUsername: {username}")
        print(f"Original password: {pwd}")
        print(f"Hashed password: {hashed}")

if __name__ == "__main__":
    hash_passwords()