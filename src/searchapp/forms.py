from django import forms
from .models import SearchModel

class SearchForm(forms.ModelForm):
	class Meta:
		model=SearchModel
		fields=["keywords","exact_phrase","minus_words","language"]
