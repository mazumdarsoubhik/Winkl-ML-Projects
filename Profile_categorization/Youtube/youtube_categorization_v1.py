import pandas as pd
import numpy as np
import nltk
import math
import time
import logging 
import requests
import json
import re
import random
import sys,os

from nltk.corpus import stopwords
from itertools import chain 
from collections import Counter
from gensim import models

print("##### Imported all packages #####")

print("..... Loading GoogleNews .....")
w = models.KeyedVectors.load_word2vec_format("/root/GoogleNews-vectors-negative300.bin.gz", binary=True)
print("##### Loaded GoogleNews #####")

# Global Parameters

avoidwords = ['youtube', 'welcome', 'official', 'love', 'pan', 'go', 'click', 'facebook', 'subscribe', 'subscribing', 'verified',
                'none', 'www', 'http', 'https', 'bit', 'ly', 'follow', 'like', 'reposted', 'influencer', 'gmail', 'com', 'collabs',
                'collaboration', 'hello', 'hi', 'hey', 'given', 'follow', 'instagram', 'channel', 'email', 'video', 'please', 'kindly',
                'connect', 'information', 'copyright', 'subjected', 'honest', 'de', 'les', 'la', 'des', 'en', 'un', 'et', 'mere', 'meri',
                'karna', 'aap', 'liked', 'join', 'apna', 'liye', 'mai', 'hoga', 'logo', 'gaya', 'best']

categories = ['food', 'fashion', 'makeup', 'beauty', 'lifestyle', 'luxury', 'travel', 'photography', 'fitness', 'sports', 'gaming', 'entertainment', 'technology', 'investment','education', 'animal', 'health', 'inspiration','art','parenting','book']
categories_list = [
                    ['food', 'cuisine', 'recipe', 'cooking', 'fried', 'spicy', 'meat', 'eat'],
                    ['fashion', 'outfit', 'clothes', 'menswear', 'wear'],
                    ['makeup', 'eyeliner', 'bridal', 'shades', 'airbrush'],
                    ['beauty', 'pimple', 'skin', 'oil', 'hair'],
                    ['lifestyle', 'life', 'vlog'],
                    ['luxury', 'rich', 'billionaire'],
                    ['travel', 'destination', 'adventure', 'landscapes'],
                    ['photography', 'photo', 'editing', 'creative', 'artist'],
                    ['fitness', 'nutrition', 'workout', 'healthy', 'exercise'],
                    ['sports', 'sport', 'football', 'cricket', 'soccer'],
                    ['gaming', 'gamer', 'games', 'stream'],
                    ['entertainment', 'movies', 'series', 'network', 'comedy', 'music', 'song', 'actor', 'actress', 'prank'],
                    ['technology', 'tech', 'geek', 'smartphones', 'mobiles', 'electronics', 'gadgets'],
                    ['investment', 'financial', 'stocks', 'market', 'trade'],
                    ['education', 'lectures', 'competitive', 'exams', 'coaching'],
                    ['animal', 'habitat', 'wild', 'documentary', 'nature', 'wildlife'],
                    ['health', 'medical', 'prevent', 'treat', 'heal'],
                    ['psychology', 'motivation', 'inspire', 'spiritual', 'mind'],
                    ['sketch', 'DIY', 'painting', 'art', 'drawing'],
                    ['children', 'kids', 'infant', 'family', 'parenting', 'toys'],
                    ['books', 'notebooks', 'journaling', 'stationery', 'study']
                    ]

col_name = ['youtube_channel_id', 'title', 'Food', 'Fashion', 'Makeup', 'Beauty', 'Lifestyle', 'Luxury', 'Travel', 'Photography', 'Fitness', 'Sports', 'Gaming', 'Entertainment', 'Gadgets & Tech', 'Finance', 'Education', 'Animal/Pet', 'Health', 'Self Improvement', 'Art', 'Parenting', 'Books', 'top keywords']
API_categories = ['Food', 'Fashion', 'Make-up', 'Beauty', 'Lifestyle', 'Luxury', 'Travel', 'Photography', 'Fitness', 'Sports', 'Gaming', 'Entertainment', 'Gadgets & Tech', 'Finance', 'Education', 'Animal/Pet', 'Health', 'Self Improvement', 'Art', 'Parenting', 'Books']


