import sys
import ptranslator
import re

desc = """
Name: ui-translator
Creator: Bogdan Caleta Ivkovic
Usage:    uitranslate fileName.ui to_language from_language

from_language and to_language are optional
to_language default is English

filenameTranslated.ui will be created after the command is run
"""

def main():
    #args
    args = sys.argv
    if len(args) > 4 or len(args)<2:
        print(desc)
        return 0
    with open(args[1], 'r') as f:
        file = f.read()
    to_lang, from_lang="auto", "auto"
    if len(args)>2: to_lang = args[2]
    if len(args)>3: from_lang = args[3]
    
    #finding and translating strings in .ui file
    reg = re.findall(r'<string>(.*?)</string>', file)
    wordsZip = zip([i for i in reg if '@' not in i], [ptranslator.translate(i, to_lang, from_lang) for i in reg if '@' not in i]) #wordsZip[x][0] = original text and wordsZip[x][1] = translated text
    
    #replacing words with their translations
    for i in wordsZip:
        print("replacing {} with {}".format(i[0], i[1]))
        file = file.replace(i[0], i[1])

    #creating a translated copy of original file
    with open(args[1].replace('.ui', '')+'Translated.ui', 'w', encoding='utf-8') as f:
        f.write(file)

if __name__ == '__main__':
    main()