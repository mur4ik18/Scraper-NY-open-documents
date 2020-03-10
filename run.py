import requests
from bs4 import BeautifulSoup
from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH

GURL = "https://www.nysenate.gov/legislation/laws/CVP" 
Gshell = '#law-doc-wrapper > .c-law-link-container'

Gtitle = 'a'

firstPage_links = []
secondPage_links = []

contShell = '.node-statute'
Article = '.c-law--inactive-breadcrumb > span.crumb-label'
Articles = '.c-law--inactive-breadcrumb > span.crumb-body'

contTitle = '#doc-type'
contName = "#law-text-title"
contLoc = '#location-id'
contText = ".c-law-doc-text"



# docx document
document = Document()



def fistPage(url, shell, mtitle):
    r = requests.get(url)
    html = BeautifulSoup(r.content , 'html.parser')
    lisst = []
    for el in html.select(shell):
        title = el.select(mtitle)
        lisst.append('https://www.nysenate.gov' + title[0].get('href'))
    
    return lisst


# start page scrap and get links
firstPage_links = fistPage(GURL, Gshell, Gtitle)
#print(firstPage_links)

for i in range(0 , len(firstPage_links)-1):
    secondPage_links.append(fistPage(firstPage_links[i], Gshell, Gtitle))
    #print(secondPage_links[i])

def contentScrap(url,shell,mcontLoc, art, artTitle, contN, contT):
    r = requests.get(url)
    html = BeautifulSoup(r.content , 'html.parser')
    for el in html.select(shell):
        #article = el.select(art)
        articleTitle = el.select(artTitle)
        titlel = el.select(mcontLoc)

        name = el.select(contN)
        texts = el.select(contT)

        text2 = titlel[0].text
        text3 = name[0].text
        
       # print(article[-1].text)
        #print(articleTitle[-1].text)

        print(text2.replace(' ', '')+ ' Section')
        #print(text3.replace('  ', ''))

        #print(texts[0].text)
        
        #p = document.add_heading(article[-1].text, 1)
        #p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        #c =document.add_paragraph(articleTitle[-1].text)
        #c.alignment = WD_ALIGN_PARAGRAPH.CENTER
        d =document.add_heading(text2.replace(' ', '')+ ' Section', 2)
        d.alignment = WD_ALIGN_PARAGRAPH.CENTER
        t=document.add_heading(text3.replace('  ', ''),3)
        t.alignment = WD_ALIGN_PARAGRAPH.CENTER
        document.add_paragraph('')
        document.add_paragraph(texts[0].text)
        document.add_paragraph('')

'''
def Article(url, shell, mtitle):
    r = requests.get(url)
    print(url)
    html = BeautifulSoup(r.content , 'html.parser')
    for el in html.select(shell):
        title = el.select(mtitle)
        Name = title[0].text
        print(Name.replace(' ', ''))
        #print('Section')
        
'''
def fistPageTit(url, shell, mtitle):
    r = requests.get(url)
    html = BeautifulSoup(r.content , 'html.parser')
    lisst = []
    for el in html.select(shell):
        title = el.select(mtitle)
        lisst.append(title[0].text)
    
    return lisst





titleList = []
NameList = []
titleList = fistPageTit('https://www.nysenate.gov/legislation/laws/CVP','.c-law-link-container', Gtitle)
NameList = fistPageTit('https://www.nysenate.gov/legislation/laws/CVP','.c-law-link-title', 'a')


for i in range(0, len(secondPage_links)-1):
    print(titleList[i].replace('  ', ''))
    print(NameList[i].replace('  ', ''))
    p = document.add_heading(titleList[i].replace('  ', ''), 1)
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    c =document.add_paragraph(NameList[i].replace('  ', ''))
    c.alignment = WD_ALIGN_PARAGRAPH.CENTER
    for j in range(0, len(secondPage_links[i])-1):        
        contentScrap(secondPage_links[i][j], contShell , contLoc, Article, Articles, contName, contText)



document.save('test.docx')