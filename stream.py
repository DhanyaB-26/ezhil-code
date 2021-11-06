import streamlit as st
from PIL import Image
import os


def rgb_values(image_path ,x = 35, y = 35):
            
        im= Image.open(image_path).convert('RGB')
        r,g,b = im.getpixel((x,y))
        a = (r,g,b)    
        c = ('#{:X}{:X}{:X}').format(r, g, b)
        l =[]
        l.append(a)
        l.append(c)
        return l

st.set_page_config(page_title="Jina Project",)
st.title("JINA PROJECT")
image = st.file_uploader("Upload an image",accept_multiple_files = True)
for img in image:
    name = img.name
    path = os.path.basename(name)
    values = rgb_values(path,40,40)
    st.image(img)
    for value in values:
        st.write(value)
                            


