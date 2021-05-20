
import pymssql

# try:
def OpenBaseSQL()  
    conn = pymssql.connect(
        #server   = 'localhosts', 
        server   = r'DokinPC',    
        user     = 'sa',
        password = 'Og5022Rn',
        database = 'Music')
 return       
 
def NewTable()
    cursor = conn.cursor(as_dict=True)
    cursor.execute("""
        IF OBJECT_ID('Tracks', 'U') IS NOT NULL Truncate Table Tracks
        else
        CREATE TABLE Tracks (
        id INT IDENTITY (1,1) PRIMARY KEY,
        Artist nVARCHAR(127),
        Title  nVARCHAR(127),
        TrackNum Int,
        TrackTell Int,
        FileName nVARCHAR(255),
        MessErr  nVARCHAR(255),
        RealTime DateTime2(0) Not NULL default CURRENT_TIMESTAMP )
        """)    

    conn.commit()
return    
    
def     
            cursor.execute("""
            INSERT INTO Tracks
            (Artist, Title, TrackNum, TrackTell, FileName, MessErr)
            VALUES (%s, %s, %d, %d, %s, %s) """
            , (Da['Artist'], Da['Title'],Da['TrackNum'], Da['TrackTell'],Da['FileName'], Da['MessErr']))
            # print(Da['Artist'], Da['Title'], )
    conn.commit()    
    
except pymssql.StandardError as DataErr:
    print ("Ошибка Базы:" + str(DataErr))    