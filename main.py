#!/usr/bin/env python
#coding:UTF-8

## JSON出力（インデントあり）
## json.dumps(<result>,indent=4)

## Load Module ##
import sys
import requests
import json

## Set variable ##
argvs = sys.argv
email = '@day5.com'

method = 'http://'
address = 'localhost'
uri = '/api/v1/'
server = method + address + uri

## !!_Set YourID and YourToken_!! ##
admin_token = ''
admin_id = ''

##### HELP PART ####
def help_all():
    #### COMMANDS ####
    print ''
    print 'Usage: ./main.py [COMMAND] [OPTIONS]'
    print ''
    print 'Commands:'
    print ' info' + '\t\t'        + 'サーバー情報の表示'
    print ' login' + '\t\t'       + 'サーバーへログイン'
    print ' about' + '\t\t'       + 'ユーザー情報の表示'
    print ' msglist' + '\t'       + 'チャットルームのメッセージリストを表示'
    print ' userlist' + '\t'      + 'ユーザー数の表示'
    print ' usercreate' + '\t'    + 'ユーザーの作成'
    print ''

    #### OPTIONS ####
    print 'Options:'
    print ' -h, --help' + '\t' + '使い方の表示'
    print ''

def help_login():
    print ''
    print 'Usage: ./main.py login [username] [password]'
    print ''

def help_about():
    print ''
    print 'Usage: ./main.py about [X-Auth-Token] [X-User-id]'
    print ''

def help_userlist():
    print ''
    print 'Usage: ./main.py userlist [OPTIONS]'
    print ''
    print 'Options:'
    print ' -v' + '\t' + '詳細表示'
    print ''

def help_msglist():
    print ''
    print 'Usage: ./main.py msglist [roomId]'
    print ''

def help_usercreate():
    print ''
    print 'Usage: ./main.py usercreate [username] [password]'
    print ''
    print 'username' + '\t'  + 'ログインユーザー名'
    print 'password' + '\t'  + 'ログインパスワード'
    print ''

#### SHARED FUNCTION ####
def error():
    print 'エラーです.'
    print '引数で -h もしくは --help を指定し、使い方を確認してください.'

#### COMMAND:INFO ####
def info():
    url = server + 'info'

    #### CONNECT SERVER & PRINT RESULT ####
    result = requests.get(url).json()
    print 'Version:{}'.format(result['info']['version'])

#### COMMAND:LOGIN ####
def login(username,password):
    url = server + 'login'
    headers = {'Content-type': 'application/json'}
    payload = {
        'username': username,
        'password': password
    }
    
    print   'username: ' + username + '\n' \
        +   'password: ' + '*' * len(password) + '\n'

    #### CONNECT SERVER & PRINT RESULT ####
    result = requests.post(url,headers=headers,data=json.dumps(payload)).json()
    print 'Login: {}'.format(result['status'])
    print 'X-Auth-Token: {}'.format(result['data']['authToken'])
    print 'X-User-Id: {}'.format(result['data']['userId'])

#### COMMAND:about ####
def about(token,id):
    url = server + 'me'
    headers = {
        'Content-type': 'application/json',
        'X-Auth-Token': token,
        'X-User-Id': id
    }

    #### CONNECT SERVER & PRINT RESULT ####
    result = requests.get(url,headers=headers).json()
    print 'Username: {}'.format(result['username'])
    print 'Name: {}'.format(result['name'])
    print 'Id: {}'.format(result['_id'])

#### COMMAND:userlist ####
def userlist(debug):
    url = server + 'users.list'
    headers = {
            'Content-type': 'application/json',
            'X-Auth-Token': admin_token,
            'X-User-Id': admin_id
        }
    #### CONNECT SERVER & PRINT RESULT ####
    result = requests.get(url,headers=headers).json()
    print 'Count: {}'.format(result['count'])
    print 'Total: {}'.format(result['total'])

    #### OPTIONAL ####
    if debug:
        print ''
        print '#### USER LIST ####'
        for i in range(len(result['users'])):
            print result['users'][i]['name'] + '\t' + result['users'][i]['status']

#### COMMAND:msglist ####
def msglist(roomid):
    url = server + 'channels.history' + '?roomId=' + roomid + '&count=10000'
    headers = {
            'Content-type': 'application/json',
            'X-Auth-Token': admin_token,
            'X-User-Id': admin_id
    }
    result = requests.get(url,headers=headers).json()
    for i in range(len(result['messages'])-1,-1,-1):
        print result['messages'][i]['u']['username'] + '\t' + result['messages'][i]['msg']

#### COMMAND:usercreate ####
def usercreate(username,password):
    url = server + 'users.create'
    headers = {
            'Content-type': 'application/json',
            'X-Auth-Token': admin_token,
            'X-User-Id': admin_id
    }
    payload = {
        'email': username + email,
        'name': username,
        'username': username,
        'password': password
    }

    #### CONNECT SERVER & PRINT RESULT ####
    result = requests.post(url,headers=headers,data=json.dumps(payload)).json()
    success = format(result['success'])
    print 'Result: ' + success
    if success == 'True':
        #print 'Name: {}'.format(result['user']['name']) + '\t' + '# Display Name'
        print 'Login Username: {}'.format(result['user']['username'])
        print 'Login Password: ' + password

#### MAIN ####
try:
    if argvs[1] == '-h' or argvs[1] == '--help':
        help_all()

    elif argvs[1] == 'info':
            info()

    elif argvs[1] == 'login':
        if argvs[2] == '-h' or argvs[2] == '--help':
            help_login()
        else:
            login(argvs[2],argvs[3])
    
    elif argvs[1] == 'about':
        if argvs[2] == '-h' or argvs[2] == '--help':
            help_about()
        else:
            about(argvs[2],argvs[3])

    elif argvs[1] == 'userlist':
        if len(argvs) < 3:
            userlist(False)
        elif len(argvs) == 3:
            if argvs[2] == '-h' or argvs[2] == '--help':
                help_userlist()
            elif argvs[2] == '-v':
                userlist(True)

    elif argvs[1] == 'msglist':
        if len(argvs) == 3:
            if argvs[2] == '-h' or argvs[2] == '--help':
                help_msglist()
            else:
                msglist(argvs[2])

    elif argvs[1] == 'usercreate':
        if argvs[2] == '-h' or argvs[2] == '--help':
            help_usercreate()
        else:
            usercreate(argvs[2],argvs[3])
    else:
        error()
except:
    error()