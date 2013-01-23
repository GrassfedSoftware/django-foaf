from django import newforms as forms

class FoafForm(forms.Form):
  name=forms.CharField(widget=forms.TextInput(attrs={'size':'30'}),label='Nom complet',max_length=60)
  firstName=forms.CharField(widget=forms.TextInput(attrs={'size':'30'}),label='Prénom',max_length=60)
  family_name=forms.CharField(widget=forms.TextInput(attrs={'size':'30'}),label='Nom',max_length=60,required=False)
  nickname=forms.CharField(widget=forms.TextInput(attrs={'size':'30'}),label='Nickname',max_length=60,required=False)
  surname=forms.CharField(widget=forms.TextInput(attrs={'size':'30'}),label='Surnom',max_length=60,required=False)
  given_name=forms.CharField(widget=forms.TextInput(attrs={'size':'30'}),label='Nom courrant',max_length=60,required=False)
  homepage=forms.URLField(widget=forms.TextInput(attrs={'size':'60'}),label='Homepage (url)',required=False)
  weblog=forms.URLField(widget=forms.TextInput(attrs={'size':'60'}),label='Blog (url)',required=False)
  workplaceHomepage=forms.URLField(widget=forms.TextInput(attrs={'size':'60'}),label='Homepage travail (url)',required=False)
  workInfoHomepage=forms.URLField(widget=forms.TextInput(attrs={'size':'60'}),label='Informations sur mon travail (url)',required=False)
  schoolHomepage=forms.URLField(widget=forms.TextInput(attrs={'size':'60'}),label='Homepage école (url)',required=False)
  #~ how does MultiValueField works?
  #knows=forms.MultiValueField(label='Connaissances',required=False)
