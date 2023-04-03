import pandas as pd
import numpy as np
from collections import Counter
import nltk
from nltk.corpus import stopwords
import re
from itertools import chain 
import math
import time
import logging 
import requests
import json
import sys,os
print("Imported all packages.")
tic = time.time()
print("Loading GoogleNews...")
from gensim import models
w = models.KeyedVectors.load_word2vec_format(r"/root/GoogleNews-vectors-negative300.bin.gz", binary=True)
print("Loaded GoogleNews!")

#Frame pre-processing function
def process(array,avoidwords):
    hashes = len(re.findall(r'#',str(array))) #counting hashtags
    text = re.sub(r'\[[0-9]*\]',' ',str(array))  #Remove Numbers
    text = re.sub("^\d+\s|\s\d+\s|\s\d+$", " ", text) # Remove nums
    text = re.sub(r'\s+',' ',text)  #Remove extra space
    text = re.sub(r"[^a-zA-Z0-9]+",' ',text)  #Remove special characters
    text = text.lower()  #Lower case all
    text = nltk.sent_tokenize(text)  #Tokenize to sentences 
    keywords = [nltk.word_tokenize(sentence) for sentence in text]
    raw_cap = len(keywords[0]) # Total number of words in caption
    stop_words = stopwords.words('english')
    stop_words.extend(avoidwords)
    for i in range(len(keywords)):
        keywords[i] = [word for word in keywords[i] if word not in stop_words]
    genuinity_percent = (raw_cap-hashes)*100/raw_cap
    return keywords,genuinity_percent

# normalize() -> given an array, converts to 1/0, top int(pos) will be 1
def normalize(keys, pos =3):  
    ax = [i for i in keys]
    temp = [i for i in keys]
    temp.sort()
    temp = temp[-pos:]
    for x in temp:
        ax[keys.index(x)] = 1
    for x in range(len(ax)):
        if ax[x] != 1:
            ax[x] = 0
    return ax

def normalizeSD(keys, thre =3):    # Given score array return shortlisted cats in given threshold
    if sum(keys) == 0:
        return keys
    ax = deviation(keys)
    ax = dev_shortlist(ax,thre)
    return ax
def deviation(array):
    mu = max(array)
    l = len(array)
    ar = []
    for x in range(l):
        ar.append(math.sqrt((array[x]-mu)**2)/l)
    total = sum(ar)
    for x in range(l):
        if total != 0:
            ar[x] = (ar[x]/total)*100
    return ar

def mean_deviation(array):
    l = len(array)
    mu = sum(array)/l
    ar = []
    for x in range(l):
        ar.append(math.sqrt((array[x]-mu)**2)/l)
    total = sum(ar)
    for x in range(l):
        if total != 0:
            ar[x] = (ar[x]/total)*100
    return ar

def dev_shortlist(dev_array,thre = 2):  # Shortlist using threshold from deviation array | return array in 1/0
    final_cat = [0]*len(dev_array)
    for i in range(len(dev_array)):
        if dev_array[i] <=thre:
            final_cat[i] = 1
    return final_cat

# compute() => category[] to be called outside
def compute2(caption,category_list,category,top =3):
    ar = []
    score = []

    # Code to get frequency distribution and unique keywords array
    keywords = []
    caption_freq = []
    counts = Counter(caption)
    if len(counts) > 0:
        labels, values = zip(*counts.items())
        ## sort your values in descending order
        indSort = np.argsort(values)[::-1]
        ## rearrange your data
        keywords = np.array(labels)[indSort]  # Label
        caption_freq = np.array(values)[indSort]  # Values
    
    # Detect words not in Google Dict | Put freq = 0
    for x in keywords:
        try:
            restConst = w.similarity(x,'something')
        except KeyError:
            caption_freq[np.where(keywords == x)] = 0
        
    #Google similaity function
    for c_tag in range(len(category_list)):
        empty1 = []
        for the_word in keywords:
            empty2 = []
            for k_tag in range(len(category_list[c_tag])):
                try:
                    empty2.append(w.similarity(category_list[c_tag][k_tag],the_word))
                except:
                    empty2.append(0)
            empty1.append(max(empty2))
        ar.append(empty1)
    # Store the similarity values in dataframe
    frame = pd.DataFrame()
    frame = pd.DataFrame(ar, columns = keywords)
  
    #Normalize | top select
    for key in frame.columns:
        frame[key] = normalizeSD(frame[key].tolist(),top)
    
    # Multiply with frequency
    for row in range(len(frame)):
        frame.values[row] = [i*j for i,j in zip(frame.values[row],caption_freq)]
    # Sum the values => Score
    for row in range(len(frame)):
        score.append(sum(frame.values[row]))
    
    frame['category'] = category
    frame['Scores'] = score
    len_keyword = len(keywords)
    if len(keywords)/2 <100 and len(keywords) > 0:
        response_keywords = keywords[:len(keywords)/2]
    elif len(keywords) > 0:
        response_keywords = keywords[:100]
    return frame,response_keywords

