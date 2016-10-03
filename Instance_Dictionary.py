import xml.etree.ElementTree as ET
import requests, os, sys, re, bs4, winsound

wavFileName = "" 
def Begins():                                                         # begins application...
    while(True):
        global wavFileName
        word = input()
        st = str.split(word)
        if(len(st)==1):
            if(st[0]=='p'):
                Play(wavFileName)
            else: print("Invalid Format")
        else:
            if(len(st)==2):
                if(st[0]=='m'): Start(st[1])
                else: print("Invalid Format")
            else: print("Invalid Format")
       
def Play(filename):                           # playing sound
    winsound.PlaySound(os.path.join('Data', filename), winsound.SND_FILENAME)

def MakeDir():
    try:
        os.makedirs('Data', exist_ok=True)
    except Exception as e:
        print(e)

def Check(Filename):
    Path = os.path.join('Data', Filename)
    if(os.path.exists(Path)):return True
    else:return False
    
def WordOfTheDay():                                                         # word of the day
    word =""
    try:
        res = requests.get('http://www.merriam-webster.com/word-of-the-day')
        soup = bs4.BeautifulSoup(res.text, 'html.parser')
        element = soup.select('div .word-and-pronunciation > h1')
        word = element[0].text
    except Exception as e:
        print(e)
    return word

def GetUrl(wavFileName):
    url = 'http://media.merriam-webster.com/soundc11/'
    subdir = wavFileName[:1]
    if(re.search(r'^bix', wavFileName)):
        subdir = "bix"
    if(re.search(r'^gg', wavFileName)):
        subdir = "gg"
    if(re.search(r'^[0-9]', wavFileName)):
        subdir = "number"
    subdir = subdir+'/'+wavFileName
    url = url+subdir
    return url

def Download(Url, FileName):
    try:
        res = requests.get(Url)
        res.raise_for_status()
        Path = os.path.join('Data', FileName)
        File = open(Path, 'wb')
        for chunk in res.iter_content(10000):
            File.write(chunk)
        File.close()
    except Exception as e:
        print(e)

def Start(word):
    global wavFileName
    if(word==""): return 0
    url = 'http://www.dictionaryapi.com/api/v1/references/collegiate/xml/%s?key=bc5c6b2a-81d7-4e22-9c85-e29986622728' %word
    try:
        filename = word+'.xml'
        if(Check(filename)==False):
            Download(url, filename)                                              #downloading file
        try:
            tree = ET.parse(os.path.join('Data', filename))                      #parsing XML
            root = tree.getroot()
        except Exception as e:
            print(e)
            return 0
        entry = root[0];
        if(entry.tag == "suggestion"):
            suggestions = root.findall('suggestion')
            print("suggestions :")
            for suggestion in suggestions:
               print(suggestion.text)
        else:
            sound = entry.find('sound')
            wav = sound.find('wav')
            wavFileName = wav.text
            if(Check(wavFileName)==False):
                wavFileUrl = GetUrl(wavFileName)
                Download(wavFileUrl, wavFileName)                                  #downloading file
            definition = entry.find('def')
            data = definition.findall('dt')
            for d in data:
                print(''.join(d.itertext()))
                print()
    
    except Exception as e:
        print(e)
        return 0
    return 1
if __name__=='__main__':
    print()
    print('Instance Dictionary                                 @copyright shishir singhal')
    print('------------------------------------------------------------------------------')
    print('Important Notes:    press p for pronunciation, m[space][word] for word meaning')
    print('-------------------------------Begin your search------------------------------')
    print()
    MakeDir()
    word = WordOfTheDay()
    if(word==""):
        print("could not find word of the day")
    else:
        print('word of the day : %s' %word)
        if(Start(word)==0): print("could not find word")
    Begins()
    