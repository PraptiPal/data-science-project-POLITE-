import nltk
#nltk.download('all')
from nltk.corpus import stopwords
from nltk.stem import SnowballStemmer, WordNetLemmatizer
from nltk.tokenize import RegexpTokenizer
import tokenize

def cleanTweets():

    stop_words = stopwords.words("english")
    stemmer = SnowballStemmer("english", ignore_stopwords=True)
    lemmatizer = WordNetLemmatizer()
    text = 'i love to Binge WATCh all Seasons of The-Peaky-Blinders and it is absloute # @ fun'
    token_text = tokenize.generate_tokens(text)
    words = [lemmatizer.lemmatize(w) for w in token_text if w not in stop_words]
    stem_text= " ".join([stemmer.stem(i) for i in words])
    print(stem_text)

cleanTweets()