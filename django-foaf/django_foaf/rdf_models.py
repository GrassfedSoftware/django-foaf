from rdfalchemy import rdfObject, rdflibSingle, rdflibMultiple
from rdflib import Namespace

FOAF=Namespace("http://xmlns.com/foaf/0.1/" )
RDFS=Namespace("http://www.w3.org/2000/01/rdf-schema#")
REL=Namespace("http://purl.org/vocab/relationship/")

class Agent(rdfObject):
  rdf_type=FOAF.Agent
  name=rdflibSingle(FOAF.name)
  mbox=rdflibSingle(FOAF.mbox)
  openid=rdflibSingle(FOAF.openid)
  weblog=rdflibSingle(FOAF.weblog)
  seeAlso=rdflibSingle(RDFS.seeAlso)

class Person(Agent):
  rdf_type=FOAF.Person
  nickname=rdflibSingle(FOAF.nick)
  firstName=rdflibSingle(FOAF.firstName)
  givenname=rdflibSingle(FOAF.givenname)
  surname=rdflibSingle(FOAF.surname)
  family_name=rdflibSingle(FOAF.family_name)
  knows=rdflibMultiple(FOAF.knows,range_type=FOAF.Person)
  homepage=rdflibSingle(FOAF.homepage)
  workplaceHomepage=rdflibSingle(FOAF.workplaceHomepage)
  workInfoHomepage=rdflibSingle(FOAF.workInfoHomepage)
  schoolHomepage=rdflibSingle(FOAF.schoolHomepage)
  interests=rdflibMultiple(FOAF.interest)
  depiction=rdflibSingle(FOAF.depiction)
  knowsByReputation=rdflibMultiple(REL.knowsByReputation,range_type=FOAF.Person)
  friendOf=rdflibMultiple(REL.friendOf,range_type=FOAF.Person)
  worksWith=rdflibMultiple(REL.worksWith,range_type=FOAF.Person)
  wouldLikeToKnow=rdflibMultiple(REL.wouldLikeToKnow,range_type=FOAF.Person)
  hasMet=rdflibMultiple(REL.hasMet,range_type=FOAF.Person)

class PersonalProfileDocument(rdfObject):
  rdf_type=FOAF.PersonalProfileDocument
  maker=rdflibSingle(FOAF.maker)
  primaryTopic=rdflibSingle(FOAF.primaryTopic)
