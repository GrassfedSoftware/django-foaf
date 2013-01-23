import os
import urllib
try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO
from rdflib.Graph import Graph
from rdflib import URIRef, Literal, BNode, Namespace, ConjunctiveGraph
from rdflib import RDF
from rdfalchemy import rdfObject
from rdfalchemy.orm import mapper
from django.conf import settings
from django_foaf.rdf_models import *

FOAF=Namespace("http://xmlns.com/foaf/0.1/" )
RDFS=Namespace("http://www.w3.org/2000/01/rdf-schema#")
REL=Namespace("http://purl.org/vocab/relationship/")

#~ ---------------- foaf controlers ---------------------
def has_foaf(user):
  filepath=settings.FOAF_DATA+user.username+'.rdf'
  if os.path.isfile(filepath):
    return settings.FOAF_URI+user.username+'.rdf'
  else:
    return False

def update_foaf(user,file,from_url=False):
  error=None
  #~ 1. verify if it is a rdf file
  if from_url:
    try:
      initiate(file)
    except:
      error="Le fichier rdf n'a pas l'air valide"
  else:
    try:
      initiate_from_file(file)
    except:
      error="Le fichier rdf n'a pas l'air valide"
  if error:
    return error
  #~ 2. verify if the file contains foaf data
  persons=list(Person.ClassInstances())
  if persons==[]:
    error='Ce fichier n\'a pas l\'air d\'un fichier foaf valide!'
  #~ 3. save file
  path=settings.FOAF_DATA+user.username+'.rdf'
  if from_url:
    urllib.urlretrieve(file,path)
  else:
    local_file=open(path,'w')
    local_file.write(file)
    local_file.close()
  if error:
    return error
  else:
    return True

