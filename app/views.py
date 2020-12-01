import datetime, os
from flask import render_template, redirect, request, url_for
from app import app
import pandas as pd

posts = []
result = None
base_url = os.path.join(os.getcwd(), "app/static/")

def get_tor_session():
    # must install pysocks
    import requests
    session = requests.session()
    session.headers.update({'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'})
    # Tor uses the 9050 port as the default socks port
    session.proxies = {'http':  'socks5://127.0.0.1:9050', 'https': 'socks5://127.0.0.1:9050'}
    return session

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html',
                           title='Hi',
                           posts=posts)

@app.route('/about')
def about():
    return render_template('about.html',
                           title='About')

@app.route('/tnt')
def tnt():
    with open(base_url + "dump.csv") as f:
        contents = sum(1 for line in f)
    return render_template('tnt.html',
                           title='TNT Village will never die!',
                           contents=contents)

@app.route('/tnt/search', methods=['GET'])
def search_tnt():
    if request.method == 'GET':
        try: search_input = request.values.get("s")
        except: search_input = None
        try: category = int(request.values.get("category"))
        except: category = None

        df = pd.read_csv(base_url + "dump.csv", index_col=False, encoding='utf-8')
        #df = pd.read_csv("C:/Users/Cttynul/Desktop/hidden-service/app/static/dump.csv", index_col=False, encoding='utf-8')

        try:
            if category:
                df = df[df['CATEGORIA'] == category]
            
            if search_input:
                df["TITOLO"] = df["TITOLO"].str.lower()
                df["MATCH"] = df["TITOLO"].str.find(search_input) 
                df = df[df['MATCH'] > -1]
                df["TITOLO"] = df["TITOLO"].str.title()
                del df['MATCH']
                del df['TOPIC']
                del df['POST']
                del df['DESCRIZIONE']
                del df['AUTORE']
                df.reset_index(drop=True, inplace=True)
                df['HASH'] = '<a href="magnet:?xt=urn:btih:' + df['HASH'].astype(str) + '&dn=&tr=udp://tracker.openbittorrent.com:80/announce&tr=udp://opentor.org:2710/announce&tr=udp://tracker.ccc.de:80/announce&tr=udp://tracker.blackunicorn.xyz:6969/announce&tr=udp://tracker.coppersurfer.tk:6969/announce&tr=udp://tracker.leechers-paradise.org:6969/announce">Download</a>'
                df['CATEGORIA'] = '<img src="/static/icon' + df['CATEGORIA'].astype(str) + '.gif">'
                df['DIMENSIONE'] = df['DIMENSIONE'].apply(lambda x: x/1024/1024)
                df['DIMENSIONE'] = df['DIMENSIONE'].astype(int)
                df['DIMENSIONE'] = df['DIMENSIONE'].astype(str) + " MB"
            else:
                df = df[df['CATEGORIA'] == category]
                del df['TOPIC']
                del df['POST']
                del df['DESCRIZIONE']
                del df['AUTORE']
                df['HASH'] = '<a href="magnet:?xt=urn:btih:' + df['HASH'].astype(str) + '&dn=&tr=udp://tracker.openbittorrent.com:80/announce&tr=udp://opentor.org:2710/announce&tr=udp://tracker.ccc.de:80/announce&tr=udp://tracker.blackunicorn.xyz:6969/announce&tr=udp://tracker.coppersurfer.tk:6969/announce&tr=udp://tracker.leechers-paradise.org:6969/announce">Download</a>'
                df['CATEGORIA'] = '<img src="/static/icon' + df['CATEGORIA'].astype(str) + '.gif">'
                df['DIMENSIONE'] = df['DIMENSIONE'].apply(lambda x: x/1024/1024)
                df['DIMENSIONE'] = df['DIMENSIONE'].astype(int)
                df['DIMENSIONE'] = df['DIMENSIONE'].astype(str) + " MB"
        except:
            df = pd.DataFrame(columns=['DATA', 'HASH', 'TITOLO','DIMENSIONE', 'CATEGORIA'])
        
        df.reset_index(drop=True, inplace=True)
        df.index += 1
        return render_template('tnt.html', title='TNT Village will never die!', data=df.to_html(escape=False))


