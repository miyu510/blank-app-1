import streamlit as st

def get_coffee_recommendation(style, roast):
    # 好みに応じた抽出パラメータのロジック
    recommendations = {
        "スッキリ・酸味重視": {
            "grind": "中細挽き (TIMEMORE 18-22クリック程度)",
            "temp": "90°C - 93°C",
            "ratio": "1:15 (豆15g に対して お湯225ml)",
            "time": "2分15秒",
            "note": "高めの温度で短時間で抽出することで、雑味を抑えつつ華やかな酸味を引き出します。"
        },
        "バランス・甘み重視": {
            "grind": "中挽き (TIMEMORE 23-25クリック程度)",
            "temp": "88°C - 90°C",
            "ratio": "1:16 (豆15g に対して お湯240ml)",
            "time": "2分30秒",
            "note": "標準的な温度と挽き目で、コーヒー本来の甘みとコクのバランスを整えます。"
        },
        "コク・苦味重視": {
            "grind": "中粗挽き (TIMEMORE 26-28クリック程度)",
            "temp": "82°C - 85°C",
            "ratio": "1:14 (豆15g に対して お湯210ml)",
            "time": "3分00秒",
            "note": "低めの温度でじっくり抽出することで、刺すような苦味を抑え、円熟したコクを引き出します。"
        }
    }
    
    # 焙煎度による微調整（例）
    res = recommendations[style]
    if roast == "深煎り":
        res["temp"] = "80°C - 83°C (さらに低めを推奨)"
    
    return res

# --- UI部分 ---
st.title("☕ Coffee Recipe Concierge")
st.write("今日の気分に合わせて、最適な淹れ方を提案します。")

col1, col2 = st.columns(2)

with col1:
    style = st.selectbox(
        "どんな味の気分ですか？",
        ["スッキリ・酸味重視", "バランス・甘み重視", "コク・苦味重視"]
    )

with col2:
    roast = st.select_slider(
        "豆の焙煎度は？",
        options=["浅煎り", "中煎り", "深煎り"]
    )

if st.button("レシピを表示する"):
    recipe = get_coffee_recommendation(style, roast)
    
    st.divider()
    st.subheader(f"✨ おすすめの抽出レシピ ({style})")
    
    metrics = st.columns(4)
    metrics[0].metric("豆の粗さ", recipe["grind"])
    metrics[1].metric("お湯の温度", recipe["temp"])
    metrics[2].metric("抽出比率", recipe["ratio"])
    metrics[3].metric("目標時間", recipe["time"])
    
    st.info(f"**アドバイス:** {recipe['note']}")
    
    st.write("---")
    st.caption("※挽き目の目安は TIMEMORE C2/C3 などのハンドグラインダーを基準にしています。")
    
