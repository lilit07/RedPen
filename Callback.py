import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import re
import nltk
from collections import Counter
from nltk.tokenize import WordPunctTokenizer
from PIL import Image, ImageDraw
from termcolor import colored
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
colors = {
    'text': '#dd3939'
}
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.layout = html.Div([
    html.Div([
        html.H1(children='RedPen', style={
        'textAlign': 'center',
        'color': 'black',
        'position':'fixed'
        }),

        ], style={
        'width':'100%',
        
        }),
    html.H1(children='Welcome to the new Armenian Spellcheck', style={
        'textAlign': 'center',
        'color': colors['text'],
        }),

    dcc.Input(id='text_in', value='',placeholder="Type the text", type='text', style={
            'width': '70%',
            'height': '200px',
            'lineHeight': '60px',
            'borderRadius': '5px',
            'textAlign': 'center',
            'margin': '10px',
            'border': 'transparent'
        },),
    html.Button(id='submit',n_clicks=0, children='CHECK',  style={
            'width': '70%',
            'height': '60px',
            'lineHeight': '60px',
            'borderRadius': '5px',
            'textAlign': 'center',
            'margin': '10px',
            'background-color': '#dd3939',
            'color': 'white',
            'font-size': '22px', 
            
       
        },),
    

    
    html.Div(id='text_out', style={
        'width': '70%',
            'height': '200px',
            'lineHeight': '60px',
            'borderWidth': '4px',
            'borderRadius': '5px',
            'textAlign': 'center',
            'margin': '10px',
            'background-color': 'white'
        }),

], style ={
    'height': '100%',
    'width': '100%',
    'background-color': "#eaeaea",
    'margin': '0',
    'padding': '0',
    'display':'flex',
    'flex-direction': 'column',
    'align-items': 'center'


} 

)

def words(text): return re.findall(r'\w+', text.lower())



with open('base.txt', 'r',encoding="UTF-8") as file:
    content = file.read()

WORDS = Counter(words(content))

def P(word, N=sum(WORDS.values())): 
    "Probability of `word`."
    return WORDS[word] / N

def correction(word): 
    "Most probable spelling correction for word."
    return max(candidates(word), key=P)

def candidates(word): 
    "Generate possible spelling corrections for word."
    return (known([word]) or known(edits1(word)) or known(edits2(word)) or [word])

def known(words): 
    "The subset of `words` that appear in the dictionary of WORDS."
    return set(w for w in words if w in WORDS)

def edits1(word):
    "All edits that are one edit away from `word`."
    letters    = 'աբգդեզիլխծկհձզճմյնշոչպջռսվտրցուփքևօֆ'
    splits     = [(word[:i], word[i:])    for i in range(len(word) + 1)]
    deletes    = [L + R[1:]               for L, R in splits if R]
    transposes = [L + R[1] + R[0] + R[2:] for L, R in splits if len(R)>1]
    replaces   = [L + c + R[1:]           for L, R in splits if R for c in letters]
    inserts    = [L + c + R               for L, R in splits for c in letters]
    return set(deletes + transposes + replaces + inserts)

def edits2(word): 
    "All edits that are two edits away from `word`."
    return (e2 for e1 in edits1(word) for e2 in edits1(e1))

def edits3(word): 
    "All edits that are two edits away from `word`."
    return (e3 for e1 in edits1(word) for e2 in edits2(word) for e3 in edits2(e2))
def check(text):
    tokenizer = nltk.tokenize.WordPunctTokenizer()
    words=tokenizer.tokenize(text)
    alpha_lst=[word.lower () for word in words if word.isalpha()]
    ls_txt=set(alpha_lst)
    print(ls_txt)
    for i in ls_txt:
            text=text.replace(str(i),correction(i))
    return text

@app.callback(
    Output(component_id='text_out', component_property='children'),
    [Input(component_id='submit', component_property='n_clicks')],
    [State(component_id='text_in', component_property='value')]
)
def update_text_output(clicks,input_value_1):

    return check(input_value_1)


if __name__ == '__main__':
    app.run_server(debug=True)