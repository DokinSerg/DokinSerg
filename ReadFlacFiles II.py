def ReadFlac(FlName: str) -> dict():
    FileStruckt = dict()   
    FileStruckt['FileName'] = FlName    # Это уже словарь, поехали заполнять, 
    try:
        Fn = open(FlName, mode = 'r+b')    
        Tbuff = Fn.read(4)
        if Tbuff != b'fLaC':
            raise NameError("Not FLAC File: " + ascii(Tbuff))
            #print("Not FLAC File: " + ascii(Tbuff))
            # Fn.close() 
            # exit()
        
        Tbuff = Fn.read(4) # читаем заголовок блока
        while int(Tbuff[0]) < 6:
            offset = int.from_bytes(Tbuff[1:],byteorder='big')
            Fn.seek(offset,1) # смещаем указатель файла, относительно текущего положения
            Tbuff = Fn.read(4) # читаем заголовок блока
            if int(Tbuff[0]) == 4:
                break
        else:
            #print("Блок Vorbis Tegs не найден")
            #FileStruckt['MessErr'] = "Блок Vorbis Tegs не найден" 
            raise NameError("Блок Vorbis Tegs не найден")           

        BlockSize = int.from_bytes(Tbuff[1:], byteorder = 'big')   # отбрасываем байт "0" и берем байты "1,2,3" старшим вперед, 
        # Это общий размер блока
        buff  = Fn.read(4) # Читаем "вектор слова      
        LineSize = int.from_bytes(buff, byteorder = 'little') #младшим вперед, тут всё через ворбис
        buff  = Fn.read(LineSize) # Читаем программа создатель тегов   
        #print(buff.decode())         
        
        buff  = Fn.read(4) # Читаем "вектор слова      
        Cycle = int.from_bytes(buff, byteorder = 'little') # получили количество тегов в блоке
      
        for ic in range(Cycle): #теперь цикл
            TrTell = Fn.tell()     
            buff  = Fn.read(4) # Читаем "вектор слова
            LineSize = int.from_bytes(buff, byteorder = 'little')
            buff  = Fn.read(LineSize) # Читаем "вектор слова 
            LineStr = buff.decode()
            LineStr = LineStr.title()
            if LineStr.startswith('Artist='):
                tstr = LineStr.removeprefix('Artist=')
                FileStruckt['Artist'] = tstr.title()
                continue 
            
            if LineStr.startswith('Title='):
                tstr = LineStr.removeprefix('Title=')
                FileStruckt['Title'] = tstr.title()
                continue
                
            if LineStr.startswith('Tracknumber='):
                tstr = LineStr.removeprefix('Tracknumber=')
                FileStruckt['TrackNum']  = int(tstr)
                FileStruckt['TrackTell'] = TrTell
                continue
    except OSError as ErrMs:
        FileStruckt['MessErr'] = str(ErrMs)      
    except Exception as ErrMs:
        FileStruckt['MessErr'] = str(ErrMs)
        Fn.close()           
        #print("offset=",hex(offset)," :  Buff=", Tbuff, buff) #int.from_bytes(Tbuff[1:],byteorder='big'))  
    else:
        FileStruckt['MessErr'] = "Добро"
        Fn.close()          
    # finally:
        # print (FileStruckt)   
    return FileStruckt
    
    
import os
for file in os.listdir('D:\YandexDisk\Python\Study\FileFlacRead'):
    #print(file)
    if 2==2: # file.endswith(".flac"):
        Da = (ReadFlac(file))
        if 1==1 :# Da['MessErr'] == 'Добро':
            print(Da)
 
