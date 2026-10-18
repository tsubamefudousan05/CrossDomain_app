"""
CrossDomain Engine - Master Harmony & Soul Edition
- 🏛️ 帝国総研：基底直交探索 ＆ 独立監査レイヤー
- ⚖️ 最高裁判所：構造化JSONによる拒絶権（Circuit Breaker）＆ 完全例外保護 ＆ 免責条項
- 🌸 仙人茶会：第5基底（生活知・偏愛贈与）＆ アンドン型対話 ＆ 魂の昇華アルゴリズム（Constraint-to-Prestige）
"""

import time
import json
import concurrent.futures
import streamlit as st
from google import genai
from google.genai import types

# ==========================================
# 1. ページ基本設定 & デザイン
# ==========================================
st.set_page_config(
    page_title="CrossDomain Engine",
    page_icon="🌸",
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
    .investigator-card {
        border-left: 4px solid #3b82f6;
        background-color: #1e293b;
        padding: 1rem;
        border-radius: 6px;
        margin-bottom: 0.8rem;
    }
    .audit-card {
        border-left: 4px solid #ef4444;
        background-color: #2a1515;
        padding: 1rem;
        border-radius: 6px;
        margin-bottom: 0.8rem;
    }
    .andon-box {
        border-left: 5px solid #f59e0b;
        background-color: #291e0a;
        padding: 1.2rem;
        border-radius: 6px;
        margin-bottom: 1.2rem;
    }
    .disclaimer-box {
        border: 1px solid #4a5568;
        background-color: #171923;
        padding: 0.8rem;
        border-radius: 4px;
        font-size: 0.82rem;
        color: #a0aec0;
        margin-top: 1.5rem;
    }
</style>
""", unsafe_allow_html=True)

LEGAL_DISCLAIMER = """
【免責事項および法的注意事項】
本システム「CrossDomain Engine」が導出するアナロジー解析結果、先例情報、および具体的施策案は、創造的発想の支援を目的とした自動生成情報であり、いかなる法的、財務的、経営的、安全管理上の保証または専門的助言を構成するものではありません。
本システムの出力結果を採用、実装、運用したことにより生じたいかなる損害（直接的・間接的・派生的損害、逸失利益、業務中断、信用毀損等を含む）についても、開発者および運営者は一切の法的責任を負いません。最終判断および法令遵守の確認は、必ず利用者の自己責任において行ってください。
"""

# ==========================================
# 2. Fail-Closed 型認証ゲート
# ==========================================
APP_PASSWORD = st.secrets.get("APP_PASSWORD")

if not APP_PASSWORD:
    st.error("【重大な設定エラー】：Secrets に APP_PASSWORD が設定されていません。システムはFail-Closed原則に基づき起動を拒絶します。")
    st.stop()

if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if not st.session_state.authenticated:
    st.title("🔒 CrossDomain Engine - 認証")
    st.caption("Master Harmony Platform ｜ 厳格なる統治と至高の創造")
    
    with st.form("auth_form"):
        pw_input = st.text_input("アクセスキーを入力してください", type="password")
        agree_terms = st.checkbox("上記および本システムの【完全免責条項】に同意し、自己責任で利用します")
        submit = st.form_submit_button("認証解除", type="primary", use_container_width=True)
            
        if submit:
            if not agree_terms:
                st.error("免責条項への同意が必須です。")
            elif pw_input == APP_PASSWORD:
                st.session_state.authenticated = True
                st.rerun()
            else:
                st.error("アクセスキーが無効です。")
                
    st.markdown(f"<div class='disclaimer-box'>{LEGAL_DISCLAIMER}</div>", unsafe_allow_html=True)
    st.stop()

# ==========================================
# 3. APIクライアント初期化 & 通信保護
# ==========================================
API_KEY = st.secrets.get("GEMINI_API_KEY", "")

if not API_KEY:
    st.error("【重大な設定エラー】：Secrets に GEMINI_API_KEY が設定されていません。")
    st.stop()

client = genai.Client(api_key=API_KEY)
MODEL_NAME = "gemini-3.8-flash"

def call_gemini_safe(prompt: str, json_schema=None, max_retries: int = 3, base_delay: float = 1.5) -> str:
    """指数バックオフと構造的例外処理を備えた通信ラッパー"""
    last_exception = None
    config_params = {}
    
    if json_schema:
        config_params["response_mime_type"] = "application/json"
        config_params["response_schema"] = json_schema
        
    config = types.GenerateContentConfig(**config_params) if config_params else None

    for attempt in range(max_retries):
        try:
            response = client.models.generate_content(
                model=MODEL_NAME,
                contents=prompt,
                config=config
            )
            if response.text:
                return response.text.strip()
            raise ValueError("APIから空の応答が返却されました。")
        except Exception as e:
            last_exception = e
            err_str = str(e)
            if any(term in err_str for term in ["429", "503", "RESOURCE_EXHAUSTED", "UNAVAILABLE"]):
                time.sleep(base_delay * (2 ** attempt))
            elif attempt < max_retries - 1:
                time.sleep(1.0)
            else:
                break
                
    raise RuntimeError(f"通信路障害（リトライ上限超過）: {last_exception}")

# セッション状態の初期化
if "analysis_result" not in st.session_state:
    st.session_state.analysis_result = None
if "research_reports" not in st.session_state:
    st.session_state.research_reports = []
if "audit_data" not in st.session_state:
    st.session_state.audit_data = None
if "current_query" not in st.session_state:
    st.session_state.current_query = ""

# ==========================================
# 4. 5大直交コア（仙人茶会・第5基底を配備）
# ==========================================
INVESTIGATORS = [
    {
        "id": "agent_alpha",
        "name": "🌌 Agent α【無機物理・散逸構造 調査官】",
        "focus": "138億年の物理普遍秩序。非平衡熱力学（散逸構造・エントロピー排出力学）、相転移、自己組織化臨界現象、ネットワークトポロジーからの構造転移。"
    },
    {
        "id": "agent_beta",
        "name": "🧬 Agent β【有機生命・淘汰適応 調査官】",
        "focus": "40億年の生命史。過酷な淘汰圧を生き抜いた適応放散、共生プロトコル、極限環境耐性、エネルギー極小化形態進化からの構造転移。"
    },
    {
        "id": "agent_gamma",
        "name": "🏛️ Agent γ【法理統御・市場設計 調査官】",
        "focus": "人類数千年の統治と資本秩序。ローマ法・信託法理、国家統治・軍事兵站、メカニズムデザイン（ゲーム理論）、信賞必罰、インセンティブ整合的均衡プロトコルからの構造転移。"
    },
    {
        "id": "agent_delta",
        "name": "🧠 Agent δ【深層心理・認知幾何 調査官】",
        "focus": "人間の心理的防衛機制（反動形成の無力化）、選択アーキテクチャ（ナッジ）、物理的制約（フールプルーフ）、儀礼・共同体規範による情動昇華機構からの構造転移。"
    },
    {
        "id": "agent_epsilon",
        "name": "🌸 Agent ε【生活知・偏愛贈与・祝祭 調査官】",
        "focus": "【仙人茶会・第5基底】生活者の路地裏の知恵、職人の偏執的こだわり（Craftsmanship）、損得勘定を超えた贈与経済、1%のコア層を狂喜させる熱狂の儀式、人を自発的に動かす『愛嬌とロマン』からの構造転移。"
    }
]

# ==========================================
# 5. サイドバー設定
# ==========================================
with st.sidebar:
    st.header("⚙️ 統合ガバナンス構成")
    st.caption("🏛️ 帝国総研 ✕ ⚖️ 最高裁 ✕ 🌸 仙人茶会")
    
    mode = st.radio(
        "探査モード",
        [
            "🌍 異分野越境モード（ブレイクスルー重視）",
            "🎯 近接ドメインモード（手堅い再現性重視）"
        ],
        index=0
    )
    
    risk_threshold = st.slider(
        "🛡️ アンドン遮断（VETO）発動閾値",
        min_value=50,
        max_value=95,
        value=80,
        step=5,
        help="Red Teamが判定したテールリスク指数がこの値を超えた場合、品質保護のためアンドンが引かれ再設計を促します。"
    )
    
    st.markdown("---")
    st.caption(
        "**【基底直交5大コア】**\n"
        "・α：無機物理・散逸構造\n"
        "・β：有機生命・淘汰適応\n"
        "・γ：法理統御・市場設計\n"
        "・δ：深層心理・認知幾何\n"
        "・ε：生活知・偏愛贈与（魂の基底）\n\n"
        "**【独立監査・アンドン機構】**\n"
        "・Critical Red Team ✕ Andon-UX\n"
        "・Constraint-to-Prestige 昇華変換"
    )
    
    st.markdown("---")
    if st.button("ログアウト（再ロック）", use_container_width=True):
        st.session_state.authenticated = False
        st.session_state.analysis_result = None
        st.session_state.research_reports = []
        st.session_state.audit_data = None
        st.rerun()

# ==========================================
# 6. メイン画面 & 入力フォーム
# ==========================================
st.title("💡 CrossDomain Engine")
st.markdown("鉄壁の統治・監査要塞の上に、人の心を震わせる熱狂と調和のアイデアを逆算するプラットフォーム")
st.divider()

st.subheader("解決したい課題・問いを入力")
default_query = "社内マニュアルをいくら整備しても若手社員が読まず、口頭で同じ質問を繰り返してベテランの業務時間を奪っている。読ませることを強制せず、自然と自律解決に向かわせるアイデアはないか。"

user_query = st.text_area(
    label="課題入力",
    value=default_query,
    height=120,
    label_visibility="collapsed"
)

run_button = st.button("🚀 5大直交コア出動 ＆ 調和発案パイプラインを実行", type="primary", use_container_width=True)

# ==========================================
# 7. パイプライン実行ロジック
# ==========================================
def run_single_investigator(inv, query, current_mode):
    prompt = f"""
あなたは【{inv['name']}】です。
【担当領域】：{inv['focus']}
【探査モード】：{current_mode}

ユーザーが提示した課題の深層構造を分析し、あなたの専門基底から
「この構造的ジレンマを解決した実在の確定先例・普遍の法則・人間的営み」を採掘してください。

【解決すべき課題】
{query}

【出力要件】：
1. 発掘した実在事例名・法則・制度・生活文化名とその背景
2. 課題との構造的一致点（因果ループと力学の相似性）
3. その事例が成立させた「不可逆的・自律的な解決ギミック」
4. 【前提崩壊リスク】：この構造を適用する上で前提が崩れた際、生じる致命的リスク
"""
    ans = call_gemini_safe(prompt)
    return inv, ans

if run_button:
    if not user_query.strip():
        st.warning("課題を入力してください。")
        st.stop()

    t_start = time.time()
    st.session_state.research_reports = []
    st.session_state.audit_data = None
    st.session_state.analysis_result = None
    
    with st.status("🌸 調和と統治の多層パイプライン駆動中...", expanded=True) as status_box:
        try:
            # ------------------------------------------------------------------
            # Phase 1: 5コア並列探索
            # ------------------------------------------------------------------
            st.write("🌌 [第1フェーズ：5大直交探索] 物理・生命・統御・心理・生活知の5方向から深層採掘中...")
            with concurrent.futures.ThreadPoolExecutor(max_workers=len(INVESTIGATORS)) as executor:
                future_to_inv = {
                    executor.submit(run_single_investigator, inv, user_query, mode): inv 
                    for inv in INVESTIGATORS
                }
                for future in concurrent.futures.as_completed(future_to_inv):
                    inv, report_text = future.result()
                    st.session_state.research_reports.append((inv, report_text))
                    st.write(f"  ✓ {inv['name']} 報告受領")

            aggregated_research = "\n\n".join([
                f"=== 【{inv['name']} の採掘報告】 ===\n{text}" 
                for inv, text in st.session_state.research_reports
            ])

            # ------------------------------------------------------------------
            # Phase 2: Critical Red Team 監査（構造化JSON）
            # ------------------------------------------------------------------
            st.write("🛡️ [第2フェーズ：冷徹な監査] Critical Red Team による破滅リスク・サボタージュ検証...")
            
            red_team_schema = {
                "type": "OBJECT",
                "properties": {
                    "survivorship_bias_analysis": {"type": "STRING", "description": "生存バイアスおよび対照群の分析"},
                    "sabotage_vulnerabilities": {"type": "STRING", "description": "サボタージュおよび脱法脆弱性"},
                    "tail_risk_analysis": {"type": "STRING", "description": "テールリスクの定量的分析"},
                    "tail_risk_score": {"type": "INTEGER", "description": "破滅確率・テールリスク指数 (0〜100の整数)"},
                    "veto_recommended": {"type": "BOOLEAN", "description": "アンドンを引いて一時停止・差戻しをすべきか"},
                    "andon_inquiry": {"type": "STRING", "description": "品質を高めて再設計するための『現場への愛ある問いかけ』"}
                },
                "required": [
                    "survivorship_bias_analysis", 
                    "sabotage_vulnerabilities", 
                    "tail_risk_analysis", 
                    "tail_risk_score", 
                    "veto_recommended",
                    "andon_inquiry"
                ]
            }

            red_team_prompt = f"""
あなたは【Critical Red Team：破滅確率・対照群・公序良俗 統合監査官】です。
5つの直交エージェントが持ち寄った以下の確定先例候補を冷徹にストレステストし、破滅確率およびサボタージュ脆弱性を監査してください。
重大な法令違反、現場の疲弊・反逆、またはモラルハザードの確率が看過できない場合は、躊躇なく veto_recommended を true に設定してください。
また、単に拒絶するだけでなく「現場がより良い品質に至るための愛ある問い（andon_inquiry）」を必ず提示してください。

【検討課題】
{user_query}

【5大コアの採掘報告】
{aggregated_research}
"""
            audit_raw_json = call_gemini_safe(red_team_prompt, json_schema=red_team_schema)
            audit_json = json.loads(audit_raw_json)
            st.session_state.audit_data = audit_json

            risk_val = audit_json.get("tail_risk_score", 0)
            is_veto = audit_json.get("veto_recommended", False) or (risk_val >= risk_threshold)
            
            st.write(f"  ✓ 監査完了：テールリスク指数 `{risk_val}/100` ｜ アンドン判定: `{is_veto}`")

            # ------------------------------------------------------------------
            # Circuit Breaker: アンドン型インターロック（豊田章男・最高裁準拠）
            # ------------------------------------------------------------------
            if is_veto:
                status_box.update(label="🔔 【アンドン作動】仲間と品質を守るため、設計プロセスを一時停止しました", state="error", expanded=True)
                st.markdown(f"""
<div class='andon-box'>
    <h3>🔔 アンドン（Andon）が引かれました</h3>
    <p><b>「アンドンは現場を処罰するためのものじゃない。仲間を信じ、品質を守り、全員でより良いものをつくるために引くんだ。」</b></p>
    <hr style="border-color: #78350f;">
    <ul>
        <li><b>検出リスク指数:</b> <code>{risk_val}/100</code>（設定閾値: <code>{risk_threshold}</code>）</li>
        <li><b>懸念される急所:</b> {audit_json.get('sabotage_vulnerabilities')}</li>
        <li><b>カイゼンのための問い:</b> <i>「{audit_json.get('andon_inquiry')}」</i></li>
    </ul>
    <p>この先例のまま進むと現場に無理なしわ寄せが生じる恐れがあります。課題の前提条件を少し整えるか、問い直して再挑戦してください。</p>
</div>
""", unsafe_allow_html=True)
                st.stop()

            # ------------------------------------------------------------------
            # Phase 3: 魂の昇華・最高次統合（仙人茶会・Constraint-to-Prestige）
            # ------------------------------------------------------------------
            st.write("🧠 [第3フェーズ：魂の受肉] 冷徹な監査要塞の上に、生活実感と熱狂のソリューションを逆算中...")
            master_prompt = f"""
あなたは卓越したアナロジカル・イノベーションの最高責任者であり、世の繁栄と人々の笑顔を願う事業アーキテクトです。
5大直交コアが持ち寄った確定先例と、Critical Red Team の冷徹な監査結果を統合し、
「鉄壁のバックエンド規律（法理・計数・安全性）」と「思わず人が笑顔で自発的に動いてしまうフロントエンド（愛嬌・美意識・熱狂）」を完璧に両立させた至高のソリューション案を策定してください。

【解決したい課題】
{user_query}

【5大直交コアによる確定先例】
{aggregated_research}

【Critical Red Team 構造化監査報告】
- 生存バイアス分析: {audit_json.get('survivorship_bias_analysis')}
- サボタージュ脆弱性: {audit_json.get('sabotage_vulnerabilities')}
- テールリスク分析: {audit_json.get('tail_risk_analysis')}
- 確定テールリスク指数: {risk_val}/100

---
以下の【仙人茶会・魂の昇華プロトコル】を厳格に適用して出力してください：

### 1. 課題の深層力学と二律背反（ジレンマ）の完全定義
- 表面的な摩擦を削ぎ落とし、物理・統御・心理・生活実感の観点から「何と何のトレードオフか」を構造図的に定義。

### 2. 厳選アンカー事例によるアナロジー構造転移
- 採掘結果（特にAgent εの生活知や偏愛・贈与の力学を含む）から最も打率の高い2〜3個のギミックを厳選し、今回の課題へどう美しく転移できるかを解説。

### 3. 【Constraint-to-Prestige】熱狂と調和を生む具体的3大ソリューション
- **バックエンドの規律**：Red Teamが指摘した脆弱性を冷徹に先回り防御する仕組み（完全な安全性）。
- **フロントエンドの愛嬌**：人々が「監視されている」と感じることなく、自ら進んで調和と行動に向かってしまう【儀式（Ritual）・美意識・お互い様（贈与）】のUX設計。
- 脆弱性を単に塞ぐだけでなく、「だからこそ参加したくなる限定性・誇り」へ反転させた具体的アイデア。

### 4. 実行ロードマップ & 魂の問いかけ（生活実感バリデータ）
- 明日から着手できるクイックウィンと、自律的に定着する境界条件。
- 最後に、糸井重里氏・松下幸之助氏の思想に基づく【結びの問い】：
  『この仕組みを手にしたとき、だれがどんな顔で「よかったね」と微笑むか？ そこにほんの少しの愛嬌と、社会の公器としての利他はあるか？』を記述し、本案の体温を検証して締めくくること。
"""
            final_resp = call_gemini_safe(master_prompt)
            st.session_state.analysis_result = final_resp
            st.session_state.current_query = user_query
            
            total_sec = time.time() - t_start
            status_box.update(
                label=f"✅ 帝国総研 ✕ 最高裁 ✕ 仙人茶会 調和パイプライン完了（総所要時間: {total_sec:.1f}秒）", 
                state="complete", 
                expanded=False
            )

        except Exception as pipeline_err:
            status_box.update(label="❌ パイプライン実行時障害", state="error", expanded=True)
            st.error(f"システム保護機構が作動しました。安全に停止しました: {pipeline_err}")

# ==========================================
# 8. 結果描画 & データ出力セクション
# ==========================================
if st.session_state.analysis_result:
    st.markdown("---")
    
    with st.expander("📂 5大直交コアの【生リサーチ報告】を確認する", expanded=False):
        for inv, text in st.session_state.research_reports:
            st.markdown(f"#### {inv['name']}")
            st.markdown(f"<div class='investigator-card'>{text}</div>", unsafe_allow_html=True)
            
    if st.session_state.audit_data:
        with st.expander("🛡️ Critical Red Team による【構造化監査データ】を確認する", expanded=False):
            ad = st.session_state.audit_data
            st.markdown(f"""
<div class='audit-card'>
    <b>■ テールリスク指数:</b> <code>{ad.get('tail_risk_score')}/100</code> ｜ <b>アンドン推奨:</b> <code>{ad.get('veto_recommended')}</code><br><br>
    <b>■ 生存バイアス・対照群検定:</b><br>{ad.get('survivorship_bias_analysis')}<br><br>
    <b>■ サボタージュ・脱法脆弱性:</b><br>{ad.get('sabotage_vulnerabilities')}<br><br>
    <b>■ テールリスク分析:</b><br>{ad.get('tail_risk_analysis')}<br><br>
    <b>■ カイゼンのための愛ある問い:</b><br><i>「{ad.get('andon_inquiry')}」</i>
</div>
""", unsafe_allow_html=True)
    
    st.markdown("### 🎯 統合ソリューション案（魂の受肉・調和昇華済み）")
    st.markdown(st.session_state.analysis_result)
    st.divider()
    
    all_reports_md = "\n\n---\n\n".join([
        f"## {inv['name']}\n{text}" for inv, text in st.session_state.research_reports
    ])
    
    audit_summary_str = json.dumps(st.session_state.audit_data, ensure_ascii=False, indent=2) if st.session_state.audit_data else "None"
    
    export_content = f"""# CrossDomain Engine 完全調和発想レポート
- **出力日時**: {time.strftime('%Y-%m-%d %H:%M:%S')}
- **入力課題**: {st.session_state.current_query}
- **探査モード**: {mode}

---
# ■ 法的免責事項（不可逆条項）
{LEGAL_DISCLAIMER.strip()}

---
# ■ 統合ソリューション案（魂の受肉・調和昇華済み）
{st.session_state.analysis_result}

---
# ■ Critical Red Team 構造化監査データ
```json
{audit_summary_str}