def process(array, avoidwords):
    """
        Clean the corpus, remove unwanted characters
        array : corpus
        avoidwords : the words that doesn't add up to the final scoring of the category
    """
    the_corpus = ""
    for xx in array:
    	the_corpus = the_corpus + xx
    text = re.sub(r'\[[0-9]*\]',' ',the_corpus)         # Remove Numbers
    text = re.sub("^\d+\s|\s\d+\s|\s\d+$", " ", text)   # Remove nums
    text = re.sub(r'\s+',' ',text)                      # Remove extra space
    text = re.sub(r"[^a-zA-Z0-9]+",' ',text)            # Remove special characters
    text = text.lower()                                 # Lower case all
    text = nltk.sent_tokenize(text)                     # Tokenize to sentences 
    keywords = [nltk.word_tokenize(sentence) for sentence in text]
    stop_words = stopwords.words('english')
    stop_words.extend(avoidwords)
    for i in range(len(keywords)):
        keywords[i] = [word for word in keywords[i] if word not in stop_words]
    
    return keywords


def normalize(keys, pos= 3):
    """
        Given an array, converts to 1/0, top int(pos) will be 1
    """
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


def normalizeSD(keys, threshold= 3):
    """
        Given score array return shortlisted cats in given threshold
    """
    if sum(keys) == 0:
        return keys
    ax = deviation(keys)
    ax = dev_shortlist(ax, threshold)
    
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


def dev_shortlist(dev_array, threshold = 2):
    """
        Shortlist using threshold from deviation array | return array in 1/0
    """
    final_cat = [0]*len(dev_array)
    for i in range(len(dev_array)):
        if dev_array[i] <=threshold:
            final_cat[i] = 1
    
    return final_cat


def compute2(caption, category_list, category, top= 3):
    """
        compute() => category[] to be called outside
    """
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
        keywords = np.array(labels)[indSort]        # Label
        caption_freq = np.array(values)[indSort]    # Values
    
    # Detect words not in Google Dict | Put freq = 0
    for x in keywords:
        try:
            restConst = w.similarity(x, 'something')
        except KeyError:
            caption_freq[np.where(keywords == x)] = 0
        
    # Cosine similaity function
    for c_tag in range(len(category_list)):
        empty1 = []
        for the_word in keywords:
            empty2 = []
            for k_tag in range(len(category_list[c_tag])):
                try:
                    empty2.append(w.similarity(category_list[c_tag][k_tag], the_word))
                except:
                    empty2.append(0)
            empty1.append(max(empty2))
        ar.append(empty1)

    # Store the similarity values in dataframe
    frame = pd.DataFrame()
    frame = pd.DataFrame(ar, columns = keywords)
  
    # Normalize | top select
    for key in frame.columns:
        frame[key] = normalizeSD(frame[key].tolist(), top)
    
    # Multiply with frequency
    for row in range(len(frame)):
        frame.values[row] = [i*j for i,j in zip(frame.values[row], caption_freq)]
    
    # Sum the values => Score
    for row in range(len(frame)):
        score.append(sum(frame.values[row]))
    
    frame['category'] = category
    frame['Scores'] = score

    return frame, keywords[:20]


def get_row_pscore(col_name, f1, i, score_list, top_keywords):
    """
        f1-mainframe | f2-frame
        f1 = dfnew
    """
    youtube_channel_id = f1.loc[i,'youtube_channel_id']
    title = f1.loc[i, 'title'].encode('utf-8')
    title = title.decode('utf-8')
    row_in_array = [youtube_channel_id, title]
    row_in_array.extend(score_list)
    row_in_array.append(', '.join(map(str, top_keywords)))
    zip_it = zip(col_name, row_in_array)
    convert_to_dict = dict(zip_it)
    
    return convert_to_dict


def to_dict_api(percentages, categories, top_keywords, youtube_channel_id):
    """
        To convert data in the DB format for the POST API request
    """
    mydict = {}
    cat_array =[]
    empty_percent = [0]*(len(categories) - len(percentages))
    percent_array = [y for y in percentages]
    percent_array.extend(empty_percent)
    mydict['youtube_channel_id'] = youtube_channel_id
    mydict['keywords'] = json.dumps(top_keywords.tolist())
    for j in range(len(categories)):
        cat_array.append({'tag':categories[j],'percentage':percent_array[j]})
    mydict['categories'] = json.dumps(cat_array)
    
    return mydict 


