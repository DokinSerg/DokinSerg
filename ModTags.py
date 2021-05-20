"""MOD Tags модуль содержит функции для чтение тегов из различных медиа файлов"""
# pylint: disable=trailing-whitespace
# pylint: disable=invalid-name
# pylint: disable=line-too-long
# pylint: disable=superfluous-parens
# pylint: disable=global-statement

import os
FileStruckt = dict() 

def ReadFlac(Fn):
    "Эта фунция по поиску и чтению тегов Vorbis из файла типа FLAC"
    global FileStruckt
    Tbuff:bytes = Fn.read(4)  # читаем заголовок блока
    
    while int(Tbuff[0]) < 6:
        offset:int = int.from_bytes(Tbuff[1:], byteorder='big')
        Fn.seek(offset, 1)  # смещаем указатель файла, относительно текущего положения
        Tbuff = Fn.read(4)  # читаем заголовок блока
        if int(Tbuff[0]) == 4:
            break
        else:
            raise NameError("Блок Vorbis Tegs не найден")
        # Это общий размер блока
        
    buff:bytes  = Fn.read(4) # Читаем "вектор слова      
    LineSize:int = int.from_bytes(buff, byteorder = 'little') #младшим вперед, тут всё через ворбис
    buff  = Fn.read(LineSize) # Читаем программа создатель тегов   
    buff  = Fn.read(4) # Читаем "вектор слова      
    Cycle = int.from_bytes(buff, byteorder = 'little') # получили количество тегов в блоке
    ic:int = 0 
    for ic in range(Cycle): #теперь цикл
        TrTell = Fn.tell()     
        buff  = Fn.read(4) # Читаем "вектор слова
        LineSize = int.from_bytes(buff, byteorder = 'little')
        buff  = Fn.read(LineSize) # Читаем "вектор слова 
        LineStr = buff.decode() # декодируем байтовую стоку в текст Genre
        LineStr = LineStr.title() # строка с заглавной буквы
        #assert len(LineStr) == 0,  buff
        if LineStr.startswith('Artist='):
            tstr = LineStr.removeprefix('Artist=')
            FileStruckt['Artist'] = tstr.title()
            continue 
            
        if LineStr.startswith('Title='):
            tstr = LineStr.removeprefix('Title=')
            FileStruckt['Title'] = tstr.title()
            continue
            
        if LineStr.startswith('Locale='):
            tstr = LineStr.removeprefix('Locale=')
            FileStruckt['Locale'] = tstr.title()
            continue 
            
        if LineStr.startswith('Genre='):
            tstr = LineStr.removeprefix('Genre=')
            FileStruckt['Genre'] = tstr.title()
            continue              
                
        if LineStr.startswith('Tracknumber='):
            tstr = LineStr.removeprefix('Tracknumber=')
            FileStruckt['TrackNum']  = int(tstr)
            FileStruckt['TrackTell'] = TrTell
            continue
    return  

def TagDecode(barr: bytes) ->str:
    Br:str
    if barr[0] == 0:
        if int(barr[-1]) == 0:
            Br = (barr[1:-1].decode())
        else:
            Br = (barr[1:].decode())        
    elif barr[0] == 1:
        if int(barr[-2]) == 0:
            Br = barr[1:-2].decode(encoding = 'utf_16')
        else: 
            Br = barr[1:].decode(encoding = 'utf_16')
    else:
        Br = 'Неизвестная кодировка'
    return(Br)
 
