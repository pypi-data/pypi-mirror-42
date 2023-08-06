import requests
import json
import random
from time import sleep
from pprint import pprint as print
#from user_class import User
from dbworker import store_user
#from win10toast import ToastNotifier

def game_login(uid):
    headers = {
        'Expect': '100-continue',
        'Content-Type': 'application/json',
        'X-Unity-Version': '2018.2.14f1',
        'User-Agent': 'Dalvik/2.1.0 (Linux; U; Android 7.0; BV6000 Build/NRD90M)',
        'Host': 'api-duels.galapagosgames.com:8001',
    }

    data = '{"ids":["'+uid+'"],"appBundle":"com.deemedyainc.duels","appVersion":"0.6.6","platform":"Android"}'

    r = requests.post('http://api-duels-test.galapagosgames.com/general/login', headers=headers, data=data)
    j = json.loads(r.text)

    return j

print(game_login('ce7437b6-a4a0-4c4f-a6a2-7c0ad4bebbe1'))

def increase_fire_mastery():
    headers = {
        'Expect': '100-continue',
        'Content-Type': 'application/json',
        'X-Unity-Version': '2018.2.14f1',
        'User-Agent': 'Dalvik/2.1.0 (Linux; U; Android 7.0; BV6000 Build/NRD90M)',
        'Host': 'api-duels.galapagosgames.com:8001',
    }

    data = '{"mastery":"FireMastery","id":"5c420b52de661c681ff98f46"}'

    r = requests.post('http://api-duels.galapagosgames.com:8001/masteries/increase', headers=headers, data=data)
    print(r.text)
#increase_fire_mastery()
def get_group_info(user_id):
    headers = {
        'Expect': '100-continue',
        'Content-Type': 'application/json',
        'X-Unity-Version': '2018.2.14f1',
        'User-Agent': 'Dalvik/2.1.0 (Linux; U; Android 7.0; BV6000 Build/NRD90M)',
        'Host': 'api-duels.galapagosgames.com:8001',
    }

    data = '{"id":"'+user_id+'"}'
    #print(data)
    r = requests.post('http://api-duels-test.galapagosgames.com/ranking/group', headers=headers, data=data)
    j = json.loads(r.text)
    #print(j)
    return j

def ranked_battle(enemy_id, group_id, user_id):
    headers = {
        'Expect': '100-continue',
        'X-Unity-Version': '2018.2.14f1',
        'Content-Type': 'application/json',
        'User-Agent': 'Dalvik/1.6.0 (Linux; U; Android 4.4.2; SM-N950W Build/NMF26X)',
        'Host': 'api-duels.galapagosgames.com:8001',
    }

    data = '{"enemyId":"'+enemy_id+'","groupId":"'+group_id+'","id":"'+user_id+'"}'

    r = requests.post('http://api-duels-test.galapagosgames.com/battle/ranked', headers=headers, data=data)
    j = json.loads(r.text)
    #print(j)
    return j.get('result', False)

def claim_reward_group(gid: str, uid: str):
    headers = {
        'Expect': '100-continue',
        'Content-Type': 'application/json',
        'X-Unity-Version': '2018.2.14f1',
        'User-Agent': 'Dalvik/2.1.0 (Linux; U; Android 7.0; BV6000 Build/NRD90M)',
        'Host': 'api-duels-test.galapagosgames.com',
    }

    data = '{"containerId":"'+str(gid)+'","id":"'+str(uid)+'"}'

    r = requests.post('http://api-duels-test.galapagosgames.com/queue/claim', headers=headers, data=data)
    j = json.loads(r.text)
    return j['_u']['Key@Value']

def defeat_group(uid):
    try:
        group_list = get_group_info(uid)
        #print(group_list[])
        group_id = group_list['group']['_id']
        print('group_id')
        print(group_id)
        members_list = group_list['group']['members']
        #print(group_id)
        #print(members_list)
        have_empty = [i for i in members_list if i.get("pid") is not None];
        print(len(have_empty))
        if len(have_empty)>=16:
            for i in members_list:
                if i.get('pid')!=uid:
                    to_sleep = random.randint(1,3)
                    print("Trying first:"+i['name'])
                    count = 0;
                    result = ranked_battle(i['pid'],group_id, uid)
                    #print(result)
                    while(result!=True and count<=50):
                        to_sleep = random.randint(1,3)
                        #sleep(to_sleep)
                        #print('Trying again: '+str(count)+" after "+str(to_sleep))
                        result = ranked_battle(i['pid'],group_id, uid)
                        count+=1;
                    if result==True:
                        #print("DEFEATED: "+i['name'])
                        pass
                    else:
                        print("Cant beat:"+i['name']);
                        print("Starting work as "+i['pid'])
                        return defeat_group(i['pid'])
                        #sleep(60*3)
                        #return -2
                else:
                    print("Prevent self destruct")
        else:
            print("Empty user")
            #sleep(60*2)
            return -1;
        claim_id = get_group_info(uid)
        keys = 0
        try:
            claim_reward_group(claim_id['_q'][0]['_id'], uid)
        except Exception as e:
            print(e)
        return keys
    except:
        return -1