x = requests.get('http://44.229.68.155/get_youtube_uncategorized_channels?current_id=0&limit=10', headers={'Authorization': 'Token ruor7REQi9KJz6wIQKDXvwtt'})
status = x.status_code
data = x.json()
df = pd.DataFrame(data['channel'])
pages = 0
idsdone = 0
text = "Done {} pages, the last_id is {} and time taken {} seconds"
#profile_percentages =  pd.DataFrame(columns = col_name)
#profile_percentages.to_csv(r'profile_backup.csv', index = False)
tic = time.time()

while(len(data['channel']) !=0):
    try:
        new_tic = time.time()
        if(status != 200):
            raise Exception("GET request error: {}".format(status))

        dfnew = pd.DataFrame(columns=['id', 'youtube_channel_id', 'title', 'description', 'video_title', 'video_description'], data = df[['id', 'youtube_channel_id', 'title', 'description', 'video_title', 'video_description']].values)
        last_id = dfnew['youtube_channel_id'].iloc[-1]

        # Empty dataframe with all category columns
        profile_percentages =  pd.DataFrame(columns = col_name)

        # START Categorization By Page #
        for i in range(len(dfnew)):
            try:
                # Account timer
                user_tic = time.time()
                # Store youtube_channel_id | title | description | video_title | video_description
                youtube_channel_id = dfnew['youtube_channel_id'].iloc[i]
                title = dfnew['title'].iloc[i]
                description = dfnew['description'].iloc[i]
                video_title = dfnew['video_title'].iloc[i]
                if video_title == None:
                    raise Exception("No Videos on the channel")
                total_posts = len(video_title)
                video_description = dfnew['video_description'].iloc[i]
#                 print("1. all variable stored")
                
                # If the channels have less than 5 videos then skip
                if total_posts < 5:
                    raise Exception("Less than 5 videos on the channel")
                
                #Keeping the whole corpus in video_title only
                i_video_description = video_description
                for vd in video_description:
                    if vd == "":
                        i_video_description.pop(i_video_description.index(vd))
                video_description = i_video_description
                video_title.extend(video_description)

                # Converting to keywords
                if description == "" or description == None:
                	  description_array = []
                else:
                	  description = process([description], avoidwords)
                	  description_array = description[0]             
#                 print("2. description processed")
                
                video_info = process(video_title, avoidwords)
                video_info_array = video_info[0]
#                 print("3. video_info processed")
                # Temporary array i-> interim
                idescription_array = [z for z in description_array]
                ivideo_info_array = [z for z in video_info_array]
                
                # Removing words not in dictionary also single characters
                description_discarded_words = []
                video_info_discarded_words = []
                
                for x in description_array:
                    try:
                        checkword = w.similarity(x, 'something')    # Check word if exist in googlenews
                        if len(x) <= 3:                             # Removing single character
                            idescription_array.pop(idescription_array.index(x))
                    except KeyError:
                        description_discarded_words.append(idescription_array.pop(idescription_array.index(x)))
                    
                for x in video_info_array:
                    try:
                        checkword = w.similarity(x, 'something')    # Check word if exist in googlenews
                        if len(x) <= 3:                             # Removing single character
                            ivideo_info_array.pop(ivideo_info_array.index(x))
                    except KeyError:
                        video_info_discarded_words.append(ivideo_info_array.pop(ivideo_info_array.index(x)))
                
                # Restore Array
                video_info_array = [z for z in ivideo_info_array]
                description_array = [z for z in idescription_array]                
#                 print("4. discarded processing done")
                # Break if less data to categorize
                if len(video_info_array) < 10*(total_posts) :
                    raise Exception("Too less words for categorization")
                
                # Check similarity in discarded words
                description_discarded_words_scores = [0]*len(categories)
                video_info_discarded_scores = [0]*len(categories)
                for x_word in description_discarded_words:
                    for category_index in range(len(categories_list)):
                        for the_category in categories_list[category_index]:
                            if the_category in x_word:
                                description_discarded_words_scores[category_index] = 1 + description_discarded_words_scores[category_index]
                for x_word in video_info_discarded_words:
                    for category_index in range(len(categories_list)):
                        for the_category in categories_list[category_index]:
                            if the_category in x_word:
                                video_info_discarded_scores[category_index] = 1 + video_info_discarded_scores[category_index]
