import numpy as np
import nltk
import string
import random

f=open('chatbot.txt', 'r', errors='ignore')
raw_doc=f.read()
raw_doc=raw_doc.lower() #converts text to lowercase
nltk.download('punkt') #using the punkt tokenizer
nltk.download('wordnet') #using the wordnet dictionary
sent_tokens = nltk.sent_tokenize(raw_doc) #converts doc to list of sentences
word_tokens = nltk.word_tokenize(raw_doc) #converts doc to list of wc


#Text preprocessing
lemmer = nltk.stem.WordNetLemmatizer()
def LemTokens(tokens):
    return [lemmer.lemmatize(token) for token in tokens]
remove_punct_dict = dict((ord(punct), None) for punct in string.punctuation)
def LemNormalize(text):
    return LemTokens(nltk.word_tokenize(text.lower().translate(remove_punct_dict)))


#Greeting function

GREET_INPUTS = ("hello", "hi", "greetings", "sup", "what's up", "hey",)
GREET_RESPONSES = ["hello", "hi", "hey", "nods", "hi there", "I am glad! Yu are talking to me"]
def greet(sentence):
    
    for word in sentence.split():
        if word.lower().strip(string.punctuation) in GREET_INPUTS:
            return random.choice(GREET_RESPONSES)

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def response(user_response):
    robo1_response = ''
    TfidfVec = TfidfVectorizer(tokenizer=LemNormalize, stop_words='english')
    tfidf = TfidfVec.fit_transform(sent_tokens)
    vals = cosine_similarity(tfidf[-1], tfidf[:-1]) #compare user input with existing document
    idx=vals.argsort()[0][-2] #get the most similar sentence
    flat = vals.flatten()
    flat.sort()
    req_tfidf = flat[-2]
    if (req_tfidf==0):
        robo1_response=robo1_response + "I am sorry! I don't understand you"
        return robo1_response
    else:
        robo1_response = robo1_response + sent_tokens[idx]
        return robo1_response
    

#defining conversation start/end ptotocols

flag=True
print("BOT: My name is Machara. Let's have a conversation! Also, if you want to exit any time, just type Bye!")
while(flag==True):
    user_response = input()
    user_response=user_response.lower()
    if user_response !='bye':
        if user_response in ('thanks', 'thank you'):
            flag=False
            print("BOT: You are welcome..")
        else:
            if greet(user_response) !=None:
                print("BOT: ", greet(user_response))
            else:
                sent_tokens.append(user_response)
                word_tokens=word_tokens+nltk.word_tokenize(user_response)
                final_words=list(set(word_tokens))
                print("BOT: ", end='')
                print(response(user_response))
                sent_tokens.remove(user_response)
    else:
        flag=False
        print("BOT: Goodbye! Take care <3")