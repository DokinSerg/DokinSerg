import os
import FlacFileMod as FFM


try:
    
    path = 'D:/YandexDisk/Lossless'
    for file in os.listdir(path):

        if file.endswith(".flac"):
            Da = (FFM.ReadFlac(path, file))
        else:
            continue
        
        if Da['MessErr'] == 'Добро':
            cursor.execute("""
            INSERT INTO Tracks
            (Artist, Title, TrackNum, TrackTell, FileName, MessErr)
            VALUES (%s, %s, %d, %d, %s, %s) """
            , (Da['Artist'], Da['Title'],Da['TrackNum'], Da['TrackTell'],Da['FileName'], Da['MessErr']))
            # print(Da['Artist'], Da['Title'], )
    conn.commit()
except Exception as ErrMs:
    print (ErrMs)

else: 
    conn.close() 
    print("Успешное завершение") 
#finally:
        #   

