
"""Тест на арифментику сдвига. Имеем байты  00 02 53 1E """

At = int.from_bytes(b'\x00' + b'\x00\x00\x00', byteorder = 'big') >> 3
print ('At = ', At.to_bytes(4, 'big').hex(' '))

Bt = int.from_bytes(b'\x00' + b'\x00\x00', byteorder = 'big') >> 2
print ('Bt = ', Bt.to_bytes(4, 'big').hex(' '))

Ct = int.from_bytes(b'\x02' + b'\x00', byteorder = 'big') >> 1
print ('Ct = ', Ct.to_bytes(4, 'big').hex(' ')) 

Dt = int.from_bytes(b'\x01', byteorder = 'big') 
print ('Dt = ', Dt.to_bytes(4, 'big').hex(' '))

Xt = At + Bt + Ct + Dt
print ('Xt = ', Xt, Xt.to_bytes(4, 'big').hex(' ')) 
