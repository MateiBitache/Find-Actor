import requests
from bs4 import BeautifulSoup
from flask import Flask,render_template,request
import threading
app=Flask(__name__)
def doo(movie,list2):
    score = movie['data-tomatometer']
    title = movie['data-title']
    link = 'https://www.rottentomatoes.com' + movie.find('a', attrs={'href': True})['href']
    if score:
        list2.append([score, title, link])
@app.route('/',methods=['GET','POST'])
def do():
    if request.method=='POST':
        actor=request.form.get('actor')
        """
            url = 'https://www.rottentomatoes.com/search?search=' + actor
            soup = BeautifulSoup(requests.get(url).content, 'html.parser')
            list = soup.find_all('search-page-media-row')
            list2 = []
            for movie in list:
                cast = movie['cast']
                score = movie['tomatometerscore']
                year = movie['releaseyear']
                v = movie.find_all('a')
                link = v[1]['href']
                title = v[1].text
                if score:
                    list2.append([score, title, cast, year, link])
            sortat = sorted(list2, key=lambda x: x[0], reverse=True)
            return render_template('index.html',actor=actor,lista=sortat)
        """
        url='https://www.rottentomatoes.com/celebrity/'+'_'.join(actor.split())
        soup = BeautifulSoup(requests.get(url).content, 'html.parser')
        list = soup.find_all('tr', attrs={'data-title': True})
        list2 = []
        threads=[]
        for movie in list:
           thread=threading.Thread(target=doo,args=(movie,list2,))
           threads.append(thread)
        for thread in threads:
            thread.start()
        for thread in threads:
            thread.join()
        sortat = sorted(list2, key=lambda x: x[0], reverse=True)
        print(f"Elapsed time: {elapsed_time} seconds")
        return render_template('index.html', actor=actor, lista=sortat)
    else:
        return render_template('index.html')
app.run()
