from musicpy import *

a1=note('C',7)
a2=note('D',7)
a3=note('E',7)
a4=note('F',7)
a5=note('G',7)
a6=note('A',7)
a7=note('B',7)
play(chord([a1,a2,a3,a4,a5,a6,a7],[1/4]*7,[1/4]*7),bpm=120)
