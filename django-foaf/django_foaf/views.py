import os
from django.shortcuts import render_to_response
from django.conf import settings
from django.template import RequestContext
from django.contrib.auth.models import User
from django_foaf.controlers import has_foaf, parse_foaf, update_foaf, save_foaf_file
from django_foaf.forms import FoafForm

def index(request):
  users=User.objects.all()
  for user in users: 
    foaf_file=has_foaf(user)
    if foaf_file:
      user.foaf_file=foaf_file
    else:
      user.foaf_file=None
  return render_to_response('foaf/index.html', {'users':users},context_instance=RequestContext(request))

def pack_person_data(person):
  #~ function used by render_foaf to pack data in a format that fits for passing to the template
  person_data={}
  #~ thanks to benoitc for suggesting the replacement of try/except by getattr
  person_data['foaf_file']=getattr(person,'foaf_file','no url')
  person_data['name']=getattr(person,'name')
  person_data['firstName']=getattr(person,'firstName')
  person_data['family_name']=getattr(person,'family_name')
  person_data['nickname']=getattr(person,'nickname')
  person_data['given_name']=getattr(person,'givenname')
  person_data['surname']=getattr(person,'surname')
  try:
    person_data['homepage']=str(person.homepage.resUri)
  except:
    person_data['homepage']=''
  try:
    person_data['weblog']=str(person.weblog.resUri)
  except:
    person_data['weblog']=''
  try:
    person_data['image_url']=str(person.depiction.resUri)
  except:
    person_data['image_url']=''
  try:
    person_data['workplaceHomepage']=str(person.workplaceHomepage.resUri)
  except:
    person_data['workplaceHomepage']=''
  try:
    person_data['workInfoHomepage']=str(person.workInfoHomepage.resUri)
  except:
    person_data['workInfoHomepage']=''
  try:
    person_data['schoolHomepage']=str(person.schoolHomepage.resUri)
  except:
    person_data['schoolHomepage']=''
  try:
    interests=[]
    for interest in person.interests:
      interests.append(str(interest.resUri))
    person_data['interests']=interests
  except:
    pass
  return person_data

def render_foaf(request):
  if request.GET.has_key('url'):
    foaf_data=parse_foaf(request.GET['url'])
  else:
    return render_to_response('error.html',{'message':"Indiquer l'url du fichier foaf"})
  #~ parsing error check
  if foaf_data.has_key('error'):
    return render_to_response('error.html',{'message':foaf_data['error']})
  #~ package main data for template
  main_person_data=pack_person_data(foaf_data['main_person'])
  relations_data={}
  for relation in foaf_data['relations'].keys():
    person_relations=[]
    for person in foaf_data['relations'][relation]:
      person_relations.append(pack_person_data(person))
    relations_data[relation]=person_relations
  #~ debug
  #msg=''
  #for el in relations_data['knows']:
  #  msg=msg+str(el)+' / '
  #return render_to_response('error.html',{'message':msg})
  #~ render template
  return render_to_response('foaf/render_foaf.html',{'person':main_person_data,'relations':relations_data})
  
def edit_foaf(request):
  if request.user.is_anonymous():
    return render_to_response('error.html',{'message':'Vous devez être connectés pour éditer votre profil'})
  #~ check if user already has a foaf file
  foaf_file=None
  if os.path.isfile(settings.FOAF_DATA+request.user.username+'.rdf'):
    foaf_file=settings.FOAF_URI+request.user.username+'.rdf'
    person=parse_foaf(foaf_file)['main_person']
    form_data=pack_person_data(person)
    form=FoafForm(form_data)
  else:
    form=FoafForm(request.POST)
  return render_to_response('foaf/edit.html',{'foaf_file':foaf_file,'form':form},context_instance=RequestContext(request))

def edit_foaf_step2(request):
  if request.user.is_anonymous():
    return render_to_response('error.html',{'message':'Vous devez être connectés pour éditer votre profil'})
  identity_data=[]
  for key in request.POST.keys():
    identity_data.append(str(key)+'#>>#'+str(request.POST[key]))
  identity_data='#$||$#'.join(identity_data)
  foaf_file=None
  internal_relations_data={}
  external_relations_data={}
  #~ get existing data
  if os.path.isfile(settings.FOAF_DATA+request.user.username+'.rdf'):
    foaf_file=settings.FOAF_URI+request.user.username+'.rdf'
    foaf_data=parse_foaf(settings.FOAF_DATA+request.user.username+'.rdf')
    #out=[]
    #out.append(str(foaf_data))
    relations=foaf_data['relations']
    #~ pack relations data
    for relation in relations.keys():
      internal_relations=[]
      external_relations=[]
      for person in relations[relation]:
        if settings.FOAF_URI in person.foaf_file:
          internal_relations.append(person.foaf_file)
        else:
          external_relations.append(person.foaf_file)
        #out.append(relation+' > '+person.foaf_file)
      #out.append(str(internal_relations))
      i=0
      external_relations_packed=[]
      while i<5:
        try:
          external_relations_packed.append(external_relations[i])
        except:
          external_relations_packed.append('')
        i=i+1
      internal_relations_data[relation]=internal_relations
      external_relations_data[relation]=external_relations_packed
      #out.append(str(internal_relations))
      #out.append(relation+' > '+str(internal_relations_data[relation]))
  ikeys=['friendOf','worksWith','hasMet','wouldLikeToKnow','knowsByReputation']
  for akey in ikeys:
    if not external_relations_data.has_key(akey):
      external_relations_data[akey]=['','','','','']
  #out.append('internal> '+str(internal_relations_data))
  #out.append('external> '+str(external_relations_data))
  users=User.objects.all()
  #~ pack user data
  users_data=[]
  for user in users:
    user_data={}
    user_data['name']=user.username
    user_data['foaf_file']=has_foaf(user)
    users_data.append(user_data)
  #~ debug
  #if foaf_data.has_key('error'):
  #  out=foaf_data['error']
  #  return render_to_response('debug.html',{'message':out})
  #out=[]
  #for el in relations.keys():
  #  for person in relations[el]:
  #    out.append(str(person.foaf_file))
  #return render_to_response('debug.html',{'message':'\n'.join(out)})
  return render_to_response('foaf/edit_step2.html',{'identity_data':identity_data,'internal_relations':internal_relations_data,'external_relations':external_relations_data,'users':users_data},context_instance=RequestContext(request))

def edit_foaf_post(request):
  if request.user.is_anonymous():
    return render_to_response('error.html',{'message':'Vous devez être connectés pour éditer votre profil'})
  result=save_foaf_file(request)
  if result<>True:
    #return render_to_response('debug.html',{'message':result})
    return render_to_response('error.html',{'message':result})
  else:
    url='/foaf/view/?url='+settings.FOAF_URI+request.user.username+'.rdf'
    return render_to_response('success.html',{'message':'Profil enregistré','url':url})
  
def import_foaf(request):
  if request.user.is_anonymous():
    return render_to_response('error.html',{'message':'Vous devez être connectés pour éditer votre profil'})
  if request.POST['url']=='':
    file=request.FILES['foaf_file']['content']
    result=update_foaf(request.user,file)
  else:
    result=update_foaf(request.user,request.POST['url'],from_url=True)
  if result==True:
    url='/foaf/view/?url='+settings.FOAF_URI+request.user.username+'.rdf'
    return render_to_response('success.html',{'message':'Profil mis à jour','url':url})
  else:
    return render_to_response('error.html',{'message':'Erreur: '+result})

