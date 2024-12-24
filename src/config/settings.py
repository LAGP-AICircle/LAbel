# JQPJ_WebAP\src\config\settings.py
import os
from pathlib import Path
import yaml
import toml
import streamlit as st

# アプリケーション設定（静的な設定）
APP_NAME = "LAbel"
VERSION = "0.1.0"
SUPPORTED_AUDIO_FORMATS = ["mp3", "mp4", "m4a", "wav"]
MAX_AUDIO_SIZE = 200 * 1024 * 1024  # 200MB

# 認証設定ファイルのパスを指定
AUTH_CONFIG_PATH = Path(__file__).parent.parent / "auth" / "config.yaml"


def load_auth_config():
    try:
        with open(AUTH_CONFIG_PATH, encoding="utf-8") as file:
            return yaml.safe_load(file)
    except Exception as e:
        print(f"認証設定ファイルの読み込みに失敗: {str(e)}")
        return None


def get_setting():
    """設定を取得する"""
    # 環境変数から取得を試みる
    if os.environ.get("OPENAI_API_KEY"):
        return {
            "OPENAI_API_KEY": os.environ.get("OPENAI_API_KEY"),
            "LABEL_EMAIL": os.environ.get("LABEL_EMAIL"),
            "LABEL_PASSWORD": os.environ.get("LABEL_PASSWORD"),
            "DATABASE_URL": os.environ.get("DATABASE_URL"),
        }

    # Streamlitのsecrets機能から取得を試みる
    try:
        return {
            "OPENAI_API_KEY": st.secrets["OPENAI_API_KEY"],
            "LABEL_EMAIL": st.secrets.get("LABEL_EMAIL"),
            "LABEL_PASSWORD": st.secrets.get("LABEL_PASSWORD"),
            "DATABASE_URL": st.secrets.get("DATABASE_URL"),
        }
    except FileNotFoundError:
        # ローカルのsecret.tomlから読み込み
        config_path = Path(__file__).parent.parent / "secret.toml"
        try:
            if not config_path.exists():
                print(f"設定ファイルが見つかりません: {config_path}")
                return {}
            with open(str(config_path), "r", encoding="utf-8") as f:
                return toml.load(f)
        except Exception as e:
            print(f"設定ファイルの読み込みに失敗: {str(e)}")
            return {}


# settings.pyに追加
def get_openai_api_key():
    # 環境変数から取得を試みる
    api_key = os.getenv("OPENAI_API_KEY")
    if api_key:
        return api_key

    # 既存のsecret.tomlからの読み込み
    settings = get_setting()
    api_key = settings.get("OPENAI_API_KEY")
    if not api_key:
        print("OpenAI APIキーが設定されていません")
        return None
    return api_key


def get_database_url():
    settings = get_setting()
    db_url = settings.get("DATABASE_URL")
    if not db_url:
        print("データベースURLが設定されていません")
        return None
    return db_url


# 認証設定の読み込み
AUTH_CONFIG = load_auth_config()


def load_streamlit_config():
    """Streamlitの設定ファイルを読み込む"""
    config_path = Path(__file__).parent.parent.parent / ".streamlit" / "config.toml"
    try:
        with open(str(config_path), "r", encoding="utf-8") as f:
            return toml.load(f)
    except Exception as e:
        print(f"Streamlit設定ファイルの読み込みに失敗: {str(e)}")
        return None


def get_mail_settings():
    """メール設定を取得する"""
    # StreamlitCloudの環境変数から取得を試みる
    if "LABEL_EMAIL" in st.secrets:
        return {"LABEL_EMAIL": st.secrets["LABEL_EMAIL"], "LABEL_PASSWORD": st.secrets["LABEL_PASSWORD"]}

    # ローカルのsecret.tomlから読み込み
    settings = get_setting()
    email = settings.get("LABEL_EMAIL")
    password = settings.get("LABEL_PASSWORD")

    if not email or not password:
        print("メール設定が見つかりません")
        return {}

    return {"LABEL_EMAIL": email, "LABEL_PASSWORD": password}


def apply_theme(theme_name):
    """指定されたテーマをStreamlit設定に適用する"""
    config = load_streamlit_config()
    if not config or "theme" not in config:
        return

    theme_settings = config["theme"]

    # Streamlitの設定を更新
    st.set_page_config(
        page_title="LAbel",
        page_icon="🏢",
        layout="wide",
        initial_sidebar_state="expanded",
        menu_items={"Get Help": None, "Report a bug": None, "About": None},
    )

    # テーマを適用
    st.markdown(
        f"""
        <style>
        :root {{
            --primary-color: {theme_settings['primaryColor']};
            --background-color: {theme_settings['backgroundColor']};
            --secondary-background-color: {theme_settings['secondaryBackgroundColor']};
            --text-color: {theme_settings['textColor']};
            --font: {theme_settings['font']};
        }}
        </style>
    """,
        unsafe_allow_html=True,
    )