def loot_battle(uid):
    headers = {
        'Expect': '100-continue',
        'X-Unity-Version': '2018.2.14f1',
        'Content-Type': 'application/json',
        'User-Agent': 'Dalvik/1.6.0 (Linux; U; Android 4.4.2; SM-N950W Build/NMF26X)',
        'Host': 'api-duels.galapagosgames.com:8001',
    }

    data = '{"id":"'+uid+'"}'

    r = requests.post('http://api-duels.galapagosgames.com:8001/battle/loot', headers=headers, data=data)
    j = json.loads(r.text)
    return j['battle']['result'], j['_u']['WinStreak@Value']



def defeat_loot(uid, need_streak):
    i = 0;
    result = False
    wins = 0;
    opponent = get_loot_opponent(uid)
    to_sleep = random.randint(6,12)
    while(wins != need_streak):
        opponent = get_loot_opponent(uid)
        if opponent.hp <= 1500 and opponent.attack <= 500:
            result, wins = loot_battle(uid)
            to_sleep = random.randint(6,12)
            print("iter:"+str(i)+" wins: "+str(wins)+" after "+str(to_sleep))
            i+=1;
        else:
            print('rerroll')
            #reroll_opponent(uid)
        #sleep(to_sleep);

def dissasemble_item(uid, item_id):
    headers = {
        'Expect': '100-continue',
        'Content-Type': 'application/json',
        'X-Unity-Version': '2018.2.14f1',
        'User-Agent': 'Dalvik/2.1.0 (Linux; U; Android 7.0; BV6000 Build/NRD90M)',
        'Host': 'api-duels.galapagosgames.com:8001',
    }

    data = '{"partId":"'+item_id+'","id":"'+uid+'"}'

    r = requests.post('http://api-duels.galapagosgames.com:8001/inventory/disassemble', headers=headers, data=data)
    j = json.loads(r.text)
    #print(j)
    #print(j)

def reroll_opponent(uid):
    headers = {
        'Expect': '100-continue',
        'Content-Type': 'application/json',
        'X-Unity-Version': '2018.2.14f1',
        'User-Agent': 'Dalvik/2.1.0 (Linux; U; Android 7.0; BV6000 Build/NRD90M)',
        'Host': 'api-duels.galapagosgames.com:8001',
    }

    data = '{"reroll":true,"id":"'+uid+'"}'

    r = requests.post('http://api-duels.galapagosgames.com:8001/battle/opponent', headers=headers, data=data)
    j = json.loads(r.text)

