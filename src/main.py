import streamlit as st
import sys
from pathlib import Path
import warnings

warnings.filterwarnings("ignore", category=RuntimeWarning)

# プロジェクトのルートディレクトリをPythonパスに追加
root_path = Path(__file__).parent.parent.resolve()
sys.path.append(str(root_path))

# 相対インポートを使用
from config.settings import get_openai_api_key, get_setting, apply_theme
from components.sidebar import show_sidebar
from components.header import show_header
from pages.matching.main import matching_page
from pages.minutes.main import minutes_page
from pages.legal_check.main import legal_check_page
from auth.login import login_page

def main():
    try:
        # テーマの適用（デフォルトテーマを使用）
        apply_theme(None)
        
        # pageの初期化
        if "page" not in st.session_state:
            st.session_state.page = "home"  # デフォルトページを設定
        
        # 認証状態をチェック
        if not st.session_state.get("authentication_status"):
            username = login_page()
            if not username:
                st.stop()
        
        # 認証済みの場合の表示
        show_header()
        show_sidebar()
        
        # ページルーティング
        if st.session_state.get("page") == 'matching':
            matching_page()
        elif st.session_state.get("page") == 'minutes':
            minutes_page()
        elif st.session_state.get("page") == 'legal_check':
            legal_check_page()
        else:  # home
            st.title("LAbelへようこそ")
            st.write(f'ようこそ {st.session_state.get("name")} さん')
        
    except Exception as e:
        st.error(f"エラーが発生しました: {str(e)}")
        st.session_state["authentication_status"] = None
        st.rerun()

if __name__ == "__main__":
    main()