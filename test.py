# -*- coding: utf-8 -*-

import os, tarfile, json, time, jieba, datetime, unicodedata
from os import listdir
from collections import Counter

#start time stamp
st=time.time()
print('Start Timestamp: {:%Y-%m-%d %H:%M:%S}'.format(datetime.datetime.now()))
#Constants
MK_KEYWORDS=["michael kors","mk","michaelkors"]
KS_KEYWORDS=["kate spade","katespade"]
OVERSEAS=u"海外"
OTHER=u"其他"

EXCLUDE_LIST = "\"? \"-cn，。！？：；［］~_@回复链接的了哦亲好吗呢你我是啊啦很?～· \\\/[]:.  http".decode('utf-8')

#Variables
results_dict={"mk":{"users":[],"posts":[], "dates":[], "hours":[], "locations":[], "key_words":[]},"ks":{"users":[],"posts":[],"dates":[],"hours":[],"locations":[], "key_words":[]}}
users_dict={}
counts={"comments":0,"reposts":0,"statuses":0}

#helper function

def numKeys(dict):
    return len(dict.keys())

def filterDict(dict):
    new_dict={}
    
    for k in dict:
        if numKeys(dict[k])>3:
            new_dict[k]=dict[k]
            
    return new_dict

#load dataset
if os.path.exists("weibo"):
    print 'already extracted'
else:
    tfile=tarfile.open("weibo_dataset.tar.gz","r:gz")

    tfile.extractall('.')
    print 'data extracted'
    
folders=os.listdir("weibo")


#analysis
for folder in folders:
    if not folder.startswith('.'):
        directories=os.listdir("weibo/"+folder)
        for date_folder in directories:
            
            if not date_folder.startswith('.'):
                file_list={}
                file_list[date_folder]=(os.listdir("weibo/"+folder+"/"+date_folder))
                
                for files in file_list[date_folder]:
                    if not files.startswith('.'):
                        json_data=open("weibo/"+folder+"/"+date_folder+"/"+files).read()
                        
                        data=json.loads(json_data)
                        
                        #Michael Kors
                        condition=False
                        #check if the post contains Michael Kors
                        if folder=='comments':
                            condition=any(key_words in data["text"].lower() for key_words in MK_KEYWORDS) or any(key_words in data["status"]["text"].lower() for key_words in MK_KEYWORDS )
                        elif folder=='reposts':
                            any(key_words in data["text"].lower() for key_words in MK_KEYWORDS)
                        elif folder=='statuses':
                            any(key_words in data["text"].lower() for key_words in MK_KEYWORDS)
                            
                        if condition:
                        
                            #Get post ID, Date, Hours
                            results_dict["mk"]["posts"].append(data["id"])
                            results_dict["mk"]["dates"].append(date_folder)
                            results_dict["mk"]["hours"].append(data["created_at"].split()[3][0:2])
                            
                            #Get user location
                            if data["user"]["location"].split()[0]==OVERSEAS and len(data["user"]["location"].split())>1:
                                results_dict["mk"]["locations"].append(data["user"]["location"].split()[1])                     
                            else:
                                results_dict["mk"]["locations"].append(data["user"]["location"].split()[0])
                                
                            #Get user ID    
                            if not data['user']['id'] in results_dict["mk"]["users"]:
                                results_dict["mk"]["users"].append(data['user']['id'] )
                            
                            #Get key words
                            seg_list=jieba.lcut(data["text"],cut_all=False)
                            filer_seg = [fil for fil in seg_list if fil not in EXCLUDE_LIST]
                            
                            results_dict["mk"]["key_words"]=results_dict["mk"]["key_words"]+filer_seg
                            
                            if data['user']['id'] in users_dict and "mk" in users_dict[data['user']['id']]:                               
                                users_dict[data['user']['id']]["mk"]=users_dict[data['user']['id']]["mk"]+1
                                users_dict[data['user']['id']]["mk_comments"].append(data["text"])
                            else:
                                if not data['user']['id'] in users_dict:
                                    users_dict[data['user']['id']]={"mk":1,"mk_comments":[data["text"]]}
                                else:
                                    users_dict[data['user']['id']]["mk"]=1
                                    users_dict[data['user']['id']]["mk_comments"]=[data["text"]]
                                                                
                        #Kate Spade       
                        condition=False
                        #check if the post contains Kate Spade
                        if folder=='comments':
                            condition=any(key_words in data["text"].lower() for key_words in KS_KEYWORDS) or any(key_words in data["status"]["text"].lower() for key_words in KS_KEYWORDS )
                        elif folder=='reposts':
                            any(key_words in data["text"].lower() for key_words in KS_KEYWORDS)
                        elif folder=='statuses':
                            any(key_words in data["text"].lower() for key_words in KS_KEYWORDS)
                            
                        if condition:
                            
                            #Get post ID, Date, Hours
                            results_dict["ks"]["posts"].append(data["id"])
                            results_dict["ks"]["dates"].append(date_folder)
                            results_dict["ks"]["hours"].append(data["created_at"].split()[3][0:2])
                            
                            #Get user location
                            if data["user"]["location"].split()[0]==OVERSEAS and len(data["user"]["location"].split())>1:
                                results_dict["ks"]["locations"].append(data["user"]["location"].split()[1])
                            else:
                                results_dict["ks"]["locations"].append(data["user"]["location"].split()[0])
                            
                            #Get user ID
                            if not data['user']['id'] in results_dict["ks"]["users"]:
                                results_dict["ks"]["users"].append(data['user']['id'] )
                            
                            #Get post key words    
                            seg_list=jieba.lcut(data["text"],cut_all=False)
                            filer_seg = [fil for fil in seg_list if fil not in EXCLUDE_LIST]
                            results_dict["ks"]["key_words"]=results_dict["ks"]["key_words"]+filer_seg
                            
                            if data['user']['id'] in users_dict and "ks" in users_dict[data['user']['id']]:
                                users_dict[data['user']['id']]["ks"]=users_dict[data['user']['id']]["ks"]+1
                                users_dict[data['user']['id']]["ks_comments"].append(data["text"])
                            else:
                                if not data['user']['id'] in users_dict:
                                    users_dict[data['user']['id']]={"ks":1,"ks_comments":[data["text"]]}
                                else:
                                    users_dict[data['user']['id']]["ks"]=1
                                    users_dict[data['user']['id']]["ks_comments"]=[data["text"]]
                            
                        counts[folder]=counts[folder]+1

