from prettytable import PrettyTable
import json
# 读取sal的位置文件

city_dict = {}

with open('sal.json', 'r') as sal_file:
    sal_data = json.load(sal_file)
    for location in sal_data.keys():
        if sal_data[location].get('gcc').strip().lower()[1] == 'g' or sal_data[location].get('gcc').strip().lower()[1] == 'a' :
            city_dict[location] = sal_data.get(location).get('gcc').strip()


gsyd = 0
gmel = 0
gbri = 0
gade = 0
gper = 0
ghob = 0
gdar = 0
acte = 0


def check_place_code(word_key):
    info = city_dict.get(word_key)
    if info != None:
        if info == '1gsyd':
            global gsyd
            gsyd += 1
        elif info == '2gmel':
            global gmel
            gmel += 1
        elif info == '3gbri':
            global gbri
            gbri += 1
        elif info == '4gade':
            global gade
            gade += 1
        elif info == '5gper':
            global gper
            gper += 1
        elif info == '6ghob':
            global ghob
            ghob +=1
        elif info == '7gdar':
            global gdar
            gdar += 1
        elif info == '8acte':
            global acte
            acte += 1



with open('./tinyTwitter.json', 'r', encoding='utf-8') as tweets_file:
    begin_line = tweets_file.readline()
    while True:
        line = tweets_file.readline()
        if line == ']\n':
            break
        if line.startswith('          "full_name": '):
            location = line.split(': ')[1].strip(',\n')
            if location == '"Sydney, New South Wales"':
                key = 'sydney'
                check_place_code(key)
            elif location == '"Melbourne, Victoria"':
                key = 'melbourne'
                check_place_code(key)
            elif location == '"Brisbane, Queensland"':
                key = 'brisbane"'
                check_place_code(key)
            elif location == '"Adelaide, South Australia"':
                key = 'adelaide"'
                check_place_code(key)
            elif location == '"Perth, Western Australia"':
                key = 'perth'
                check_place_code(key)
            elif location == '"Hobart, Tasmania"':
                key = 'hobart'
                check_place_code(key)
            elif location == '"Canberra, Australian Capital Territory"':
                key = 'canberra'
                check_place_code(key)
            elif location == '"Central Coast, New South Wales"':
                key = 'alison (central coast - nsw)'
                check_place_code(key)
            else:
                check1 = location.split(', ')
                if len(check1) == 1:
                    if check1[0].lower() != '"australia"':
                        key = eval(check1[0])
                        check_place_code(key)

                elif len(check1) == 2:
                    small_position = check1[0].lower()
                    big_position = check1[1].lower()
                    if small_position != '"new south wales' and small_position != '"victoria' and small_position != '"queensland' and small_position != '"tasmania' and small_position != '"western australia' and small_position != '"south australia':
                        key = small_position+'"'
                        key = eval(key)
                        check_place_code(key)
                    # 去sal dic中用key来对应 地区

# Q1 tiny:
t = PrettyTable(['Greater Capital City', 'Number of Tweets Made'])
t.add_row(['1gysd', gsyd])
t.add_row(['1gmel', gmel])
t.add_row(['1gbri', gbri])
t.add_row(['1gade', gade])
t.add_row(['1gper', gper])
t.add_row(['1ghob', ghob])
t.add_row(['1gmel', gdar])
t.add_row(['1acte', acte])




    
# Q2


def rank_top10_users(user_dic):
    top10_rank = sorted(user_dic.items(), key=lambda x: x[1], reverse=True)
    t = PrettyTable(['Rank','Author ID', 'Number of Tweets Made'])
    i = 1
    while i < len(top10_rank):
        if i == 11:
            break
        t.add_row([i,top10_rank[i-1][0], top10_rank[i-1][1]])
        i += 1
    return t



