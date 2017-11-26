#! /usr/bin/env python
# -*- coding: utf-8 -*-

import urllib2, ntpath, re
import sys
import json
import subprocess
import scholar

journal_database = {
                        
                    'Accounts of Chemical Research' : ['Acc.Chem.Res'],
                    'ACS Nano' : ['ACSNano'],
                    'Annual Review of Biophysics and Biomolecular Structure' : ['Annu.Rev.Biophys.Biomol.Struct.'],
                    'Angewandte Chemie' : [ 'Angew.Chem.Int.Edit.'],
                    'ArXiV' : ['arXiv'],
                    'Biophysical Journal' : ['Biophys.J.'],
                    'Biopolymers' : ['Biopolymers'],
                    'Faraday Discussions' : ['FaradayDiscuss'],
                    'Interdisciplinary Reviews: Computational Molecular Science' : ['Interdisc.Rev.Comput.Mol.Sc.'],
                    'Journal of Chemical Theory and Computation': ['J.Chem.TheoryComput.'],
                    'Journal of Molecular Biology' : ['J.Mol.Biol.'],
                    'Journal of the American Chemical Society' : ['J.Am.Chem.Soc.'],
                    'Journal of Computational Chemistry' : ['J.Comput.Chem.'],
                    'Journal of Physical Chemistry B' : ['J.Phys.Chem.B'],
                    'Journal of Physical Chemistry' : ['J.Phys.Chem.'],
                    'Journal of Physics: Condensed Matter' : ['J.Phys.:Condens.Matter','JournalofPhysics:CondensedMatter'],
                    'The Journal of Chemical Physics' : ['J.Chem.Phys.'],
                    'Langmuir' : ['Langmuir'],
                    'Methods' : ['Methods'],
                    'Nano Letters' : ['NanoLett.'],
                    'Natural Computing' : ['NaturalComputing'],
                    'Nature' : ['Nature'],
                    'Nature Communications' : ['Nat.Comm.'],
                    'Nature Nanotechnology' : ['Nat.Nano'],
                    'Nucleic Acids Research' : ['NucleicAcidRes','NucleicAcidsRes.'],
                    'Physical Chemistry and Chemical Physics': ['Phys.Chem.Chem.Phys.'],
                    'Physical Review Letters' : ['Phys.Rev.Lett.'],
                    'Polymers' : ['Polymers'],
                    'Proceedings of the national academy of sciences' : ['Proc.Nat.Acad.Sci.','Proc.Natl.Acad.Sci.USA'],
                    'Science' : ['Science'],
                    'Scientific Reports' : ['Sci.Rep'],
                    'Soft Matter' : ['SoftMatter'],
                    'WIREs Computational Molecular Science ' : ['WIREsComput.Mol.Sci']}
class Ref:
    '''
    A reference, with the journal (plus pages/volumes etc.), authors, year.
    '''
    def __init__(self, i_string):
        self.string = str(i_string)
        inner_string = str(self.string)
        year = re.search('\(.*(\d\d\d\d)\).', inner_string)
        if year:
            self.year = year.group(1)
            inner_string = re.sub('\('+self.year+'\)\.','', inner_string)
        else:
            print "Warning: don't know the year in string",inner_string
            self.year = None
        self.journal = Ref.get_journal(inner_string)
        self.set_authors_ids(inner_string)
        self.num_citations = None
        self.excerpt = None
        self.url = None
    @staticmethod
    def get_journal(inner_string):
        for j in journal_database:
            for jj in journal_database[j]:
                if jj in inner_string.replace(' ',''):
                    return j
        print "Warning: don't know the journal in string",inner_string
        return None
    def set_authors_ids(self,inner_string):
        self.ids = []
        inner_string = inner_string.replace(r'\ufb00','ff')
        inner_string = inner_string.replace(r'\ufb01','fi')
        inner_string = inner_string.replace(r'\u02c7','')
        inner_string = inner_string.replace(r'(cid:32)','')
        inner_string = inner_string.replace(r'¨','')

        authors = str(inner_string)
        if 'and' in authors:
