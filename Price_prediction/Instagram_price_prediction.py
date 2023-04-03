#Utility
def get_units(n):
    temp_n =n
    unit=0
    while temp_n > 9:
        temp_n = round(temp_n/10)
        unit= unit+1
    return unit
def roundoff(number,digit=1):
    temp_num = number
    temp_num = temp_num/(10**digit)
    temp_num = round(temp_num)
    return temp_num*(10**digit)
def range_it(nm):
    low_price = nm*0.9
    high_price = nm*1.05
    low_price = roundoff(low_price,get_units(low_price)-1)
    high_price = roundoff(high_price,get_units(high_price)-1)
    return low_price,high_price

# Main

def instagram_price(followers,eng_rate,story,image,video,reel,carousel):
    eng_num = followers*eng_rate/100
    num_post = story+image+video+reel+carousel
    video_rate = 0.24583049*followers + 0.01875384*eng_num
    if followers <= 10000:
        story_rate = video_rate*0.3
        image_rate = video_rate*0.5
        carousel_rate = video_rate*0.5
        reel_rate = video_rate*1.4
    if 10000 < followers <=50000:
        story_rate = video_rate*0.6
        image_rate = video_rate*0.5
        carousel_rate = video_rate*0.5
        reel_rate = video_rate*1.4
        video_rate = video_rate*1.35
    if 50000 < followers <=100000:
        story_rate = video_rate*0.3
        image_rate = video_rate*0.5
        carousel_rate = video_rate*0.5
        reel_rate = video_rate*1.4
        video_rate = video_rate*1.3
    if 100000 < followers <=300000:
        story_rate = video_rate*0.3
        image_rate = video_rate*0.6
        carousel_rate = video_rate*0.65
        reel_rate = video_rate*1.4
        video_rate = video_rate*1.3
    if 300000 <followers <= 800000 :
        story_rate = video_rate*0.3
        image_rate = video_rate*0.7
        carousel_rate = video_rate*0.75
        reel_rate = video_rate*1.4
        video_rate = video_rate*1.45
    if 800000 <followers <= 1000000  :
        story_rate = video_rate*0.4
        image_rate = video_rate*0.7
        carousel_rate = video_rate*0.75
        reel_rate = video_rate*1.4
        video_rate = video_rate*1.50
    if 1000000 <followers <= 3000000  :
        story_rate = video_rate*0.25
        image_rate = video_rate*0.55
        carousel_rate = video_rate*0.42
        reel_rate = video_rate*1.3
        video_rate = video_rate*1.3
    if followers > 3000000 :
        story_rate = video_rate*0.03
        image_rate = video_rate*0.40
        carousel_rate = video_rate*0.42
        reel_rate = video_rate*0.8
        video_rate = video_rate*0.9
    if followers <=5000000:
        base_amount = story_rate*story+image_rate*image+video_rate*video+reel_rate*reel+carousel_rate*carousel
    if followers>5000000:
        rate_dec = ((followers/1000000)-(5000000/1000000))*7.87272727
        video_rate = 0.24583049*5000000 + 0.01875384*eng_num
        story_rate = video_rate*0.03
        image_rate = video_rate*0.40
        carousel_rate = video_rate*0.42
        reel_rate = video_rate*0.8
        video_rate = video_rate*0.9
        base_amount = story_rate*story+image_rate*image+video_rate*video+reel_rate*reel+carousel_rate*carousel
        base_amount = base_amount*(1+rate_dec/100)
    if eng_rate > 2:
        base_amount = base_amount*(100+(1.14055527*eng_rate))/100
    if num_post>=3:
        discount_amount = base_amount*0.75
        return discount_amount
    else:
        return base_amount