def total_tweet_users(filepath):
    user_dic = {}
    with open(filepath, 'r', encoding='utf-8') as tweets_file:
        begin_line = tweets_file.readline()
        while True:
            line = tweets_file.readline()
            if line == ']\n':
                break
            if line.startswith('      "author_id": '):
                user_id = line.split(': ')[1].strip(',\n')
                user_id = eval(user_id)
                if user_dic.get(user_id) == None:
                    user_dic[user_id] = 0
                else:
                    user_dic[user_id] += 1
    return user_dic


# print(rank_top10_users(total_tweet_users('./tinyTwitter.json')))




# --------------------------------------
# Q3 

# gcc = {'1gsyd': 0, '2gmel': 0, '3gbri': 0 ,'4gade': 0, '5gper': 0, '6ghob' :0,'7gdar': 0 ,'8acte': 0}
d = total_tweet_users('./tinyTwitter.json')
user_places_dict = {}
for i in d.keys():
    user_places_dict[i] = [0,0,0,0,0,0,0,0]
    # 不要用这种办法

#print(user_places_dict)


# user_places_dict['836119507173154816']['1gsyd'] += 1
# user_places_dict['1399941819950006272']['1gsyd'] += 2
# print(user_places_dict)


# user_places_dict 指 author_id 和 gcc组成 dictionary

# def count_places(author, place_code, user_places_dict):
#     info = city_dict.get(place_code)
#     if info != None:
#         if info == '1gsyd':
#             user_places_dict[author]['1gsyd'] += 1
#         elif info == '2gmel':
#             user_places_dict[author]['2gmel'] += 1
#         elif info == '3gbri':
#             user_places_dict[author]['3gbri'] += 1
#         elif info == '4gade':
#             user_places_dict[author]['4gade'] += 1
#         elif info == '5gper':
#             user_places_dict[author]['5gper'] += 1
#         elif info == '6ghob':
#             user_places_dict[author]['6ghob'] += 1
#         elif info == '7gdar':
#             user_places_dict[author]['7gdar'] += 1
#         elif info == '8acte':
#             user_places_dict[author]['8acte'] += 1


def analyse(j, user_places_dict, city_dict):
    author = j.get('data').get('author_id')
    gcc_place = j.get('includes').get('places')[0].get('full_name')
    if gcc_place == 'Sydney, New South Wales':
        key = 'sydney'
        info = city_dict.get(key)
        if info != None:
            if info == '1gsyd':
                user_places_dict[author][0] += 1

    elif gcc_place == 'Melbourne, Victoria':
        key = 'melbourne'
        info = city_dict.get(key)
        if info != None:
            if info == '2gmel':
                user_places_dict[author][1] += 1


        
    elif gcc_place == 'Brisbane, Queensland':
        key = 'brisbane'
        info = city_dict.get(key)
        if info != None:
            if info == '3gbri':
                user_places_dict[author][2] += 1


        
    elif gcc_place == 'Adelaide, South Australia':
        key = 'adelaide'
        info = city_dict.get(key)
        if info != None:
            if info == '4gade':
                user_places_dict[author][3] += 1

        
    elif gcc_place == 'Perth, Western Australia':
        key = 'perth'
        info = city_dict.get(key)
        if info != None:   
            if info == '5gper':
                user_places_dict[author][4] += 1


        
    elif gcc_place == 'Hobart, Tasmania':
        key = 'hobart'
        info = city_dict.get(key)
        if info != None:
            if info == '6ghob':
                user_places_dict[author][5] += 1


        
    elif gcc_place == 'Canberra, Australian Capital Territory':
        key = 'canberra'
        info = city_dict.get(key)
        if info != None:
            if info == '7gdar':
                user_places_dict[author][6] += 1

        
    elif gcc_place == 'Central Coast, New South Wales':
        key = 'alison (central coast - nsw)'
        info = city_dict.get(key)
        if info != None:
            if info == '8acte':
                user_places_dict[author][7] += 1

        
    else:
        check1 = gcc_place.split(', ')
        if len(check1) == 1:
            if check1[0].lower() != 'australia':
                key = check1[0]
                info = city_dict.get(key)
                if info != None:
                    if info == '1gsyd':
                        user_places_dict[author][0] += 1
                    elif info == '2gmel':
                        user_places_dict[author][1] += 1
                    elif info == '3gbri':
                        user_places_dict[author][2] += 1
                    elif info == '4gade':
                        user_places_dict[author][3] += 1
                    elif info == '5gper':
                        user_places_dict[author][4] += 1
                    elif info == '6ghob':
                        user_places_dict[author][5] += 1
                    elif info == '7gdar':
                        user_places_dict[author][6] += 1
                    elif info == '8acte':
                        user_places_dict[author][7] += 1


        elif len(check1) == 2:
            small_position = check1[0].lower()
            if small_position != 'new south wales' and small_position != 'victoria' and small_position != 'queensland' and small_position != 'tasmania' and small_position != 'western australia' and small_position != 'south australia':
                key = small_position
                info = city_dict.get(key)
                if info != None:
                    if info == '1gsyd':
                        user_places_dict[author][0] += 1
                    elif info == '2gmel':
                        user_places_dict[author][1] += 1
                    elif info == '3gbri':
                        user_places_dict[author][2] += 1
                    elif info == '4gade':
                        user_places_dict[author][3] += 1
                    elif info == '5gper':
                        user_places_dict[author][4] += 1
                    elif info == '6ghob':
                        user_places_dict[author][5] += 1
                    elif info == '7gdar':
                        user_places_dict[author][6] += 1
                    elif info == '8acte':
                        user_places_dict[author][7] += 1
    return user_places_dict


