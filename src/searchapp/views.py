from django.shortcuts import render,redirect
from .forms import SearchForm
import requests
import json
import pandas as pd
from collections import Counter
import numpy as np
import plotly
import plotly.graph_objects as go
import plotly.express as px
import re
import itertools
from nltk.corpus import stopwords
from plotly.subplots import make_subplots

#functions
def add_None(l,post_count):
    curr_l=len(l)
    n=post_count-curr_l
    if(n>0):
        for i in range(n):
            l.append(None)
    return l
def get_posts(query,lang="en"):
    response_list=[]
    limit=1000
    API_KEY="29c8bf6be225c26786640b80d18d2319"
    url="https://api.social-searcher.com/v2/search?q="+query+"&limit="+str(limit)+"&lang="+lang+"&key="+API_KEY
    print("URL",url)
    res1=requests.get("https://api.social-searcher.com/v2/search?q="+query+"&limit="+str(limit)+"&lang="+lang+"&key="+API_KEY)
    pages=limit//100
    limit=100
    requestid=res1.json()['meta']['requestid']
    response_list.append(res1)
    for i in range(1,pages):
        res_x=requests.get("https://api.social-searcher.com/v2/search?requestid="+requestid+"&page="+str(i)+"&limit="+str(limit)+"&lang="+lang+"&key="+API_KEY)
        response_list.append(res_x)
    return response_list

def dataset_generator(response_list):
    sentiment=[]
    network=[]
    date=[]
    text=[]
    influence=[]
    popularity=[]
    type_of_post=[]
    post_count=0
    for response in response_list:
        for post in response.json()['posts']:
            post_count+=1
            try:
                sentiment.append(post['sentiment'])
                date.append(post['posted'])
                network.append(post['network'])    
                text.append(post['text'])
                type_of_post.append(post['type'])
                try:
                    popularity_val={post['popularity'][0]['name']:post['popularity'][0]['count']}
                    popularity.append(popularity_val)
                except:
                    pass
                try:
                    influence_val={post['user']['influence']['name']:post['user']['influence']['count']}
                    influence.append(influence_val)
                except Exception as ex:
                    pass
            except Exception as ex:
                pass
    sentiment=add_None(sentiment,post_count)
    network=add_None(network,post_count)
    date=add_None(date,post_count)
    text=add_None(text,post_count)
    influence=add_None(influence,post_count)
    popularity=add_None(popularity,post_count)
    type_of_post=add_None(type_of_post,post_count)
    data= {
        "Date":date , 
        "Network":network , 
        "Text":text , 
        "Sentiment":sentiment , 
        "Influence":influence , 
        "Popularity": popularity,
          }
    return pd.DataFrame(data)
def posts_per_network(data_collected):
    c=Counter(data_collected.Network)
    network=[]
    counting=[]
    for x in c:
        network.append(x)
        counting.append(c[x])
    df1 = pd.DataFrame(dict(x=network, y=counting))
    fig = px.bar(df1, y='x', x='y', color='x', height=550, color_discrete_sequence= px.colors.sequential.Agsunset, labels={'x':'Network','y':'Count of posts'},title="Posts by Social Network")
    fig.update_layout({'plot_bgcolor': 'rgb(28, 28, 28)', 'paper_bgcolor': 'rgb(28, 28, 28)'},font_color="white")
    fig = plotly.offline.plot(fig, auto_open = False, output_type="div")
    return fig   
def get_percentages(data_collected):
    x=Counter(data_collected['Sentiment'])
    mentions=sum(list(x.values()))
    positiveper=round(x['positive']*100/mentions)
    negativeper=round(x['negative']*100/mentions)
    neutralper=round(x['neutral']*100/mentions)
    network=Counter(data_collected['Network'])
    network=network.most_common(1)[0][0]
    return [positiveper, negativeper, neutralper,mentions,network.title()]
def network_sentiment_graph(data_collected):
    network_sentiment={}
    for network in data_collected['Network'].unique():
        network_sentiment[network]=Counter(data_collected[data_collected['Network']==network]['Sentiment'])

    night_colors = ['rgb(75, 41, 145)', 'rgb(192, 54, 157)', 'rgb(234, 79, 136)']
    network_fig=[]
    for network in network_sentiment.keys():
        arr=np.transpose(np.array(list(network_sentiment[network].items())))
        x=arr[0]
        y=list(map(int,arr[1]))
        fig = go.Figure(data=[go.Pie(labels=x, values=y,hole=0.3,sort=True,pull=[0.0,0.0,0.,0.5],title=network.title(),marker_colors=night_colors)],layout={'width':500,'height':400})
        fig.update_layout({'plot_bgcolor': 'rgb(28, 28, 28)', 'paper_bgcolor': 'rgb(28, 28, 28)'},font_color="white",font_size=10,margin=dict(l=0,r=0,b=0,t=0),showlegend=False)
        fig = plotly.offline.plot(fig, auto_open = False, output_type="div")
        network_fig.append(fig)
    return network_fig