def get_loot_opponent(uid):
    headers = {
        'Expect': '100-continue',
        'Content-Type': 'application/json',
        'X-Unity-Version': '2018.2.14f1',
        'User-Agent': 'Dalvik/2.1.0 (Linux; U; Android 7.0; BV6000 Build/NRD90M)',
        'Host': 'api-duels.galapagosgames.com:8001',
    }

    data = '{"reroll":false,"id":"'+uid+'"}'

    r = requests.post('http://api-duels.galapagosgames.com:8001/battle/opponent', headers=headers, data=data)
    j = json.loads(r.text)
    #print(j)
    opp = User()
    opp.name = j['opponent']['name']
    for mast in j['opponent']['masteries']:
        if mast['info']=='ColdMastery':
            opp.cold_mastery = mast['points'];
        elif mast['info']=='FireMastery':
            opp.fire_mastery = mast['points'];
        elif mast['info']=='HolyMastery':
            opp.holy_mastery = mast['points'];
        elif mast['info']=='PhysicalMastery':
            opp.physical_mastery = mast['points'];
        elif mast['info']=='PoisonMastery':
            opp.poison_mastery = mast['points'];

    for part in j['opponent']['parts']:
        for resist in part['resistances']:
            if resist['info']=='PhysicalResistanceAffix':
                opp.physical_damage_resist += resist['value'];
            elif resist['info']=='ColdResistanceAffix':
                opp.cold_damage_resist += resist['value'];
            elif resist['info']=='FireResistanceAffix':
                opp.fire_damage_resist += resist['value'];
            elif resist['info']=='PoisonResistanceAffix':
                opp.poison_damage_resist += resist['value'];
            elif resist['info']=='HolyResistanceAffix':
                opp.holy_damage_resist += resist['value'];
        for stat in part['brms']:
            #print(stat)
            if stat['info']=='Dodge':
                opp.dodge_chance += stat['value'];
            elif stat['info']=='CritChance':
                opp.crit_chance += stat['value'];
            elif stat['info']=='Block':
                opp.block_chance += stat['value'];
            elif stat['info']=='CritDamage':
                opp.crit_bonus += stat['value'];
        if part['stat']['info']=='Health':
            opp.hp += part['stat']['value']
        elif part['stat']['info']=='Attack':
            opp.attack += part['stat']['value']

    for stat in j['opponent']['stats']:
        if stat['info']=='Attack':
            opp.attack += stat['value']
            opp.stat_attack_add += stat['value']
        elif stat['info']=='Health':
            opp.hp += stat['value']
            opp.stat_health_add += stat['value']


    return opp;

def get_ranked_opponent(uid, enemy_id, group_id):
    headers = {
        'Expect': '100-continue',
        'Content-Type': 'application/json',
        'X-Unity-Version': '2018.2.14f1',
        'User-Agent': 'Dalvik/2.1.0 (Linux; U; Android 7.0; BV6000 Build/NRD90M)',
        'Host': 'api-duels.galapagosgames.com:8001',
    }

    data = '{"enemyId":"'+enemy_id+'","groupId":"'+group_id+'","id":"'+uid+'"}'

    r = requests.post('http://api-duels.galapagosgames.com:8001/battle/ranked/opponent', headers=headers, data=data)
    j = json.loads(r.text)
    print(j)
    opp = User()
    opp.name = j['opponent']['name']
    #opp.id = j['opponent']['_id']
    for mast in j['opponent']['masteries']:
        if mast['info']=='ColdMastery':
            opp.cold_mastery = mast['points'];
        elif mast['info']=='FireMastery':
            opp.fire_mastery = mast['points'];
        elif mast['info']=='HolyMastery':
            opp.holy_mastery = mast['points'];
        elif mast['info']=='PhysicalMastery':
            opp.physical_mastery = mast['points'];
        elif mast['info']=='PoisonMastery':
            opp.poison_mastery = mast['points'];

    for part in j['opponent']['parts']:
        for resist in part['resistances']:
            if resist['info']=='PhysicalResistanceAffix':
                opp.physical_damage_resist += resist['value'];
            elif resist['info']=='ColdResistanceAffix':
                opp.cold_damage_resist += resist['value'];
            elif resist['info']=='FireResistanceAffix':
                opp.fire_damage_resist += resist['value'];
            elif resist['info']=='PoisonResistanceAffix':
                opp.poison_damage_resist += resist['value'];
            elif resist['info']=='HolyResistanceAffix':
                opp.holy_damage_resist += resist['value'];
        for stat in part['brms']:
            #print(stat)
            if stat['info']=='Dodge':
                opp.dodge_chance += stat['value'];
            elif stat['info']=='CritChance':
                opp.crit_chance += stat['value'];
            elif stat['info']=='Block':
                opp.block_chance += stat['value'];
            elif stat['info']=='CritDamage':
                opp.crit_bonus += stat['value'];
        if part['stat']['info']=='Health':
            opp.hp += part['stat']['value']
        elif part['stat']['info']=='Attack':
            opp.attack += part['stat']['value']

    for stat in j['opponent']['stats']:
        if stat['info']=='Attack':
            opp.attack += stat['value']
            opp.stat_attack_add += stat['value']
        elif stat['info']=='Health':
            opp.hp += stat['value']
            opp.stat_health_add += stat['value']


    return opp;

