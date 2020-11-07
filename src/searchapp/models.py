from django.db import models

# Create your models here.
class SearchModel(models.Model):
	keywords = models.CharField(max_length=255)
	exact_phrase =models.CharField(max_length=255,blank=True)
	minus_words = models.CharField(max_length=255,blank=True)
	language_choices = (('af', 'Afrikaans'),('ar', 'Arabic'),('bg', 'Bulgarian'),('bn', 'Bengali'),('en', 'English'),('de', 'German'),('fr', 'French'),('it', 'Italian'),('pt-BR', 'Portuguese(Brazil)'),('pt-PT', 'Portuguese(Portugal)'),('cs', 'Czech'),('hr', 'Croatian'),('da', 'Danish'),('nl', 'Dutch'),('et', 'Estonian'),('fi', 'Finnish'),('el', 'Greek'),('no', 'Norwegian'),('nn', 'Norwegian (Nynorsk)'),('hi', 'Hindi'),('hu', 'Hungarian'),('id', 'Indonesian'),('ja', 'Japanese'),('lv', 'Latvian'),('lt', 'Lithuanian'),('fa', 'Persian'),('pl', 'Polish'),('ro', 'Romanian'),('ru', 'Russian'),('es', 'Spanish'),('sk', 'Slovak'),('sl', 'Slovenian'),('sw', 'Swahili'),('sv', 'Swedish'),('ta', 'Tamil'),('te', 'Telugu'),('th', 'Thai'),('tr', 'Turkish'),('ko', 'Korean'),('uk', 'Ukrainian'),('ur', 'Urdu'),('vi', 'Vietnamese'))
	language = models.CharField(choices=language_choices,max_length=255)	