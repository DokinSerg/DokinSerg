import sqlite3
import ModTags as MTags
# dbName = 'Music.db'
# tbName = 'Tracks'

def GreateTable() -> str:
    GT = ()
    try:
        conn = sqlite3.connect('Music.db')
        # cur = conn.cursor()
        conn.execute("""DROP TABLE IF EXISTS Tracks; """)
        conn.execute("""
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
    except sqlite3.Warning as Warn: 
        GT = Warn
    except sqlite3.Error as DErr:
        GT = DErr
    else:
        conn.commit()
        conn.close()         
        GT = 'Ok'
    # finally:    
        # print (Warn)
    return GT
        
def InsertBase(Tags) ->str :
    IB = ''
    try:    
        conn = sqlite3.connect('Music.db')    
        # cur = Conn.cursor()    
        conn.execute("INSERT INTO Tracks(Artist, Title, Locale, Genre, TrackNum, TrackTell, FileName, MessErr) VALUES(?,?,?,?,?,?,?,?);"
        ,(Tags.get('Artist',''), Tags.get('Title',''), Tags.get('Locale',''), Tags.get('Genre',''), Tags.get('TrackNum',''), Tags.get('TrackTell',''), Tags.get('FileName',''), Tags.get('MessErr','')))
        conn.commit() 
    except sqlite3.Warning as Warn: 
       IB = Warn
    except sqlite3.Error as DErr:
        IB = DErr
    else:
        conn.commit()
        conn.close()         
        IB = 'Ok'
    # finally:    
        # print (Warn)
    return IB

if __name__ == '__main__':
    print ("Тест модуля работы SQL Lite ")
    Tn = GreateTable()
    if Tn =='Ok':
        InsertBase(MTags.ReadFileTags('','Валевская Н - Гага.mp3'))   
        InsertBase(MTags.ReadFileTags('','Moscow Calling.mp3'))    
    else:
        print('Проблемы с созданием базы/таблицы', Tn)
    
