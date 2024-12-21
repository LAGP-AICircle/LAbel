import streamlit as st
from pathlib import Path
import tempfile
import os
from typing import Optional, List
from datetime import datetime
from openai import OpenAI
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage
from config.settings import get_openai_api_key, get_setting, SUPPORTED_AUDIO_FORMATS
from pydub import AudioSegment

# OpenAI APIキーを取得
OPENAI_API_KEY = get_openai_api_key()

# FFmpegの設定を環境に応じて変更
if os.environ.get('STREAMLIT_CLOUD'):
    # StreamlitCloud環境ではシステムのFFmpegを使用
    FFMPEG_PATH = "/usr/bin"  # Linuxシステムの標準的なパス
else:
    # ローカル環境（Windows）用の設定
    FFMPEG_PATH = r"C:\Users\r0u8b\OneDrive\一時保管場所（削除してよいもの）\ffmpeg-master-latest-win64-gpl\ffmpeg-master-latest-win64-gpl\bin"

# 環境変数にFFmpegのパスを追加
os.environ["PATH"] = os.environ["PATH"] + os.pathsep + FFMPEG_PATH

# OSに応じてFFmpegの設定を変更
if os.name == 'nt':  # Windowsの場合
    AudioSegment.converter = os.path.join(FFMPEG_PATH, "ffmpeg.exe")
    AudioSegment.ffmpeg = os.path.join(FFMPEG_PATH, "ffmpeg.exe")
    AudioSegment.ffprobe = os.path.join(FFMPEG_PATH, "ffprobe.exe")

def initialize_minutes_state():
    """議事録機能のセッション状態を初期化"""
    if 'minutes_state' not in st.session_state:
        st.session_state.minutes_state = {
            'transcription': None,
            'minutes': None,
            'meeting_date': datetime.now(),
            'meeting_name': ""
        }

def transcribe_audio(client: OpenAI, audio_file) -> str:
    """音声ファイルの文字起こし処理"""
    try:
        transcription = client.audio.transcriptions.create(
            model="whisper-1",
            file=audio_file,
            response_format="text"
        )
        return transcription
    except Exception as e:
        st.error(f"文字起こし処理中にエラーが発生しました: {str(e)}")
        return ""

def generate_minutes(transcription: str) -> bool:
    """議事録の生成"""
    try:
        chat_model = ChatOpenAI(
            model="gpt-4o-mini",
            temperature=0,
            api_key=OPENAI_API_KEY
        )
        
        system_prompt = """
        以下の文字起こしデータから、簡潔で分かりやすい議事録を作成してください。
        
        フォーマット:                        
        # 議事内容
        - 重要なポイントを箇条書きで記載
                    
        # アクションアイテム
        - ミーティング後に行うアクションを箇条書きで記載
        
        # 会議内容
        - 会話のテーマを大項目事に分類して記載
        - 中項目、小項目として発言内容を記載していく
        - できる限りやり取りを網羅しつつ、一つ一つは簡潔に要約

        # 次回開催日時
        - 言及があれば記載
        """
        
        with st.spinner('議事録を生成中...'):
            messages = [
                HumanMessage(content=f"{system_prompt}\n\n文字起こしデータ:\n{transcription}")
            ]
            response = chat_model.invoke(messages)
            st.session_state.minutes_state['minutes'] = response.content
            return True
            
    except Exception as e:
        st.error(f"議事録生成中にエラーが発生しました: {str(e)}")
        return False

def save_minutes(minutes_text: str) -> tuple[Optional[str], Optional[str]]:
    """議事録の保存"""
    try:
        # ファイル名の生成
        date_str = st.session_state.minutes_state['meeting_date'].strftime('%Y%m%d')
        meeting_name = st.session_state.minutes_state['meeting_name'].strip()
        if not meeting_name:
            meeting_name = "議事録"
        filename = f"{date_str}_{meeting_name}.txt"
        
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt', encoding='utf-8') as tmp_file:
            # 会議情報をヘッダーとし���追加
            header = f"会議名: {meeting_name}\n"
            header += f"開催日: {st.session_state.minutes_state['meeting_date'].strftime('%Y年%m月%d日')}\n\n"
            tmp_file.write(header + minutes_text)
            return tmp_file.name, filename
    except Exception as e:
        st.error(f"ファイル保存中にエラーが発生しました: {str(e)}")
        return None, None

