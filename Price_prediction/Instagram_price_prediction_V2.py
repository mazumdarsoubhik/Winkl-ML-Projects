def instagram_price_v2(followers,eng_rate,story,image,video,reel,carousel):
    eng_num = followers*eng_rate/100
    num_post = story+image+video+reel+carousel
    if followers <= 10000:
        image_rate = (0.08580218 * followers + 0.00947688 * eng_num) * 2.3
        story_rate = image_rate * 0.6
        video_rate = image_rate * 2
        carousel_rate = image_rate * 1.1
        reel_rate = image_rate * 2.8
    if 10000 < followers <= 20000:
        image_rate = (0.024 * followers + 0.00947688 * eng_num) * 7.5
        story_rate = image_rate * 0.6
        video_rate = image_rate * 2
        carousel_rate = image_rate * 1.1
        reel_rate = image_rate * 2.8
    if 20000 < followers <= 50000:
        image_rate_1 = (0.03517652 * followers + 0.01662693 * eng_num) * 3.5
        image_rate_2 = (0.024 * 20000 + 0.00947688 * eng_num) * 7.5
        if image_rate_2 > image_rate_1:
            image_rate = image_rate_2
        else: 
            image_rate = image_rate_1
        story_rate = image_rate * 0.6
        video_rate = image_rate * 2
        carousel_rate = image_rate * 1.1
        reel_rate = image_rate * 2.8
    if 50000 < followers <= 100000:
        image_rate_1 = (0.02752566 * followers + 0.00921316 * eng_num) * 2.9
        image_rate_2 = (0.03517652 * 50000 + 0.01662693 * eng_num) * 3.5
        if image_rate_2 > image_rate_1:
            image_rate = image_rate_2 
        else:
            image_rate = image_rate_1
        story_rate = image_rate * 0.6
        video_rate = image_rate * 2
        carousel_rate = image_rate * 1.1
        reel_rate = image_rate * 2.8
    if 100000 < followers <=300000:
        image_rate_1 = (0.01687308 * followers + 0.10067394 * eng_num) * 2.8
        image_rate_2 = (0.02752566 * 100000 + 0.00921316 * eng_num) * 2.9
        if image_rate_2 > image_rate_1:
            image_rate = image_rate_2 
        else:
            image_rate = image_rate_1
        story_rate = image_rate * 0.6
        video_rate = image_rate * 2
        carousel_rate = image_rate * 1.1
        reel_rate = image_rate * 2.8
    if 300000 <followers <= 800000 :
        image_rate_1 = (0.01595681 * followers + 0.08665652 * eng_num) * 3.0
        image_rate_2 = (0.01687308 * followers + 0.10067394 * eng_num) * 2.8
        if image_rate_2 > image_rate_1:
            image_rate = image_rate_2 
        else:
            image_rate = image_rate_1
        story_rate = image_rate * 0.6
        video_rate = image_rate * 2
        carousel_rate = image_rate * 1.1
        reel_rate = image_rate * 2.8
    if 800000 <followers <= 1000000  :
        image_rate = (0.01595681 * followers + 0.08665652 * eng_num) * 2.5
        story_rate = image_rate * 0.6
        video_rate = image_rate * 2
        carousel_rate = image_rate * 1.1
        reel_rate = image_rate * 2.8
    if 1000000 <followers <= 3000000  :
        image_rate = (0.01595681 * followers + 0.08665652 * eng_num) * 2.5
        story_rate = image_rate * 0.6
        video_rate = image_rate * 2
        carousel_rate = image_rate * 1.1
        reel_rate = image_rate * 2.8
    if followers > 3000000 :
        image_rate = (0.01595681 * followers + 0.08665652 * eng_num) * 2.5
        story_rate = image_rate * 0.6
        video_rate = image_rate * 2
        carousel_rate = image_rate * 1.1
        reel_rate = image_rate * 2.8
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
        return range_it(discount_amount)
    else:
        return range_it(base_amount)
 
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
