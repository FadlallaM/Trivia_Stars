from sqlalchemy import create_engine
import os
import pandas as pd
from pandas.io import sql
import warnings

   
database_name = "leaderboard"
filetable_name = "leader_board.sql"
table_name = 'leader_board'  

#create sql if not exits 
os.system('mysql -u root -pcodio -e "CREATE DATABASE IF NOT EXISTS '+database_name+';"')
os.system("mysql -u root -pcodio "+database_name+" < " + filetable_name)
engine = create_engine('mysql://root:codio@localhost/'+database_name+'?charset=utf8', encoding='utf-8')



def addData_save(data):

  df = [] 

  #inserting data to sql table 
  id = 1
  
  col_names = ["ID", "Nickname", "score", "Time"]
  df_i = pd.DataFrame(columns = col_names)

  for player in data:
    nickname, score, time = player
    df_i.loc[len(df_i.index)] = [str(id), str(nickname), score, round(time, 4)]
   
    df.append(df_i)
    id+=1
  

  #save sql 
  for df_name in df:
    df_name.to_sql(table_name, con=engine, if_exists='replace', index=False)
  os.system('mysqldump -u root -pcodio '+database_name+' > '+ filetable_name)


def clearTables():
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        sql.execute('DROP TABLE IF EXISTS leader_board', engine)

# testing = [['name1', '7', '5:00'], ['name2', '5', '2:20'], ['name3', '2', '5:25'], ['name4', '51', '51:20']]
# addData_save(testing)

clearTables()