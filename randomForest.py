from sklearn.feature_extraction.text import TfidfTransformer, CountVectorizer
from sklearn import svm
from sklearn.metrics import accuracy_score
from sklearn.ensemble import RandomForestClassifier
import json
from sklearn.linear_model import LogisticRegression


with open('training_80%.json','r') as file:
    Train_X_text=json.load(file)
with open('training_80%_labels.json','r') as file:
    Train_Y=json.load(file)

with open('testing_20%.json','r') as file:
    Test_X_text=json.load(file)
with open('testing_20%_labels.json','r') as file:
    Test_Y=json.load(file)


tfidf_transformer = TfidfTransformer(norm = 'l2')
count_vec = CountVectorizer(analyzer="char",max_features = 10000,stop_words='english',ngram_range = (1,5))
trainx_tr = count_vec.fit_transform(Train_X_text)
testx_tr=count_vec.transform(Test_X_text)
train_x = tfidf_transformer.fit_transform(trainx_tr)
test_x= tfidf_transformer.transform(testx_tr)
train_x_char=train_x.toarray()
test_x_char=test_x.toarray()

tfidf_transformer = TfidfTransformer(norm = 'l2')
count_vec = CountVectorizer(analyzer="word",max_features = 10000,stop_words='english',ngram_range = (1,2))
trainx_tr = count_vec.fit_transform(Train_X_text)
testx_tr=count_vec.transform(Test_X_text)
train_x_word = tfidf_transformer.fit_transform(trainx_tr)
test_x_word= tfidf_transformer.transform(testx_tr)


RF = RandomForestClassifier(n_estimators=1000, random_state=0,class_weight='balanced') 
RF.fit(train_x_char,Train_Y)
pred=RF.predict(test_x_char)
print("Tfidf(char)+RF Accuracy Score -> ",accuracy_score(pred,Test_Y)*100)

#tfidf(word)+rf
RF = RandomForestClassifier(n_estimators=1000, random_state=0,class_weight='balanced') 
RF.fit(train_x_word,Train_Y)
pred=RF.predict(test_x_word)
print("Tfidf(word)+RF Accuracy Score -> ",accuracy_score(pred,Test_Y)*100)
