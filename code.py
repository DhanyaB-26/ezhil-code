'''
pip install scikit-image
'''
import glob
from skimage import io,data
from skimage.color import rgba2rgb
import os
import pandas as pd
import numpy as np
from jina import Document, Executor, Flow, DocumentArray


class Colors(Executor):
      
    def find_rgb(self, image_path, **kwargs):
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
        
# class SimpleIndexer(Executor):
    
#     @requests (on='\search')
#     def find_color_name():
        
#_________________________________________________________________________________


df = pd.read_csv('colors.csv')
colors = df[['Name','Red (8 bit)', 'Green (8 bit)', 'Blue (8 bit)']].copy()
colors2 = colors[['Red (8 bit)', 'Green (8 bit)', 'Blue (8 bit)']].copy()
    
class Checker(Executor):
    
    def checking_presence(self, rgb, **kwargs):
        
        # matching r values
        def match_red():
            dar = DocumentArray()
            for c in c_train_r:
                dar.append(Document(embedding = c))

            dar1 = DocumentArray()
            for c in num_r:
                dar1.append(Document(embedding = c))

            dar1.match(dar, metric='euclidean', limit = 1)
            query = dar1[2]
            print("___________________________________________________________________")
            print(f'query emb = {query.embedding}')
            for m in query.matches:
                print('match emb =', m.embedding, 'score =', m.scores['euclidean'].value)
                return m.embedding

        # matching g values
        def match_green():
            dag = DocumentArray()
            for c in c_train_g:
                dag.append(Document(embedding = c))

            dag1 = DocumentArray()
            for c in num_g:
                dag1.append(Document(embedding = c))

            dag1.match(dag, metric='euclidean', limit = 1)
            query = dag1[2]
            print("___________________________________________________________________")
            print(f'query emb = {query.embedding}')
            for m in query.matches:
                print('match emb =', m.embedding, 'score =', m.scores['euclidean'].value)
                return m.embedding
        #________________________________________________________________________________

        # matching b values
        def match_blue():
            dab = DocumentArray()
            for c in c_train_b:
                dab.append(Document(embedding = c))

            dab1 = DocumentArray()
            for c in num_b:
                dab1.append(Document(embedding = c))

            dab1.match(dab, metric='euclidean', limit = 1)
            query = dab1[2]
            print("___________________________________________________________________")
            print(f'query emb = {query.embedding}')
            for m in query.matches:
                print('match emb =', m.embedding, 'score =', m.scores['euclidean'].value)
                return m.embedding
        
        colors_r = colors['Red (8 bit)'].copy()
        colors_g = colors['Green (8 bit)'].copy()
        colors_b = colors['Blue (8 bit)'].copy()

        #________________________________________________________________________________

        r,g,b = rgb[0],rgb[1],rgb[2]
        r = {'Red (8 bit)': [r]}
        g = {'Green (8 bit)': [g]}
        b = {'Blue (8 bit)': [b]}

        # DataFrame creation
        r_colour = pd.DataFrame(r)
        g_colour = pd.DataFrame(g)
        b_colour = pd.DataFrame(b)

        # 1D array to numpy
        c_test_r = pd.DataFrame(r_colour).to_numpy()
        c_test_g = pd.DataFrame(g_colour).to_numpy()
        c_test_b = pd.DataFrame(b_colour).to_numpy()

        # 2D array to numpy
        c_train_r = pd.DataFrame(colors_r).to_numpy()
        c_train_g = pd.DataFrame(colors_g).to_numpy()
        c_train_b = pd.DataFrame(colors_b).to_numpy()

        #________________________________________________________________________________

        # to duplicate c_test_r
        r = []
        for i in range(1298):
            for c in c_test_r:
                r.append(c)
        num_r = np.array(r)

        # to duplicate c_test_g
        g = []
        for i in range(1298):
            for c in c_test_g:
                g.append(c)
        num_g = np.array(g)

        # to duplicate c_test_b
        b = []
        for i in range(1298):
            for c in c_test_b:
                b.append(c)
        num_b = np.array(b)

        #________________________________________________________________________________
        red = match_red()
        green = match_green()
        blue = match_blue()

        z = np.array([int(red),int(green),int(blue)])
        result = (colors2 == z).all(1).any()

        if result == False : 
            colors2.append({'Red (8 bit)':red,'Green (8 bit)':green,'Blue (8 bit)':blue}, ignore_index = True)
            colors2.to_csv('color_names.csv')
            print("Color added")

#________________________________________________________________________________
# to find the file path
def file_finder():
    file_name = input("Enter the file name::")
    img_path = os.path.abspath(file_name)
    return img_path

# starting .....
val = file_finder()
shade = Colors()
check = Checker()
color = shade.find_rgb(val)
check.checking_presence(color[0])
print("RGB value::", color[0])
print("Hex code value::", color[1])

#_________________________________________________________________________________
        

f = Flow().add(uses = Colors, name = 'color_finder').add(uses = Checker, name = 'presence_of_color'
).plot('f.svg')
