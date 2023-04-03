import time
import math
import re
import requests
import json
import logging

import spacy
import en_core_web_sm
from spacymoji import Emoji
from pprint import pprint

from collections import Counter

headers = {'Authorization': 'Token ruor7REQi9KJz6wIQKDXvwtt'}

nlp = en_core_web_sm.load()
emoji = Emoji(nlp)


def generate_word_cloud(word_array):
    counter = Counter(word_array)
    common = counter.most_common(20)
    word_cloud = []
    for word in common:
        word_cloud.append(word[0])
    return word_cloud


def logreg(NER_count, propn_count, likes_count_stdev, captions_count_stdev):
    coef = [1.20112155, -0.0150792, 0.66137062, -0.66630538]
    bias = -0.82816386
    x = bias + (coef[0] * NER_count) + (coef[1] * propn_count) + (coef[2] * likes_count_stdev) + (coef[3] * captions_count_stdev)
    pred = 1 / (1 + math.exp(-x))
    return round(pred,4)


def deviation(array):
    mu = max(array)
    l = len(array)
    ar = []
    for x in range(l):
        ar.append(math.sqrt((array[x]-mu)**2)/l)
    total = sum(ar)
    for x in range(l):
        if total != 0:
            ar[x] = round((ar[x]/total)*100, 2)
    return ar


def remove_emoji(string):
    emoji_pattern = re.compile("["
                                u"\U0001F600-\U0001F64F" # emoticons
                                u"\U0001F300-\U0001F5FF" # symbols & pictographs
                                u"\U0001F680-\U0001F6FF" # transport & map symbols
                                u"\U0001F1E0-\U0001F1FF" # flags (iOS)
                                u"\U00002702-\U000027B0"
                                u"\U000024C2-\U0001F251"
                                "]+", flags=re.UNICODE)
    
    return emoji_pattern.sub(r'', string)


def clean(caption):
    try:
        caption = remove_emoji(caption)
        doc = nlp(caption)
    except Exception as e:
        print("SOME ERROR OCCURED IN PIPILINE")
        print(e)
    no_of_emojis = len(doc._.emoji)
    ner_org = 0
    ner_product = 0
    ner_list = []
    propn = 0
    propn_list = []
    
    hashtags_list = re.findall("#(\w+)", caption)
    caption = re.sub('\n',' ', caption)
    caption_list = caption.split(" ")
    
    for word in hashtags_list:
        try:
            word_ = '#' + str(word)
            caption_list.remove(word_)
        except:
            continue
    
    for word in caption_list:
        if word == '' or word == ',' or word == '.' or word == '_':
            caption_list.remove(word)
    
    length = len(caption_list)
    caption = ' '.join(caption_list)
    no_of_hashtags = len(hashtags_list)
    
    try:
        caption = remove_emoji(caption)
        doc = nlp(caption)
    except:
        caption = remove_emoji(caption)
        doc = nlp(caption)
        
    for entity in doc.ents:
        # pprint(entity.text + " : " + entity.label_ + " : " + str(spacy.explain(entity.label_)))
        if entity.label_ == 'ORG':
            ner_org += 1
            ner_list.append(str(entity))
        elif entity.label_ == 'PRODUCT':
            ner_product += 1
            ner_list.append(str(entity))
    
    try:
        caption_ = re.sub('#','',caption)
        caption = remove_emoji(caption_)
    except:
        caption_ = re.sub('#','',caption)
        caption = remove_emoji(caption_)

    doc = nlp(caption)

    for token in doc:
        if token.pos_ == 'PROPN':
            if token.text == '•' or token.text == '-' or token.text == '_':
                continue
            else:
                propn += 1
                propn_list.append(str(token))

    return length, no_of_hashtags, no_of_emojis, ner_org, ner_product, ner_list, propn, propn_list


def calc_promotional_score(insta_user):

    sum_length = 0
    sum_hashtags = 0
    sum_NER = 0
    sum_likes = 0
    post_ner_sum = 0
    list_likes = []
    list_captions = []
    list_NER_count = []
    list_PROPN_count = []
    word_cloud = []

    posts = insta_user['posts']
    for post in posts:
        caption = str(post['caption'])
        length, no_of_hashtags, no_of_emojis, ner_org, ner_product, ner_list, propn, propn_list = clean(caption)
        
        '''
        print(length)
        print(no_of_hashtags)
        print(no_of_emojis)
        print(ner_org)
        print(ner_product)
        print(ner_list)
        print(propn)
        print(propn_list)
        '''

        word_cloud += ner_list
        word_cloud += propn_list

        sum_length += length
        list_captions.append(length)
        
        sum_hashtags += no_of_hashtags
        
        post_ner_sum = ner_org + ner_product
        list_NER_count.append(post_ner_sum)
        
        list_PROPN_count.append(propn)
        
        sum_likes += post['like_count']
        list_likes.append(int(post['like_count']))

    # print(list_NER_count)
    # print(list_PROPN_count)

    standard_deviation_captions = deviation(list_captions)
    standard_deviation_likes = deviation(list_likes)

    # print(standard_deviation_likes)
    # print(standard_deviation_captions)

    result = {
        "status": True,
        "insta_user_id": insta_user['insta_user_id'],
        "promotional_word_cloud": json.dumps(generate_word_cloud(word_cloud)),
        "post_details": []
    }

    index = 0

    for post in posts:
        pred = logreg(list_NER_count[index], list_PROPN_count[index], standard_deviation_likes[index], standard_deviation_captions[index])
        post_result = {
            'insta_user_post_id': post['insta_user_post_id'],
            'promotional_score': pred
        }

        result['post_details'].append(post_result)
        index += 1

    result['post_details'] = json.dumps(result['post_details'])
    
    return result


