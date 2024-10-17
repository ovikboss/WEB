import sqlite3 as sq

with sq.connect("C:\\Users\\ovikb\\Desktop\\проекты\\Flask\\WEB\\users.db",timeout=30,check_same_thread=False) as con:
    cur=con.cursor()
    cur.execute("""CREATE TABLE IF NOT EXISTS USERS(
       user_id INTEGER PRIMARY KEY,
       user_name CHAR(16),
       phonenum INTEGER,
       password CHAR(12),
       contact_coll  TEXT)
    """)

    def insert(name, password,phonenum):
        cur.execute("""INSERT INTO USERS (user_name,password,phonenum,contact_coll)VALUES(?,?,?,"")""",
                    (name,password,phonenum))
        con.commit()
    
    def select(username):
        cur.execute(""" SELECT * FROM USERS WHERE user_name = ?""",(username,))
        cnt = cur.fetchone()
        return cnt
    
    def checkpass(username,password):
        cur.execute(""" SELECT password FROM USERS WHERE user_name = ?""",(username,))
        cnt = cur.fetchone()
        if password == cnt[0]:
            return True
        else:
            return False
    
    def checklog(username):
        cur.execute(""" SELECT EXISTS(SELECT 1 FROM USERS WHERE user_name  = ?)""", (username,))
        cnt = cur.fetchone()
        if cnt != (0,):
            return True
        else:
            return False
        
    def dictlist(mytuple):
        if mytuple[4] is not None:
            con = mytuple[4].split("\n")
            print(mytuple)
            mydict = {"name":mytuple[1],"contact":con,"phonenum":mytuple[2]}
            return mydict
        else:
            return {"name":mytuple[1],"contact":"","phonenum":mytuple[2]}
        
    def update(name, contact):
        cur.execute("UPDATE USERS SET contact_coll = contact_coll || ? WHERE user_name = ?", (contact, name))
        con.commit()






