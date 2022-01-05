from django.shortcuts import render
from django.http import HttpResponse
from PyDictionary import PyDictionary
import requests
from bs4 import BeautifulSoup

def synonym(term):
    response = requests.get('https://www.thesaurus.com/browse/{}'.format(term))
    soup = BeautifulSoup(response.text, 'html.parser')
    soup.find('section', {'class': 'css-191l5o0-ClassicContentCard e1qo4u830'})
    return [span.text for span in soup.findAll('a', {'class': 'css-1kg1yv8 eh475bn0'})] 

def antonym(term):
    response = requests.get('https://www.thesaurus.com/browse/{}'.format(term))
    soup = BeautifulSoup(response.text, 'lxml')
    soup.find('section', {'class': 'antonym-container'})
    return [span.text for span in soup.findAll('a', {'class': 'css-18rr30y'})] # class = .css-7854fb for less relevant

import dictionary
# Create your views here.

def index(request):
	return render(request,'dictionary/index.html')

def word(request):
	search=request.GET.get('search')
	dictionary=PyDictionary()
	meaning=dictionary.meaning(search)
	synonyms=synonym(search)
	antonyms=antonym(search)

	context={
		'meaning':meaning,
		'synonyms':synonyms,
		'antonyms':antonyms
	}

	return render(request,'dictionary/word.html',context)