def get_api_data(last_id,on_winkl):
    try:
        response = requests.get('http://44.229.68.155/insta_user/get_recent_captions/?last_insta_user_id={}&on_winkl={}'.format(last_id,on_winkl), headers= headers)
        status = response.status_code
        data = response.json()
        print("+", last_id)
        return data, status
    except Exception as e:
        print("X",last_id, e)
        res_str = str(response.content)
        res_list = res_str.split(',')
        last_id = res_list[1].split(':')[-1]
        # last_id = last_id +1
        get_api_data(last_id, on_winkl)


def get_api_data_v2(offset):
    response = requests.get('http://localhost:9292/get_recent_captions_v2?offset={}'.format(offset), headers= headers)
    status = response.status_code
    check_str = str(response.content)
    # print(check_str[-2])
    while check_str[-2] != '}':
        print("X",last_id)
        check_str = str(response.content)
        res_list = check_str.split(',')
        last_id = res_list[1].split(':')[-1]
        response = requests.get('http://localhost:9292/get_recent_captions_v2?offset={}'.format(offset + 1), headers= headers)
        status = response.status_code
        check_str = str(response.content)
    data = response.json()
    print("+", offset)
    return data, status


def update_promotional_posts(offset= 0):

    print("Updating from offset " + str(last_id))

    get_url = 'http://44.229.68.155/get_recent_captions_v2?offset={}'.format(offset)
    post_url = 'http://44.229.68.155/insta_user/update_promotional_posts'
    update_url = 'http://44.229.68.155/insta_user/update_promotional_posts?update_to_insta_user=1'

    response = requests.get(get_url, headers= headers)
    status = response.status_code
    data = response.json()

    accounts = 0
    if status == 200:
        while data['status'] == True:
            
            try:
                last_id = data['insta_user_id']
                post_list = data['posts']
                offset = data['offset']

                if len(post_list) == 0:
                    next_url = 'http://44.229.68.155/get_recent_captions_v2?offset={}'.format(offset + 1)
                    response = requests.get(next_url, headers= headers)
                    status = response.status_code
                    data = response.json()
                    continue
                
                store_list = []
                
                for index in range(len(post_list)):
                    if post_list[index]['caption'] is None or post_list[index]['caption'] == '':
                        continue
                    else:
                        store_list.append(post_list[index])
                
                data['posts'] = store_list
                promo_result = calc_promotional_score(data)
                post = requests.post(post_url, data= promo_result, headers= headers)
                
                if post.status_code == 200:
                    print("POSTED for InstaUser {}".format(last_id))
                
                accounts += 1
                offset += 1
                text = 'Total {} accounts done with last insta_user_id {}'.format(accounts, last_id)
                print(text)
                
                f = open(r"logs.txt", "a")  
                f.write(text + "\n") 
                f.close()
                
                new_url = 'http://44.229.68.155/get_recent_captions_v2?offset={}'.format(offset)
                x = requests.get(new_url, headers= headers)
                status = x.status_code
                data = x.json()

                '''
                if accounts > 3:
                    break
                '''

            except Exception as Argument:
                print("Exception occurred : ", Argument)
                f = open(r"error.txt", "a") 
                f.write("Last id was {}".format(last_id) + "\t" + str(Argument) + "\n") 
                f.close()  
                new_url = 'http://44.229.68.155/get_recent_captions_v2?offset={}'.format(offset + 1)
                x = requests.get(new_url, headers= headers)
                status = x.status_code
                data = x.json()
        
        print("Updating InstaUser table ...")
        y = requests.post(update_url, headers= headers)
        if y.status_code == 200:
            print("Updated InstaUser successfully!")
        else:
            print("Not updated because error : ", y.status_code)


def update_v2(offset):
    print("Updating from offset " + str(offset))

    post_url = 'http://localhost:9292/insta_user/update_promotional_posts'
    update_url = 'http://localhost:9292/insta_user/update_promotional_posts?update_to_insta_user=1'

    data, status = get_api_data_v2(offset)

    accounts = 0
    if status == 200:
        while data['status'] == True:
            
            try:
                last_id = data['insta_user_id']
                post_list = data['posts']
                offset = data['offset']

                if len(post_list) == 0:
                    data, status = get_api_data_v2(offset + 1)
                    continue
                
                store_list = []
                
                for index in range(len(post_list)):
                    if post_list[index]['caption'] is None or post_list[index]['caption'] == '':
                        continue
                    else:
                        store_list.append(post_list[index])
                
                data['posts'] = store_list
                promo_result = calc_promotional_score(data)
                post = requests.post(post_url, data= promo_result, headers= headers)
                
                if post.status_code == 200:
                    print("POSTED for InstaUser {}".format(last_id))
                
                accounts += 1
                offset += 1
                text = 'Total {} accounts done with last insta_user_id {}'.format(accounts, last_id)
                print(text)
                
                f = open(r"logs.txt", "a")  
                f.write(text + "\n") 
                f.close()
                
                data, status = get_api_data_v2(offset)

                
                if accounts > 3:
                    break

            except Exception as Argument:
                print("Exception occurred : ", Argument)
                f = open(r"error.txt", "a") 
                f.write("Last id was {}".format(last_id) + "\t" + str(Argument) + "\n") 
                f.close()  
                data, status = get_api_data_v2(offset + 1)
        
        # print("Updating InstaUser table ...")
        # y = requests.post(update_url, headers= headers)
        # if y.status_code == 200:
        #     print("Updated InstaUser successfully!")
        # else:
        #     print("Not updated because error : ", y.status_code)
        print("Updated all posts - Promotional")


update_v2(offset=0)


