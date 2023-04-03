import requests
import json

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
              ['children', 'kids', 'infant', 'parenting', 'toys'],
              ['books', 'review', 'journaling', 'stationery', 'study']]
API_categories = ['Food','Fashion', 'Make-up', 'Beauty', 'Lifestyle','Luxury', 'Travel','Photography','Fitness','Sports','Gaming', 'Entertainment', 'Gadgets & Tech','Finance','Education', 'Animal/Pet', 'Health','Self Improvement','Art', 'Parenting', 'Books']

expressions = []
for ind in range(len(categories_list)):
    keywords = categories_list[ind]
    keyword_sentence = ""
    for k in keywords:
        keyword_sentence = keyword_sentence + k + " "
    exp = {"category": API_categories[ind],
           "expressions": keyword_sentence}
    expressions.append(exp)

response = {"status": True,
            "category_expressions": json.dumps(expressions)}

# Exp_update_url = 'http://44.229.68.155/update_category_tag_exp'
Exp_update_url = 'http://localhost:9292/update_category_tag_exp'
y = requests.post(Exp_update_url, data = response,headers={'Authorization': 'Token ruor7REQi9KJz6wIQKDXvwtt'})
print(y.status_code)
print(y.json())