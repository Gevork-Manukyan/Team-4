import stanfordnlp

nlp = stanfordnlp.Pipeline(processors='tokenize,mwt,pos,lemma,depparse', treebank='en_ewt', use_gpu=False, pos_batch_size=3000) 

def parse(text):
  doc = nlp(text)
  for sentence in doc.sentences:
    translation = translate(sentence)
    result = []
    for word in translation[0]:
      result.append(word['text'].lower())
  return result

def getLemmaSequence(meta):
  tone = ""
  translation = []
  for word in meta:
    if (word['text'].lower(), word['lemma'].lower()) not in (('is', 'be'), ('the', 'the'), ('of', 'the'), ('is', 'are'), ('by', 'by'), (',', ','), (';', ';'), (':'), (':')):
      
      if word['upos'] == 'PUNCT':
        if word['lemma'] == "?":
          tone = "?"
        elif word['lemma'] == "!":
          tone = "!"
        else:
          tone = ""
        continue
      
      elif word['upos'] == 'SYM' or word['upos'] == 'X':
        continue
      
      if word['upos'] == 'PART':
        continue

      elif word['upos'] == 'PROPN':
        fingerSpell = []
        for letter in word['text'].lower():
          print(letter)
          spell = {}
          spell['text'] = letter
          spell['lemma'] = letter
        
          fingerSpell.append(spell)
        print(fingerSpell)
        translation.extend(fingerSpell)
        print(translation)

      elif word['upos'] == 'NUM':
        fingerSpell = []
        for letter in word['text'].lower():
          spell = {}
          pass
          fingerSpell.append(spell)

      elif word['upos'] == 'CCONJ':
        translation.append(word)
      
      elif word['upos'] == 'SCONJ':
        if (word['text'].lower(), word['lemma'].lower() not in (('that', 'that'))):
          translation.append(word)
      
      elif word['upos'] == 'INTJ':
        translation.append(word)

      elif word['upos']=='ADP':
        pass

      elif word['upos']=='DET':
        pass

      elif word['upos']=='ADJ':
        translation.append(word)

      elif word['upos'] == 'PRON' and word['dependency_relation'] not in ('nsubj'):
        translation.append(word)

      elif word['upos'] == 'NOUN':
        translation.append(word)

      elif word['upos']=='ADV':
        translation.append(word)
      
      elif word['upos']=='AUX':
        pass

      elif word['upos']=='VERB':
        translation.append(word)


  return (translation, tone)
def getMeta(sentence):
  englishStruct = {}

  aslStruct = {
    'rootElements':[],
    'UPOS': {
      'ADJ':[], 'ADP':[], 'ADV':[], 'AUX':[], 'CCONJ':[], 'DET':[], 'INTJ':[], 'NOUN':[], 'NUM':[], 'PART':[], 'PRON':[], 'PROPN':[], 'PUNCT':[], 'SCONJ':[], 'SYM':[], 'VERB':[], 'X':[]
    }
  }

  reordered = []
  words = []
  for token in sentence.tokens:
    for word in token.words:
      print(word.index, word.governor, word.text, word.lemma, word.upos, word.dependency_relation) 
      j = len(words)
      for i, w in enumerate(words):
        if word.governor <= w['governor']:
          continue
        else:
          j = i
          break
     
      words.insert(j, wordToDictionary(word))

  reordered = words
  return reordered

def wordToDictionary(word):
  dictionary = {
    'index': word.index,
    'governor': word.governor,
    'text': word.text.lower(),
    'lemma': word.lemma.lower(),
    'upos': word.upos,
    'xpos': word.xpos,
    'dependency_relation': word.dependency_relation,
    'feats': word.dependency_relation,
    'children': []
  }
  return dictionary

def translate(parse):
  meta = getMeta(parse)
  translation = getLemmaSequence(meta)
  return translation

