import os
import ModTags   as FFM
import ModSqLite as Bs


try:
    BsR = Bs.GreateTable()
    if BsR != 'Ok':
        raise NameError("Проблемы с базой/таблицей: " + BsR)
    
    path = 'D:/YandexDisk/Lossless'
    for file in os.listdir(path):
        if file.endswith('.flac') or file.endswith('.mp3'):
            print('!',end = '')
            Da = (FFM.ReadFileTags(path, file))
        else:
            continue
        
        if Da['MessErr'] == 'Добро':
            BsR = Bs.InsertBase(Da)
            if BsR != 'Ok': print (BsR)
        else:
            continue
            
except Exception as ErrMs:
    print (ErrMs)

else: 
    print("Успешное завершение") 
#finally:
        #   

