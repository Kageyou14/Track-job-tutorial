import streamlit as st
import pandas as pd

st.markdown(
    "[論文一覧に戻る](./app)",
    unsafe_allow_html=True
)

# 仮データの
if "papers" not in st.session_state:
    st.session_state.papers = pd.DataFrame([
        {"title": "論文A", 
         "authors": "著者1, 著者2", 
         "journal": "雑誌A", 
         "year": 2021, 
         "doi": "10.1234/abcd", 
         "url": "https://example.com/abcd",
         "memo": ""}
    ])
papers = st.session_state.papers

# edit_mode の初期化（辞書）
if "edit_mode" not in st.session_state:
    st.session_state.edit_mode = {}


for idx, paper in papers.iterrows():
    st.write(f"#### {paper['title']}")
    st.write(f"**著者:** {paper['authors']}")
    st.write(f"**雑誌:** {paper['journal']}")
    st.write(f"**発行年:** {paper['year']}")
    st.write(f"**DOI:** {paper['doi']}")
    st.markdown(f"**URL:** [{paper['url']}]({paper['url']})")
    

if st.session_state.edit_mode.get(idx, False):
    memo_input = st.text_area("メモを入力してください", value=paper["memo"], key=f"memo_{idx}")
    if st.button("保存", key=f"save_{idx}"):
        # メモを保存して編集モードを終了
        st.session_state.papers.at[idx, "memo"] = memo_input
        st.session_state.edit_mode[idx] = False
        st.rerun()  # ページをリロードして状態更新を反映
else:
    st.write(f"**メモ:** {paper['memo']}")
    if st.button("編集", key=f"edit_{idx}"):
        st.session_state.edit_mode[idx] = True
        st.rerun()  # ページをリロードして編集モードに切替
