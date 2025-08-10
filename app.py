import streamlit as st
import pandas as pd
from get_paper_info import get_paper_info_from_crossref
import db_utils

st.set_page_config(layout="wide") 

db_utils.init_db()
# #データフレームの作成
# if "papers" not in st.session_state:
#     st.session_state.papers = pd.DataFrame(columns=["title", "authors", "journal", "year", "doi", "url"])

# st.sidebar.title("操作パネル")
#テキスト入力欄
st.sidebar.header("論文検索")
# 1. 検索バーをメイン画面に設置
search_query = st.sidebar.text_input("登録論文をタイトルで検索", placeholder="キーワードを入力…")


st.sidebar.header("論文の追加")
with st.sidebar.form(key="add_form"):
    doi = st.text_input("DOIを入力してください")
    submitted = st.form_submit_button("追加")
    if submitted:
            if doi:
                if db_utils.check_doi_exists(doi):
                    st.warning("このDOIは既に追加されています。")
                else:
                    data = get_paper_info_from_crossref(doi)
                    if data:
                        # メタデータの記録 
                        paper_info = {
                            "title": data["title"],
                            "authors": data["authors"],
                            "journal": data["journal"],
                            "year": data["year"],
                            "volume": data["volume"],  
                            "issue": data["issue"],   
                            "pages": data["pages"],    
                            "doi": data["doi"],
                            "url": data["url"],
                            "memo": ""
                        }
                        
                        # データフレームに追加 
                        db_utils.add_paper(paper_info)
                    
                        st.toast(f"論文「{data['title']}」を追加しました！", icon="✅")
                    else:
                        st.error("正しいDOIではないか、情報が見つかりませんでした。")
            else:
                st.warning("DOIを入力してください。")

st.title("論文管理ツール")
st.subheader("登録済み論文一覧")
all_papers = db_utils.get_all_papers()
if search_query:
    # .str.contains() を使い、タイトル列に検索語が含まれる行だけを抽出する
    filtered_papers = all_papers[all_papers['title'].str.contains(search_query, case=False, na=False)]
else:
    # 検索バーが空の場合は、すべての論文を表示する
    filtered_papers = all_papers

st.divider()

# 1. ヘッダー行を手動で作成
col_header1, col_header2, col_header3, col_header4 = st.columns([4, 3, 1, 1])
with col_header1:
    st.markdown("**タイトル**")
with col_header2:
    st.markdown("**著者**")
with col_header3:
    st.markdown("**発行年**")
with col_header4:
    st.markdown("**論文URL**")

st.divider()

# 2. forループで各論文の行を描画
if filtered_papers.empty:
    st.info("表示する論文がありません。")
else:
    for index, paper in filtered_papers.iterrows():
        col1, col2, col3, col4 = st.columns([4, 3, 1, 1])
        
        # タイトル自体を詳細ページへのリンクにする
        with col1:
            # Markdownのリンク構文: [表示テキスト](URL)
            st.markdown(
                f" [{paper['title']}](details?id={int(paper['id'])})",
                unsafe_allow_html=True # リンクを有効にするために必要
            )

        
        # その他の情報を表示
        with col2:
            st.write(paper["authors"])
        with col3:
            st.write(paper["year"])
        with col4:
            if paper["url"]:
                st.markdown(
                    f'<a href="{paper["url"]}" target="_blank">🔗 Link</a>', 
                    unsafe_allow_html=True
                )
        
        st.divider()
