from PIL import Image
import streamlit as st
from streamlit_jina import jina
import os
from jina import Executor, requests

class Colors(Executor):

    def rgb_values(self, image_path, x, y, **kwargs):
            im= Image.open(image_path).convert('RGB')
            r,g,b = im.getpixel((x,y))
            a = (r,g,b)    
            c = ('#{:X}{:X}{:X}').format(r, g, b)
            l =[]
            l.append(a)
            l.append(c)
            return l

# Use Executor out of Flow
shade = Colors()
image = 'color.jpg'
# st.title("JINA PROJECT")
# image = st.file_uploader("Upload an image", accept_multiple_files = True)
# for img in image:
# byte_data = image.read()
#     name = img.name
#     path = os.path.abspath(name)
#     values = shade.rgb_values(path,35,35)
#     st.image(img)
#     for value in values:
#         st.write(value)

path = os.path.abspath(image)
value = shade.rgb_values(path, 35,35)
for val in value:
    print(val)

