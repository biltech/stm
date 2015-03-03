#!/usr/bin/env python

from bs4 import BeautifulSoup
import requests, urllib2, re
import itertools
import time
import nltk

def getSiteData(url):
    # return article related info from the souped site data
    extract = {}
    response = requests.get(url)
    extract['soup'] = BeautifulSoup(response.text, 'html.parser')
    extract['citations link'] = None
    try:
        extract['Article name'] = extract['soup'].find("meta", {"name" : "citation_title"})['content']
    except Exception as e:
        pass
    try: 
        extract['Authors'] = extract['soup'].find("meta", {"name" : "citation_authors"})['content']       
    except Exception as e:
        pass
    try: 
        extract['Journal Title'] = extract['soup'].find("meta", {"name" : "citation_journal_title"})['content']       
    except Exception as e:
        pass
    try: 
        extract['Keywords'] = extract['soup'].find("meta", {"name" : "citation_keywords"})['content']       
    except Exception as e:
        pass
    try: 
        extract['arXiv link'] = extract['soup'].findAll('a', href=re.compile('[&amp;]link_type=PREPRINT'))[0].get('href')       
    except Exception as e:
        pass
    try: 
        extract['citations link'] = extract['soup'].findAll('a', href=re.compile('[&amp;]link_type=CITATIONS'))[0].get('href')       
    except Exception as e:
        pass    
    return extract

def getTitle(url):
    # return title from the souped site data
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    title = str(soup.title.contents[0])
    return title

def getAbstract(url):
    # return abstract from the extracted site data
    extracted = getSiteData(url)
    return extracted['soup'].blockquote.contents[2]

def arXivAds(url):
    # use arXiv link to goto ads
    arXiv_id = url.split('abs/')[1]
    ads_search = requests.get('http://adsabs.harvard.edu/cgi-bin/basic_connect?qsearch=arxiv:' + arXiv_id)
    extract = BeautifulSoup(ads_search.text, 'html.parser')
    adslink = extract.findAll('a', href=re.compile('http://adsabs.harvard.edu/cgi-bin/nph-data_query?'))[0].get('href')
    return adslink

def get_tags(txt):
    # returns part of speech tags for input text
    tokens = nltk.word_tokenize(txt)
    return nltk.pos_tag(tokens)

def extract_entity_names(tagged):
    # returns named entity for input tagged text
    namedEnt = nltk.ne_chunk(tagged, binary = True)
    NE = []
    for c in namedEnt:
      if hasattr(c, 'label'):
        NE.append(' '.join(i[0] for i in c.leaves()))
    return NE

def entities(subs):
    Ent = [0]*len(subs);
    ### Get entity name from titles   
    for w in xrange(0, len(subs)):
        tgs = get_tags(str(subs[w]))
        # specific type
        Ent[w] = extract_entity_names(tgs)
    Ent = list(set([item for sublist in Ent for item in sublist])) 
    return Ent

def citeAuthors(url):
    # get names of last authors of papers citing the main 
    preprint = getSiteData(url)
    lastAuts = sub = titl = stitles = subtitles = []; autLink = None
    try:
        titl = preprint['Article name']
    except Exception as e:
        pass
    if preprint['citations link'] is not None:
        citeData = getSiteData(preprint['citations link']) # soup of the citations link page
        sublinks = citeData['soup'].findAll('a', href = re.compile('link_type=ABSTRACT')) # get links of individual citations
        sublink = [sublinks[w].get('href') for w in range(0, len(sublinks))] 
        sub = list(set(sublink)) # keeping only unique links to the citation pages
        citingAuthors = [''.join(node.findAll(text=True)) for node in citeData['soup'].findAll('td', align=re.compile('left'), valign=re.compile('top'), width=re.compile('25%'))]
        stitles = [''.join(node.findAll(text=True)) for node in citeData['soup'].findAll('td', align=re.compile('left'), valign=re.compile('top'), colspan=re.compile('3'))]
        lastAuts = [0]*len(citingAuthors)
        subtitles = [0]*len(citingAuthors)
        for w in xrange(0, len(citingAuthors)):
            try:
                lastAuts[w] = (citingAuthors[w].split(';')[-1]).encode('utf-8')  # to change values from unicode to string // .encode() is for special characters
                subtitles[w] = (stitles[w].split(';')[-1]).encode('utf-8')
            except Exception as e:
                print e
            pass

    return titl, lastAuts, subtitles, sub 

