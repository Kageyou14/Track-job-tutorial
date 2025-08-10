import requests

def get_paper_info_from_crossref(doi: str) -> dict | None:
    """
    DOIを元にCrossref APIから論文のメタデータを取得

    Args:
        doi (str)

    Returns:
        dict: 成功した場合は、タイトル、著者、雑誌名、発行年を含む辞書
              失敗した場合は、None
    """
    if "doi.org/" in doi:
        clean_doi = doi.split("doi.org/")[-1]
    else:
        clean_doi = doi.strip()
    url = f"https://api.crossref.org/works/{doi}"
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        data = response.json()["message"]
        title_list = data.get("title", [])
        title = title_list[0] if title_list else None
        authors_list = data.get("author", [])
        authors_str = ", ".join(
            f"{author.get('given', '')} {author.get('family', '')}".strip()
            for author in authors_list
        )
        authors = authors_str if authors_str else None

        journal_list = data.get("container-title", [])
        journal = journal_list[0] if journal_list else None

        published_data = data.get("published", {})
        date_parts = published_data.get("date-parts", [[]])

        year = date_parts[0][0] if date_parts and date_parts[0] else None
        paper_url = data.get("URL", None)
        volume = data.get("volume", None)
        issue = data.get("issue", None)
        pages = data.get("page", None)
        paper_info = {
            "title": title,
            "authors": authors,
            "journal": journal,
            "year": year,
            "volume": volume, 
            "issue": issue,   
            "pages": pages, 
            "doi": clean_doi,
            "url": paper_url
        }
        return paper_info

    except (requests.exceptions.RequestException, KeyError, IndexError) as e:
        print(f" {type(e).__name__} - {e}")
        return None
