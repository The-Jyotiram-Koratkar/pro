#!/usr/bin/env python
#Suhas Pote

# Imports
import pandas as pd
import glob
import os
# -----------------------------------------------------------------------------


# Add your imports here


# Step 1: Reading in the data
# -----------------------------------------------------------------------------


def readMessagesFromFile(fPath, colNames, **kwargs):
    """Reads a file with messages and corresponding sentiments and
    returns a pandas DataFrame.

    fPath    : Path to the file to read messages from.
    colNames : Column names for the returned DataFrame.
    Returns  : Pandas DataFrame containing messages and sentiments
               as columns.

    Sample Output:
                                                 message  sentiment
    0                           Wow... Loved this place.          1
    1  I learned that if an electric slicer is used t...        NaN
    2                   But they don't clean the chiles?        NaN
    3                                 Crust is not good.          0
    4          Not tasty and the texture was just nasty.          0

    """
    df = pd.read_csv(fPath,names=colNames,header=None,sep='\t')
    
    return df

readMessagesFromFile('C:/Users/Suhas/Downloads/recruitment-task/data/amazon_cells_labelled.txt',['message','sentiment'])


def findFilesInDir(dirPath, pattern):
    """Finds the list of filenames in `dirPath` that match `pattern`.

    dirPath : Path to the directory to find files in.
    pattern : A glob pattern to match filenames against.
    Returns : List of filenames in `dirPath` that match `pattern`.
    """
    text_files = [f for f in os.listdir(dirPath) if f.endswith(pattern)]
	
    return text_files

findFilesInDir('C:\\Users\\Suhas\\Downloads\\recruitment-task\\data','.txt')


def readMessagesFromDir(dirPath, fileNamePattern, dfColNames, **kwargs):
    """For files in directory that match a pattern, return a dictionary of
    pandas DataFrames labeled by the filepaths.

    dirPath         : Path to the directory to find files in.
    fileNamePattern : A glob pattern to match filenames against.
    dfColNames      : Column names for the returned DataFrame.
    Returns         : Dictionary of DataFrames labeled by the filepaths.

    """
    filepaths = glob.glob(dirPath + fileNamePattern)
    d = {}
    for fp in filepaths:
        df = pd.read_csv(fp,names=dfColNames,header=None,sep='\t')
        d[fp] = df
        
    return d


col = ['messages','sentiment']

DFDict = readMessagesFromDir('C:/Users/Suhas/Downloads/recruitment-task/data/','*_labelled.txt',col)


# Have a look at the data files in this directory to become familiar.
dataDir = '../data/'

# Add code here that uses the functions written above to read msg
# files into a dictionary of DFs.


# Step 2: Compiling the corpus
# -----------------------------------------------------------------------------


def makeLabel(fromFilePath):
    """Make label for file from file path.

    fromFilePath : Input file path.
    Returns      : String label.

    Sample output:

    '../abc/xyz_labelled.txt' -> 'xyz'
    """
    return (os.path.basename(fromFilePath)).split("_labelled")[0]


def concatDataFrames(msgDFDict, labelFunc):
    """Concatenate DataFrames by rows adding a column that indicates the
    source of the message. Make sure that the index for each row is unique.

    Sample output:

                                             messages  sentiment         label
    The CG opening sequence in space looked like i...          0          imdb
    Then one day, I went to use them and the recie...        NaN  amazon_cells
    And the pho is much better when it is served f...        NaN          yelp
    I have always had cases for my cell phones bec...        NaN  amazon_cells
                    I'll let you know how it goes....        NaN          yelp
                                  It looks very nice.          1  amazon_cells
        The Veggitarian platter is out of this world!          1          yelp
                  It looked like a wonderful story.            1          imdb
                       Too much hassle for my liking.        NaN  amazon_cells
    So far so good with this one, plus the glowing...        NaN  amazon_cells
    """
    old_keys = [*msgDFDict.keys()]

    new_labels = [makeLabel(x) for x in old_keys]

    for i in range(len(old_keys)):
        msgDFDict[new_labels[i]] = msgDFDict.pop(old_keys[i])
    
    dd1 = { k:v for k, v in msgDFDict.items()}

    df11 = pd.concat(dd1, axis=0)
    df11['labels'] = df11.index
    df11['labels'] = df11['labels'].apply(lambda x: x[0])
    df11.reset_index(drop = True, inplace = True)
    df11 = df11.drop_duplicates()
    df11.dropna(inplace=True)
    df11['sentiment'] = df11['sentiment'].astype('int64')
        
    return df11


msgsDF = concatDataFrames(DFDict)

# Use functions above to generate a DF which contains messages from
# all sources with corresponding sentiments and labels.

# Some of the messages do not have the sentiment populated. Let's drop
# these from the DF here.


# Step 3: Counting the vocabulary
# -----------------------------------------------------------------------------


def makeTermsFrom(msg):
    """Use this function to convert a message into vocabulary terms to
    avoid confusion regarding what is a valid term.
    """
    return [m for m in msg.lower().split() if m]


def countVocabulary(msgsDF):
    """Take a DF of messages, sentiments, and labels and return a DF with
    terms, sentiments, labels, and the corresponding counts. Write
    whatever helper functions are required to achieve this task.

    Sample output:
              term  sentiment         label  count
    0            !          0  amazon_cells      1
    1            !          0          yelp      1
    2            !          1  amazon_cells      1
    3            !          1          imdb      1
    4            !          1          yelp      1
    5           !!          1  amazon_cells      1
    6          !!!          1          yelp      1
    7     !....the          0          yelp      1
    8          !2.          1  amazon_cells      1
    9           !i          1  amazon_cells      1
    10       "1.2"          1  amazon_cells      1
    11        "10"          1          imdb      1
    12          "a          1          imdb      1
    13     "about"          1          imdb      1
    14     "acting          1          imdb      1
    15        "are          0          yelp      1
    16        "art          1          imdb      1
    17         "at          1          imdb      1
    18        "big          1          imdb      1
    19  "breeders"          0          imdb      1
    20      "clip"          0  amazon_cells      1
    21   "collect"          0          imdb      1
    22    "crumby"          0          yelp      1
    23        "don          1          imdb      1
    24        "eel          0          yelp      1
    """
    msgsDF['messages'] = msgsDF['messages'].apply(lambda x: makeTermsFrom(x))
    
    count_v = pd.DataFrame([(row.sentiment,row.labels, word) for row in msgsDF.itertuples() 
                          for word in row.messages], 
                         columns=['sentiment','labels','terms'])
    count_voc = count_v.groupby(['terms','sentiment'])['labels'].value_counts()
    count_vocab = pd.DataFrame({'count': count_voc})
    count_vocab_df = count_vocab.reset_index()
    
    return count_vocab_df



counts = countVocabulary(msgsDF)
