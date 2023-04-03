import requests # to get image from the web
import shutil # to save it locally
new_url = []
img_url_list = ['./Good_0.14647046.jpg', './Good_0.14359905.jpg', './Good_0.12849887.jpg', './Good_0.22457208.jpg', './Good_0.27442384.jpg', './Bad_0.74745935.jpg', './Good_0.38731715.jpg', './Good_0.48121968.jpg', './Good_0.24311939.jpg', './Good_0.16775194.jpg', './Bad_0.62026274.jpg', './Good_0.40948105.jpg', './Bad_0.9111298.jpg', './Good_0.26298591.jpg', './Good_0.10110654.jpg', './Good_0.49224675.jpg', './Good_0.22246307.jpg', './Good_0.10563126.jpg', './Good_0.04420968.jpg', './Good_0.38082448.jpg', './Good_0.055540435.jpg', './Good_0.09638107.jpg', './Good_0.24985203.jpg', './Bad_0.5194554.jpg', './Good_0.08310619.jpg', './Bad_0.5463415.jpg', './Good_0.27948505.jpg', './Good_0.030042881.jpg', './Good_0.1117732.jpg', './Good_0.10949742.jpg', './Good_0.23315486.jpg', './Good_0.054355294.jpg', './Good_0.08788112.jpg', './Good_0.28128776.jpg', './Bad_0.6646549.jpg', './Good_0.034846533.jpg', './Good_0.33565798.jpg', './Good_0.18822658.jpg', './Good_0.29978085.jpg', './Good_0.047962923.jpg', './Good_0.062845364.jpg', './Good_0.13735883.jpg', './Good_0.08813419.jpg', './Good_0.1676429.jpg', './Good_0.0827533.jpg', './Good_0.13606526.jpg', './Good_0.28607586.jpg', './Good_0.2362608.jpg', './Bad_0.52302593.jpg', './Good_0.32269004.jpg', './Good_0.020289512.jpg', './Good_0.2896417.jpg', './Good_0.047407664.jpg', './Good_0.25708234.jpg', './Good_0.08932444.jpg', './Good_0.049647823.jpg', './Good_0.15130742.jpg', './Good_0.42753494.jpg', './Good_0.31479722.jpg', './Good_0.16186346.jpg', './Bad_0.54895.jpg', './Good_0.079292215.jpg', './Good_0.107763186.jpg', './Good_0.10377447.jpg', './Good_0.059570376.jpg', './Good_0.06783378.jpg', './Bad_0.5230657.jpg', './Good_0.4641555.jpg', './Good_0.11514666.jpg', './Good_0.089568935.jpg', './Good_0.12548752.jpg', './Good_0.108399436.jpg', './Good_0.07733991.jpg', './Good_0.13066822.jpg', './Good_0.101588726.jpg', './Good_0.34901878.jpg', './Good_0.087366596.jpg', './Good_0.35471818.jpg', './Good_0.09061761.jpg', './Good_0.08537024.jpg', './Good_0.16820922.jpg', './Good_0.35399887.jpg', './Good_0.13942866.jpg', './Bad_0.6588175.jpg', './Good_0.3022782.jpg', './Good_0.19771662.jpg', './Good_0.17477874.jpg', './Good_0.22137341.jpg', './Good_0.11298614.jpg', './Good_0.19531831.jpg', './Good_0.04789791.jpg', './Good_0.31266245.jpg', './Good_0.14358734.jpg', './Good_0.05268574.jpg', './Good_0.07587063.jpg', './Good_0.10346567.jpg', './Good_0.38473642.jpg', './Good_0.41244864.jpg', './Good_0.32074836.jpg', './Good_0.31836691.jpg', './Good_0.2734092.jpg', './Good_0.26158753.jpg', './Bad_0.74007154.jpg', './Good_0.03402041.jpg', './Good_0.07039558.jpg', './Good_0.07115132.jpg', './Good_0.37508944.jpg', './Good_0.089120306.jpg', './Good_0.033180512.jpg', './Good_0.48237875.jpg', './Good_0.21695974.jpg', './Good_0.15732189.jpg', './Good_0.108766496.jpg', './Good_0.06389952.jpg', './Good_0.055766433.jpg', './Good_0.13213097.jpg', './Bad_0.711096.jpg', './Good_0.16931124.jpg', './Good_0.1324305.jpg', './Good_0.4759721.jpg', './Good_0.2537979.jpg', './Good_0.3512362.jpg', './Good_0.24555424.jpg', './Good_0.09580018.jpg', './Good_0.32692683.jpg', './Good_0.05843801.jpg', './Good_0.2810207.jpg', './Good_0.2968919.jpg', './Good_0.2436777.jpg', './Good_0.102541536.jpg', './Good_0.036185093.jpg', './Good_0.41329813.jpg', './Good_0.118305214.jpg', './Good_0.023372453.jpg', './Good_0.18137853.jpg', './Good_0.07323291.jpg', './Good_0.02877772.jpg', './Good_0.33537805.jpg', './Good_0.07983333.jpg', './Good_0.0364592.jpg', './Good_0.26264188.jpg', './Bad_0.5049385.jpg', './Good_0.07281925.jpg', './Good_0.44333038.jpg', './Good_0.12690175.jpg', './Good_0.058021087.jpg', './Good_0.37372464.jpg', './Good_0.029154561.jpg', './Bad_0.64120984.jpg', './Good_0.06825863.jpg', './Good_0.23742206.jpg', './Good_0.4643958.jpg', './Good_0.3634165.jpg', './Good_0.18059291.jpg', './Good_0.40603894.jpg', './Good_0.07447383.jpg', './Good_0.47970286.jpg', './Good_0.20517895.jpg', './Good_0.22895142.jpg', './Bad_0.6006279.jpg', './Good_0.078521974.jpg', './Good_0.39449385.jpg', './Good_0.08325884.jpg', './Good_0.30215716.jpg', './Good_0.14428169.jpg', './Good_0.037289783.jpg', './Bad_0.5475244.jpg', './Good_0.44634414.jpg', './Good_0.3739747.jpg', './Good_0.14946525.jpg', './Good_0.22084123.jpg', './Good_0.38167822.jpg', './Good_0.40345907.jpg', './Good_0.052364454.jpg', './Good_0.4178431.jpg', './Good_0.26508275.jpg', './Good_0.020400796.jpg', './Good_0.10028211.jpg', './Good_0.1489863.jpg', './Good_0.24731751.jpg', './Good_0.39484596.jpg', './Bad_0.6536715.jpg', './Good_0.40823323.jpg', './Good_0.2222919.jpg', './Good_0.045931626.jpg', './Good_0.09047759.jpg', './Good_0.36258516.jpg', './Good_0.23362832.jpg', './Good_0.29505032.jpg', './Good_0.1702744.jpg', './Good_0.3771351.jpg', './Good_0.4146251.jpg', './Good_0.038948227.jpg', './Good_0.33271858.jpg', './Good_0.29783615.jpg', './Bad_0.50548106.jpg', './Good_0.21479043.jpg', './Good_0.16741908.jpg', './Good_0.36023828.jpg', './Good_0.26684427.jpg', './Good_0.040082257.jpg', './Good_0.09390724.jpg', './Good_0.015662877.jpg', './Bad_0.78267974.jpg', './Good_0.12034274.jpg', './Good_0.10253081.jpg', './Good_0.34068185.jpg', './Good_0.4349232.jpg', './Good_0.15011266.jpg', './Good_0.18444362.jpg', './Good_0.111992314.jpg', './Good_0.23264265.jpg', './Good_0.27220196.jpg', './Good_0.31571028.jpg', './Good_0.14101428.jpg', './Good_0.16068012.jpg', './Good_0.03072259.jpg', './Good_0.10141195.jpg', './Good_0.20441282.jpg', './Good_0.2780965.jpg', './Good_0.21187133.jpg', './Good_0.13689859.jpg', './Good_0.1335563.jpg', './Good_0.33123487.jpg', './Good_0.02288742.jpg', './Good_0.058693647.jpg', './Good_0.17093344.jpg', './Good_0.039198436.jpg', './Good_0.08119244.jpg', './Good_0.22146091.jpg', './Good_0.09530924.jpg', './Bad_0.7529252.jpg', './Good_0.26499775.jpg', './Good_0.07550285.jpg', './Good_0.43714547.jpg', './Good_0.054188658.jpg', './Good_0.0992164.jpg', './Good_0.224843.jpg', './Good_0.09105719.jpg', './Good_0.093969844.jpg', './Good_0.23411846.jpg', './Good_0.41220212.jpg', './Good_0.46385878.jpg', './Good_0.2608302.jpg', './Good_0.12025939.jpg', './Good_0.46430054.jpg', './Good_0.02978727.jpg', './Good_0.1571814.jpg', './Good_0.14464971.jpg', './Good_0.26907554.jpg', './Bad_0.72072625.jpg', './Good_0.30598044.jpg', './Good_0.19102626.jpg', './Good_0.17827268.jpg', './Good_0.16960768.jpg', './Good_0.2747078.jpg', './Good_0.09546119.jpg', './Good_0.22070295.jpg', './Good_0.20044698.jpg', './Good_0.035733845.jpg', './Bad_0.50354683.jpg', './Good_0.12567195.jpg', './Good_0.16363582.jpg', './Good_0.05985378.jpg', './Good_0.42987764.jpg', './Good_0.09174979.jpg', './Good_0.17755073.jpg', './Good_0.42399222.jpg', './Good_0.08535439.jpg', './Good_0.14831287.jpg', './Good_0.35919395.jpg', './Good_0.20147313.jpg', './Good_0.17136721.jpg', './Good_0.14999472.jpg', './Good_0.21895286.jpg', './Good_0.24153791.jpg', './Good_0.12219802.jpg', './Good_0.47491392.jpg', './Good_0.27374473.jpg', './Good_0.2125714.jpg', './Good_0.39937487.jpg', './Good_0.13058387.jpg', './Good_0.22181384.jpg', './Bad_0.7636487.jpg', './Good_0.07611707.jpg', './Good_0.066928275.jpg', './Good_0.46803373.jpg', './Good_0.046636574.jpg', './Good_0.13437489.jpg', './Bad_0.559203.jpg', './Good_0.2062131.jpg', './Good_0.08762152.jpg', './Good_0.025281278.jpg', './Good_0.30465832.jpg', './Bad_0.57017183.jpg', './Good_0.23623012.jpg', './Good_0.47563517.jpg', './Good_0.2735867.jpg', './Good_0.193434.jpg', './Good_0.19866826.jpg', './Good_0.014688002.jpg', './Good_0.17911546.jpg', './Good_0.21509072.jpg', './Good_0.22772244.jpg', './Good_0.25048086.jpg', './Good_0.39757746.jpg', './Good_0.13688508.jpg', './Good_0.123166166.jpg', './Good_0.22393477.jpg', './Good_0.28572133.jpg', './Good_0.013551684.jpg', './Good_0.23018515.jpg', './Good_0.059244312.jpg', './Good_0.17580873.jpg', './Good_0.030589217.jpg', './Good_0.10786008.jpg', './Good_0.30081874.jpg', './Good_0.45302373.jpg', './Good_0.03147999.jpg', './Good_0.26849124.jpg', './Good_0.026749728.jpg', './Good_0.040682185.jpg', './Good_0.2709229.jpg', './Good_0.19657226.jpg', './Good_0.30245134.jpg', './Good_0.26935726.jpg', './Good_0.2614706.jpg', './Good_0.076899104.jpg', './Good_0.21444777.jpg', './Good_0.43013152.jpg', './Good_0.42868155.jpg', './Good_0.08590131.jpg', './Good_0.15649214.jpg', './Good_0.07633377.jpg', './Good_0.14846633.jpg', './Good_0.49027562.jpg', './Good_0.48814467.jpg', './Good_0.074727416.jpg', './Good_0.3704703.jpg', './Good_0.21209632.jpg', './Good_0.08788665.jpg', './Bad_0.8844505.jpg', './Good_0.18377712.jpg', './Good_0.4892911.jpg', './Bad_0.56412965.jpg', './Good_0.411551.jpg', './Good_0.15310311.jpg', './Good_0.08852147.jpg', './Good_0.461737.jpg', './Good_0.35573378.jpg', './Good_0.042907912.jpg', './Good_0.25023094.jpg', './Good_0.038744126.jpg', './Good_0.035525195.jpg', './Good_0.26774982.jpg', './Good_0.21725936.jpg', './Good_0.44575045.jpg', './Good_0.25637278.jpg', './Good_0.19699512.jpg', './Good_0.42237014.jpg', './Bad_0.5649054.jpg', './Good_0.12826544.jpg', './Good_0.010420876.jpg', './Good_0.27445272.jpg', './Good_0.10498278.jpg', './Good_0.06697935.jpg', './Good_0.028016951.jpg', './Good_0.18679342.jpg', './Good_0.43466264.jpg', './Good_0.10183577.jpg', './Good_0.2675404.jpg', './Good_0.0061770338.jpg', './Good_0.24639204.jpg', './Good_0.2259323.jpg', './Good_0.06437546.jpg', './Good_0.42370525.jpg', './Good_0.23475204.jpg', './Good_0.19692269.jpg', './Good_0.21686642.jpg', './Bad_0.7437028.jpg', './Good_0.12958583.jpg', './Good_0.35765123.jpg', './Bad_0.7973729.jpg', './Good_0.13945833.jpg', './Good_0.13925469.jpg', './Bad_0.51613146.jpg', './Good_0.15510707.jpg', './Bad_0.5935127.jpg', './Good_0.041132152.jpg', './Good_0.44085845.jpg', './Good_0.30258974.jpg', './Good_0.30259952.jpg', './Good_0.17424756.jpg', './Good_0.09162119.jpg', './Good_0.32175773.jpg', './Bad_0.6381628.jpg', './Good_0.058813103.jpg', './Good_0.043592498.jpg', './Good_0.29628056.jpg', './Good_0.117675275.jpg', './Good_0.20723428.jpg', './Good_0.22522698.jpg', './Good_0.08666231.jpg', './Bad_0.8219538.jpg', './Good_0.2130687.jpg', './Good_0.11753531.jpg', './Good_0.3444175.jpg', './Bad_0.51362026.jpg', './Good_0.24517128.jpg', './Bad_0.6357132.jpg', './Good_0.17961265.jpg', './Good_0.35850137.jpg', './Good_0.41412628.jpg', './Good_0.14980684.jpg', './Good_0.10689309.jpg', './Good_0.27547136.jpg', './Good_0.09176881.jpg', './Good_0.048192285.jpg', './Good_0.39548594.jpg', './Good_0.19830623.jpg', './Good_0.093729995.jpg', './Good_0.38676646.jpg', './Good_0.22132885.jpg', './Good_0.19017394.jpg', './Good_0.120793335.jpg', './Good_0.052460033.jpg', './Good_0.1989235.jpg', './Bad_0.5628667.jpg', './Good_0.13696758.jpg', './Good_0.463082.jpg', './Good_0.2982513.jpg', './Bad_0.5896262.jpg', './Good_0.33235943.jpg', './Good_0.04869878.jpg', './Bad_0.5038516.jpg', './Good_0.08098005.jpg', './Good_0.13506892.jpg', './Good_0.111735314.jpg', './Good_0.27541283.jpg', './Good_0.19834225.jpg', './Bad_0.6111985.jpg', './Good_0.11584025.jpg', './Good_0.20460843.jpg', './Good_0.22417016.jpg', './Good_0.06453601.jpg', './Good_0.10454982.jpg', './Good_0.08913773.jpg', './Good_0.0885987.jpg', './Good_0.1652156.jpg', './Good_0.15514316.jpg', './Good_0.3322084.jpg', './Good_0.08220801.jpg', './Good_0.10050198.jpg', './Good_0.24089003.jpg', './Good_0.0764251.jpg', './Good_0.49033546.jpg', './Good_0.25201815.jpg', './Good_0.16404828.jpg', './Good_0.48666987.jpg', './Good_0.13266219.jpg', './Good_0.38668928.jpg', './Good_0.17433229.jpg', './Good_0.1315191.jpg', './Good_0.17661364.jpg', './Good_0.1148821.jpg', './Good_0.33797592.jpg', './Good_0.02645959.jpg', './Good_0.12080126.jpg', './Good_0.30932006.jpg', './Good_0.109922156.jpg', './Good_0.20756257.jpg', './Good_0.4503803.jpg', './Bad_0.5114111.jpg', './Good_0.34588578.jpg', './Good_0.2969699.jpg', './Good_0.064279474.jpg', './Good_0.24306993.jpg', './Good_0.10013008.jpg', './Good_0.06652452.jpg', './Good_0.024568304.jpg', './Good_0.21432571.jpg', './Good_0.2908031.jpg', './Good_0.12809826.jpg', './Good_0.21566476.jpg', './Good_0.2143844.jpg', './Good_0.38512683.jpg', './Good_0.037007656.jpg', './Bad_0.57903445.jpg', './Good_0.09373391.jpg', './Good_0.2691272.jpg', './Good_0.3060589.jpg', './Good_0.17483589.jpg', './Good_0.12373771.jpg', './Good_0.39290616.jpg', './Good_0.26242062.jpg', './Good_0.123926595.jpg', './Good_0.34661335.jpg', './Good_0.039081167.jpg', './Good_0.2424813.jpg']

