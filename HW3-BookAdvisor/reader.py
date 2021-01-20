import requests
import json
import os
import sys

'''
creates an object-like dictionary which holds values predescribed in the assignment paper
 @params
 url: url of the book
 @return
 book: an object-like dictionary which holds the values predescribed in the assignment paper
'''

def getData(url : str): #
    book = {}           #initilization
    book["url"] = url
    data = ""
    while True:         #a while loop to ensure the data is retrieved from the url
        try:
                    
            webUrl = requests.get(url)
            
            
            data = webUrl.text
            break
        except requests.ConnectionError as exception:
            print(exception,"retry")

    start = data.find('<h1 id=\"bookTitle" class="gr-h1 gr-h1--serif" itemprop="name">') #finds the starting of the title
    end = data[start:].find('</h1>')    #find the ending of the title
    title = data[start+69:start+end-1]  #and get the title with the manually calculated offsets
    book["title"] = title
    print(title,"retrieved")
    #description
    descDiv = data.find('<div id="description" class="readable stacked" style="right:0">')  #starting of the description div Block
    descDivEnd = data[descDiv:].find('</div>') + descDiv  #ending of the description div block. it is to find out if the freetext I found is between these blocks, hence what I want.
    
    start = data.find('<span id="freeTextContainer')  #short description
    startForLong = data[start+1:].find('<span id="freeText') + start #long description
    desc = ""
    if startForLong < descDivEnd:   #if it is in the div block, take the long description
        startForLong = data[startForLong:].find('style="display:none">') + startForLong 
        end = data[startForLong:].find('</span>')
        desc = data[startForLong+21:startForLong+end]
    else:   #if it isn't, that means there is no long description, only one, so take that one.
        start = data[start:].find('">') + start
        end = data[start:].find('</span>')
        desc = data[start+2:start+end]
    book["desc"] = desc


# genres###############################################################################
    two = False
    book["genres"] = {}
    p1 = 0
    genresStart = data.find('<div class="bigBoxContent containerWithHeaderContent">') #find the genres block
    temp = genresStart
    i = 0
    lastElement = data[:].find('<div class="elementList elementListLast">') + genresStart #find the last element in the list of genres
    while True:
        elementStart = data[temp:].find('<div class="elementList ') + temp #find the starting of the element
        
        if elementStart == -1 or lastElement == elementStart :
            break
        leftStart = data[elementStart:].find('<div class="left">') + elementStart #find the genre's block
        genre = data[leftStart:].find('<a class="actionLinkLite bookPageGenreLink" href=') + leftStart #genre

        genreStart = data[genre:].find('>') + genre
        genreEnd = data[genreStart:].find('</a>') + genreStart
        if genre == leftStart-1:
            break
        
        
        
        
        rightStart = data[genreEnd:].find('<div class="right">') + genreEnd
        howmanyStart = data[rightStart:].find('<a title="') + rightStart + 10
        howmanyEnd = data[howmanyStart:].find(' people') + howmanyStart
        
        genre2 =  data[genreEnd:].find('<a class="actionLinkLite bookPageGenreLink" href=')  + genreEnd
        genre2End = genreEnd
        if genre2 < rightStart:
            genre2Start = data[genre2:].find('>') + genre2
            genre2End = data[genre2Start:].find('</a>') + genre2Start
            two = True
        
        
        
        genreText = data[genreStart+1:genreEnd]
        howMany = data[howmanyStart:howmanyEnd]
        if genre != leftStart-1: #if there is no genre it has to be handled
            if genreText in book["genres"]:    
                book["genres"][genreText] += howMany
            else:
                book["genres"][genreText] = howMany
            if two:
                genre2Text = data[genre2Start+1:genre2End]
                if genre2Text in book["genres"]:    
                    book["genres"][genre2Text] += howMany
                else:
                    book["genres"][genre2Text] = howMany
            
        temp = genre2End
        i+=1
        two = False
    leftStart = data[lastElement:].find('<div class="left">') + elementStart
    genre = data[leftStart:].find('<a class="actionLinkLite bookPageGenreLink" href=') + leftStart
    genreStart = data[genre:].find('>') + genre
    genreEnd = data[genreStart:].find('</a>') + genreStart
    rightStart = data[genreEnd:].find('<div class="right">') + genreEnd
    howmanyStart = data[rightStart:].find('<a title="') + rightStart + 10
    howmanyEnd = data[howmanyStart:].find(' people') + howmanyStart
    
    genreText = data[genreStart+1:genreEnd]
    howMany = data[howmanyStart:howmanyEnd]
    if genre != leftStart-1:#if there is no genre it has to be handled
        book["genres"][genreText] = howMany 
    
    
    #author##############################################################################
    
    authorStart = data.find('<span itemprop="name">') +22 
    authorEnd = data[authorStart:].find('</span>') + authorStart
    book["author"] = data[authorStart:authorEnd]
    
    #urls of the books#####################################################################
    stop = data.find('>See similar books')
    book["recomms"] = []
    temp =0
    while True:    
        urlCover = data[temp:].find("<li class='cover' id='bookCover_") + temp
    
        urlStart = data[urlCover:].find('<a href="https://www.goodreads.com') + urlCover
        urlEnd = data[urlStart:].find('"><img') + urlStart
        if urlCover == temp-1 or urlEnd <= urlStart-1 or urlStart <= urlCover-1 or urlCover > stop: 
            
            break
        # print(data[urlStart+9:urlEnd])
        book["recomms"].append(data[urlStart+9:urlEnd])
        temp = urlEnd
    return book

"""
if the given is not an url, it will delete booksOut.json which is the dictionary of the books, and tfidfs.json which holds
the tfidfs of the words. Which will initiliaze the sequence of the data retrival allover.
"""
if 'https://' not in sys.argv[1]:
    try:
        os.remove("booksOut.json")
        os.remove("tfidfs.json")
    except:
        pass
"""
starts the sequence of the data retrieval if there is no json file of the dictionary that holds the books.
"""
if not os.path.exists(os.path.join(os.getcwd(),'booksOut.json')):
    f = open(sys.argv[1],'r')
    urls = f.read()
    f.close()
    urls = urls.split('\n')
    books = {}
    for url in urls:
        
        books[url] = getData(url)
        if books[url]["recomms"] == []:
            del books[url]
    out = open("booksOut.json",'w')
    out.write(json.dumps(books))
    out.close()

# start = data[p1+102:].find(">")
# end = data[p1:].find("</a>")
# print(data[p1:p1+100])
