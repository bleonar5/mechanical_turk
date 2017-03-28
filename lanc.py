import nltk
from nltk.stem.lancaster import LancasterStemmer

st = LancasterStemmer()

print(st.stem('baking-hot'))