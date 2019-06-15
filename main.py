#!/usr/bin/python
#coding:utf-8

import urllib.request as urllib2
import time
import json
friends=['Zzzyt','XIZCM','Who_is_IC']
submissions={}
for s in friends:
    submissions[s]=[]

while True:
    for p in friends:
        link='https://codeforces.com/api/user.status?handle=%s&from=1&count=5'%(p)
        js=urllib2.urlopen(link).read().decode('utf-8')
        #time.sleep(0.2)
        #print(js)
        result=json.loads(js)
        if result['status']!='OK':
            print('API Failed.')
        else:
            result=result['result'] 
            for sub in result:
                if not sub['id'] in submissions[p]:
                    print('%s has a new submission!Problem:%d%s '%(p,sub['problem']['contestId'],sub['problem']['index']),end='')
                    if sub['verdict']=='OK':
                        print('Accepted')
                    elif sub['verdict']=='COMPILATION_ERROR':
                        print('Compilation Error')
                    elif sub['verdict']=='TIME_LIMIT_EXCEEDED':
                        print('TLE on Test %d'%(sub['passedTestCount']+1))
                    elif sub['verdict']=='MEMORY_LIMIT_EXCEEDED':
                        print('MLE on Test %d'%(sub['passedTestCount']+1))
                    elif sub['verdict']=='WRONG_ANSWER':
                        print('WA on Test %d'%(sub['passedTestCount']+1))
                    else:
                        print('Other Verdict.')
                    submissions[p].append(sub['id'])

        time.sleep(0.2)
    time.sleep(5)
