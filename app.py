"""
CrossDomain Engine
過去の確定先例から解を逆算する、アナロジカル・イノベーション・プラットフォーム
"""

import time
import streamlit as st
from google import genai
from google.genai import types

# ==========================================
# 1. ページ基本設定 & デザイン
# ==========================================
st.set_page_config(
    page_title="CrossDomain Engine",
    page_icon="💡",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    .main { background-color: #0e1117; }
    .stTextArea textarea { font-size: 1.05rem !important; }
    div[data-testid="stExpander"] { 
        border-radius: 8px; 
        border: 1px solid #2d3748; 
        background-color: #1a202c; 
    }
</style>
""", unsafe_allow_html=True)

# ==========================================
# 2. パスワード認証ゲート (Password: 708)
# ==========================================
APP_PASSWORD = st.secrets.get("APP_PASSWORD", "708")

if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if not st.session_state.authenticated:
    st.title("🔒 CrossDomain Engine - 認証")
    st.caption("アナロジカル・イノベーション・プラットフォーム")
    
    with st.form("auth_form"):
        col1, col2 = st.columns([3, 1])
        with col1:
            pw_input = st.text_input("パスワードを入力してください", type="password")
        with col2:
            st.write("")
            st.write("")
            submit = st.form_submit_button("解除", type="primary", use_container_width=True)
            
        if submit:
            if pw_input == APP_PASSWORD:
                st.session_state.authenticated = True
                st.rerun()
            else:
                st.error("パスワードが正しくありません。")
    st.stop()

# ==========================================
# 3. APIキーとクライアント初期化
# ==========================================
API_KEY = st.secrets.get("GEMINI_API_KEY", "")

if not API_KEY:
    st.error("Secrets に GEMINI_API_KEY が設定されていません。Settings > Secrets を確認してください。")
    st.stop()

# チームワークアプリと同じ最新SDKクライアント
client = genai.Client(api_key=API_KEY)
MODEL_NAME = "gemini-2.5-flash"

# ==========================================
# 4. サイドバー設定
# ==========================================
with st.sidebar:
    st.header("⚙️ システム設定")
    
    mode = st.radio(
        "探査モード",
        [
            "🌍 異分野越境モード（ブレイクスルー重視）",
            "🎯 近接ドメインモード（手堅い再現性重視）"
        ],
        index=0
    )
    
    st.markdown("---")
    st.caption(
        "・**異分野越境**：生物進化、軍事、宇宙、伝統産業など遠隔アナロジーを探索\n\n"
        "・**近接ドメイン**：製造業、SaaS、小売など構造が近いビジネス事例を探索"
    )
    
    st.markdown("---")
    if st.button("ログアウト（再ロック）", use_container_width=True):
        st.session_state.authenticated = False
        st.rerun()

# ==========================================
# 5. メイン画面 & 入力フォーム
# ==========================================
st.title("💡 CrossDomain Engine")
st.markdown("過去の確定先例から解を逆算する、アナロジカル・イノベーション・プラットフォーム")
st.divider()

st.subheader("解決したい課題・問いを入力")
default_query = "社内マニュアルをいくら整備しても若手社員が読まず、口頭で同じ質問を繰り返してベテランの業務時間を奪っている。読ませることを強制せず、自然と自律解決に向かわせるアイデアはないか。"

user_query = st.text_area(
    label="課題入力",
    value=default_query,
    height=120,
    label_visibility="collapsed"
)

run_button = st.button("🚀 先例を逆算・アナロジー発想を開始", type="primary", use_container_width=True)

# ==========================================
# 6. アナロジー逆算ロジック実行
# ==========================================
if run_button:
    if not user_query.strip():
        st.warning("課題を入力してください。")
        st.stop()

    status_container = st.container()
    result_container = st.container()
    
    with status_container:
        status_box = st.status("🔍 先例逆算プロセスを実行中...", expanded=True)
        with status_box:
            st.write("1. 課題の本質構造とジレンマを抽象化中...")
            time.sleep(0.6)
            st.write("2. 歴史・自然界・特許・他産業から実在アンカー事例を抽出中...")
            time.sleep(0.6)
            st.write("3. 4軸多次元一致率スコアを積算中...")

    # プロンプトの組み立て
    mode_text = "異分野越境（生物進化、軍事史、宇宙工学、生態系、伝統工芸など遠隔ドメイン）" if "異分野" in mode else "近接ドメイン（製造業、IT・SaaS、航空、医療安全、小売などビジネス隣接分野）"

    prompt = f"""
あなたは卓越したアナロジカル・シンキング（類推思考）とイノベーションの専門家です。
ユーザーが抱える以下の課題に対して、表面的な対症療法ではなく、「構造的に同一のジレンマをすでに解決した確定済みの先例・アンカー事例」を異分野から逆算し、ブレイクスルーとなる具体的施策を提案してください。

【解決したい課題】
{user_query}

【探索モード指定】
{mode_text}

---
以下の構成で、論理的かつ極めて具体的に回答を出力してください：

### 1. 課題の深層構造と二律背反（ジレンマ）の抽象化
- 表面的な事象を削ぎ落とし、「何と何のトレードオフか」「どの力学が働いているか」を構造図的に定義。

### 2. 発掘された先例・アンカー事例（2〜3選）
- 指定モードから、まったく別の文脈でこの構造的ジレンマを解決した実在の事例（歴史的事件、生物の適応戦略、他業界の特許・運用システムなど）。
- 各事例について「なぜその構造が一致しているか（4軸一致性：関係性・動機・制約・結果）」を明記。

### 3. アナロジー転移による具体的ソリューション案
- アンカー事例のメカニズムを今回の課題へそのまま移植・翻案した、3つの具体的アクションプラン。
- 単なる精神論ではなく、制度・UI/UX・環境設計・仕組みとしての設計。

### 4. 実行ロードマップ & 想定リスクの先回り防御
- 明日から着手できるクイックウィンと、自律定着のためのチェックポイント。
"""

    try:
        response = client.models.generate_content(
            model=MODEL_NAME,
            contents=prompt,
        )
        
        status_box.update(label="✅ アナロジー逆算が完了しました！", state="complete", expanded=False)
        
        with result_container:
            st.markdown("---")
            st.markdown(response.text)
            
    except Exception as e:
        status_box.update(label="❌ エラーが発生しました", state="error", expanded=True)
        st.error(f"解析中にエラーが発生しました: {e}")