def get_row_pscore(col_name,f1,i,f2,genuinity_score,top_keywords, scoreType):  # f1-mainframe | f2-frame
    ud = f1.loc[i,'id']
    ul = f1.loc[i,'url']
    row_in_array = [ud,ul]
    score_array = f2[scoreType].tolist()
    row_in_array.extend(score_array)
    row_in_array.append(genuinity_score)
    row_in_array.append(','.join(map(str,top_keywords)).encode('utf-8').strip())
    zip_it = zip(col_name,row_in_array)
    convert_to_dict = dict(zip_it)
    return convert_to_dict

# To make data in 
# DB format | API post 
def to_dict_api(percentages,categories,top_keywords,user_id,g_score): #frame and i to get id
    mydict = {}
    cat_array =[]
    empty_percent = [0]*(len(categories)-len(percentages))
    percent_array = [y for y in percentages]
    percent_array.extend(empty_percent)
    mydict['user_id'] = user_id
    mydict['keywords'] = json.dumps(top_keywords.tolist())
    for j in range(len(categories)):
        cat_array.append({'tag':categories[j],'percentage':percent_array[j]})
    mydict['categories'] = json.dumps(cat_array)
    mydict['genuinity_score'] = g_score
    return mydict 


# Extended category list
categories = ['food', 'fashion', 'makeup', 'beauty', 'lifestyle', 'luxury', 'travel', 'photography', 'fitness', 'sports', 'gaming', 'entertainment', 'technology', 'investment', 'education', 'animal', 'health', 'inspiration', 'art', 'parenting', 'book']
categories_list = [['food', 'recipe', 'cooking'],
              ['fashion', 'outfit', 'clothes'],
              ['makeup', 'shades', 'haircare', 'face'],
              ['beauty', 'skin', 'oil', 'hair'],
              ['lifestyle', 'style'],
              ['luxury', 'rich', 'billionaire', 'car'],
              ['travel', 'world', 'destination', 'adventures', 'landscapes', 'bucket'],
              ['photography', 'photo', 'editing'],
              ['fitness', 'nutrition', 'workout', 'healthy', 'exercise', 'run'],
              ['sport', 'sports', 'win', 'loss'],
              ['gaming', 'stream', 'freefire', 'pubg', 'giveaway'],
              ['entertainment', 'movies', 'series', 'film', 'films', 'comedy', 'actor', 'actress', 'model'],
              ['technology', 'tech', 'smartphones', 'mobiles', 'laptop', '4G', 'LTE', 'PC', 'internet', 'phone', 'devices', 'wireless', 'unboxing'],
              ['investment', 'financial', 'stocks', 'market', 'trade'],
              ['education', 'lectures', 'competitive', 'exams', 'coaching'],
              ['animal', 'wild', 'wildlife', 'dog', 'cat', 'horse', 'parrot', 'pet'],
              ['health', 'medical', 'prevention','cure', 'treatment', 'heal', 'healthy', 'physical', 'ayurveda'],
              ['psychology', 'motivation', 'inspire', 'happiness', 'mind','spiritual'],
              ['sketch', 'DIY', 'painting', 'art', 'drawing'],
              ['children', 'kids', 'infant', 'family', 'parenting', 'toys'],
              ['books', 'review', 'journaling', 'stationery', 'study']]
col_name = ['user_id','url','Food','Fashion', 'Make-up', 'Beauty', 'Lifestyle','Luxury', 'Travel','Photography','Fitness','Sports','Gaming', 'Entertainment', 'Gadgets & Tech','Finance','Education', 'Animal/Pet', 'Health', 'Self Improvement','Art', 'Parenting', 'Books', 'genuinity_score','top keywords']
API_categories = ['Food','Fashion', 'Make-up', 'Beauty', 'Lifestyle','Luxury', 'Travel','Photography','Fitness','Sports','Gaming', 'Entertainment', 'Gadgets & Tech','Finance','Education', 'Animal/Pet', 'Health','Self Improvement','Art', 'Parenting', 'Books']