def read_file2(filepath, user_places_dict, city_dict):
    with open(filepath, 'r', encoding='utf-8') as tweets_file:
        object_str = ''
        begin_line = tweets_file.readline()
        while True:
            line = tweets_file.readline()
            if line == '  },\n' or line == '  }\n':
                object_str += line.split(',')[0]
                twweet_json = json.loads(object_str)
                user_places_dict = analyse(twweet_json,user_places_dict, city_dict)
                # print(user_places_dict)
                # print('------------------')
                object_str = ''
            elif line == ']\n':
                break
            elif line.strip() == ',':
                continue
            else:
                object_str += line

read_file2('./tinyTwitter.json',user_places_dict, city_dict)


# 计算在几个不同的城市发送过tweet

def count_number_user(user_places_dict):
    new_user_dict = {}
    for i in user_places_dict:
        total = user_places_dict[i]
        number_gcc = 0
        total_tweet = 0
        for j in total:
            total_tweet += j
            if j > 0:
                number_gcc += 1
        # total_tweets = 0
        # for z in total.values():
        #     total_tweets += z
        new_user_dict[i] = total + [number_gcc, total_tweet]
    return new_user_dict


print(len(user_places_dict))


# def rank_Q3(dic):
#     top10_rank = sorted(dic.items(), key=lambda x: (-x[1][8], -x[1][9]))
#     t = PrettyTable(['Rank','Author ID', 'Number of Unique City Locations and #Tweets'])
#     i = 1

    
#     while i < len(top10_rank):
#         if i == 11:
#             break
#         total_city = top10_rank[i-1][1][-2]
#         total_tweets = top10_rank[i-1][1][-1]
#         words = str(total_city) + '(#' +str(total_tweets) + ' - ' + str(top10_rank[i-1][1][0])+'gsyd' + ', ' + str(top10_rank[i-1][1][1])+'gmel' + ', ' + str(top10_rank[i-1][1][2])+'gbri' + ', ' + str(top10_rank[i-1][1][3])+'gade' + ', ' + str(top10_rank[i-1][1][4])+'gper' + ', ' + str(top10_rank[i-1][1][5])+'ghob' + ', ' + str(top10_rank[i-1][1][6])+'gdar' + ', ' + str(top10_rank[i-1][1][7])+'acte' + ')'

#         t.add_row([i,top10_rank[i-1][0], words])
#         i += 1
#     return t


# result = rank_Q3(count_number_user(user_places_dict))

# print(result)