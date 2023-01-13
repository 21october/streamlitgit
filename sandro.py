import streamlit as st
import pandas as pd
import requests
from urllib.request import urlopen
import urllib.request
from bs4 import BeautifulSoup
import os
# python3 -m streamlit run /Users/youkyung/21October/streamlitgit/sandro.py

st.title('공식 홈페이지 이미지 다운로드: 산드로')

uploaded_file = st.file_uploader(label="Url 리스트(엑셀)를 업로드 하세요.", type='xlsx')
if uploaded_file is not None:
    df = pd.read_excel(uploaded_file)
    st.dataframe(df)
    urls = df['링크']

    start_down = st.button(label="다운로드 시작하기")
    if start_down is not None:
        indx = 1
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
                    with open(path+"/"+str(indx)+"_"+name+str(n)+'.jpg','wb') as h:
                        img = f.read()
                        h.write(img)
                n += 1
            indx += 1
    st.success(f"작업이 완료되었습니다. 저장경로:{path}")