def auts1NL(url, threshold=0):
    if url is None:
        return None, None, None, None
    elif (re.search('Paper does not exist', getTitle(url))):
        return None, None, None, 'Paper does not exist : try another'
    else:        
        url = arXivAds(url)
        artName, autList, stitles, autLink  = citeAuthors(url)
        str_ar = []; Ent = []
        autitle = dict(zip(stitles, autList)) # author-title dict
        uniques = [autList.count(w) for w in set(autList)] # count num. of times unique author names appear
        uniq = dict(zip(set(autList), uniques)) # dict of unique authorname, no. of times it appears 
        uniq = dict((key,value) for key, value in uniq.iteritems() if value > threshold) # keeping only frequently occurring authornames
        uniq = dict((k, v) for k, v in autitle.items() if v in uniq.keys()) # dict of title-author with above filter
        ### Get entity name from titles   
        [Ent.append(w) for w in uniq.keys()]
        Ent = str(entities(Ent)).strip('[]')
        '''
        # Error handling : print to browser
        try:
            Ent = entities('Nonlinearity effects on the directed momentum current')
        except Exception as e:
            Ent = e
        pass
        '''

        no_cite = "<li> <span><i class='icon-leaf'></i> No citations! </span><a href=""></a> </li>"
        if len(autList):
            for k, item in enumerate(autList):
                if item is not None:
                    str_ar.append("<li> <span><i class='icon-leaf'></i> " + item + " </span><a href=""> " + stitles[k] + "</a> </li>") 
            return str(artName), str(len(str_ar)), "".join(str_ar), Ent
        else:
            return str(artName), str(len(str_ar)), no_cite, Ent

def auts2NL(url,threshold=0):
    if url is None:
        return None, None, None, None
    elif (re.search('Paper does not exist', getTitle(url))):
        return None, None, None, 'Paper does not exist : try another'
    else:  
        url = arXivAds(url)
        artName, autList, stitles, autLink = citeAuthors(url)
        str_ar = []; Ent = []
        no_cite = "<li> <span><i class='icon-leaf'></i> No citations! </span><a href=""></a> </li>"
        if len(autList):
            br = []
            br = [(citeAuthors(autLink[w])) for w in range(len(autLink))] # Level 2 citations
            alls = [br[w][1] for w in range(len(br))] # putting together all Level 2 author names
            alls = list(autList) + list(itertools.chain(*alls)) 
            allsubs = [br[w][2] for w in range(len(br))] # putting together all subtitle names
            allsubs = list(stitles) + list(itertools.chain(*allsubs)) # all titles together
            autitle = dict(zip(allsubs, alls)) # author-title dict
            
            uniques = [alls.count(w) for w in set(alls)] # count num. of times unique author names appear
            uniq = dict(zip(set(alls), uniques)) # dict of unique authorname, no. of times it appears 
            uniq = dict((key,value) for key, value in uniq.iteritems() if value > threshold) # keeping only frequently occurring authornames
            uniq = dict((k, v) for k, v in autitle.items() if v in uniq.keys()) # dict of title-author with above filter
            # finding entity names
            [Ent.append(w) for w in uniq.keys()]
            Ent = str(entities(Ent)).strip('[]')
            for k, item in enumerate(autList):
                sub_str = str()
                if item is not None:
                    for j, subitem in enumerate(br[k][1]):
                        if subitem is not None:
                            sub_str = sub_str + "<li> <span><i class='icon-leaf'></i> " + subitem + " </span><a href=""> " + br[k][2][j]+ " </a> </li>"
                    if len(br[k][1]):
                        sub_str = "<ul>" + sub_str + "</ul>"
                    str_ar.append("  <li> <span><i class='icon-leaf'></i> " + item + " </span><a href=""> " + stitles[k]+ " </a> "
                              + sub_str + "</li>" )
            return str(artName), str(len(str_ar)), "".join(str_ar), Ent
        else:
            return str(artName), str(len(str_ar)), no_cite, Ent


