from musicpy import*

d = note('Eb',4)         # 降E4
r = note('F',4)          # F4  
m = note('G',4)          # G4
f = note('Ab',4)         # 降A4
s = note('Bb',4)         # 降B4
l = note('C',5)          # C5
x = note('D',5)          # D5
d1 = note('Eb',5)        # 降E5（高八度）
r1 = note('F',5)         # F5
m1 = note('G',5)         # G5
f1 = note('Ab',5)        # 降A5 
s1 = note('Bb',5)        # 降B5
l1 = note('C',6)         # C6
x1 = note('D',6)         # D6
d0 = note('Eb',3)        # 降E3（低八度）
r0 = note('F',3)         # F3
m0 = note('G',3)         # G3
f0 = note('Ab',3)        # 降A3
s0 = note('Bb',3)        # 降B3
l0 = note('C',4)         # C4
x0 = note('D',4)         # D4
rest = rest(1)            # 休止符
play(chord(notes=[d,r,rest,m,f,s,l,x,rest], 
           
           
           
           
           
           interval=[3/4, 1/8,1/4,1/16,1/8,1/4,1/16], 
      start_time=0))