def save_foaf_file(request):
  error=None
  #~ package identity data
  identity_props=request.POST['identity_data'].split('#$||$#')
  identity_data={}
  for prop in identity_props:
    propset=prop.split('#>>#')
    identity_data[propset[0]]=propset[1]
  #~ can't get rdflib to work for generating foaf file: help needed here!
  """
  store=Graph()
  store.bind("dc", "http://http://purl.org/dc/elements/1.1/")
  store.bind("foaf", "http://xmlns.com/foaf/0.1/")
  store.bind("rel", "http://purl.org/vocab/relationship/")
  #~ add nodes
  person=URIRef(settings.FOAF_URI+request.user.username+'.rdf')
  #~ identity nodes
  store.add((person,RDF.type,FOAF["Person"]))
  store.add((person,FOAF["name"],Literal(identity_data['name'])))
  store.add((person,FOAF["firstName"],Literal(identity_data['firstName'])))
  store.add((person,FOAF["family_name"],Literal(identity_data['family_name'])))
  store.add((person,FOAF["nick"],Literal(identity_data['nickname'])))
  store.add((person,FOAF["surname"],Literal(identity_data['surname'])))
  store.add((person,FOAF["givenname"],Literal(identity_data['givenname'])))
  store.add((person,FOAF["homepage"],Literal(identity_data['homepage'])))
  store.add((person,FOAF["weblog"],Literal(identity_data['weblog'])))
  store.add((person,FOAF["workplaceHomepage"],Literal(identity_data['workplaceHomepage'])))
  store.add((person,FOAF["workInfoHomepage"],Literal(identity_data['workInfoHomepage'])))
  store.add((person,FOAF["schoolHomepage"],Literal(identity_data['schoolHomepage'])))
  #~ relations nodes
  #for uri in data.getlist('friend_of'):
  #  store.add((person,rdf.type,REL['friendOf']))
  #  store.add((person,FOAF["name"],Literal(identity_data['name'])))
  out=store.serialize(format="xml", max_depth=3)
  error=str(out)
  """
  #~ temporary dirty solution: generate at hand
  out=[]
  out.append("""<?xml version="1.0" encoding="UTF-8"?>
<rdf:RDF
      xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"
      xmlns:rdfs="http://www.w3.org/2000/01/rdf-schema#"
      xmlns:foaf="http://xmlns.com/foaf/0.1/"
      xmlns:doap="http://usefulinc.com/ns/doap#"
      xmlns:dc="http://purl.org/dc/elements/1.1/"
      xmlns:rel="http://purl.org/vocab/relationship/">""")
  out.append('<foaf:PersonalProfileDocument rdf:about="'+settings.FOAF_URI+request.user.username+'.rdf">')
  out.append('  <foaf:maker rdf:resource="#me"/>')
  out.append('  <foaf:primaryTopic rdf:resource="#me"/>')
  out.append('</foaf:PersonalProfileDocument>')
  out.append('<foaf:Person rdf:ID="me">')
  #~ identity
  out.append('  <foaf:name>'+identity_data['name']+'</foaf:name>')
  if identity_data['firstName']:
    out.append('  <foaf:firstName>'+identity_data['firstName']+'</foaf:firstName>')
  if identity_data['family_name']:
    out.append('  <foaf:family_name>'+identity_data['family_name']+'</foaf:family_name>')
  if identity_data['given_name']:
    out.append('  <foaf:givenname>'+identity_data['given_name']+'</foaf:givenname>')
  if identity_data['surname']:
    out.append('  <foaf:surname>'+identity_data['surname']+'</foaf:surname>')
  if identity_data['nickname']:
    out.append('  <foaf:nick>'+identity_data['nickname']+'</foaf:nick>')
  if identity_data['homepage']:
    out.append('  <foaf:homepage rdf:resource="'+identity_data['homepage']+'" />')
  if identity_data['weblog']:
    out.append('  <foaf:weblog rdf:resource="'+identity_data['weblog']+' "/>')
  if identity_data['workplaceHomepage']:
    out.append('  <foaf:workplaceHomepage rdf:resource="'+identity_data['workplaceHomepage']+'" />')
  if identity_data['workInfoHomepage']:
    out.append('  <foaf:workInfoHomepage rdf:resource="'+identity_data['workInfoHomepage']+'" />')
  if identity_data['schoolHomepage']:
    out.append('  <foaf:schoolHomepage rdf:resource="'+identity_data['schoolHomepage']+'" />>')
  #~ relations
  friends=request.POST.getlist('friendOf')
  i=1
  while i<6:
    if request.POST['friendOf_url'+str(i)]:
      friends.append(request.POST['friendOf_url'+str(i)])
    i=i+1
  for friend in friends:
    out.append('  <rel:friendOf>')
    out.append('    <foaf:Person>')
    out.append('      <foaf:name>'+friend+'</foaf:name>')
    out.append('      <rdfs:seeAlso rdf:resource="'+friend+'" />')
    out.append('    </foaf:Person>')
    out.append('  </rel:friendOf>')
  knowsByReputation=request.POST.getlist('knowsByReputation')
  i=1
  while i<6:
    if request.POST['knowsByReputation_url'+str(i)]:
      knowsByReputation.append(request.POST['knowsByReputation_url'+str(i)])
    i=i+1
  for person in knowsByReputation:
    out.append('  <rel:knowsByReputation>')
    out.append('    <foaf:Person>')
    out.append('      <foaf:name>'+person+'</foaf:name>')
    out.append('      <rdfs:seeAlso rdf:resource="'+person+'" />')
    out.append('    </foaf:Person>')
    out.append('  </rel:knowsByReputation>')
  worksWith=request.POST.getlist('worksWith')
  i=1
  while i<6:
    if request.POST['worksWith_url'+str(i)]:
      worksWith.append(request.POST['worksWith_url'+str(i)])
    i=i+1
  for person in worksWith:
    out.append('  <rel:worksWith>')
    out.append('    <foaf:Person>')
    out.append('      <foaf:name>'+person+'</foaf:name>')
    out.append('      <rdfs:seeAlso rdf:resource="'+person+'" />')
    out.append('    </foaf:Person>')
    out.append('  </rel:worksWith>')
  hasMet=request.POST.getlist('hasMet')
  i=1
  while i<6:
    if request.POST['hasMet_url'+str(i)]:
      hasMet.append(request.POST['hasMet_url'+str(i)])
    i=i+1
  for person in hasMet:
    out.append('  <rel:hasMet>')
    out.append('    <foaf:Person>')
    out.append('      <foaf:name>'+person+'</foaf:name>')
    out.append('      <rdfs:seeAlso rdf:resource="'+person+'" />')
    out.append('    </foaf:Person>')
    out.append('  </rel:hasMet>')
  wouldLikeToKnow=request.POST.getlist('wouldLikeToKnow')
  i=1
  while i<6:
    if request.POST['wouldLikeToKnow_url'+str(i)]:
      wouldLikeToKnow.append(request.POST['wouldLikeToKnow_url'+str(i)])
    i=i+1
  for person in wouldLikeToKnow:
    out.append('  <rel:wouldLikeToKnow>')
    out.append('    <foaf:Person>')
    out.append('      <foaf:name>'+person+'</foaf:name>')
    out.append('      <rdfs:seeAlso rdf:resource="'+person+'" />')
    out.append('    </foaf:Person>')
    out.append('  </rel:wouldLikeToKnow>')
  out.append('</foaf:Person>')
  out.append('</rdf:RDF>')
  #error=('\n'.join(out))
  #~ save file
  file='\n'.join(out)
  path=settings.FOAF_DATA+request.user.username+'.rdf'
  local_file=open(path,'w')
  local_file.write(file)
  local_file.close()
  if error:
    return error
  else:
    return True

