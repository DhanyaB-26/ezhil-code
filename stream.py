import streamlit as st
from PIL import Image
import os

 def find_rgb(image_path):
            value = io.imread(image_path)
            rgb = []
            for i in range(3):
                rgb.append(value[0][0][i])
            r,g,b = rgb[0],rgb[1],rgb[2]
            hexcode = ('#{:X}{:X}{:X}').format(r, g, b)
            l = []
            l.append(rgb)
            l.append(hexcode)
            return l

st.set_page_config(page_title="Jina Project",)
st.title("JINA PROJECT")
image = st.file_uploader("Upload an image",accept_multiple_files = True)
for img in image:
    name = img.name
    path = os.path.basename(name)
    values = find_rgb(path)
    st.image(img)
    for value in values:
        st.write(value)
                            


