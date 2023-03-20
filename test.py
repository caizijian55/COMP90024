from mpi4py import MPI
from prettytable import PrettyTable
import json
city_dict = {}

with open('sal.json', 'r') as sal_file:
    sal_data = json.load(sal_file)
    for location in sal_data.keys():
        if sal_data[location].get('gcc').strip().lower()[1] == 'g' or sal_data[location].get('gcc').strip().lower()[1] == 'a' :
            city_dict[location] = sal_data.get(location).get('gcc').strip()


# def rank_top10_users(user_dic):
#     top10_rank = sorted(user_dic.items(), key=lambda x: x[1], reverse=True)
#     t = PrettyTable(['Rank','Author ID', 'Number of Tweets Made'])
#     i = 1
#     while i < len(top10_rank):
#         if i == 11:
#             break
#         t.add_row([i,top10_rank[i-1][0], top10_rank[i-1][1]])
#         i += 1
#     return t





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


d = total_tweet_users('./tinyTwitter.json')
user_places_dict = {}
for i in d.keys():
    user_places_dict[i] = [0,0,0,0,0,0,0,0]








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

comm = MPI.COMM_WORLD
size = comm.Get_size()
rank = comm.Get_rank()

def read_file2(filepath, user_places_dict, city_dict):
    with open(filepath, 'r', encoding='utf-8') as tweets_file:
        count = 0
        object_str = ''
        begin_line = tweets_file.readline()
        while True:
            line = tweets_file.readline()
            if line == '  },\n' or line == '  }\n':
                count += 1
                if count % size != rank:
                    object_str = ''
                    continue
                    
                object_str += line.split(',')[0]
                twweet_json = json.loads(object_str)
                user_places_dict = analyse(twweet_json,user_places_dict, city_dict)
                object_str = ''
            elif line == ']\n':
                break
            elif line.strip() == ',':
                continue
            else:
                object_str += line

read_file2('./tinyTwitter.json',user_places_dict, city_dict)

user_places_dict_all = comm.gather(user_places_dict, root=0)

if rank == 0:
    print(user_places_dict_all)



    


