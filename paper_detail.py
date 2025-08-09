import streamlit as st
import pandas as pd

st.markdown(
    "[論文一覧に戻る](./app)",
    unsafe_allow_html=True
)

# サンプルのデータフレーム（本来はセッションなどから取得）
papers = pd.DataFrame([
    {"title": "論文A", 
     "authors": "著者1, 著者2", 
     "journal": "雑誌A", 
     "year": 2021, 
     "doi": "10.1234/abcd", 
     "url": "https://example.com/abcd",
     "memo":""}
    ])

for idx, paper in papers.iterrows():
    st.write(f"#### {paper['title']}")
    st.write(f"**著者:** {paper['authors']}")
    st.write(f"**雑誌:** {paper['journal']}")
    st.write(f"**発行年:** {paper['year']}")
    st.write(f"**DOI:** {paper['doi']}")
    st.markdown(f"**URL:** [{paper['url']}]({paper['url']})")
    
    # メモ入力欄（キーにidxを使う）
    memo_input = st.text_area("メモを入力してください", value=paper["memo"], key=f"memo_{idx}")

    if st.button("メモを保存", key=f"save_{idx}"):
        # セッションのデータフレームを更新
        st.session_state.papers.at[idx, "memo"] = memo_input
        st.success("メモを保存しました")

    st.write("---")
