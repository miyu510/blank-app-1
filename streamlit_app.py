
   import streamlit as st
from st_supabase_connection import SupabaseConnection
import pandas as pd

# --- Supabase 接続設定 ---
conn = st.connection("supabase", type=SupabaseConnection)

def get_coffee_recommendation(style, roast):
    # 基本のレシピ設定
    recommendations = {
        "スッキリ・酸味重視": {
            "grind": "中細挽き (TIMEMORE 18-22クリック程度)",
            "temp": 92,
            "ratio": "1:15 (豆15g に対して お湯225ml)",
            "time": "2分15秒",
            "note": "高めの温度で短時間で抽出することで、雑味を抑えつつ華やかな酸味を引き出します。"
        },
        "バランス・甘み重視": {
            "grind": "中挽き (TIMEMORE 23-25クリック程度)",
            "temp": 89,
            "ratio": "1:16 (豆15g に対して お湯240ml)",
            "time": "2分30秒",
            "note": "標準的な温度と挽き目で、コーヒー本来の甘みとコクのバランスを整えます。"
        },
        "コク・苦味重視": {
            "grind": "中粗挽き (TIMEMORE 26-28クリック程度)",
            "temp": 84,
            "ratio": "1:14 (豆15g に対して お湯210ml)",
            "time": "3分00秒",
            "note": "低めの温度でじっくり抽出することで、刺すような苦味を抑え、円熟したコクを引き出します。"
        }
    }
    
    # 辞書をコピーして使用
    res = recommendations[style].copy()
    
    # 焙煎度による温度の微調整
    if roast == "深煎り":
        res["temp"] -= 4
        res["temp_display"] = f"{res['temp']}°C (苦味を抑えるため低め)"
    elif roast == "浅煎り":
        res["temp"] += 3
        res["temp_display"] = f"{res['temp']}°C (成分を出しやすくするため高め)"
    else:
        res["temp_display"] = f"{res['temp']}°C"
    
    return res

# --- UI部分 ---
st.title("☕ Coffee Recipe Concierge")
st.write("今日の気分に合わせて、最適な淹れ方を提案します。")

col1, col2 = st.columns(2)
with col1:
    style = st.selectbox("どんな味の気分ですか？", ["スッキリ・酸味重視", "バランス・甘み重視", "コク・苦味重視"])
with col2:
    roast = st.select_slider("豆の焙煎度は？", options=["浅煎り", "中煎り", "深煎り"])

if st.button("レシピを表示する"):
    recipe = get_coffee_recommendation(style, roast)
    
    # ★ Supabaseへ履歴を保存 ★
    try:
        conn.table("coffee_logs").insert([
            {
                "style": style, 
                "roast": roast, 
                "temp": recipe["temp"]
            }
        ]).execute()
        st.toast("抽出ログをSupabaseに保存しました！")
    except Exception as e:
        st.error(f"データの保存に失敗しました: {e}")

    # レシピ表示
    st.divider()
    st.subheader(f"✨ おすすめの抽出レシピ ({style})")
    st.write(f"**🫘 豆の粗さ:** {recipe['grind']}")
    st.write(f"**🌡️ お湯の温度:** {recipe['temp_display']}")
    st.write(f"**⚖️ 抽出比率:** {recipe['ratio']}")
    st.write(f"**⏳ 目標時間:** {recipe['time']}")
    st.info(f"**アドバイス:** {recipe['note']}")

# --- 履歴の表示 ---
st.write("---")
if st.checkbox("これまでの抽出履歴を表示"):
    # ttl=0 でキャッシュを無効化し、常に最新データを取得
    rows = conn.query("*", table="coffee_logs", ttl="0").execute()
    
    if rows.data:
        df = pd.DataFrame(rows.data)
        # 見やすいようにカラム名を変更して表示
        df_display = df.rename(columns={
            'created_at': '日時',
            'style': '好み',
            'roast': '焙煎度',
            'temp': '設定温度'
        })
        st.dataframe(df_display[['日時', '好み', '焙煎度', '設定温度']], use_container_width=True)
        
        # ちょっとした分析機能
        st.caption(f"合計 {len(df)} 回の抽出データが保存されています。")
    else:
        st.info("まだ履歴はありません。")