########################## MAIN CODE ###############################
last_offset = int(input("Enter last offset(Default put 0): "))
x = requests.get('http://44.229.68.155/insta_users/get_uncategorized_accounts_v2?limit=10&offset={last_offset}', headers={'Authorization': 'Token ruor7REQi9KJz6wIQKDXvwtt'})
status = x.status_code
data = x.json()
df = pd.DataFrame(data['users'])
pages = 0
idsdone = 0
txt = "Done {} pages, the last_id is {} , last offset {} and time taken {} seconds"
profile_percentages =  pd.DataFrame(columns = col_name)
# profile_percentages.to_csv(r'profile_backup.csv',index=False)

while(len(data['users']) !=0):
    try:
        new_len = len(data['users'])
        last_offset = last_offset + new_len
        new_tic = time.time()
        if(status != 200):
            raise Exception("GET request error: {}".format(status))
        dfnew = pd.DataFrame(columns=['id','handle','name','url','gender','country','captions','bio'], data = df[['id','handle','name','url','gender','country','captions','bio']].values)
        last_id = dfnew['id'].iloc[-1]
        # Fresh dataframe
        profile_percentages =  pd.DataFrame(columns = col_name)


        # START Categorization By Page #
        for i in range(len(dfnew)):

            try:
                #Store userid | caption | total posts
                userid = dfnew['id'].iloc[i]
                captions = dfnew['captions'].iloc[i]
                bio = dfnew['bio'].iloc[i]
                total_posts = len(captions)
                # Words which mostly occurs in insta post and we want to avoid considering them for the sake of accuracy of results
                avoidwords = ['verified','none','follow','like','reposted','influencer','gmail','com','collabs','collaboration','hello', 'hi', 'hey', 'given','instagram','please', 'like', 'kindly']

                #Converting to keywords
                captions,genuinity_score = process(captions,avoidwords)
                caption_array = captions[0]
                bio,ignore_this_var = process([bio],avoidwords)
                bio_array = bio[0]
                # Punishing accounts which has less than 3 words in caption
                if len(caption_array) < 5*(total_posts):
                    raise Exception("Too less words for categorization")

                #Temporary array i-> interim
                icaption_array = [z for z in caption_array]
                ibio_array = [z for z in bio_array]
                # Removing words not in dictionary also single characters
                discarded_words = []
                discarded_bio_words = []
                for x in caption_array:
                    try:
                        checkword = w.similarity(x,'something') #Check word if exist in googlenews
                        if len(x) <2: #Removing single character
                            icaption_array.pop(icaption_array.index(x))
                    except KeyError:
                        discarded_words.append(icaption_array.pop(icaption_array.index(x)))
                for x in bio_array:
                    try:
                        checkword = w.similarity(x,'something') #Check word if exist in googlenews
                        if len(x) <2: #Removing single character
                            ibio_array.pop(ibio_array.index(x))
                    except KeyError:
                        discarded_bio_words.append(ibio_array.pop(ibio_array.index(x)))
                #Restore Array
                caption_array = [z for z in icaption_array]
                bio_array = [z for z in ibio_array]
                # Check similarity in discarded words
                discard_word_scores = [0]*len(categories)
                discard_bio_word_scores = [0]*len(categories)
                for x_word in discarded_words:
                    for category_index in range(len(categories_list)):
                        for the_category in categories_list[category_index]:
                            if the_category in x_word:
                                discard_word_scores[category_index] = 1 + discard_word_scores[category_index]
                for x_word in discarded_bio_words:
                    for category_index in range(len(categories_list)):
                        for the_category in categories_list[category_index]:
                            if the_category in x_word:
                                discard_bio_word_scores[category_index] = 1 + discard_bio_word_scores[category_index]           
                if len(caption_array) ==0:
                    raise Exception("No Words in profile for categorization or Different language")

                # Word2vec computation
                frame = pd.DataFrame()
                frame, top_keywords = compute2(caption_array,categories_list,categories,3) ##############
                # Word2vec for bio
                frame_bio = pd.DataFrame()
                bio_score = [0]*len(categories)
                for x_word in bio_array:
                    for category_index in range(len(categories_list)):
                        for the_category in categories_list[category_index]:
                            if the_category in x_word:
                                bio_score[category_index] = 1 + bio_score[category_index]
            
                for sc in range(len(bio_score)):
                    bio_score[sc] = bio_score[sc] + discard_bio_word_scores[sc] 

                # Add up computed score with discarded score
                score_column = frame['Scores'].tolist()
                for ind in range(len(score_column)):
                    score_column[ind] = score_column[ind] + discard_word_scores[ind]

                # Add weighted score of bio in main score
                normalize_bio_score = normalizeSD(bio_score,3)
                for sc in range(len(normalize_bio_score)):
                    if normalize_bio_score[sc] == 1:
                        score_column[sc] = score_column[sc]*2
                frame['Scores'] = score_column

                #Convert to Percentage
                per = frame['Scores'].tolist()
                per_sum = sum(per)
                for x in range(len(per)):
                    temp_number = (float)(per[x])
                    per[x] = round((temp_number/per_sum)*100)
                frame['Percentage'] = per

                #Store profile percentage
                # row_df = get_row_pscore(col_name,dfnew,i,frame,genuinity_score,top_keywords.tolist(),'Percentage')
                # profile_percentages = profile_percentages.append(row_df,ignore_index=True)
                # POST API Request
                file = to_dict_api(frame['Percentage'].tolist(),API_categories,top_keywords,userid,genuinity_score)
                url = 'http://44.229.68.155/insta_user/add_category_to_insta_user'
                y = requests.post(url, data = file,headers={'Authorization': 'Token ruor7REQi9KJz6wIQKDXvwtt'})

                if y.status_code !=200:
                    raise Exception("Post request error {}".format(y.status_code))
                
                idsdone = idsdone +1
                print("ID no. {} Done! Total {} ids done".format(userid,idsdone))
                f = open(r"logs.txt", "a") 
                f.write("ID no. {} Done! Total {} ids done".format(userid,idsdone)+"\n") 
                f.close()
                
            except Exception as Argument:
                exc_type, exc_obj, exc_tb = sys.exc_info()
                # creating/opening a file 
                f = open(r"errorfile.txt", "a") 
                # writing in the file 
                f.write("Line number {exc_tb.tb_lineno} "+"Userid\t"+str(userid)+"\t: "+str(Argument)+str("\n")) 
                print("Line number {exc_tb.tb_lineno} "+"Userid\t"+str(userid)+"\t: "+str(Argument))
                # closing the file 
                f.close()

        # END of Main Categorization #
        # profile_percentages.to_csv(r'profile_backup.csv',mode='a',header=False,index =False)
        # print('Data Appended to CSV')
        pages = pages +1
        toc = time.time()
        print(txt.format(pages,last_id,last_offset,toc-new_tic))
        f = open(r"logs.txt", "a") 
        f.write(txt.format(pages,last_id,last_offset,toc-new_tic)+"\n") 
        f.close()
        # Request new page
        x = requests.get('http://44.229.68.155/insta_users/get_uncategorized_accounts_v2?limit=10&offset={last_offset}', headers={'Authorization': 'Token ruor7REQi9KJz6wIQKDXvwtt'})
        data = x.json()
        df = pd.DataFrame(data['users'])
        status = x.status_code
        print("Requested new page! last_offset{last_offset}")

    except Exception as Argument:
        exc_type, exc_obj, exc_tb = sys.exc_info()
#         fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
#         print(exc_type, fname, exc_tb.tb_lineno)
        f = open(r"errorfile.txt", "a") 
        f.write("Line number{exc_tb.tb_lineno} "+"page no "+str(pages)+" with last_offset {last_offset}"+"\t"+str(Argument)+str("\n")) 
        f.close()
        print("Line number{exc_tb.tb_lineno} "+"page no "+str(pages)+" with last_offset {last_offset}"+"\t"+str(Argument))

toc = time.time()
f = open(r"logs.txt", "a") 
f.write("The model ran in "+str(toc - tic)+" seconds"+str("\n")) 
f.write("Total ids done: "+str(idsdone)+"\n")
f.write("Last user_id {}".format(last_id)+"\n")
f.write("Last Offset {}".format(last_offset)+"\n")
f.close() 

