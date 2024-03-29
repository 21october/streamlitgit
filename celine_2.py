import streamlit as st
import pandas as pd
import requests
from urllib.request import urlopen
import urllib.request
from bs4 import BeautifulSoup
import os
import zipfile
# python3 -m streamlit run /Users/youkyung/21October/streamlitgit/celine.py

st.title('CELINE')
st.header('공식 홈페이지 이미지 다운로드')

st.write("1/ URL로 다운로드 받기")
input = st.text_input(label="👇 여기에 제품 링크를 입력하고 ENTER 를 클릭하세요.")
btn_clicked = st.button("ENTER",key='confirm_btn',disabled=(input is None))

if btn_clicked:
    start_down = st.button(label="다운로드 시작하기")
    if start_down is not None:
        indx = 1
        url = input
        headers = {'User-Agent' : 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36'}
        response = requests.get(url, headers=headers)
        html = response.text
        soup = BeautifulSoup(html, 'html.parser')
        name = soup.select_one('span.o-product__title-truncate.f-body--em').text
        images = soup.find_all('button','m-thumb-carousel__img')
        list1 = []
        for img in images:
            imgUrl = img.find('img')['data-src-zoom']
            list1.append(imgUrl)

        path = os.getcwd()
        
        n = 1
        for i in list1:
            with urlopen(i) as f:
                with open(path+"/"+str(indx)+"_"+name+str(n)+'.jpg','wb') as h:
                    img = f.read()
                    h.write(img)
            n += 1
        st.write(f"{indx}번 완료")
        indx += 1

    #파일 압축하기
    with zipfile.ZipFile("img.zip",'w') as my_zip:
        for file in os.listdir(path):
            if file.endswith('.jpg') or file.endswith('.jpeg') or file.endswith('.png'):
                my_zip.write(file)

    with open('img.zip', 'rb') as f:
        st.download_button('이미지 압축 파일 다운로드 받기', f, file_name='img.zip')
    
    st.success(f"작업이 완료되었습니다. 압축파일을 다운로드 받으세요.")


#############
st.write("")
st.write("")
st.write("")
st.write("2/ 엑셀 대량 다운로드")
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
            name = soup.select_one('span.o-product__title-truncate.f-body--em').text
            images = soup.find_all('button','m-thumb-carousel__img')
            list = []
            for img in images:
                imgUrl = img.find('img')['data-src-zoom']
                list.append(imgUrl)

            path = os.getcwd()
            
            n = 1
            for i in list:
                with urlopen(i) as f:
                    with open(path+"/"+str(indx)+"_"+name+str(n)+'.jpg','wb') as h:
                        img = f.read()
                        h.write(img)
                n += 1
            indx += 1

    #파일 압축하기
    with zipfile.ZipFile("img.zip",'w') as my_zip:
        for file in os.listdir(path):
            if file.endswith('.jpg') or file.endswith('.jpeg') or file.endswith('.png'):
                my_zip.write(file)

    with open('img.zip', 'rb') as f:
        st.download_button('이미지 압축 파일 다운로드 받기', f, file_name='img.zip')
    
    st.success(f"작업이 완료되었습니다. 압축파일을 다운로드 받으세요.")