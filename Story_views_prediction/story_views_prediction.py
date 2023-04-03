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

def story_view_6(followers,eng_rate=2):
    eng_num = followers*eng_rate/100
    if eng_rate<=5:
        reach = (-2.50174147e-05) * followers + 1.11329127 * eng_num
    if eng_rate>5:
        reach = 0.04176708 * followers + 0.38973658 * eng_num
    return roundoff(reach,get_units(reach)-2)

follow = int(input('Follow: '))
eng = float(input('eng: '))
print(story_view_6(follow,eng))
