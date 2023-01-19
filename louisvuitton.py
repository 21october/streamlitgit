from io import BytesIO
import streamlit as st
import pandas as pd
import requests
from urllib.request import urlopen
import urllib.request
from bs4 import BeautifulSoup
import os
import zipfile
from PIL import Image
# python3 -m streamlit run /Users/youkyung/21October/streamlitgit/louisvuitton.py
try:
    os.mkdir("LV")
except:
    pass

st.title('LOUIS VUITTON')
st.header('공식 홈페이지 이미지 다운로드')

st.write("")
st.write("")
st.write("")
st.write("엑셀 대량 다운로드")
uploaded_file = st.file_uploader(label="Url 리스트(엑셀)를 업로드 하세요.", type='xlsx')
if uploaded_file is not None:
    df = pd.read_excel(uploaded_file)
    st.dataframe(df)
    urls = df['링크']

    start_down = st.button(label="다운로드 시작하기")
    if start_down is not None:
        indx = 1
        for url in urls:            
            headers = {'User-Agent' : 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36'}
            response = requests.get(url, headers=headers)
            html = response.text
            soup = BeautifulSoup(html, 'html.parser')
            name = soup.select_one('h1.lv-product__name').text.strip()
            images = soup.select('li > button > div > picture > img')
            images2 = soup.select('section.lv-product__sections > section.lv-product-immersion.lv-product__section > div > div > div > picture > img')
            list = []
            for image in images:
                if image.get('srcset') is not None:
                    strings = image.get('srcset')
                    imgUrls = strings.split(',')
                    img456 = imgUrls[2].strip()
                    list.append(img456)
                else:
                    strings = image.get('data-srcset')
                    imgUrls = strings.split(',')
                    img456 = imgUrls[2].strip()
                    list.append(img456)
            
            #하단 이미지            
            for image2 in images2:
                if image2.get('srcset') is not None:
                    strings2 = image2.get('srcset')
                    imgUrls2 = strings2.split(',')
                    img456_2 = imgUrls2[2].strip()
                    list.append(img456_2)
                else:
                    strings2 = image2.get('data-srcset')
                    imgUrls2 = strings2.split(',')
                    img456_2 = imgUrls2[2].strip()
                    list.append(img456_2)

            path = os.getcwd() + '/LV'
            
            n = 1
            for i in list:
                res = requests.get(i,headers=headers)
                image = Image.open(BytesIO(res.content))
                image.save(path+'/'+str(indx)+'_'+name+str(n)+'.png','PNG')
                n += 1
            st.write(f"{indx}번 완료")
            indx += 1

    # #파일 압축하기
    # with zipfile.ZipFile("img.zip",'w') as my_zip:
    #     for file in os.listdir(path):
    #         if file.endswith('.jpg') or file.endswith('.jpeg') or file.endswith('.png'):
    #             my_zip.write(file)

    # with open('img.zip', 'rb') as f:
    #     st.download_button('이미지 압축 파일 다운로드 받기', f, file_name='img.zip')
    
    st.success(f"작업이 완료되었습니다. 이미지가 {path}에 저장되었습니다.")