#~ --------------- data packaging utilities -------------
def add_uris(persons):
  for person in persons:
    try:
      person.foaf_file=str(person.seeAlso.resUri).replace('file://'+settings.FOAF_DATA,'').strip()
    except:
      person.foaf_file=''
  return persons

def get_relations(persons):
  main_person=None
  relations={}
  mapper()
  #~ check if there is only one person if the file
  if len(persons)==1:
    return (persons[0],relations)
  for person in persons:
    #~ check for main person
    if person.knows or person.hasMet or person.knowsByReputation or person.friendOf:
      main_person=person  
    #~ check for relations
    if person.knows:
      relations['knows']=person.knows
      add_uris(relations['knows'])
    if person.hasMet:
      relations['hasMet']=person.hasMet
      add_uris(relations['hasMet'])
    if person.knowsByReputation:
      relations['knowsByReputation']=person.knowsByReputation
      add_uris(relations['knowsByReputation'])
    if person.friendOf:
      relations['friendOf']=person.friendOf
      add_uris(relations['friendOf'])
    if person.worksWith:
      relations['worksWith']=person.worksWith
      add_uris(relations['worksWith'])
    if person.wouldLikeToKnow:
      relations['wouldLikeToKnow']=person.wouldLikeToKnow
      add_uris(relations['wouldLikeToKnow'])
  return (main_person,relations)

#~ ------------------- foaf parser -------------------
def parse_foaf(filepath):
  foaf_data={}
  #~ control the availability of the file
  if filepath=='':
    foaf_data['error']='Fichier indisponible'
    return foaf_data
  file=urllib.urlopen(filepath)
  num_lines=len(file.readlines())
  file.close()
  #~ control the size of the file
  if num_lines>settings.FOAF_MAX_LINES:
    foaf_data['error']='Fichier trop volumineux'
    return foaf_data
  #~ control if file is in rdf format
  try:
    initiate(filepath)
  except:
    foaf_data['error']="Le fichier rdf "+filepath+" n'a pas l'air valide"
    return foaf_data
  #~ parse foaf file
  persons=list(Person.ClassInstances())
  #~ find main person and relations
  foaf_data['main_person'],foaf_data['relations']=get_relations(persons)
  foaf_data['main_person'].foaf_file=filepath

  #foaf_data['error']=str('Err: '+str(foaf_data['relations']))
  return foaf_data
  
#~ ----------- rdf controlers ------------
def initiate(url):
  rdfObject.db = ConjunctiveGraph()
  rdfObject.db.load(url, format='xml')
  return

def initiate_from_file(file):
  rdfObject.db=ConjunctiveGraph()
  rdfObject.db.load(StringIO(file))
  return