#                 print("5. description scores stored")
                # Word2vec computation
                frame = pd.DataFrame()
                frame, top_keywords = compute2(video_info_array, categories_list, categories, 3)
#                 print("6. compute done")
                # Brute force search for description
                description_score = [0]*len(categories)
                for x_word in description_array:
                    for category_index in range(len(categories_list)):
                        for the_category in categories_list[category_index]:
                            if the_category in x_word:
                                description_score[category_index] = 1 + description_score[category_index]                
               
                # Add discarded score to main description score
                for sc in range(len(description_score)):
                    description_score[sc] = description_score[sc] + description_discarded_words_scores[sc]

                # Add up computed score with discarded score
                score_column = frame['Scores'].tolist()
                for ind in range(len(score_column)):
                    score_column[ind] = score_column[ind] + video_info_discarded_scores[ind]
                
                 # Add weighted score of description in main score
                normalize_description_score = normalizeSD(description_score,3)
                for sc in range(len(normalize_description_score)):
                    if normalize_description_score[sc] == 1:
                        score_column[sc] = score_column[sc]*2
                
                # Convert to Percentage
                per_sum = sum(score_column)
                for x in range(len(score_column)):
                    temp_number = (float)(score_column[x])
                    score_column[x] = round((temp_number/per_sum) *100)
                frame['Percentage'] = score_column
#                 print("7. all scores stored")
                # Store profile percentage
#                 row_df = get_row_pscore(col_name, dfnew, i, score_column, top_keywords.tolist())
#                 profile_percentages = profile_percentages.append(row_df, ignore_index=True)
#                 print("8. csv append done")
                # POST API Request
                file = to_dict_api(frame['Percentage'].tolist(), API_categories, top_keywords, youtube_channel_id)
                url = 'http://44.229.68.155/add_category_to_youtube'
                y = requests.post(url, data= file, headers= {'Authorization': 'Token ruor7REQi9KJz6wIQKDXvwtt'})
                if y.status_code != 200:
                   raise Exception("Post request error {}".format(y.status_code))
#                 print("9. post API")
                idsdone = idsdone +1
                user_toc = time.time()
                print("ID no. {} Done! Total {} ids done in {} secs".format(youtube_channel_id, idsdone, user_toc - user_tic))

            except Exception as Argument:
                f = open(r"errorfile.txt", "a") 
                print('Warning 1', str(Argument))
                f.write("youtube_channel_id\t" + str(youtube_channel_id) + "\t: " + str(Argument) + str("\n")) 
                f.close()
        
#         profile_percentages.to_csv(r'profile_backup.csv', mode= 'a', header= False, index= False)
#         profile_percentages =  pd.DataFrame(columns = col_name)
        pages = pages + 1
        toc = time.time()
        print(text.format(pages, last_id, toc-new_tic))
        
        # Request new page
        x = requests.get('http://44.229.68.155/get_youtube_uncategorized_channels?current_id=' + str(last_id) + '&limit=10', headers= {'Authorization': 'Token ruor7REQi9KJz6wIQKDXvwtt'})
        data = x.json()
        df = pd.DataFrame(data['channel'])
        status = x.status_code
        

    except Exception as Argument:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        f = open(r"errorfile.txt", "a") 
        print('Warning 2', str(Argument))
        f.write("Currently in page" + str(pages) + "\t" + str(Argument) + "\t"+ "In line number: "+str(exc_tb.tb_lineno)+" Raised from "+str(exc_type)+str("\n")) 
        f.close()

toc = time.time()
f = open(r"errorfile.txt", "a") 
f.write("The model ran in " + str(toc - tic) + " seconds" + str("\n")) 
f.write("Total ids done: " + str(idsdone) + "\n")
f.write("Last youtube_channel_id {}".format(last_id) + "\n")
f.close() 
