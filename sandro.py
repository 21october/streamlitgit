import streamlit as st
import pandas as pd
from urllib.request import urlopen
import requests
from bs4 import BeautifulSoup
import urllib.request
import os


st.title('Download images')
st.header("공식 홈페이지 이미지 다운로드: 산드로")

uploaded_file = st.file_uploader(label="Url 리스트(엑셀)를 업로드 하세요.", type='xlsx')
if uploaded_file is not None:
    df = pd.read_excel(uploaded_file)
    st.dataframe(df)
    urls = df['링크']
    numbers = df['번호']

    start_down = st.button(label="다운로드 시작하기")
    if start_down is not None:
        for url in urls:
            response = requests.get(url)
            html = response.text
            soup = BeautifulSoup(html, 'html.parser')
            name = soup.select_one("#title").text
            images = soup.select("img",attrs={"class":"productthumbnail lazyload loaded"})
            list = []
            for img in images:
                if "data-hires" in img.attrs:
                    imgUrl = img["data-hires"]
                    list.append(imgUrl)
                else:
                    pass
            path = os.getcwd()
            n = 1
            for i in list:
                with urlopen(i) as f:
                    with open(path+"/"+name+str(n)+'.jpg','wb') as h:
                        img = f.read()
                        h.write(img)
                n += 1