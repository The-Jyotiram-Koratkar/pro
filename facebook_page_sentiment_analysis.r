library(plyr)
install.packages("ROAuth")
library(ROAuth)
library(stringr)
library(ggplot2) # Plot word frequencies.
install.packages("httr")
library(httr)
library(base64enc)
install.packages("wordcloud")
library(wordcloud)
install.packages("Rstem")
library(Rstem)
library(RColorBrewer) # Generate palette of colours for plots.
install.packages("SnowballC")
library(SnowballC)
install.packages("devtools")
library(devtools)
install.packages("sentimentr")
library(sentimentr)
install.packages("Rfacebook")
library(Rfacebook)  #1library(Rfacebook)
install.packages("Rook")
library(Rook)
require(RCurl)
require(rjson)#0155014076099024


##############################################################################################################
fb_oauth <- fbOAuth(app_id = "552639178448406", 
                    app_secret = "f55cfc0a7b7c9133ccc5d6d5b2bfddd0", extended_permissions = TRUE)

# Saving authorization file on the computer (in default working directory)
save(fb_oauth, file="fboauth")

# Loading authorization file from the computer (from default working directory)
load("fboauth")

##############################################################################################
getpagedata = getPage(316980541726369, token = fb_oauth, n=1000)
#View(getpagedata)
cleanedcomments<- (getpagedata$message)
Encoding(cleanedcomments)
write.csv(getpagedata, file = "Aegisbellaward.csv")
myCleanedText <- sapply(cleanedcomments, function(x) iconv(enc2utf8(x), sub = "byte"))
my_corpus<- Corpus(VectorSource(myCleanedText))
my_function<- content_transformer(function(x,pattern) gsub(pattern, " ", x))
my_cleaned_corpus<- tm_map(my_corpus,my_function,"/")
my_cleaned_corpus<- tm_map(my_cleaned_corpus,my_function,"\\|")
my_cleaned_corpus<- tm_map(my_cleaned_corpus,my_function,"@")
my_cleaned_corpus<- tm_map(my_cleaned_corpus,tolower)
#my_cleaned_corpus<- tm_map(my_cleaned_corpus,function(x) iconv(enc2utf8(x), sub = "byte")
my_cleaned_corpus<- tm_map(my_cleaned_corpus,removeWords, c(stopwords("english")))
my_cleaned_corpus<- tm_map(my_cleaned_corpus,removePunctuation)
my_cleaned_corpus<- tm_map(my_cleaned_corpus,stripWhitespace)

my_tdm<- TermDocumentMatrix(my_cleaned_corpus)
m<- as.matrix(my_tdm)
words<- sort(rowSums(m), decreasing = TRUE)
my_data<- data.frame(word = names(words),freq= words)

library(wordcloud)
wordcloud(words = my_data$word, freq = my_data$freq,min.freq = 2,max.words = 200,random.order = FALSE, rot.per = 0.35,colors = brewer.pal(8,"Dark2"))
class_emo = classify_emotion(my_data, algorithm="bayes", prior=1.0)
emotion = class_emo[,7]
emotion[is.na(emotion)] = "unknown"
# classify polarity
class_pol = classify_polarity(my_data, algorithm="bayes")


# get polarity best fit
polarity = class_pol[,4]
# data frame with results
text=getpagedata$message
sent_df = data.frame(text=getpagedata$message,emotion=emotion[0:617],polarity=polarity[0:617], stringsAsFactors=FALSE)

# sort data frame
sent_df = within(sent_df,
                 emotion <- factor(emotion, levels=names(sort(table(emotion), decreasing=TRUE))))

View(sent_df)
# plot distribution of emotions

ggplot(sent_df, aes(x=emotion)) +
  geom_bar(aes(y=..count.., fill=emotion))+xlab("Emotions Categories") + ylab("Post Count")+ggtitle("Sentiment Analysis of Tweets on Emotions")
# plot distribution of polarity

ggplot(sent_df, aes(x=polarity)) +
  geom_bar(aes(y=..count.., fill=polarity))+xlab("Polarities") + ylab("No of Post")+ggtitle("Sentiment Analysis of FacebookPage Post on Polarity")

# comparison word cloud
comparison.cloud(my_tdm, colors = brewer.pal(nemo, "Dark2"),
                 scale = c(3,.5), random.order = FALSE, title.size = 1.5)
