import streamlit_authenticator as stauth
import yaml
from pathlib import Path

def hash_passwords():
    # config.yamlのパスを取得
    yaml_path = Path(__file__).parent / "config.yaml"
    
    # 現在のconfig.yamlを読み込む
    with open(yaml_path, "r", encoding="utf-8") as file:
        config = yaml.safe_load(file)

    # 各ユーザーのパスワードをハッシュ化
    for username in config["credentials"]["usernames"]:
        password = config["credentials"]["usernames"][username]["password"]
        hashed_password = stauth.Hasher([password]).hash(password)
        config["credentials"]["usernames"][username]["password"] = hashed_password

    # 新しいconfig.yamlを書き出す
    with open(yaml_path, "w", encoding="utf-8") as file:
        yaml.dump(config, file, allow_unicode=True)

if __name__ == "__main__":
    hash_passwords()
    print("パスワードのハッシュ化が完了しました。")