def word_frequency(data_collected,keywords,exact_phrase=""):
    text=[]
    text_no_urls=[]
    collection_words=[]
    for i in data_collected['Text']:
        if 'RT @' not in i:
            text.append(i)
    for i in text:
        text_no_urls.append(" ".join(re.sub("([^0-9A-Za-z \t])|(\w+://\S+)", "", i).split()))
    words_in_text = [text.lower().split() for text in text_no_urls]
    stop_words = set(stopwords.words('english'))
    text_nsw = [[word for word in text_words if not word in stop_words] for text_words in words_in_text]
    collection_words+=keywords.lower().split(" ")+exact_phrase.lower().split(" ")
    texts_nsw_nc = [[w for w in word if not w in collection_words] for word in text_nsw]
    all_words_nsw_nc = list(itertools.chain(*texts_nsw_nc))
    counts_nsw_nc = Counter(all_words_nsw_nc)
    clean_texts_ncw = pd.DataFrame(counts_nsw_nc.most_common(15),columns=['words', 'count'])
    clean_texts_ncw.sort_values(by='count',ascending=False)
    print(clean_texts_ncw)
    fig = px.bar(clean_texts_ncw, x='words', y='count', color='words', color_discrete_sequence= px.colors.sequential.Agsunset, labels={'x':'Words','y':'Frequency'},title="Common words found in Posts")
    fig.update_layout({'plot_bgcolor': 'rgb(28,28,28)', 'paper_bgcolor': 'rgb(28,28,28)'},font_color="white")
    fig = plotly.offline.plot(fig, auto_open = False, output_type="div")
    return fig

def posts_by_time(data_collected):
    date,time=[],[]
    for i in data_collected['Date']:
        date.append(i[0:10].strip())
        time.append(i[11:19].strip())
        hours=[]
    data_collected['Date']=date
    data_collected['Time']=time
    data_collected['Time'] = pd.to_datetime(data_collected['Time'],format= '%H:%M:%S' ).dt.time
    data_collected['Date']=pd.to_datetime(data_collected['Date'])
    time_x=[]
    num_posts_y=[]
    for time in data_collected['Time']:
        hours.append(time.hour)
    d=Counter(hours)
    for time in sorted(d):
        time_x.append(time)
        num_posts_y.append(d[time])
    df = pd.DataFrame(dict(x=time_x, y=num_posts_y))
    fig = px.bar(df, y='y', x='x', color='x', height=550, color_discrete_sequence= px.colors.sequential.Agsunset, labels={'x':'Time in 24hr format','y':'Count of posts'},title="Frequency of Posts by Time")
    fig.update_layout({'plot_bgcolor': 'rgb(28, 28, 28)', 'paper_bgcolor': 'rgb(28, 28, 28)'},font_color="white")
    fig = plotly.offline.plot(fig, auto_open = False, output_type="div")
    return fig

def top_influential(data_collected):
    df=data_collected[data_collected['Influence'].notnull()]
    followers=[]
    for i in df['Influence']:
        for key in i:
            followers.append(i[key])
    df = df.assign(Followers = followers) 
    a =df.sort_values(by='Followers', ascending=False).iloc[0:,]
    network=a['Network'].values[0:20]
    text=a['Text'][0:20].values
    sentiment=a['Sentiment'].values[0:20]
    followers=a['Followers'].values[0:20]
    data=list(zip(network,text,sentiment,followers))
    return data
# Create your views here.
def search_page(request):
	form = SearchForm()
	context={'form': form}
	return render(request,'search_page.html',context)
def results_page(request):
    context={}
    keywords=request.GET.get('keywords')
    language=request.GET.get('language')
    exact_phrase,minus_words="",""
    exact_phrase=request.GET.get('exact_phrase')
    minus_words=request.GET.get('minus_words')
    query=keywords
    if exact_phrase!="":
        query=query+' OR "'+exact_phrase+'"'
    if minus_words !="":
        query = query+  ' -'+minus_words
    print("Query: ",query)
    try:
        #  positive negative neutral mentions network
        response_list=get_posts(query,language)
        data_collected=dataset_generator(response_list)
        percentages=get_percentages(data_collected)
        print(percentages)
        posts_per_network_graph=posts_per_network(data_collected)
        sentiment_per_network_graph=network_sentiment_graph(data_collected)
        word_freq=word_frequency(data_collected,keywords,exact_phrase)
        graph_posts_by_time=posts_by_time(data_collected)
        data=top_influential(data_collected)
        # network,text,sentiment,date,followers
        context={"g1":posts_per_network_graph ,"g2":sentiment_per_network_graph,"g3":word_freq,"g4":graph_posts_by_time,"percentages":percentages,"data":data}
    except Exception as ex:
        print(ex)
        return redirect('error')

    return render(request,'results.html',context)
def error_page(request):
	return render(request,'error_page.html',{})