def buy_box(uid):
    headers = {
        'Expect': '100-continue',
        'Content-Type': 'application/json',
        'X-Unity-Version': '2018.2.14f1',
        'User-Agent': 'Dalvik/2.1.0 (Linux; U; Android 7.0; BV6000 Build/NRD90M)',
        'Host': 'api-duels.galapagosgames.com:8001',
    }

    data = '{"info":"SpecialCrate1","id":"'+uid+'"}'

    r = requests.post('http://api-duels-test.galapagosgames.com/crates/buy', headers=headers, data=data)
    j = json.loads(r.text)
    print(j)
    try:
        '''for item in j['crate']['rewards']:
            item = item['reward']
            print(item['__type'])
            if item['rarity']=='Legendary':
                if item['__type']!="Head" or item['__type']!="Hands" or item['__type']!="Shoulders":
                    dissasemble_item(uid, item['__id'])
                else:
                    print('GOOD')
            else:
                dissasemble_item(uid, item['__id'])'''
        check_items(uid, j['crate']['rewards'])
    except Exception as e:
        #print(d)
        return -4, -4

    return j['_u']['Key@Value'], len(game_login(login_id)['profile']['inventory']['items'])



'''ef buy_keys(uid):
    headers = {
        'Expect': '100-continue',
        'Content-Type': 'application/json',
        'X-Unity-Version': '2018.2.14f1',
        'User-Agent': 'Dalvik/2.1.0 (Linux; U; Android 7.0; BV6000 Build/NRD90M)',
        'Host': 'api-duels.galapagosgames.com:8001',
    }

    data = '{"info":"duels_keys_100","id":"'+uid+'"}'

    r = requests.post('http://api-duels.galapagosgames.com:8001/inapps/duels', headers=headers, data=data)
    j = json.loads(r.text)'''

def dung(uid):
    headers = {
        'Expect': '100-continue',
        'Content-Type': 'application/json',
        'X-Unity-Version': '2018.2.14f1',
        'User-Agent': 'Dalvik/2.1.0 (Linux; U; Android 7.0; BV6000 Build/NRD90M)',
        'Host': 'api-duels.galapagosgames.com:8001',
    }

    data = '{"id":"5c420b52de661c681ff98f46"}'

    r = requests.post('http://api-duels.galapagosgames.com:8001/battle/dungeon', headers=headers, data=data)
    j = json.loads(r.text)
    #print(j)
    #print(j['battle']['result'])
    if j['battle']['result']==True:
        check_items(uid, j['crate']['rewards'])
        return True#['result']
    else:
        return False;

def equip_item(uid, item_id):
    headers = {
        'Expect': '100-continue',
        'Content-Type': 'application/json',
        'X-Unity-Version': '2018.2.14f1',
        'User-Agent': 'Dalvik/2.1.0 (Linux; U; Android 7.0; BV6000 Build/NRD90M)',
        'Host': 'api-duels.galapagosgames.com:8001',
    }

    data = '{"partId":"'+item_id+'","id":"'+uid+'"}'

    r = requests.post('http://api-duels.galapagosgames.com:8001/inventory/equip', headers=headers, data=data)
    j = json.loads(r.text)
    print(j)

def check_items(uid, items):
    for i in items:
        item = i['reward']
        try:
            print(item['__type'])
            if item['rarity']!='Legendary':
                print("disas item: "+item['__id'])
                dissasemble_item(uid, item['__id'])
        except:
            pass;

def delete_inventory(uid, login_id):
    u = game_login(login_id)
    #print(u)

    for i in u['profile']['inventory']['items']:
        item = i
        try:
            print(item['__id'])
            dissasemble_item(uid, item['__id'])
        except:
            pass;

def join_clan(uid, clan_id):
    headers = {
        'Expect': '100-continue',
        'Content-Type': 'application/json',
        'X-Unity-Version': '2018.2.14f1',
        'User-Agent': 'Dalvik/2.1.0 (Linux; U; Android 7.0; BV6000 Build/NRD90M)',
        'Host': 'api-duels-test.galapagosgames.com',
    }

    data = '{"clanId":"'+clan_id+'","id":"'+uid+'"}'

    r = requests.post('http://api-duels-test.galapagosgames.com/clans/join', headers=headers, data=data)
    j = json.loads(r.text)
    #print(j)

def leave_clan(uid):
    headers = {
        'Expect': '100-continue',
        'Content-Type': 'application/json',
        'X-Unity-Version': '2018.2.14f1',
        'User-Agent': 'Dalvik/2.1.0 (Linux; U; Android 7.0; BV6000 Build/NRD90M)',
        'Host': 'api-duels-test.galapagosgames.com',
    }

    data = '{"id":"'+uid+'"}'

    r = requests.post('http://api-duels-test.galapagosgames.com/clan/leave', headers=headers, data=data)
    j = json.loads(r.text)
    print(j)

