import requests
import re
import pyperclip
from bs4 import BeautifulSoup
import streamlit as st

#streamlitの設定
st.title("PubMed検索")

#  指定のPubmedアドレスからURLを抽出。number_urlで抽出する数を選択可能
def Pubmed_URL_extraction (url, number_url=10):
  load = str(requests.get(url).content)
  pattern = "https://pubmed.ncbi.nlm.nih.gov/\d+/"
  URLs = re.findall(pattern,load)
  #  ダブっているので1意の値に変換。順番を保っていたいのでSetは使わない。
  URLs = URLs[::2]
  return (URLs[:number_url+1])

def get_contents (url):
  # ページのHTMLを取得
  response = requests.get(url)
  html = response.text

  # BeautifulSoupを使ってHTMLをパース
  soup = BeautifulSoup(html, "html.parser")

  ### 以下、Abstractを抽出
  # <div class="abstract-content selected">で抽出
  abstract_element = soup.find("div", class_="abstract-content selected")

  # Abstractが無い場合
  if abstract_element is None:
    abstract_stripped = "No abstract"

  # Abstractが有る場合
  else:
    abstract = abstract_element.text.strip().split("\n")
    abstract_stripped = "" # 中身の無いリストを削除
    for abst in abstract:
      if len(abst.strip()) !=0: abstract_stripped += (abst.strip() + "\n")

  ### 以下、タイトルを抽出
  # <h1 class="heading-title">で抽出
  title_element = soup.find("h1", class_="heading-title")
  title = title_element.text.strip()

  return(f"Title: {title} \nAbstract: {abstract_stripped}")

# trending articleからURL抽出
url_trend = "https://pubmed.ncbi.nlm.nih.gov/trending/"
pubmed_url_list = Pubmed_URL_extraction(url_trend)

# get_content使ってスクレイピングして一つの文字列に成形
GPT_input = ""
for url in pubmed_url_list:
    GPT_input += get_contents(url)

#  chat GPT用に成形して出力
GPT_order = "あなたは優れた科学者です。以下に示す論文の各内容を200字程度に要約してください。\n"\
"論文は全部で10本あり、それぞれについて省略せずに完全にアウトプットしてください。\n"\
"Abstractの記載がない論文はタイトルのみの表示で構いません。"\
"出力は表形式で、論文タイトル（原文）・論文タイトル（日本語）・要約（日本語）を出力してください。\n\n\n"
print(GPT_order+GPT_input)
