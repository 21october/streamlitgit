import streamlit as st
import pandas as pd
import requests
from urllib.request import urlopen
import urllib.request
from bs4 import BeautifulSoup
import os
import zipfile
import shutil
# python3 -m streamlit run /Users/youkyung/21October/streamlitgit/dior_2.py

st.title('DIOR')
st.header('공식 홈페이지 이미지 다운로드')

# st.write("1/ URL로 다운로드 받기")
# input = st.text_input(label="👇 여기에 제품 링크를 입력하고 ENTER 를 클릭하세요.")
# btn_clicked = st.button("ENTER",key='confirm_btn',disabled=(input is None))

# if btn_clicked:
#     start_down = st.button(label="다운로드 시작하기")
#     if start_down is not None:
#         indx = 1
#         url = input
#         headers = {'User-Agent' : 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36'}
#         response = requests.get(url, headers=headers)
#         html = response.text
#         soup = BeautifulSoup(html, 'html.parser')
#         name = soup.select_one('span.multiline-text.Titles_title__PAVsd').text
#         reference = soup.select_one('p.Titles_ref__7LPN1').text.split(':')[1].strip()
#         images = soup.select('img')
#         list1 = []
#         for img in images:
#             if reference in img['src']:
#                 try:
#                     list1.append(img['src'])
#                 except:
#                     pass

#         path = os.getcwd()
#         print(path)
        
#         n = 1
#         for i in list1:
#             with urlopen(i) as f:
#                 with open(path+"/"+str(indx)+"_"+name+str(n)+'.jpg','wb') as h:
#                     img = f.read()
#                     h.write(img)
#             n += 1
#         indx += 1

#     #파일 압축하기
#     with zipfile.ZipFile("img.zip",'w') as my_zip:
#         for file in os.listdir(path):
#             if file.endswith('.jpg') or file.endswith('.jpeg') or file.endswith('.png'):
#                 my_zip.write(file)

#     with open('img.zip', 'rb') as f:
#         st.download_button('이미지 압축 파일 다운로드 받기', f, file_name='img.zip')
    
#     st.success("작업이 완료되었습니다. 압축파일을 다운로드 받으세요.")


##########
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
            name = soup.select_one('span.multiline-text.Titles_title__PAVsd').text
            reference = soup.select_one('p.Titles_ref__7LPN1').text.split(':')[1].strip()
            images = soup.select('img')
            list = []
            for img in images:
                if reference in img['src']:
                    try:
                        list.append(img['src'])
                    except:
                        pass

            f_path = os.getcwd()
            st.write(f_path)
            n = 1
            for i in list:
                with urlopen(i) as f:
                    with open(f_path+"/"+str(indx)+"_"+name+str(n)+'.jpg','wb') as h:
                        img = f.read()
                        h.write(img)
                n += 1
            indx += 1

    #파일 압축하기
    with zipfile.ZipFile("img.zip",'w') as my_zip:
        for file in os.listdir(f_path):
            if file.endswith('.jpg') or file.endswith('.jpeg') or file.endswith('.png'):
                my_zip.write(file)

    with open('img.zip', 'rb') as f:
        down = st.download_button('이미지 압축 파일 다운로드 받기', f, file_name='img.zip')

    if down:
        import shutil
        shutil.rmtree(f_path)
        
    st.success(f"작업이 완료되었습니다. 압축파일을 다운로드 받으세요.")