def search_clans(uid: int) -> list:
    headers = {
        'Expect': '100-continue',
        'Content-Type': 'application/json',
        'X-Unity-Version': '2018.2.14f1',
        'User-Agent': 'Dalvik/2.1.0 (Linux; U; Android 7.0; BV6000 Build/NRD90M)',
        'Host': 'api-duels-test.galapagosgames.com',
    }

    data = '{"id":"'+uid+'"}'

    r = requests.post('http://api-duels-test.galapagosgames.com/clans/search', headers=headers, data=data)
    j = json.loads(r.text)
    clans = []
    for i in j['clans']:
        clans.append({'clan_id': i['_id'], 'members':[member['id'] for member in i['members']],'name':i['name']})
    return clans

def defeat_all_group(uid):
    c = 0
    have_place = True
    while(True):
        try:
            res = defeat_group(uid)
            if res==1:
                c+=1;
                print("defeated group number "+str(c))
                sleep(1);
                return True
            elif res==-1:
                return True
                #sleep(30)
            '''elif res==-1 and have_place==True:
                print("!!!! STARTING SPEND KEYS !!!!");
                buys = spend_all_keys_to_box(uid);
                if buys==-3:
                    print("!!!! DONT HAVE PLACE FOR ITEMS !!!!");
                    have_place = False;
                elif buys==-4:
                    print("!!!! DONT ENOUGH KEYS !!!! sleep 30")
                    sleep(30)'''
        except Exception as e:
            print(e)


def write_to_clan_chat(text: str, uid: int) -> bool:
    headers = {
        'Expect': '100-continue',
        'Content-Type': 'application/json',
        'X-Unity-Version': '2018.2.14f1',
        'User-Agent': 'Dalvik/2.1.0 (Linux; U; Android 7.0; BV6000 Build/NRD90M)',
        'Host': 'api-duels-test.galapagosgames.com',
    }

    data = '{"msg":"'+text+'","id":"'+str(uid)+'"}'

    response = requests.post('http://api-duels-test.galapagosgames.com/clan/write', headers=headers, data=data)

def get_clan_opponent(uid: int):
    headers = {
        'Expect': '100-continue',
        'Content-Type': 'application/json',
        'X-Unity-Version': '2018.2.14f1',
        'User-Agent': 'Dalvik/2.1.0 (Linux; U; Android 7.0; BV6000 Build/NRD90M)',
        'Host': 'api-duels-test.galapagosgames.com',
    }

    data = '{"chat":false,"id":"'+uid+'"}'

    r = requests.post('http://api-duels-test.galapagosgames.com/clan', headers=headers, data=data)
    j = json.loads(r.text)
    return j['clan']['war']['war'].get('opponentInfo', None)

def get_clan_info(uid: int, clan_id: int) -> list:
    headers = {
        'Expect': '100-continue',
        'Content-Type': 'application/json',
        'X-Unity-Version': '2018.2.14f1',
        'User-Agent': 'Dalvik/2.1.0 (Linux; U; Android 7.0; BV6000 Build/NRD90M)',
        'Host': 'api-duels-test.galapagosgames.com',
    }

    data = '{"clanId":"'+str(clan_id)+'","id":"'+str(uid)+'"}'

    r = requests.post('http://api-duels-test.galapagosgames.com/clan/info', headers=headers, data=data)
    j = json.loads(r.text)
    return j['members']

def clan_battle(uid: str):
    headers = {
        'Expect': '100-continue',
        'Content-Type': 'application/json',
        'X-Unity-Version': '2018.2.14f1',
        'User-Agent': 'Dalvik/2.1.0 (Linux; U; Android 7.0; BV6000 Build/NRD90M)',
        'Host': 'api-duels-test.galapagosgames.com',
    }

    data = '{"id":"'+str(uid)+'"}'

    r = requests.post('http://api-duels-test.galapagosgames.com/clan/war/battle', headers=headers, data=data)
    j = json.loads(r.text)
    print(j)
    if j.get('error', None) is not None:
        if j['error']['code']==150:
            print('Не хватает ключей')
            return -1
    else:
        return 1

