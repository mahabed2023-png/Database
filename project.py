import sqlite3

db= sqlite3.connect("app.db")

cr = db.cursor()

def Commit_and_closed():
    
  db.commit()
 
  db.close()
 
  print("Datebesa it closed")

uid =1

input_masseg = """
What do you want to do ?
"s"=> Show all skills
"a"=> Add skils
"d"=> Delete skills
"u"=> Updete skiils
"q"=> Quite datebase
choos Opsion: 
"""


def Show_skills():
    
  cr.execute(f"select * from skiles where user_id = '{uid}'")
  
  result =cr.fetchall()
  
  if len(result) > 0:
    
    print(f"you have {len(result)} Skills.")
  
  print("your skills it : ")
  
  for row in result:
      
      print(f"Skill=> {row[0]},",end=" ")
      print(f"progress=> {row[1]}%")
  
  Commit_and_closed()
 
def add_skills():
    
  sk = input("write skill name :").strip().capitalize()
  
  cr.execute(f"select name from skiles where name ='{sk}' and user_id = '{uid}'")
  
  result =cr.fetchone()
  
  if result == None :
    
    prog= input("write skill progress :").strip()
  
    cr.execute(f"insert into skiles(name,progress,user_id) values('{sk}','{prog}','{uid}')")
    
  else:
      
    print("the skill it exsest")
 
  Commit_and_closed()

def delete_skills():
    
  sk = input("write skill name :").strip().capitalize()
    
  
  cr.execute(f"delete from skiles where name = '{sk}' and user_id = '{uid}'")
  
  Commit_and_closed()

def updete_skills():
    
 sk = input("write skill name :").strip().capitalize()
    
 prog= input("write skill progress :").strip()
  
 cr.execute(f"update skiles set progress ='{prog}' where name ='{sk}' and user_id = '{uid}'")

 Commit_and_closed()
  

user_input= input(input_masseg).strip().lower()

commeds_list=["s","a","d","u","q"]

  
if user_input in commeds_list :
   
    print(f"coomend founed{user_input}") 
   
    if user_input == "s":
       
       Show_skills()
       
    elif user_input == "a":
       
       add_skills()
       
    elif user_input == "d":
       
      delete_skills()
      
    elif user_input == "u":
       
       updete_skills()  
    
    else:    
        
        print("it Closed.")
         
else:
    print(f"Sorry commed not founed \"{user_input}\"")