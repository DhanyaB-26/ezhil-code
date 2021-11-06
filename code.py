from jina import Executor, DocumentArray, Document
import pandas as pd

df = pd.read_csv('colors.csv')

colors = df[['Name','Red (8 bit)', 'Green (8 bit)', 'Blue (8 bit)']].copy()
colors2 = colors[['Red (8 bit)', 'Green (8 bit)', 'Blue (8 bit)']].copy()

colors_r = colors['Red (8 bit)'].copy()
colors_g = colors['Green (8 bit)'].copy()
colors_b = colors['Blue (8 bit)'].copy()

import numpy as np

r = {'Red (8 bit)': [90]}
g = {'Green (8 bit)': [80]}
b = {'Blue (8 bit)': [90]}

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

# matching r values
dar = DocumentArray()
for c in c_train_r:
    dar.append(Document(embedding = c))
    
dar1 = DocumentArray()
for c in num_r:
    dar1.append(Document(embedding = c))

dar1.match(dar, metric='euclidean', limit = 3)
query = dar1[2]
print("hello")
print(f'query emb = {query.embedding}')
for m in query.matches:
    print('match emb =', m.embedding, 'score =', m.scores['euclidean'].value)

# matching g values
dag = DocumentArray()
for c in c_train_g:
    dag.append(Document(embedding = c))
    
dag1 = DocumentArray()
for c in num_g:
    dag1.append(Document(embedding = c))

dag1.match(dag, metric='euclidean', limit = 3)
query = dag1[2]
print("hello")
print(f'query emb = {query.embedding}')
for m in query.matches:
    print('match emb =', m.embedding, 'score =', m.scores['euclidean'].value)

# matching b values
dab = DocumentArray()
for c in c_train_b:
    dab.append(Document(embedding = c))
    
dab1 = DocumentArray()
for c in num_b:
    dab1.append(Document(embedding = c))

dab1.match(dab, metric='euclidean', limit = 3)
query = dab1[2]
print("hello")
print(f'query emb = {query.embedding}')
for m in query.matches:
    print('match emb =', m.embedding, 'score =', m.scores['euclidean'].value)