def get_user_info(uid: int, info_user_id:int):
    headers = {
        'Expect': '100-continue',
        'Content-Type': 'application/json',
        'X-Unity-Version': '2018.2.14f1',
        'User-Agent': 'Dalvik/2.1.0 (Linux; U; Android 7.0; BV6000 Build/NRD90M)',
        'Host': 'api-duels-test.galapagosgames.com',
    }

    data = '{"playerId":"'+info_user_id+'","id":"'+uid+'"}'

    r = requests.post('http://api-duels-test.galapagosgames.com/profiles/details', headers=headers, data=data)
    j = json.loads(r.text)
    return j

def buy_keys(uid):
    headers = {
        'Expect': '100-continue',
        'Content-Type': 'application/json',
        'X-Unity-Version': '2018.2.14f1',
        'User-Agent': 'Dalvik/2.1.0 (Linux; U; Android 7.0; BV6000 Build/NRD90M)',
        'Host': 'api-duels-test.galapagosgames.com',
    }

    data = '{"sku":"duels_keys_15","receipt":"{\\"Store\\":\\"GooglePlay\\",\\"TransactionID\\":\\"GPA.3365-5976-8522-78444\\",\\"Payload\\":\\"{\\\\\\"json\\\\\\":\\\\\\"{\\\\\\\\\\\\\\"orderId\\\\\\\\\\\\\\":\\\\\\\\\\\\\\"GPA.3365-5976-8522-78444\\\\\\\\\\\\\\",\\\\\\\\\\\\\\"packageName\\\\\\\\\\\\\\":\\\\\\\\\\\\\\"com.deemedyainc.duels\\\\\\\\\\\\\\",\\\\\\\\\\\\\\"productId\\\\\\\\\\\\\\":\\\\\\\\\\\\\\"duels_keys_3\\\\\\\\\\\\\\",\\\\\\\\\\\\\\"purchaseTime\\\\\\\\\\\\\\":1551459081215,\\\\\\\\\\\\\\"purchaseState\\\\\\\\\\\\\\":0,\\\\\\\\\\\\\\"developerPayload\\\\\\\\\\\\\\":\\\\\\\\\\\\\\"{\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\"developerPayload\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\":\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\"\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\",\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\"is_free_trial\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\":false,\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\"has_introductory_price_trial\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\":false,\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\"is_updated\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\":false}\\\\\\\\\\\\\\",\\\\\\\\\\\\\\"purchaseToken\\\\\\\\\\\\\\":\\\\\\\\\\\\\\"fkjbpofapnbmikfbnbbjppmi.AO-J1OyI4h7GV42DyYB-1Aj0ZSMJkkmaHXco-LlDTlUFWASlpjUfGMfct2BFv2RTixnHyR_Tv7yvwydS_xZXrvTCg6n0m1UoVnKWSwtb5Fw2kKfiHExu36nq3mTPlh6ZDUicuiSGCIeJ\\\\\\\\\\\\\\"}\\\\\\",\\\\\\"signature\\\\\\":\\\\\\"E7h7M+hTO87a60yQ6MhBWBHM7M\\\\\\\\/xoJfPAB5k8YQ7cBfrLwnOY1MeMEw6L8yURcHa1PxBLd\\\\\\\\/5+mSx2WGsywJXrny4SWYJuf8GtNu6+t0kSuU\\\\\\\\/ptRZa6VXQDDwG4Yc3A2oGsCyVpSxKpLJkwmbwwgdJU447RsIOWwm6GI9k5hqCAuCEp4F1vFjm46GYmbflcJI016Ha1uAORTK\\\\\\\\/n9Pu5uo8yrbM1+COnU1ay5+5wG5dCVb\\\\\\\\/W1TFAnw10YR7spPOwmQE9k68TYYPr\\\\\\\\/ff\\\\\\\\/BN75n08hL\\\\\\\\/m80cKiEYWEonfe2g2Fn4l6hKMl9yR\\\\\\\\/cDsoly\\\\\\\\/j87bsrXu2LY3vqKmbMpZK4zyQ==\\\\\\",\\\\\\"skuDetails\\\\\\":\\\\\\"{\\\\\\\\\\\\\\"productId\\\\\\\\\\\\\\":\\\\\\\\\\\\\\"duels_keys_3\\\\\\\\\\\\\\",\\\\\\\\\\\\\\"type\\\\\\\\\\\\\\":\\\\\\\\\\\\\\"inapp\\\\\\\\\\\\\\",\\\\\\\\\\\\\\"price\\\\\\\\\\\\\\":\\\\\\\\\\\\\\"84,99\\u00a0\\u0433\\u0440\\u043d.\\\\\\\\\\\\\\",\\\\\\\\\\\\\\"price_amount_micros\\\\\\\\\\\\\\":84990000,\\\\\\\\\\\\\\"price_currency_code\\\\\\\\\\\\\\":\\\\\\\\\\\\\\"UAH\\\\\\\\\\\\\\",\\\\\\\\\\\\\\"title\\\\\\\\\\\\\\":\\\\\\\\\\\\\\"Mini Keys Pack (Duels)\\\\\\\\\\\\\\",\\\\\\\\\\\\\\"description\\\\\\\\\\\\\\":\\\\\\\\\\\\\\"Mini Keys Pack\\\\\\\\\\\\\\"}\\\\\\",\\\\\\"isPurchaseHistorySupported\\\\\\":true}\\"}","id":"5c420b52de661c681ff98f46"}'

    r = requests.post('http://api-duels-test.galapagosgames.com/shop/verify', headers=headers, data=data)
    j = json.loads(r.text)
    print(j)

