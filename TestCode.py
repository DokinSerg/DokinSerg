
"""Тест на арифментику сдвига. Имеем байты  00 02 53 1E """
Ct= b'\x01\xff\xfe\x12\x040\x04\x3b\x045\x042\x04A\x04\x3A\x040\x04O\x04\ \x00\x1d\x040\x04B\x040\x04;\x04L\x04O\x04 \x00\x00\x00'
print (Ct[1:-2].decode(encoding='utf_16') )
print (Ct[3:-3])
At = 'Валевская Наталья'
Bt = At.encode('utf_16_le')
print (Bt) 
#print(ascii(At))
#print (Bt.decode(encoding='utf_8_sig'))
# Bt = int.from_bytes(b'\x00' + b'\x00\x00', byteorder = 'big') >> 2
# print ('Bt = ', Bt.to_bytes(4, 'big').hex(' '))

# Ct = int.from_bytes(b'\x02' + b'\x00', byteorder = 'big') >> 1
# print ('Ct = ', Ct.to_bytes(4, 'big').hex(' ')) 

# Dt = int.from_bytes(b'\x01', byteorder = 'big') 
# print ('Dt = ', Dt.to_bytes(4, 'big').hex(' '))

# Xt = At + Bt + Ct + Dt
# print ('Xt = ', Xt, Xt.to_bytes(4, 'big').hex(' ')) 
