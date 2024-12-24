import os
import streamlit as st
import yaml
from yaml.loader import SafeLoader
import streamlit_authenticator as stauth
import traceback  # スタックトレース用に追加

def login_page():
    try:
        # config.yamlのパスをより確実に解決
        current_dir = os.path.dirname(os.path.abspath(__file__))
        yaml_path = os.path.join(current_dir, "config.yaml")
        
        # configの読み込み
        try:
            with open(yaml_path, encoding="utf-8") as file:
                config = yaml.load(file, Loader=SafeLoader)
        except FileNotFoundError:
            st.error(f"設定ファイルが見つかりません: {yaml_path}")
            return None
        except Exception as yaml_error:
            st.error(f"設定ファイルの読み込みエラー: {str(yaml_error)}")
            return None
        
        # 認証オブジェクトの作成
        authenticator = stauth.Authenticate(
            config['credentials'],
            config['cookie']['name'],
            config['cookie']['key'],
            config['cookie']['expiry_days']
        )
        
        # ロ���イン実行
        authenticator.login()

        if st.session_state.get("authentication_status"):
            if authenticator.logout('Logout', 'main', key='unique_key'):
                # セッションをクリア
                for key in list(st.session_state.keys()):
                    del st.session_state[key]
                st.rerun()
            st.write(f'ようこそ {st.session_state["name"]} さん')
            st.session_state['name'] = user_info['name']  # ユーザーの表示名
            st.session_state['email'] = user_info['email']  # ユーザーのメールアドレス
            return st.session_state.get("username")
        elif st.session_state.get("authentication_status") is False:
            st.error('ユーザー名またはパスワードが正しくありません')
        elif st.session_state.get("authentication_status") is None:
            st.warning('ユーザー名とパスワードを入力してください')

    except Exception as e:
        st.error(f"ログイン処理でエラー: {str(e)}")
        st.write(traceback.format_exc())
    
    return None