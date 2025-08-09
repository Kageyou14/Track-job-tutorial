import streamlit as st
import pandas as pd

st.title("論文管理ツール")

#データフレームの作成
if "papers" not in st.session_state:
    st.session_state.papers = pd.DataFrame(columns=["title", "authors", "journal", "year", "doi", "url"])

#テキスト入力欄
doi=st.text_input("DOIを入力してください")

#論文追加ボタン
if st.button("論文を追加する"):
    if doi:
        #メタデータの記録
        paper_info =  {
        "title": "タイトル",
        "authors": "著者",
        "journal": "雑誌",
        "year": "発行年",
        "doi": doi,
        "url": "URL"
        }  
        
        #データフレームに追加
        st.session_state.papers = pd.concat(
            [st.session_state.papers, pd.DataFrame([paper_info])],
            ignore_index=True
        )
        st.success("追加完了")  
    else:
        st.warning("DOIを入力してください")
          

# 表の表示
st.subheader("登録済み論文一覧")
st.dataframe(st.session_state.papers)
