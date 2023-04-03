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

def youtube_prediction(subscribers,avg_views,videos):
    video_rate = (0.42044539*subscribers)+(0.09215903*avg_views)
    if 100000<subscribers <=300000:
        video_rate = (0.42044539*100000)+(0.09215903*(avg_views/subscribers)*100000)
        video_rate = video_rate*(1+((subscribers/100000)-1)*0.1)
    if 300000<subscribers<=500000:
        video_rate = (0.42044539*100000)+(0.09215903*(avg_views/subscribers)*100000)
        video_rate = video_rate*(1+((subscribers/100000)-1)*0.6)
    if 500000<subscribers<=2000000:
        video_rate = (0.42044539*100000)+(0.09215903*(avg_views/subscribers)*100000)
        video_rate = video_rate*(1+((subscribers/100000)-1)*0.6)
    if subscribers>2000000:
        video_rate = (0.42044539*500000)+(0.09215903*(avg_views/subscribers)*500000)
        video_rate = video_rate*(1+((subscribers/100000)-5)*0.1)
    if (avg_views/subscribers) < 0.11:
        video_rate = video_rate*0.5
    dedicated_rate = video_rate
    intregated_rate = video_rate*0.65
    cpv_dedicated =  dedicated_rate/avg_views
    cpv_intregated =  intregated_rate/avg_views
    if videos > 2:
        dedicated_rate = dedicated_rate*videos*0.75
        dedicated_low,dedicated_high = range_it(dedicated_rate)
        intregated_rate = intregated_rate*videos*0.75
        intregated_low,intregated_high = range_it(intregated_rate)
        return dedicated_low,dedicated_high,intregated_low,intregated_high,cpv_dedicated,cpv_intregated
    else:
        dedicated_rate = dedicated_rate*videos
        dedicated_low,dedicated_high = range_it(dedicated_rate)
        intregated_rate = intregated_rate*videos
        intregated_low,intregated_high = range_it(intregated_rate)
        return dedicated_low,dedicated_high,intregated_low,intregated_high,cpv_dedicated,cpv_intregated