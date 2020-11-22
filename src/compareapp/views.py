from django.shortcuts import render
from django.conf import settings
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
from searchapp.forms import SearchForm
import concurrent.futures
# Create your views here.

#my functions


#views
def compare_page(request):
	from searchapp.views import compare_dataset
	from searchapp.views import global_query
	context={}
	if global_query!="":
		context["global_query"] = global_query
		if "OR" in global_query:
			temp=global_query.split("OR")
			keywords=temp[0]
			context["keywords"]=keywords
			if "-" in temp[1]:
				temp2=temp[1].split("-")
				exact_phrase=temp2[0].strip('"').strip().strip('"')
				minus_words=temp2[1]
				context["minus_words"]=minus_words
				context["exact_phrase"]=exact_phrase
			else:
				context["exact_phrase"]=temp[1].strip('"').strip().strip('"')
		elif "-" in global_query:
			temp=global_query.split("-")
			context["keywords"]=temp[0]
			context["minus_words"]=temp[1]
		else:
			context["keywords"]=global_query
	form = SearchForm()
	context['form']=form
	return render(request,'compare_page.html',context)