import os
for file in os.listdir('D:\YandexDisk\Python\Study\FileFlacRead'):
    if file.endswith(".flac"):
        print(file)