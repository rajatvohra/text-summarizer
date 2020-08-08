from pagerank import main as rank
from frequency_based import main as freq

x=input("freq or rank?\n" )
if(x=='freq'):
    freq()
else:
    rank()
    