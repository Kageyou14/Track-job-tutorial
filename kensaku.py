import tkinter as tk
from tkinter import ttk

# サンプルデータ
data = [
    "Pythonプログラミング",
    "機械学習の基礎",
    "深層学習の応用",
    "データサイエンス入門",
    "AI倫理と課題"
]

def search_keyword():
    keyword = search_entry.get()  # 検索バーからキーワードを取得
    results = [item for item in data if keyword in item]  # キーワードを含むデータを検索
    result_text.delete(1.0, tk.END)  # 結果表示エリアをクリア
    if results:
        result_text.insert(tk.END, "検索結果:\n")
        for result in results:
            result_text.insert(tk.END, f"- {result}\n")
    else:
        result_text.insert(tk.END, "該当する結果が見つかりませんでした。\n")

# GUIの設定
root = tk.Tk()
root.title("検索ツール")

# 検索バー
frame = ttk.Frame(root, padding="10")
frame.grid(row=0, column=0, sticky=(tk.W, tk.E))

search_label = ttk.Label(frame, text="検索キーワード:")
search_label.grid(row=0, column=0, padx=5)

search_entry = ttk.Entry(frame, width=30)
search_entry.grid(row=0, column=1, padx=5)

search_button = ttk.Button(frame, text="検索", command=search_keyword)
search_button.grid(row=0, column=2, padx=5)

# 結果表示エリア
result_text = tk.Text(root, width=50, height=15)
result_text.grid(row=1, column=0, padx=10, pady=10)

# メインループ
root.mainloop()