# ☕ Coffee Recipe Concierge

今日の気分とコーヒー豆の状態に合わせて、最適な抽出レシピを提案するアプリです。
抽出したデータは Supabase に蓄積され、過去の傾向を振り返ることができます。

## 🚀 アプリを試す
以下のURLから直接アプリを使用できます：
[https://blank-app-nblbh80qxf.streamlit.app/](https://blank-app-nblbh80qxf.streamlit.app/)

## ✨ 主な機能
- **パーソナライズ・レシピ提案**: 「スッキリ・酸味重視」「バランス・甘み重視」「コク・苦味重視」の3つの気分と、豆の焙煎度から、最適な抽出パラメータを算出します。
- **こだわり設定**: TIMEMOREなどのハンドグラインダー利用者を想定し、具体的な「クリック数（挽き目）」を提案します。
- **データの永続化**: Supabase をバックエンドに使用しており、抽出ログ（味の好み、焙煎度、設定温度、日時）を永続的に保存します。
- **履歴表示機能**: 過去の抽出データを一覧で確認でき、自分の味の好みの傾向を分析可能です。

## 🛠 使用技術
- **Frontend**: Streamlit
- **Backend/Database**: Supabase
- **Language**: Python

## 📝 開発の背景と工夫
このアプリは、初心者でもハンドドリップを安定して楽しめるように開発しました。

- **改良した点**: 当初は画面上での計算のみでしたが、Supabase を導入することで利用データの保存を可能にしました。
- **苦労した点**: Streamlit Cloud で外部ライブラリを動作させるための `requirements.txt` の設定や、Python 特有のインデント（字下げ）エラーの解消、APIキーの安全な管理（Secrets）に取り組みました。

## 🗂 セットアップ（開発者向け）
ローカル環境で実行する場合は、`.streamlit/secrets.toml` に Supabase の API 情報を設定してください。

```toml
[connections.supabase]
SUPABASE_URL = "YOUR_SUPABASE_URL"
SUPABASE_KEY = "YOUR_SUPABASE_ANON_KEY"
