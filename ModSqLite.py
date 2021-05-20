import sqlite3
import ModTags as MTags
try:
    def ConnectBase():
        conn = sqlite3.connect('Music.db')
        # conn = sqlite3.connect(r'D:\Music.db')    

        cur = conn.cursor()
        cur.execute("""DROP TABLE IF EXISTS Tracks; """)
        cur.execute("""
            CREATE TABLE IF NOT EXISTS Tracks(
            Id INTEGER PRIMARY KEY AUTOINCREMENT 
            , Artist      TEXT 
            , Title       TEXT 
            , Locale      TEXT 
            , Genre       TEXT 
            , TrackNum    INTEGER 
            , TrackTell   INTEGER 
            , FileName    TEXT  
            , MessErr     TEXT  
            , DateInsert  CURRENT_TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL
            );
            """)
        conn.commit()
          # RealTime DateTime2(0) Not NULL default CURRENT_TIMESTAMP  
        return conn
        
    def InsertBase(Conn,Tags):
    
        cur = Conn.cursor()    
        cur.execute("INSERT INTO Tracks(Artist, Title, Locale, Genre, TrackNum, TrackTell, FileName, MessErr) VALUES(?,?,?,?,?,?,?,?);"
        ,(Tags.get('Artist',''), Tags.get('Title',''), Tags.get('Locale',''), Tags.get('Genre',''), Tags.get('TrackNum',''), Tags.get('TrackTell',''), Tags.get('FileName',''), Tags.get('MessErr','')))
        Conn.commit() 
        DataErr = sqlite3.DatabaseError.message
        print(DataErr)
        return

except sqlite3.DatabaseError as DataErr:
    print ("Ошибка Базы:" + str(DataErr))   

if __name__ == '__main__':
    print ("Тест модуля работы SQL Lite ")
    Cn = ConnectBase()
    Tn = MTags.ReadFileTags('','МКПН - Патиритилап.flac')
    # print(Tn['Artist'], Tn['Title'])
    InsertBase(Cn, Tn)
    Tn = MTags.ReadFileTags('','Валевская Н - Гага.mp3') 
    InsertBase(Cn, Tn)   
    Tn =  MTags.ReadFileTags('','Moscow Calling.mp3')     
    InsertBase(Cn, Tn)    
    # print (Cn)
    Cn.close()
