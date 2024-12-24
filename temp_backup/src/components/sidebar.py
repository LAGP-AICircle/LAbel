# src/components/sidebar.py
import streamlit as st
import streamlit_antd_components as sac

def show_sidebar():
    with st.sidebar:
        st.title("LAbel")
        
        # メニューの実装
        selected = sac.menu([
            sac.MenuItem('Home', 
                        icon='house-fill', 
                        description='ダッシュボード'),
            sac.MenuItem('Matching',
                        icon='people-fill', 
                        description='案件マッチング'),
            sac.MenuItem('Minutes Preparation',
                        icon='pencil-fill', 
                        description='議事録作成支援'),
            sac.MenuItem('Legal Review',
                        icon='shield-fill', 
                        description='リーガルチェック')
        ], 
        format_func='title',
        open_all=True,
        indent=24)
        
        # ナビゲーション処理
        if selected:
            page_mapping = {
                'Home': 'home',
                'Matching': 'matching',
                'Minutes Preparation': 'minutes',
                'Legal Review': 'legal_check'
            }
            
            if selected in page_mapping:
                new_page = page_mapping[selected]
                if st.session_state.page != new_page:
                    st.session_state.page = new_page
                    st.rerun()
        
        # 区切り線とログアウトボタン
        st.markdown("---")
        # 通常のStreamlitボタンを使用
        if st.button('ログアウト', key='logout_button'):
            st.session_state.logged_in = False
            st.rerun()