#filter users who comments both Kate spade and Michael Kors
new_dict=filterDict(users_dict)
                        
#sort data
results_dict["mk"]["posts"]=sorted(results_dict["mk"]["posts"])
results_dict["mk"]["users"]=sorted(results_dict["mk"]["users"])
results_dict["ks"]["posts"]=sorted(results_dict["ks"]["posts"])
results_dict["ks"]["users"]=sorted(results_dict["ks"]["users"])

#output results
print "number of Michael Kors post: " +str(len(results_dict["mk"]["posts"]))
print "number of unique users who mentioned Michael Kors: "+str(len(results_dict["mk"]["users"]))


print "top date: "+str(Counter(results_dict["mk"]["dates"]).most_common(1))
print "peak hour: "+str(Counter(results_dict["mk"]["hours"]).most_common(1))
print "top 10 locations: "
mk_locations=Counter(results_dict["mk"]["locations"]).most_common(10)
for loc in mk_locations:
    print loc[0].encode('utf-8')+' : '+str(loc[1])

mk_key_words=Counter(results_dict["mk"]["key_words"]).most_common(10)
print "top 10 key words: " 
for key_words in mk_key_words:
    print key_words[0].encode('utf-8')+' : '+str(key_words[1])

print "number of Kate Spade post: "+str(len(results_dict["ks"]["posts"]))
print "number of unique users who mentioned Kate Spade: "+str(len(results_dict["ks"]["users"]))     
print "top date: "+str(Counter(results_dict["ks"]["dates"]).most_common(1))
print "peak hour: "+str(Counter(results_dict["ks"]["hours"]).most_common(1))

print "top 10 locations: "
ks_locations=Counter(results_dict["ks"]["locations"]).most_common(10)
for loc in ks_locations:
    print loc[0].encode('utf-8')+' : '+str(loc[1])

print "top 10 key words: "     
ks_key_words=Counter(results_dict["ks"]["key_words"]).most_common(10)
 
for key_words in ks_key_words:
    print key_words[0].encode('utf-8')+' : '+str(key_words[1])
    
print "analyzed the following "+str(counts)

#end time stamp
et=time.time()
print('End Timestamp: {:%Y-%m-%d %H:%M:%S}'.format(datetime.datetime.now()))
print 'analysis took '+str(int(et-st))+' seconds.'