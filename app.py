import streamlit as st
import pandas as pd
from get_paper_info import get_paper_info_from_crossref


st.set_page_config(layout="wide") 


#データフレームの作成
if "papers" not in st.session_state:
    st.session_state.papers = pd.DataFrame(columns=["title", "authors", "journal", "year", "doi", "url"])


# st.sidebar.title("操作パネル")
#テキスト入力欄
st.sidebar.header("論文検索")
search = st.sidebar.text_input("入力")


st.sidebar.header("論文の追加")
with st.sidebar.form(key="add_form"):
    doi = st.text_input("DOIを入力してください")
    submitted = st.form_submit_button("追加")
    if submitted:
            if doi:
                data = get_paper_info_from_crossref(doi)
                if data:
                    # メタデータの記録 
                    paper_info = {
                        "title": data["title"],
                        "authors": data["authors"],
                        "journal": data["journal"],
                        "year": data["year"],
                        "doi": data["doi"],
                        "url": data["url"]
                    }
                    
                    # データフレームに追加 
                    st.session_state.papers = pd.concat(
                        [st.session_state.papers, pd.DataFrame([paper_info])], 
                        ignore_index=True
                    )
                    # モダンな通知に変更
                    st.toast(f"論文「{data['title']}」を追加しました！", icon="✅")
                else:
                    st.error("正しいDOIではないか、情報が見つかりませんでした。")
            else:
                st.warning("DOIを入力してください。")

st.title("論文管理ツール")
st.subheader("登録済み論文一覧")

# 表の表示をリッチにする
st.dataframe(
    st.session_state.papers,
    # 表示する列の設定
    column_config={
        "title": st.column_config.TextColumn("タイトル", width="large"),
        "authors": st.column_config.ListColumn("著者", width="medium"),
        "year": st.column_config.NumberColumn("発行年", format="%d"),
        "url": st.column_config.LinkColumn("URL", display_text="🔗 Link")
    },
    # 表示する列の順番を指定 (doiやjournalは非表示に)
    column_order=("title", "authors", "year", "url"),
    hide_index=True,
    use_container_width=True # 横幅いっぱいに表示
)
