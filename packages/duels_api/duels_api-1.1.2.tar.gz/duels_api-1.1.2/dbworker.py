import sqlite3
import os.path
import time
import json
import datetime

def store_user(user_id, stats):
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(BASE_DIR, "users.sqlite")
    con = sqlite3.connect(db_path, check_same_thread=False)

    #print(con)
    cur = con.cursor()
    sql_command = "insert into users(id, stats) values('{}','{}')".format(user_id, json.dumps(stats.to_primitive()))
    #print(sql_command)
    try:
        cur.execute(sql_command)
    except:
        pass
    con.commit()
    con.close()

#store_user('1','1')

def set_lang(user_id, locale):
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(BASE_DIR, "bot_users.sqlite")
    con = sqlite3.connect(db_path, check_same_thread=False)

    #print(con)
    cur = con.cursor()
    cur.execute("select lang from users_state where id={}".format(int(user_id)))
    val=cur.fetchall()
    if len(val)<=0:
        cur.execute("insert into users_state(id, lang) values({},{})".format(int(user_id), locale))
    else:
        cur.execute('update users_state set lang = "{}" where id = {}'.format(locale,int(user_id)))
    con.commit()
    con.close()

def get_lang(user_id):
    #print(user_id)
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(BASE_DIR, "bot_users.sqlite")
    con = sqlite3.connect(db_path, check_same_thread=False)

    #print(con)
    cur = con.cursor()
    cur.execute("select lang from users_state where id={}".format(int(user_id)))
    value=cur.fetchall()
    con.close()
    if len(value)>0:
        return list(list(value)[0])[0]
    else:
        return "ru";

#set_lang(383492784,"ru")
#print(get_lang(383492784))#, "ru")

def get_user_list():
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(BASE_DIR, "bot_users.sqlite")
    con = sqlite3.connect(db_path, check_same_thread=False)

    #print(con)
    cur = con.cursor()
    sql_command = "SELECT id from users_state"
    cur.execute(sql_command)
    value=cur.fetchall()
    con.close()
    return value;

#get_user_list()
def get_unsolved(user_id):
    print(user_id)
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(BASE_DIR, "bot_users.sqlite")
    con = sqlite3.connect(db_path, check_same_thread=False)

    #print(con)
    cur = con.cursor()
    cur.execute("select not_solved from users_state where id={}".format(int(user_id)))
    value=cur.fetchall()
    con.close()
    if len(value)>0:
        return list(list(value)[0])[0]
    else:
        return 0;

def get_solved(user_id):
    print(user_id)
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(BASE_DIR, "bot_users.sqlite")
    con = sqlite3.connect(db_path, check_same_thread=False)

    #print(con)
    cur = con.cursor()
    cur.execute("select solved from users_state where id={}".format(int(user_id)))
    value=cur.fetchall()
    con.close()
    if len(value)>0:
        return list(list(value)[0])[0]
    else:
        return 0;

#print(get_solved(1))

def update_solved(user_id):
    print(user_id)
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(BASE_DIR, "bot_users.sqlite")
    con = sqlite3.connect(db_path, check_same_thread=False)

    #print(con)
    cur = con.cursor()
    cur.execute("select state from users_state where id={}".format(int(user_id)))
    value=cur.fetchall()
    if len(value)<=0:
        cur.execute("insert into users_state(id,state) values({},{})".format(int(user_id),int(0)))
        con.commit()
    sql_command = "UPDATE users_state SET solved = solved + 1 WHERE id = {}".format(int(user_id))
    print(sql_command)
    cur.execute(sql_command)
    con.commit()
    con.close()

def update_unsolved(user_id):
    print(user_id)
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(BASE_DIR, "bot_users.sqlite")
    con = sqlite3.connect(db_path, check_same_thread=False)

    #print(con)
    cur = con.cursor()
    cur.execute("select state from users_state where id={}".format(int(user_id)))
    value=cur.fetchall()
    if len(value)<=0:
        cur.execute("insert into users_state(id,state) values({},{})".format(int(user_id),int(0)))
        con.commit()
    sql_command = "UPDATE users_state SET not_solved = not_solved + 1 WHERE id = {}".format(int(user_id))
    print(sql_command)
    cur.execute(sql_command)
    con.commit()
    con.close()

#update_unsolved(2)

def get_state(user_id):
    print(user_id)
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(BASE_DIR, "bot_users.sqlite")
    con = sqlite3.connect(db_path, check_same_thread=False)

    #print(con)
    cur = con.cursor()
    cur.execute("select state from users_state where id={}".format(int(user_id)))
    value=cur.fetchall()
    #print(list(list(value)[0])[0])
    if len(value)<=0:
        cur.execute("insert into users_state(id,state) values({},{})".format(int(user_id),int(0)))
        con.commit()
        con.close()
    else:
        #time.sleep(1)
        con.close();
        return list(list(value)[0])[0]

# Сохраняем текущее «состояние» пользователя в нашу базу
def set_state(user_id, value):
    #print(user_id,value)
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(BASE_DIR, "bot_users.sqlite")
    con = sqlite3.connect(db_path, check_same_thread=False)

    #print(con)
    cur = con.cursor()
    cur.execute("select state from users_state where id={}".format(int(user_id)))
    val=cur.fetchall()
    if len(val)<=0:
        cur.execute("insert into users_state(id,state) values({},{})".format(int(user_id), int(value)))
    else:
        cur.execute("update users_state set state = {} where id = {}".format(int(value),int(user_id)))
    con.commit()
    con.close()

#set_state(1,6)

#print(get_state(1))
