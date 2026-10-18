"""
CrossDomain Engine (アナロジカル・イノベーション・エンジン)
- 過去の確定実在事例からのアナロジー逆算・アイデア創出
- 4軸多次元一致率スコアリング（計100%）＆ 3段階ランク判定
- 難易度別（下・中・上）アイデア展開
- TeamWork共通パスワード認証ゲート搭載
- 最新モデル gemini-3.8-flash (JSON Mode) 稼働版
"""

import json
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
    .main { background-color: #0f1117; }
    .stTextArea textarea { font-size: 1.05rem !important; }
    .score-card {
        background-color: #1a202c;
        border: 1px solid #2d3748;
        border-radius: 8px;
        padding: 1.2rem;
        margin-bottom: 1rem;
    }
    .badge-high {
        background-color: #065f46;
        color: #34d399;
        font-weight: bold;
        padding: 0.3rem 0.8rem;
        border-radius: 6px;
        font-size: 1.1rem;
    }
    .badge-mid {
        background-color: #1e3a8a;
        color: #60a5fa;
        font-weight: bold;
        padding: 0.3rem 0.8rem;
        border-radius: 6px;
        font-size: 1.1rem;
    }
    .badge-low {
        background-color: #78350f;
        color: #fbbf24;
        font-weight: bold;
        padding: 0.3rem 0.8rem;
        border-radius: 6px;
        font-size: 1.1rem;
    }
    .idea-box-low {
        border-left: 5px solid #10b981;
        background-color: #132a24;
        padding: 1rem;
        border-radius: 6px;
        margin-bottom: 1rem;
    }
    .idea-box-mid {
        border-left: 5px solid #3b82f6;
        background-color: #172554;
        padding: 1rem;
        border-radius: 6px;
        margin-bottom: 1rem;
    }
    .idea-box-high {
        border-left: 5px solid #8b5cf6;
        background-color: #2e1065;
        padding: 1rem;
        border-radius: 6px;
        margin-bottom: 1rem;
    }
</style>
""", unsafe_allow_html=True)

# ==========================================
# 2. パスワード認証ゲート (TeamWork共通仕様)
# ==========================================
# secrets.toml に設定があればそれを使い、なければ "708" をデフォルト採用
APP_PASSWORD = st.secrets.get("APP_PASSWORD", "708")

if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if not st.session_state.authenticated:
    st.title("🔒 Access Restricted")
    st.caption("CrossDomain Engine - Analogical Innovation Platform")
    
    col1, col2, _ = st.columns([2, 1, 3])
    with col1:
        input_pw = st.text_input("パスワードを入力してください", type="password", key="login_field")
    with col2:
        st.write("")
        st.write("")
        login_btn = st.button("解除", type="primary", use_container_width=True)
    
    if login_btn or input_pw:
        if input_pw == APP_PASSWORD:
            st.session_state.authenticated = True
            st.rerun()
        else:
            st.error("パスワードが正しくありません。")
            
    st.stop()

# ==========================================
# 3. コンフィグレーション
# ==========================================
API_KEY = st.secrets.get("GEMINI_API_KEY", st.session_state.get("custom_api_key", ""))
TARGET_MODEL = "gemini-3.8-flash"

with st.sidebar:
    st.header("⚙️ システム設定")
    search_mode = st.radio(
        "探査モード",
        ["🌍 異分野越境モード（ブレイクスルー重視）", "🎯 近接ドメインモード（手堅い再現性重視）"],
        index=0
    )
    st.caption("・異分野越境：生物進化、軍事、宇宙、伝統産業など遠隔アナロジーを探索\n・近接ドメイン：製造業、SaaS、小売など構造が近いビジネス事例を探索")
    st.divider()
    
    if not st.secrets.get("GEMINI_API_KEY"):
        key_input = st.text_input("Gemini API Key", type="password", value=API_KEY)
        if key_input:
            st.session_state.custom_api_key = key_input
            API_KEY = key_input
            st.divider()
            
    if st.button("ログアウト (再ロック)", use_container_width=True):
        st.session_state.authenticated = False
        st.session_state.pop("custom_api_key", None)
        st.rerun()

# ==========================================
# 4. コアロジック（プロンプト＆API呼び出し）
# ==========================================
SYSTEM_INSTRUCTION = """
あなたは先人たちのイノベーション史、自然界の進化、特許、ビジネス史の全体系に精通したアナロジー思考の最高峰エンジン「CrossDomain」です。

ユーザーから提示された課題の表層を剥ぎ取り、「本質的な力学・因果・ジレンマの構造」を特定した上で、
過去に実在し検証可能な確定事例（架空の物語は厳禁）を逆算的に特定し、4軸の一致率スコアリング（計100%）と難易度別（下・中・上）のアイデア提案を行ってください。

【出力要件】：
必ず以下のJSONスキーマに完全準拠したJSONオブジェクトのみを出力してください。Markdownのバッククォート等も不要です。

{
  "problem_abstraction": {
    "core_dilemma": "課題の本質的な対立構造・ジレンマ",
    "structural_bottleneck": "表層の言葉を剥ぎ取った力学的ボトルネック"
  },
  "analogous_case": {
    "title": "実在する先例・事例の正式名称",
    "era_and_domain": "発生年代および該当分野（例：1960年代・NASA宇宙工学、生物界の共生関係 等）",
    "historical_fact": "当時実際に存在した課題と、それをどう解決したかという確認可能な歴史的事実",
    "transfer_logic": "なぜその事例の解決ロジックが、今回の課題に対してアナロジーとして成立するのかの因果律"
  },
  "matching_scores": {
    "structural_match": 20,
    "structural_reason": "採点根拠",
    "vector_match": 22,
    "vector_reason": "採点根拠",
    "cross_domain_match": 18,
    "cross_domain_reason": "採点根拠",
    "constraint_match": 21,
    "constraint_reason": "採点根拠",
    "total_score": 81,
    "rank": "かなり似ている"
  },
  "action_proposals": {
    "low_difficulty": {
      "level": "難易度【下】：即時・低摩擦のクイックウィン",
      "summary": "明日から既存リソースの範囲でできる試行",
      "action_detail": "具体的なアクションと仕組み"
    },
    "mid_difficulty": {
      "level": "難易度【中】：プロセスの再設計・構造改革",
      "summary": "ルール改定やフロー見直しを伴う本格運用",
      "action_detail": "具体的なアクションと仕組み"
    },
    "high_difficulty": {
      "level": "難易度【上】：前提を覆すゲームチェンジ",
      "summary": "ビジネスモデルやパラダイムの転換を伴う大技",
      "action_detail": "具体的なアクションと仕組み"
    }
  }
}
"""

def run_crossdomain_engine(user_prompt: str, mode: str) -> dict:
    if not API_KEY:
        raise ValueError("APIキーが設定されていません。")
        
    client = genai.Client(api_key=API_KEY)
    
    prompt = f"""
【探査モード】：{mode}
【検討課題・解決したい問い】：
{user_prompt}
"""
    
    response = client.models.generate_content(
        model=TARGET_MODEL,
        contents=[prompt],
        config=types.GenerateContentConfig(
            system_instruction=SYSTEM_INSTRUCTION,
            temperature=0.7,
            response_mime_type="application/json"
        )
    )
    
    return json.loads(response.text)

# ==========================================
# 5. メインUI
# ==========================================
st.title("💡 CrossDomain Engine")
st.caption("過去の確定先例から解を逆算する、アナロジカル・イノベーション・プラットフォーム")

default_issue = (
    "社内マニュアルをいくら整備しても若手社員が読まず、"
    "口頭で同じ質問を繰り返してベテランの業務時間を奪っている。"
    "読ませることを強制せず、自然と自律解決に向かわせるアイデアはないか。"
)
user_input = st.text_area("解決したい課題・問いを入力", value=default_issue, height=110)

col_run, _ = st.columns([2, 5])
with col_run:
    start_btn = st.button("🚀 先例を逆算・アナロジー発想を開始", type="primary", use_container_width=True)

# ==========================================
# 6. 解析＆描画パイプライン
# ==========================================
if start_btn:
    if not API_KEY:
        st.error("Gemini APIキーを設定してください。")
    elif not user_input.strip():
        st.warning("課題を入力してください。")
    else:
        with st.status("🔍 確定過去事例の探査・アナロジー逆算中...", expanded=True) as status:
            t0 = time.time()
            try:
                status.write("1. 課題の本質構造とジレンマを抽象化中...")
                status.write("2. 歴史・自然界・特許・他産業から実在アンカー事例を抽出中...")
                status.write("3. 4軸多次元一致率スコアを積算中...")
                
                result = run_crossdomain_engine(user_input, search_mode)
                
                status.update(label=f"✅ 解析完了 (+{time.time() - t0:.1f}秒)", state="complete", expanded=False)
                
                # --- 結果描画 ---
                scores = result["matching_scores"]
                total = scores["total_score"]
                rank = scores["rank"]
                
                st.divider()
                
                # 総合一致率ヘッダー
                col_badge, col_meter = st.columns([2, 5])
                with col_badge:
                    if total >= 80:
                        st.markdown(f"<span class='badge-high'>一致率: {total}% ｜ {rank}</span>", unsafe_allow_html=True)
                    elif total >= 55:
                        st.markdown(f"<span class='badge-mid'>一致率: {total}% ｜ {rank}</span>", unsafe_allow_html=True)
                    else:
                        st.markdown(f"<span class='badge-low'>一致率: {total}% ｜ {rank}</span>", unsafe_allow_html=True)
                with col_meter:
                    st.progress(total / 100)
                
                st.write("")
                
                # 2カラム：左に先例情報、右にスコア内訳
                col_case, col_score = st.columns([3, 2])
                
                with col_case:
                    case = result["analogous_case"]
                    abstr = result["problem_abstraction"]
                    
                    st.markdown("### 🏛️ 逆算された実在アンカー事例")
                    with st.container(border=True):
                        st.subheader(f"📌 {case['title']}")
                        st.caption(f"**年代・分野**: {case['era_and_domain']}")
                        st.markdown(f"**【歴史的ファクト・当時の解決策】**\n\n{case['historical_fact']}")
                        st.divider()
                        st.markdown(f"**【アナロジー転用ロジック】**\n\n{case['transfer_logic']}")
                        st.caption(f"※課題の抽象構造: {abstr['core_dilemma']} ｜ ボトルネック: {abstr['structural_bottleneck']}")

                with col_score:
                    st.markdown("### 📊 4軸一致率の内訳")
                    with st.container(border=True):
                        st.markdown(f"**① 構造・機構一致度**: `{scores['structural_match']}/25`")
                        st.caption(scores["structural_reason"])
                        
                        st.markdown(f"**② ベクトル・方向性一致度**: `{scores['vector_match']}/25`")
                        st.caption(scores["vector_reason"])
                        
                        st.markdown(f"**③ 異分野・目的一致度**: `{scores['cross_domain_match']}/25`")
                        st.caption(scores["cross_domain_reason"])
                        
                        st.markdown(f"**④ 環境・力学制約一致度**: `{scores['constraint_match']}/25`")
                        st.caption(scores["constraint_reason"])

                # 難易度別アイデア提案
                st.divider()
                st.markdown("### 🎯 先例ロジックに基づく3段階アイデア提案")
                
                proposals = result["action_proposals"]
                
                col_l, col_m, col_h = st.columns(3)
                
                with col_l:
                    p = proposals["low_difficulty"]
                    st.markdown(f"""
                    <div class='idea-box-low'>
                        <h4>🟢 {p['level']}</h4>
                        <b>{p['summary']}</b>
                        <hr style='border:0.5px solid #2d3748;'>
                        {p['action_detail']}
                    </div>
                    """, unsafe_allow_html=True)
                    
                with col_m:
                    p = proposals["mid_difficulty"]
                    st.markdown(f"""
                    <div class='idea-box-mid'>
                        <h4>🔵 {p['level']}</h4>
                        <b>{p['summary']}</b>
                        <hr style='border:0.5px solid #2d3748;'>
                        {p['action_detail']}
                    </div>
                    """, unsafe_allow_html=True)
                    
                with col_h:
                    p = proposals["high_difficulty"]
                    st.markdown(f"""
                    <div class='idea-box-high'>
                        <h4>🟣 {p['level']}</h4>
                        <b>{p['summary']}</b>
                        <hr style='border:0.5px solid #2d3748;'>
                        {p['action_detail']}
                    </div>
                    """, unsafe_allow_html=True)
                
                # Markdown ダウンロード
                md_output = f"""# CrossDomain アナロジー着想レポート
課題: {user_input}
探査モード: {search_mode}
総合一致率: {total}% ({rank})

---
## ■ 逆算された実在アンカー事例
- **名称**: {case['title']}
- **年代・分野**: {case['era_and_domain']}
- **歴史的ファクト**: {case['historical_fact']}
- **転用因果律**: {case['transfer_logic']}

---
## ■ 4軸一致率スコア
1. 構造・機構一致度: {scores['structural_match']}/25 ({scores['structural_reason']})
2. ベクトル一致度: {scores['vector_match']}/25 ({scores['vector_reason']})
3. 異分野一致度: {scores['cross_domain_match']}/25 ({scores['cross_domain_reason']})
4. 制約一致度: {scores['constraint_match']}/25 ({scores['constraint_reason']})

---
## ■ 難易度別アクション提案
### {proposals['low_difficulty']['level']}
- **概要**: {proposals['low_difficulty']['summary']}
- **詳細**: {proposals['low_difficulty']['action_detail']}

### {proposals['mid_difficulty']['level']}
- **概要**: {proposals['mid_difficulty']['summary']}
- **詳細**: {proposals['mid_difficulty']['action_detail']}

### {proposals['high_difficulty']['level']}
- **概要**: {proposals['high_difficulty']['summary']}
- **詳細**: {proposals['high_difficulty']['action_detail']}
"""
                st.download_button(
                    "📥 この着想レポートをMarkdownで保存",
                    data=md_output.encode("utf-8"),
                    file_name="crossdomain_idea_report.md",
                    mime="text/markdown",
                    use_container_width=True
                )
                
            except Exception as e:
                status.update(label="❌ エラーが発生しました", state="error")
                st.error(f"解析中にエラーが発生しました: {e}")