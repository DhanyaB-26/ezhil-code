from jina import Executor, DocumentArray, Document, Flow
import pandas as pd
import numpy as np
from PIL import Image
import os

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
#________________________________________________________________________________

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
#________________________________________________________________________________

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

#________________________________________________________________________________ 

# starting
shade = Colors()
image = 'green.png'

path = os.path.abspath(image)
value = shade.rgb_values(path, 35,35)
for val in value:
    print(val)

df = pd.read_csv('colors.csv')

#________________________________________________________________________________

colors = df[['Name','Red (8 bit)', 'Green (8 bit)', 'Blue (8 bit)']].copy()
colors2 = colors[['Red (8 bit)', 'Green (8 bit)', 'Blue (8 bit)']].copy()

colors2.to_csv('color_name.csv')

da = DocumentArray()
for c in colors2:
    da.append(Document(content = c))

d = []

for index, row in colors2.iterrows():
    d.append(list(row))

colors_r = colors['Red (8 bit)'].copy()
colors_g = colors['Green (8 bit)'].copy()
colors_b = colors['Blue (8 bit)'].copy()

#________________________________________________________________________________

a = []
for i in value[0]:
    a.append(i)

r,g,b = a[0],a[1],a[2]
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
    print("Color added")
        
#________________________________________________________________________________

flow = (
    Flow(install_requirements = True)
    .add(
        name="color_seeker",
        uses='jinahub://SimpleIndexer',
    )
).plot()

with flow:
    flow.index(
        inputs=da,
    )  
    
print(flow.inspect())

#________________________________________________________________________________