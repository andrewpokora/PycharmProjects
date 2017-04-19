# Script by Vladyslav Emelien
# coding: utf-8
import re
from tqdm import tqdm

def check(parts, option):
#    if parts.decode('utf-8') in strange:
#        return strange[parts.decode('utf-8')]
    check = False
    result = {}
    words = []
    parts = _trashRemove(parts.decode('utf-8'))
    for word in dictionary:
        word_formated = _trashRemove(word)
        for l in letters:
            word_formated = word_formated.replace(l, '')
        if option==True:
            if len(word_formated)==len(parts):
                result.update({word:1})
                words.append(word)
        else:
            resu = compare(word_formated, parts)
            if resu!=None:
                result.update({word:resu[word_formated]})
                words.append(word)
    if len(result)==1:
        return words[0]
    elif len(result)>1:
        if prePostCheck(words) != None:
            return prePostCheck(words)
        else:
            for ex in range(1,4):
                for dex in result:
                    if ex==result[dex]:
                        return dex

def prePostCheck(words):
    pt = []
    results = {}
    for dex in range(i-3, i+4):
        for l in letters:
            pt.append(f_tab[dex].replace(l, ''))
    for word in words:
        for ind in dictionary[word]:
            wd = []
            for dex in range(ind-3, ind+4):
                for l in letters:
                    wd.append(f_txt[dex].replace(l, ''))
            for ex in range(7):
                wdpt = (wd[ex], pt[ex])
                wd[ex] = wdpt[0]
                pt[ex] = wdpt[1]
            cter = 0
            for ex in range(7):
                if wd[ex] in pt:
                    cter+=1
            results.update({cter:word})
    for dex in range(7,0,-1):
        for ex in results:
            if ex==dex: return results[ex]
    return None

def _trashRemove(word_raw):
    if type(word_raw)=='bytes':
        for l in trash:
            word_raw = word_raw.replace(bytes(l), b'')
        word_raw = word_raw.decode('utf-8')
    else:
        for l in trash:
            word_raw = word_raw.replace(l, '')
    return word_raw

def compare(word, parts):
    if parts==word:
        return {word:1}
    elif parts.lower()==word.lower():
        return {word:2}
    else: return None

def compiler(text):
    global source
    spaces = ''
    open('output.txt', 'w')
    output = open('output.txt', 'a+', encoding='utf-8')
    for i in text:
        spaces += i
    counter = 0
    source = list(source)
    bar = tqdm(total=len(source))
    spaces = _trashRemove(spaces)
    for i in range(len(source)):
        if re.match(re.compile(r'\s'), source[i])==None:
            if re.match(re.compile(r'\W'), source[i])==None:
                output.write(source[i])
                counter+=1
            else:
                if source[i].encode('utf-8') in splitter:
                    output.write(spaces[counter])
                    counter+=1
                else:
                    output.write(source[i])
        else:
            output.write(source[i])
        bar.update(i)
    output.close()

err_present = False
var_word_log = {}
try:
    word_log = open('word_log.txt', 'r', encoding='utf-8')
    wdlog_spltd = word_log.read().split('\n')
    if wdlog_spltd!='':
        for i in word_log.read().split('\n'):
            var_word_log.update({wdlog_spltd[0]:wdlog_spltd[1]})
except FileNotFoundError:
    pass
log = open('log.txt', 'a')
trash = (',', '.', '"', "'", '/', "\\", '(', ')', '!', '?', ':', ';', '[', ']', '{', '}')
pattern = re.compile(r'\s')
source = open(input('>> Input name of file to format: '), 'r', encoding='utf-8').read()
f_tab = re.sub(pattern, ' ', source).split(' ')
f_txt = re.sub(pattern, ' ', open('Tab.txt', 'r', encoding='iso-8859-16').read()).split(' ')
letters = ('Ä', 'É', 'Ö', 'Ü', 'ß', 'ä', 'é', 'ö', 'ü', 'À', 'Ó', '`', 'Ú', 'ő',
           'Â', 'Æ', 'Ç', 'È', 'Ê', 'Ë', 'Î', 'Ï', 'Ô', 'Í', '°', "'", 'ú', 'ę',
           'Ù', 'Û', 'à', 'â', 'æ', 'ç', 'è', 'ê', 'ë', 'Ì', 'Ű', '\x92',, 'Ł'
           'î', 'ï', 'ô', 'ù', 'û', 'á', 'Á', 'í', 'ì', 'ó', 'ű', 'ń', 'Ą', 'ą',
           'Š', 'š', 'Ș', 'Ź', 'ź', 'Ż', 'Č', 'ł', 'Ž', 'ž', 'č', 'ș', 'Œ', 'œ',
           'Ÿ', 'ż', 'Ă', 'Ć', 'Đ', 'Ń', 'Ś', 'Ę', 'Ț', 'ă', 'ć', 'đ', 'ń', 'ś', 'ț'
           )

dictionary = {}
splitter = [b'\xd0\xbf\xd1\x97\xd0\x85', b'\xef\xbf\xbd', b'\xc2\x92']
print('>> Creating dictionary...')
t = tqdm(total=len(f_txt))
for i in range(len(f_txt)):
    t.update()
    for n in letters:
        if n in f_txt[i]:
            if f_txt[i] not in dictionary:
                dictionary[f_txt[i]] = []
            dictionary[f_txt[i]].append(i)

t.close()
print('>> Correcting words...')
with tqdm(total=len(f_tab)) as bar:
    for i in range(len(f_tab)):
        spltd_parts = ''
        bar.update()
        parts = f_tab[i].encode('utf-8')
        to_split = False
        for split in splitter:
            if split in parts:
                spltd_parts = parts.replace(split, b'')
                to_split = True
        if to_split == False:
            continue
        if len(spltd_parts)<=0:
            word = check(spltd_parts, True)
        else:
            word = check(spltd_parts, False)
        wrd = spltd_parts.decode('utf-8')
        if word != None:
            f_tab[i] = word
        else:
            err_present = True
            f_tab[i] = spltd_parts.decode('utf-8')
            log.write('>->->Failed with word '+f_tab[i]+'\n')
        if _trashRemove(wrd) not in var_word_log:
            var_word_log.update({_trashRemove(wrd):_trashRemove(f_tab[i])})
open('word_log.txt', 'w', encoding='utf-8')
word_log = open('word_log.txt', 'a', encoding='utf-8')
for i in var_word_log:
    word_log.write(i+' '+var_word_log[i]+'\n')
log.close()
bar.close()
if err_present == True:
    print('>> Some errors with correcting words occured. See log.txt for details.')
print('>> Writing to file...')
compiler(f_tab)
print('>> Done.')
