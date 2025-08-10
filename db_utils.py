import sqlite3
import pandas as pd

DB_NAME = "papers.db"

def init_db():
    """データベースを初期化し、テーブルが存在しない場合は作成する"""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    # 論文情報を保存するテーブルを作成
    # IF NOT EXISTS をつけることで、既に存在する場合にエラーになるのを防ぐ
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS papers (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT,
        authors TEXT,
        journal TEXT,
        year INTEGER,
        doi TEXT NOT NULL UNIQUE,
        url TEXT
    )
    """)
    conn.commit()
    conn.close()

def add_paper(paper_info: dict):
    """論文情報をデータベースに追加する"""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO papers (title, authors, journal, year, doi, url) VALUES (?, ?, ?, ?, ?, ?)",
        (
            paper_info["title"],
            paper_info["authors"],
            paper_info["journal"],
            paper_info["year"],
            paper_info["doi"],
            paper_info["url"],
        )
    )
    conn.commit()
    conn.close()

def get_all_papers() -> pd.DataFrame:
    """データベースから全ての論文情報をDataFrameとして取得する"""
    conn = sqlite3.connect(DB_NAME)
    # read_sql_query を使うと、SQLの実行結果を直接DataFrameに変換できて便利
    df = pd.read_sql_query("SELECT * FROM papers", conn)
    conn.close()
    return df

def check_doi_exists(doi: str) -> bool:
    """指定されたDOIがデータベースに既に存在するかチェックする"""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    # COUNT(*)で条件に合う行の数を数える
    cursor.execute("SELECT COUNT(*) FROM papers WHERE doi = ?", (doi,))
    count = cursor.fetchone()[0]
    conn.close()
    return count > 0
