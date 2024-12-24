# -*- coding: utf-8 -*-
import streamlit as st
from pages.minutes.main import minutes_page
from pages.matching.main import matching_page
from pages.legal_check.main import legal_check_page
from components.sidebar import show_sidebar
from auth.login import login_page


def main():
    st.set_page_config(page_title="Label", page_icon="🏷️", layout="wide", initial_sidebar_state="expanded")

    # セッション状態の初期化
    if "authentication_status" not in st.session_state:
        st.session_state.authentication_status = None
    if "page" not in st.session_state:
        st.session_state.page = "home"

    # ログイン状態の確認
    if not st.session_state.get("authentication_status"):
        # ログインページを表示
        st.title("Label - ログイン")
        login_page()
    else:
        # ログイン成功後の処理
        show_sidebar()  # サイドバーを表示

        # ページのルーティング
        if st.session_state.page == "minutes":
            minutes_page()
        elif st.session_state.page == "matching":
            matching_page()
        elif st.session_state.page == "legal_check":
            legal_check_page()
        else:  # home
            st.title("ホーム")
            st.write(f"ようこそ、{st.session_state.get('name')}さん")
            st.markdown(
                """
            ### 機能一覧
            
            - **議事録作成支援**: 音声ファイルから議事録を自動生成
            - **案件マッチング**: 案件と人材のマッチング支援
            - **リーガルチェック**: 契約書のリーガルチェック支援
            """
            )


if __name__ == "__main__":
    main()