import streamlit as st

st.title("論文管理ツール")

#テキスト入力欄
post_content=st.text_input("DOIを入力してください")

#投稿ボタン
if st.button("論文を追加する"):
    if post_content:
        #st.success("投稿完了")
        st.text_area("投稿内容",post_content)
    else:
        st.warning("投稿内容を入力してください")
        

# 表の表示
st.subheader("登録済み論文一覧")
st.dataframe(st.session_state.papers)