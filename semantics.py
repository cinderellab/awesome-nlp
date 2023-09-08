## STANDARD SUBJ
##   subj += ref
##   S.*|SX.*|Mg.*|Mx.*
##   #and not
##   Mx.[rj].*
##   MX|MXs|MXp
## INVERTED SUBJ
##   subj += ref
##   SI.*|SXI.
## RELATIVE SUBJ
##   subj += ref
##   RS-FLAG = T
##   REL-SUBJ-FLAG = T
##   B.*|\BW.*
## OBJ LINK TAG INIT 1
##   RS-FLAG != T
##   OBJ-LINK-TAG = UNSET
##   Mv.*|Pv.*|B.*|BW.*
## OBJ LINK TAG INIT 2