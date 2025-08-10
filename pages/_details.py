import streamlit as st
import db_utils

st.set_page_config(layout="wide") 

st.markdown("""
    <style>
        /* サイドバー本体を非表示にする */
        section[data-testid="stSidebar"] {
            display: none !important;
        }
        /* サイドバーを開くためのヘッダーのボタンを非表示にする */
        button[title="View big"] {
            display: none !important;
        }
    </style>
    """, 
    unsafe_allow_html=True
)
try:
    # URLのクエリパラメータ (?id=1 のような部分) を取得
    paper_id = int(st.query_params["id"])
except (KeyError, ValueError):
    st.error("論文IDが指定されていません。一覧ページから論文を選択してください。")
    st.stop()

paper = db_utils.get_paper_by_id(paper_id)
if paper is None:
    st.error("指定された論文が見つかりませんでした。")
    st.stop()
st.title("論文詳細・メモ編集")
st.markdown("[論文一覧に戻る](/)")
st.divider()

st.subheader(paper['title'])
st.write(f"**著者:** {paper['authors']}")
st.write(f"**雑誌名:** {paper['journal']}")
st.write(f"**発行年:** {paper['year']}")

# 巻、号、ページが存在する場合のみ表示
if paper['volume']:
    st.write(f"**巻/号:** {paper['volume']} / {paper['issue']}")
if paper['pages']:
    st.write(f"**ページ:** {paper['pages']}")

st.write(f"**DOI:** {paper['doi']}")
if paper['url']:
    st.markdown(f"**URL:** [{paper['url']}]({paper['url']})")
df=db_utils.get_paper_by_id(paper_id)
#引用文献フォーマット
authors = df.get('authors', '')
year = df.get('year', '')
title = df.get('title', '')
journal = df.get('journal', '')
pages = df.get('pages', '')
doi = df.get('doi', '')
url = df.get('url', '')

parts = []
if authors and str(authors).strip():
    parts.append(f"{authors}.")
if year and str(year).strip():
    parts.append(f"({year}).")
if title and str(title).strip():
    parts.append(f"{title}.")
if journal and str(journal).strip():
    parts.append(f"{journal}.")
if pages and str(pages).strip():
    parts.append(f"{pages}")
if url and str(url).strip():
    parts.append(f"{url}")
        
citation = " ".join(parts)
st.write(f"**引用文献(APA):** {citation}")

st.divider()
st.subheader("メモ")

if "edit_mode" not in st.session_state:
    st.session_state.edit_mode = False

# 編集モードの場合
if st.session_state.edit_mode:
    memo_input = st.text_area("メモ内容", value=paper["memo"], height=200)
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("保存", use_container_width=True):
            db_utils.update_memo(paper_id, memo_input)
            st.session_state.edit_mode = False
            st.toast("メモを保存しました！", icon="✅")
            st.rerun() # ページを再読み込みして表示を更新
    with col2:
        if st.button("キャンセル", use_container_width=True):
            st.session_state.edit_mode = False
            st.rerun()

# 表示モードの場合
else:
    # メモが空の場合はメッセージを表示
    if paper["memo"]:
        st.write(paper["memo"])
    else:
        st.info("この論文にはまだメモがありません。")

    if st.button("編集する"):
        st.session_state.edit_mode = True
        st.rerun()
# # edit_mode の初期化（辞書）
# if "edit_mode" not in st.session_state:
#     st.session_state.edit_mode = {}


# for idx, paper in papers.iterrows():
#     st.write(f"#### {paper['title']}")
#     st.write(f"**著者:** {paper['authors']}")
#     st.write(f"**雑誌:** {paper['journal']}")
#     st.write(f"**発行年:** {paper['year']}")
#     st.write(f"**DOI:** {paper['doi']}")
#     st.markdown(f"**URL:** [{paper['url']}]({paper['url']})")
    

# if st.session_state.edit_mode.get(idx, False):
#     memo_input = st.text_area("メモを入力してください", value=paper["memo"], key=f"memo_{idx}")
#     if st.button("保存", key=f"save_{idx}"):
#         # メモを保存して編集モードを終了
#         st.session_state.papers.at[idx, "memo"] = memo_input
#         st.session_state.edit_mode[idx] = False
#         st.experimental_rerun()  # ページをリロードして状態更新を反映
# else:
#     st.write(f"**メモ:** {paper['memo']}")
#     if st.button("編集", key=f"edit_{idx}"):
#         st.session_state.edit_mode[idx] = True
#         st.experimental_rerun()  # ページをリロードして編集モードに切替
