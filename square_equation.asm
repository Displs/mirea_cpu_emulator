.data
num 1
num 3
num -4
.code
LDA ?1
MUL ?1
STA /A
LDA ?0
MUL ?2
MUL #-4
STA /B
ADD /A
STA /C

CMP #0
JL #END

SQRT /C
STA /C

LDA ?1
MUL #-1
SUB /C
DIV ?0
DIV #2
STA /A

LDA ?1
MUL #-1
ADD /C
DIV ?0
DIV #2
STA /B

OUT /A
OUT /B

END:
HLT #0