def ReadID3(Fn):
    "Эта фунция по поиску и чтению тегов ID3 из разных файлов"

    global FileStruckt
    Tbuff = Fn.read(2)  # минор версия и флага, ничего интересного
    Tbuff = Fn.read(1)  # 1-й, старший байт размера
    At =int.from_bytes(Tbuff + b'\x00\x00\x00', byteorder = 'big') >> 3 # раздвигаем до 4-х байт
    # преобразуем в инт и сдвигаем на 3 бита, для компенсации 7-битного формата
    Tbuff = Fn.read(1)  # 2-й байт размера
    Bt =int.from_bytes(Tbuff + b'\x00\x00', byteorder = 'big') >> 2 
    Tbuff = Fn.read(1)  # 3-й байт размера
    Ct =int.from_bytes(Tbuff + b'\x00', byteorder = 'big') >> 1   
    Tbuff = Fn.read(1)  # 4-й, младший байт размера
    Dt =int.from_bytes(Tbuff , byteorder = 'big')  
    #print (Tbuff,Tbuff + b'\x00',Dt, Dt.to_bytes(4, 'big').hex(' ') )   
    Dt = Dt + Ct + Bt + At - 10
    It = 0
    while It <= Dt:
        TrTell = Fn.tell()     
        buff = Fn.read(4)  # Заголовок кадра
        LineStr = buff.decode() # в строку
        Tbuff = Fn.read(4) # Размер кадра
        buff = Fn.read(2)  # Флаги, не используем     
        offset = int.from_bytes(Tbuff, byteorder='big')
        buff = Fn.read(offset)  # Кадр
        It += offset + 10 # ведем подсчет считанных байт дабы не вылететь за размер]
        if LineStr == 'TPE1':
            FileStruckt['Artist'] = TagDecode(buff).strip(' ')           
            continue
        if LineStr == 'TIT2':
            FileStruckt['Title'] = TagDecode(buff).strip(' ')            
            continue
        if LineStr == 'TRCK':
            Tmp = TagDecode(buff).split(sep = '/', maxsplit = 1)
            FileStruckt['TrackNum']  = int(Tmp[0])
            FileStruckt['TrackTell'] = TrTell          
            continue            
        # if LineStr in ( 'TALB','TIT1', 'TIT3', 'TPE3',  ):  # Анализ заголовка
            # print(LineStr,'/',offset, ' = ', TagDecode(buff)) #  ): 
            # continue
    if (not (('Artist' in FileStruckt) and ('Title'in FileStruckt) and ('TrackNum' in FileStruckt))):        
        Fn.seek(-128, 2)    
        Tbuff = Fn.read(3)
        if Tbuff != b'TAG':
            raise NameError("Блок ID3v1 не найден")
        else:
            buff = Fn.read(30)
            if 'Title' not in FileStruckt:
                Tt = buff.strip(b'\x00')     
                FileStruckt['Title'] = buff.decode('cp1251')
                #print (Fn.tell().to_bytes(4, 'big').hex(' '),' = ',Tt.decode('cp1251'))   
            buff = Fn.read(30)
            if 'Artist' not in FileStruckt:
                Tt = buff.strip(b'\x00')    
                FileStruckt['Artist'] = buff.decode('cp1251')                
            buff = Fn.read(30)  # Album             
            buff = Fn.read(32)  # Year(4) + Note(28)
            buff = Fn.read(1)
            if (buff == 0) and ('TrackNum' not in FileStruckt):
                FileStruckt['TrackTell'] = Fn.tell()
                buff = Fn.read(1)
                FileStruckt['TrackNum']  = int(buff[0])
                #print(Fn.tell().to_bytes(4, 'big').hex(' '),' = ',int(buff[0]))
    return
    
def ReadFileTags(PathName: str, FlName: str) -> dict:
    global FileStruckt
    FileStruckt = dict()   
    FileStruckt['FileName'] = FlName    # Это уже словарь, поехали заполнять 
    try: 
        if PathName != '': 
            FlName = os.path.join(PathName, FlName)
        Fln = open(FlName, mode = 'r+b')
        Tbuff = Fln.read(4)
        if Tbuff == b'fLaC':
            FileStruckt['TypeTags'] = "FLAC"
            ReadFlac(Fln) 
        elif Tbuff == b'ID3\x03':
            FileStruckt['TypeTags'] = "ID3"
            ReadID3(Fln)            
        else:    
            raise NameError("Неизвестный тип файла: " + ascii(Tbuff))

    except OSError as ErrMs:
        FileStruckt['MessErr'] = str(ErrMs)      
    except Exception as ErrMs:
        FileStruckt['MessErr'] = str(ErrMs)
        Fln.close()           
    else:
        FileStruckt['MessErr'] = "Добро"
        Fln.close()          
    return FileStruckt

def WriteFlac(PathName: str, FlName: str, FileStruckt: dict ) -> dict(): 
    "Эта фунция по записи тегов Vorbis в файл типа FLAC"
    pass

if __name__ == '__main__':
    print ("Тест функция ReadFlac() ")
    print (ReadFileTags('','МКПН - Патиритилап.flac'))
    print (ReadFileTags('','Валевская Н - Гага.mp3'))   
    print (ReadFileTags('','Moscow Calling.mp3'))      
    print ("Функции WriteFlac() не готова")    