#buy_keys(uid);

#toaster = ToastNotifier()
login_id = "5b3b1128-9f2a-40d9-9497-83bae2273abf"
enemy_id = "5c2cae0ba8682465060999d2"
gid = "5c50d49ad77998731cd202b5"
uid = "5c420b52de661c681ff98f46" ##MY ID
my_clan_id = '5c785db3bcfce62301705079'
clan_id = "5c785a80bcfce62301704d23"
item_id1 = "310f57fa-4bc7-4cf9-b091-92496764524f"
item_id2 = "8387cdf7-3448-4024-96a7-39c7a218212f"
#buy_keys(uid)
#print(game_login(login_id))
#delete_inventory(uid, login_id)
#get_clan_opponent(uid)
'''for i in range(0, 10, 1):
    for user in get_clan_info(uid, my_clan_id):
        opponent = get_clan_opponent(user['id'])
        if opponent is not None:
            res = clan_battle(user['id'])
            #if res == -1:
            #    defeat_all_group(user['id'])
            #    res = clan_battle(user['id'])
            #    print(res)'''
'''
while True:
    for n, user in enumerate(get_clan_info(uid, my_clan_id)):
        if n>0:
            print('started as')
            u_name = get_user_info(uid, user['id'])['player']['name']
            print(u_name)
            for i in range(0, 5, 1):
                print(defeat_group(user['id']))
                print('ключей сейчас: ')
            print('clan battle as')
            print(u_name)
            try:
                for i in range(0, 5, 1):
                    clan_battle(user['id'])
            except Exception as e:
                print(e)
'''
    #defeat_all_group(user['id'])
#buy_box(uid)
'''c = 0;
while(True):
    res = dung(uid);
    if res == True:
        c+=1;
    print(c)
    if c==20:
        exit()
'''
#leave_clan('5c308d6a9c4b034196099617')
#count = 0
'''for i in search_clans(uid):
    for m in i['members']:
        if count<10:
            leave_clan(m)
            join_clan(m, my_clan_id)
            count+=1
            print(count)
'''
#for i in range(0, 100, 1):
#    write_to_clan_chat("SORRY FOR THIS SHEIT !!!! ITS HACKER FROM RUSSIAN I WRITE ABOUT THIS BUG TO DEVELOPER!!!", uid)
#print(search_clans(uid))
#leave_clan(uid)
#print(get_group_info(uid))
#for i in get_group_info(uid)['group']['members']:
#    print(i['_id'])
#    join_clan(i['_id'], clan_id)
#print(game_login('adzxczxc'))
#join_clan(uid, clan_id)
#defeat_group(uid)

#equip_item(uid, item_id1)
#dung(uid);
#print(buy_keys(uid))
#while(True):
#    buy_box(uid)
#reroll_opponent(uid)
#print(get_loot_opponent(uid).to_primitive())
#print(get_group_info(uid))
#print(get_ranked_opponent(uid, "5bfa61208e8e1d0538b867ae", "5c501e80d77998731cd1b3f6"))



#check_items(uid, u['profile']['inventory']['items'])

def spend_all_keys_to_box(uid):pass




#spend_all_keys_to_box(uid)
#defeat_all_group(uid)
