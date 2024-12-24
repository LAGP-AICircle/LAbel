import streamlit as st

def show_header():
    # カスタムCSS
    st.markdown(f"""
        <style>
        .header-container {{
            display: flex;
            justify-content: flex-end;
            padding: 1rem 2rem;
            background: var(--background-color);
            border-bottom: 1px solid var(--secondary-background-color);
            box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        }}
        .user-info {{
            display: flex;
            align-items: center;
            padding: 0.5rem 1rem;
            background: var(--secondary-background-color);
            border-radius: 50px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.05);
            transition: all 0.3s ease;
        }}
        .user-info:hover {{
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            transform: translateY(-1px);
        }}
        .user-icon {{
            font-size: 1.5rem;
            margin-right: 0.75rem;
            color: var(--primary-color);
        }}
        .user-name {{
            font-weight: 600;
            color: var(--text-color);
            font-size: 0.95rem;
            font-family: var(--font);
        }}
        </style>
    """, unsafe_allow_html=True)

    # ヘッダーの内容
    st.markdown(
        f"""
        <div class="header-container">
            <div class="user-info">
                <span class="user-icon">👤</span>
                <span class="user-name">{st.session_state['name']}</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    # スペースを追加して他のコンテンツと分離
    st.markdown("<div style='margin-bottom: 2rem;'></div>", unsafe_allow_html=True)