#            print 'starting with',authors
            authors = [a.strip() for a in inner_string.split('and')]
#            print 'now have',authors
            other_things = [a.strip() for a in authors[-1].split(',')[1:]]
            authors = [a.strip() for a in authors[0].split(',')] + [authors[-1].split(',')[0].strip()]
            if '' in authors: authors.remove('')
#            print 'and finally',authors
        else:
            other_things = inner_string.split(',')
            other_things = [ b.strip() for b in other_things]
            authors = [other_things.pop(0)]
        for b in other_things:
            if b.isdigit(): self.ids += [b]
        self.authors = authors
#        print authors
    def get_info_from_scholar(self,querier):
        '''
        Set all the nice goodies from google scholar
        '''
        query = scholar.SearchScholarQuery()
        author_string = ' '.join([a.split(' ')[-1] for a in self.authors])
        query.set_author(author_string)
        query.set_timeframe(self.year, self.year)
        query.set_pub(self.journal)
        
        try:
            querier.send_query(query)
        except:
            print 'problem with',self.string
            raise
        articles = querier.articles
        if len(articles) == 0:
            print 'warning: article from string',self.string,'not found on google scholar'
            print self.journal
            print self.year
            print author_string
            return -1
        if len(articles) > 1:
            print 'warning: several articles from string',self.string,'found on google scholar'
            return -2
        self.num_citations = articles[0]['num_citations']
        self.url = articles[0]['url']
        self.excerpt = articles[0]['excerpt']





def get_pdf_from_url(url):
    download_file( url)

def download_file(download_url):
    response = urllib2.urlopen(download_url)
    file = open(ntpath.basename(download_url), 'wb')
    file.write(response.read())
    file.close()
    if verbose: print "pdf downloaded"

def extract_references(paper_txt):
    '''
    Extract the references from the paper text file.
    '''
    in_bib = False
    curr_ref_id = 1
    refs = {}
    i = -1
    with open(paper_txt, 'r') as f:
        for line in f.readlines():
            if 'REFERENCES' in line: in_bib = True
            elif not in_bib: continue
            if 'Appendix' in line: break
            m = re.search('^(\d+)[A-Z]\. ',line)
            if m:
                #if i >= 0: print i,refs[i]
                if i >= 0: refs[i] = Ref(refs[i])
                i = int(m.group(1))
                if i in refs.keys():
                    print 'conflict between line',line,' and previous entry',refs[i]
                else: refs[i] = re.sub('^'+str(i),'',line.rstrip())
            elif refs != {}:
                refs[i] += line.rstrip()

    return refs
                

'''
Citation project - given a pdf, look up the references and provide:
    1) link
    2) citations
    3) points at which it's cited
'''

if __name__ == '__main__':
    scholar.ScholarConf.COOKIE_JAR_FILE = 'cookie.blah'
    paper_id = '1504.00821'
    paper_pdf = paper_id+'.pdf'
    paper_txt = paper_id+'.txt'
    # fetch paper from the arxiv
    print 'getting item from the arxiv'
    #get_pdf_from_url('https://arxiv.org/pdf/'+ paper_pdf)
    # extract the text
    print 'extracting the text... (might take a while)'
    # pdfx paper_pdf -t > paper_txt
    #subprocess.call('pdfx '+paper_pdf+' -t > '+paper_txt,shell = True)
    # extract the references
    print 'extracting the references from the paper...'
    refs = extract_references(paper_txt)
    # for each reference, look it up on google scholar to get the citation
    print 'looking them up online...'
    querier = scholar.ScholarQuerier()
    settings = scholar.ScholarSettings()
    querier.apply_settings(settings)
    for i in refs.keys():
        refs[i].get_info_from_scholar(querier)
    # find where it's cited
    # pretty print it
    querier.save_cookies()


