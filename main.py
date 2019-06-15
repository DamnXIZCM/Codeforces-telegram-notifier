#!/usr/bin/python
#coding:utf-8

import urllib.request as urllib2
import time
import json
import telebot

TOKEN='BOT TOKEN'
bot=telebot.TeleBot(TOKEN)


submissions={}
friends=[]
admin_id=CHAT_ID

@bot.message_handler(commands=['start'])
def welcome(message):
    bot.reply_to(message,'Hello!')

@bot.message_handler(commands=['add'])
def add_friend(message):
    if message.chat.id!=admin_id:
        bot.send_message(message.chat.id,'Sorry, this bot is for private usage only.')
        return
    users=message.text.split()
    for i in range(1,len(users)):
        user=users[i]
        if(user in friends):
            pass
        else:
            url='https://codeforces.com/api/user.info?handles=%s'%(user)
            try:
                js=urllib2.urlopen(url).read().decode('utf-8')
            except:
                bot.reply_to(message,'Invalid username %s'%(user))
                continue
            friends.append(user)
            submissions[user]=[]
            bot.reply_to(message,'User %s added!'%(user))

@bot.message_handler(commands=['on'])
def goon(message):
    if message.chat.id!=admin_id:
        bot.send_message(message.chat.id,'Sorry, this bot is for private usage only.')
        return
    while True:
        for p in friends:
            link='https://codeforces.com/api/user.status?handle=%s&from=1&count=5'%(p)
            js=urllib2.urlopen(link).read().decode('utf-8')
            result=json.loads(js)
            if result['status']!='OK':
                print('API Failed.')
            else:
                result=result['result'] 
                for sub in result:
                    if not sub['id'] in submissions[p]:
                        submission_url='http://codeforces.com/contest/%d/submission/%d'%(sub['contestId'],sub['id'])
                        bot.send_message(message.chat.id,'%s has a new submission! Problem:%d%s '%(p,sub['problem']['contestId'],sub['problem']['index']))
                        if sub['verdict']=='OK':
                            bot.send_message(message.chat.id,'Accepted')
                            bot.send_message(message.chat.id,submission_url)
                        elif sub['verdict']=='COMPILATION_ERROR':
                            bot.send_message(message.chat.id,'Compilation Error')
                            bot.send_message(message.chat.id,submission_url)
                        elif sub['verdict']=='TIME_LIMIT_EXCEEDED':
                            bot.send_message(message.chat.id,'TLE on Test %d'%(sub['passedTestCount']+1))
                            bot.send_message(message.chat.id,submission_url)
                        elif sub['verdict']=='MEMORY_LIMIT_EXCEEDED':
                            bot.send_message(message.chat.id,'MLE on Test %d'%(sub['passedTestCount']+1))
                            bot.send_message(message.chat.id,submission_url)
                        elif sub['verdict']=='WRONG_ANSWER':
                            bot.send_message(message.chat.id,'WA on Test %d'%(sub['passedTestCount']+1))
                            bot.send_message(message.chat.id,submission_url)
                        else:
                            bot.send_message(message.chat.id,'Other Verdict.')
                            bot.send_message(message.chat.id,submission_url)
                        submissions[p].append(sub['id'])

            time.sleep(0.2)
        
        time.sleep(5)

bot.polling()