def minutes_page():
    """議事録ページのメイン関数"""
    initialize_minutes_state()
    
    st.title("📝 議事録作成")
    st.write("音声ファイルをアップロードして、AIで議事録を自動生成します。")

    # 会議情報入力
    cols = st.columns(2)
    with cols[0]:
        meeting_date = st.date_input(
            "会議日付",
            value=st.session_state.minutes_state['meeting_date'],
            format="YYYY/MM/DD",
            key="meeting_date_input"
        )
        st.session_state.minutes_state['meeting_date'] = meeting_date
        
    with cols[1]:
        meeting_name = st.text_input(
            "会議名",
            value=st.session_state.minutes_state['meeting_name'],
            placeholder="例：ACR技術太郎_ヒアリング",
            key="meeting_name_input"
        )
        st.session_state.minutes_state['meeting_name'] = meeting_name

    # ファイルアップロード
    st.info("25MB以上の音声ファイルは分割して処理します")
    uploaded_file = st.file_uploader(
        "音声ファイルをアップロード",
        type=SUPPORTED_AUDIO_FORMATS,
        help=f"対応形式: {', '.join(SUPPORTED_AUDIO_FORMATS)}",
        key="audio_uploader"
    )
    
    if uploaded_file:
        file_size = len(uploaded_file.getvalue()) / (1024 * 1024)  # MB単位
        st.write(f"ファイルサイズ: {file_size:.1f}MB")
        
        if st.button("文字起こしを開始", key="transcribe_btn"):
            process_audio_file(uploaded_file)
    
    # 議事録の表示
    if st.session_state.minutes_state['minutes']:
        st.subheader("生成された議事録")
        edited_minutes = st.text_area(
            "議事録（編集可能）",
            st.session_state.minutes_state['minutes'],
            height=400,
            key="minutes_editor"
        )
        
        cols = st.columns(2)
        with cols[0]:
            if st.button("議事録をダウンロード", key="download_btn"):
                tmp_path, filename = save_minutes(edited_minutes)
                if tmp_path and filename:
                    with open(tmp_path, 'r', encoding='utf-8') as f:
                        st.download_button(
                            "テキストファイルをダウンロード",
                            f,
                            filename,
                            mime="text/plain",
                            key="download_file_btn"
                        )
                    os.unlink(tmp_path)
        
        with cols[1]:
            if st.button("新規作成", key="new_minutes_btn"):
                initialize_minutes_state()
                st.rerun()

def process_audio_file(uploaded_file) -> bool:
    """音声ファイルの処理"""
    if not OPENAI_API_KEY:
        st.error("OpenAI APIキーが設定されていません。")
        return False

    try:
        # 音声データを一時的にバイトデータとして保持
        audio_data = uploaded_file.getvalue()
        file_size = len(audio_data)
        MAX_CHUNK_SIZE = 24 * 1024 * 1024  # 24MB
        
        if file_size > MAX_CHUNK_SIZE:
            st.info("ファイルサイズが25MBを超えるため、分割して処理します。")
            
            try:
                # 一時ファイルを作成（delete=Falseで明示的に削除するまでファイルを保持）
                with tempfile.NamedTemporaryFile(suffix=f'.{uploaded_file.name.split(".")[-1]}', delete=False) as temp_file:
                    temp_file.write(audio_data)
                    temp_path = temp_file.name

                try:
                    # 音声ファイルを読み込む
                    st.write(f"Loading audio file from: {temp_path}")  # デバッグ用
                    st.write(f"File exists: {os.path.exists(temp_path)}")  # デバッグ用
                    audio = AudioSegment.from_file(temp_path)
                    
                    # サイズベースではなく時間ベースで分割（10分ごと）
                    chunk_length_ms = 10 * 60 * 1000  # 10分
                    chunks = [audio[i:i + chunk_length_ms] for i in range(0, len(audio), chunk_length_ms)]
                    
                    transcriptions = []
                    client = OpenAI(api_key=OPENAI_API_KEY)
                    
                    # 各チャンクを処理
                    with st.spinner('音声の文字起こしを実行中...'):
                        for i, chunk in enumerate(chunks):
                            st.write(f"パート {i+1}/{len(chunks)} を処理中...")
                            
                            # チャンクを一時ファイルとして保存
                            chunk_path = f"{temp_path}_chunk_{i}.mp3"
                            chunk.export(chunk_path, format='mp3')
                            
                            try:
                                # 文字起こし実行
                                with open(chunk_path, 'rb') as f:
                                    transcription = transcribe_audio(client, f)
                                    transcriptions.append(transcription)
                            finally:
                                # チャンクファイルを削除
                                if os.path.exists(chunk_path):
                                    os.unlink(chunk_path)
                    
                    # 文字起こし結果の結合
                    full_transcription = " ".join(transcriptions)
                    
                finally:
                    # 元の一時ファイルを削除
                    if os.path.exists(temp_path):
                        os.unlink(temp_path)
                
            except Exception as e:
                st.error(f"音声分割処理中にエラーが発生しました: {str(e)}")
                return False
            
            # 文字起こし結果の結合
            full_transcription = " ".join(transcriptions)
            
        else:
            # 25MB以下のファイルは直接処理
            client = OpenAI(api_key=OPENAI_API_KEY)
            with st.spinner('音声の文字起こしを実行中...'):
                full_transcription = client.audio.transcriptions.create(
                    model="whisper-1",
                    file=uploaded_file,
                    response_format="text"
                )

        # 文字起こし結果の表示と議事録生成
        if full_transcription:
            st.session_state.minutes_state['transcription'] = full_transcription
            st.subheader("文字起こし結果")
            st.text_area(
                "文字起こしテキスト",
                full_transcription,
                height=200,
                key="transcription_result"
            )
            
            # 議事録の自動生成
            with st.spinner('議事録を生成中...'):
                generate_minutes(full_transcription)
            
            return True
        else:
            st.error("文字起こしに失敗しました。")
            return False
            
    except Exception as e:
        st.error(f"処理中にエラーが発生しました: {str(e)}")
        return False

if __name__ == "__main__":
    minutes_page()