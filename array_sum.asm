.data
num 5
num 10
num 4
num 7
num 5
num 3
.code
LDA #1
STA /A
ADD ?0
STA /B
LDA #0
LOOP:
ADD @A
STA /C
INC /A
LDA /A
CMP /B
LDA /C
JZ #LOOP
HLT #0