for ind in range(len(img_url_list)):
    new_url.append(img_url_list[ind].split('/')[-1])

download_url = 'https://www.kaggleusercontent.com/kf/59694288/eyJhbGciOiJkaXIiLCJlbmMiOiJBMTI4Q0JDLUhTMjU2In0..NBXHMO3n9LSAPA6qU1CoyA.1p6yxzzQNusJ4rdyu6RHICRyZgTBXKrmNG4jNNafUYaWxIkqHtWYZuzeCZHjWtP1M_fAiQT6KVgwzEFNCCKVH9d-npCGDq44f49sm0iJ5T2ocaBjdGUo0dS5ZKnq7oLKGAlXsQLDK7af-lOfnhs7J_zCpfcC8rD0UeI6vudNxCXPLk5KThYcRNIQDafR0WLoYjPjLpupX9NI0AS7JOq5eFXWkUvKZDpX9xnc2gcisALRhVDX5GwomhaH8ePzMYmecImh36vXMNOxSisVTai_ZYpAh91dbjwGWvp0oMy6PPvlC3_jeCIuagAnNdHRXryD5o0hIjZF8WGdHZvBJJ_Az7eiDbMVOBL4QHAwR0VHJgYKSRAyejc0VEcC5wS1h9TIb9Z_TkuZMA7eXfTfMWOKl1n3_oGa6sffV6FOSknZlpeqADfuFXIyVQ2cjqIwOnnLfbVn-VhnpoDe4-IVfpRUglxT099TbSoYcFogrnx4eywetgoV4lC0yyUDqcMScDWI2vALW77e5yy_ga2mekzXLqPKSRoQ0TDt8wSGPCif1tRlTIi1kKDzhEKB26DuaPg5Fwd22h0MuyYM3uznykxEly23c_0iHWdv9wgRHgvkgEbzpWOmJ1nGUc4fdL9ijO9LRtLtTz8fKceY6fu39GaFHirgz9rABYtp1Z39Qbb07Hs.7IwnF2eBTbN1pKE8nsq0GQ/'

for filename in new_url:
    image_url = download_url + filename
    r = requests.get(image_url, stream = True)

    if r.status_code == 200:
        r.raw.decode_content = True
        with open(filename,'wb') as f:
            shutil.copyfileobj(r.raw, f)
        print('Image sucessfully Downloaded: ',filename)
    else:
        print('Image Couldn\'t be retreived')