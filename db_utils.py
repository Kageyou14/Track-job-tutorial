import sqlite3
import pandas as pd

DB_NAME = "papers.db"

def init_db():
    """データベースを初期化し、テーブルが存在しない場合は作成する"""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS papers (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT,
        authors TEXT,
        journal TEXT,
        year INTEGER,
        volume TEXT,
        issue TEXT,
        pages TEXT,
        doi TEXT NOT NULL UNIQUE,
        url TEXT,
        memo TEXT DEFAULT '',
        file_data BLOB,
        file_type TEXT
    )
    """)
    conn.commit()
    conn.close()

def add_paper(paper_info: dict):
    """論文情報をデータベースに追加する"""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    # 修正1: "memo," の後ろの不要なカンマを削除
    cursor.execute(
        "INSERT INTO papers (title, authors, journal, year, volume, issue, pages, doi, url, memo) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
        (
            paper_info.get("title"),
            paper_info.get("authors"),
            paper_info.get("journal"),
            paper_info.get("year"),
            paper_info.get("volume"),
            paper_info.get("issue"),
            paper_info.get("pages"),
            paper_info.get("doi"),
            paper_info.get("url"),
            paper_info.get("memo", ""),
        )
    )
    conn.commit()
    conn.close()

def get_all_papers() -> pd.DataFrame:
    """データベースから全ての論文情報をDataFrameとして取得する"""
    conn = sqlite3.connect(DB_NAME)
    df = pd.read_sql_query("SELECT * FROM papers ORDER BY id DESC", conn)
    conn.close()
    return df

def check_doi_exists(doi: str) -> bool:
    """指定されたDOIがデータベースに既に存在するかチェックする"""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM papers WHERE doi = ?", (doi,))
    count = cursor.fetchone()[0]
    conn.close()
    return count > 0

def get_paper_by_id(paper_id: int) -> pd.Series | None:
    """IDを指定して単一の論文情報を取得する"""
    conn = sqlite3.connect(DB_NAME)
    # 修正2: SQLインジェクション対策のため、パラメータ渡しに変更
    df = pd.read_sql_query(
        "SELECT * FROM papers WHERE id = ?", 
        conn, 
        params=(paper_id,)
    )
    conn.close()
    return df.iloc[0] if not df.empty else None

def update_memo(paper_id: int, memo: str):
    """指定されたIDの論文のメモを更新する"""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("UPDATE papers SET memo = ? WHERE id = ?", (memo, paper_id))
    conn.commit()
    conn.close()

def delete_paper(paper_id: int):
    """指定されたIDの論文をデータベースから削除する"""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM papers WHERE id = ?", (paper_id,))
    conn.commit()
    conn.close()

def update_file(paper_id: int, file_data: bytes, file_type: str):
    """添付ファイルをデータベースに保存/更新する"""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE papers SET file_data = ?, file_type = ? WHERE id = ?",
        (file_data, file_type, paper_id)
    )
    conn.commit()
    conn.close()

def delete_file(paper_id: int):
    """添付ファイルをデータベースから削除する"""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE papers SET file_data = NULL, file_type = NULL WHERE id = ?",
        (paper_id,)
    )
    conn.commit()
    conn.close()
