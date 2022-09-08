

# -*- coding: utf-8 -*-
"""
Created on Sat Aug 11 12:36:39 2018

@author: AMALENDU
"""

import numpy as np
import time
CHESS_BOX = np.arange(64).reshape((8,8)) 
B = 0
for i in range(8):
       for j in range(8 ): 
           B = B + 1
           CHESS_BOX[i][j] = B
            
###print("CHESS_BOX SET  at  DECLARATION  ")
##print(CHESS_BOX)        

for i in range(8):
       for j in range(8 ): 
           CHESS_BOX[i][j] = 0
            
##print("CHESS_BOX SET  at  STARTING  ")
##print(CHESS_BOX)      
global BACK_TO_Qn
global CUML_VALID_BOX_TOT
global CUML_BLOCK_BOX_TOT
global TOT_SET_REPEAT_COUNT 
global THIS_SET_REPEAT_COUNT
global TOT_SET_NO
global IS_SET_VALID
global VALID_SET_NO
global PREV_VALID_SET_NO
global VALID_SET_BOXES
BACK_TO_Qn = 1
Qn_BOX_NO = 0
CUML_VALID_BOX_TOT = 0      
CUML_BLOCK_BOX_TOT = 0
TOT_SET_REPEAT_COUNT = 0
THIS_SET_REPEAT_COUNT = 0
TOT_SET_NO = 0
IS_SET_VALID = ""
VALID_SET_NO = 0
PREV_VALID_SET_NO = 0
SET_NO = 1000
Qn_NO = 8 
CHESS_TOT_BOX_NO = 64

# CONSTRUCT & INITIALIZE AN ARRAY < CQn_BLOCK_BOX_SET >  STORING  TOT.NO OF BLOCK BOX / CQn_BLOCK_BOX_SET [1...64] STORES SUBSEQUENT EACH BOX NO EQUVALENT TO IT'S INDEX NO  
CQn_BLOCK_BOX_SET = np.arange(65)    
for i in range(65):
    CQn_BLOCK_BOX_SET[i] = 0

# CONSTRUCT & INITIALIZE AN ARRAY < CUML_BLOCK_BOX_SET >  ALIKE  CQn_BLOCK_BOX_SET  TO BE USES AS VARIABLE
CUML_BLOCK_BOX_SET = np.arange(65)    
for i in range(65):
    CUML_BLOCK_BOX_SET[i] = 0    
 

# CONSTRUCT & INITIALIZE AN ARRAY < Qn_WISE_BLOCK_BOX_SET > HOLDING  Qn-NO  WISE  SET OF BLOCK BOX_NO    
# AT  STARTING, THERE  IS  NO  BLOCK  BOX-NOS  AS  ALL  ARE VALID    
Qn_WISE_BLOCK_BOX_SET = np.arange(9*65).reshape((9,65))
for i in range(1,8): 
    for j in range(1,65):
         Qn_WISE_BLOCK_BOX_SET[i][j] = 0  
    
Qn_WISE_BLOCK_BOX_SET[1][0] = 0  


# CONSTRUCT & INITIALIZE AN ARRAY < CUML_VALID_BOX_SET >  ALIKE  CQn_BLOCK_BOX_SET  TO BE USES AS VARIABLE
# AT  STARTING  ALL BOX-NOS   ARE VALID 
CUML_VALID_BOX_SET = np.arange(65)    
for i in range(65):
    CUML_VALID_BOX_SET[i] = i   
         
# CONSTRUCT & INITIALIZE AN ARRAY < Qn_WISE_VALID_BOX_SET > HOLDING  Qn-NO  WISE  SET OF VALID BOX_NO      
Qn_WISE_VALID_BOX_SET = np.arange(9*65).reshape((9,65))
BOX_NO = 0
for i in range(1,8):
    for j in range(1,65):
         Qn_WISE_VALID_BOX_SET[i][j] = 0  
         
Qn_WISE_VALID_BOX_SET[1][0] = 64   
      
# STORE ALL CHESS BOX NO AS  VALID BOX IN Qn_WISE_VALID_BOX_SET[0]]B]
BOX_NO = 0
for j in range(1,65):
         BOX_NO = BOX_NO + 1
         Qn_WISE_VALID_BOX_SET[0][j] = BOX_NO  
Qn_WISE_VALID_BOX_SET[0][0] = BOX_NO

# CONSTRUCT & INITIALIZE AN ARRAY < Qn_WISE_CUML_VALID_BOX_SET > HOLDING  Qn-NO  WISE  CUML_VALID_BOX NOS DURING PROCESSING OF ANY SET      
Qn_WISE_CUML_VALID_BOX_SET = np.arange(9*65).reshape((9,65))
for i in range(1,8):
    for j in range(1,65):
        Qn_WISE_CUML_VALID_BOX_SET[i][j] = 0  
         

# CONSTRUCT & INITIALIZE AN ARRAY < VALID_SET_Qn_BOX > HOLDING  VALID SET-NO  WISE  8 BOX_NO  OCCUPIED BY ALL THE 8 Qns OF  THAT  SET ]    
VALID_SET_Qn_BOX = np.arange(SET_NO*(Qn_NO+1)).reshape((SET_NO,Qn_NO+1))
for i in range(SET_NO):
    for j in range(Qn_NO ): 
         VALID_SET_Qn_BOX[i][j] = 0

# CONSTRUCT & INITIALIZE AN ARRAY < SET_Qn_BOX_NO > HOLDING  BOX-NO OCCUPIED BY THAT Qn   
SET_Qn_BOX_NO = np.arange(Qn_NO+1)
for j in range(Qn_NO +1):
    SET_Qn_BOX_NO[j] = 0

# ---------------------------------  BLOCK-BOX / VALID-BOX ---  Function   EVALUATE_BLOCKED_BOXES() -  START  ------------------------------------------------
# Define  Function <EVALUATE_BLOCKED_BOXES>  to  evaluate  all boxes  in chess table  connecting the selected box horizontally, vertically, diagonally
# Evaluate corresponding  [Row,Col] of  all Boxes connecting the opted box in Horizontal / Vertical / 2-Diagonals  directions 
# Step1 : For Horizontal directions  : Select Col Loop  from 1 to 8 : Replace box value CHESS_BOX[R0,Cn]  by a[R0,Cn] 
# Step2 : For Vertical directions  : Select Row Loop  from 1 to 8 : Replace box value CHESS_BOX[Rn,C0]  by a[Rn,C0] 
# Step3 : For 2-Diagonals  directions, we  devide the whole  Matrix in 4 segments, based upon the opted Box R0C0  value
#       : 4 segments  are :[A] Left Upper  Portion; [B] Left Down  Portion ; [C] Right Upper  Portion ; [D] Right Down  Portion
# Step5 : We  use 4 loops  one  each  for  respective segments [A]/[B]/[C]/[D] for  replace  the value of respective boxes connecting the opted box

def EVALUATE_BLOCKED_BOXES(r0, c0, Cqno) :
    
#-----------------------------------------------------------------------------------------------------------
# ALL THESE THREE  1-DIMENTIONAL ARRAYS  ARE  GENERAL VARIABLES, INDENDENT OF Qn-NO.    
# 1-DIMENTIONAL ARRAY  -->  CQn_BLOCK_BOX_SET[v]  STORES  INSTANTLY  CALCULATED EACH  BLOCK BOX OF CURRENT Qn  IN CURRENT SET
# 1-DIMENTIONAL ARRAY  -->  CUML_BLOCK_BOX_SET[v] STORES  CUML-BLOCK BOX OF ALL Qn STARTING FROM 1 UPTO CURRENT Qn 
# 1-DIMENTIONAL ARRAY  -->  CUML_VALID_BOX_SET[v] STORES  CUML-VALID BOX OF OF ALL Qn STARTING FROM 1 UPTO CURRENT Qn 
# HERE INITIALIZE BY MAKING 0  ALL ENTRIS  IN  THREE  1-DIMENTIONAL ARRAYS -->  CQn_BLOCK_BOX_SET[v]  /  CUML_BLOCK_BOX_SET[v]  /  CUML_VALID_BOX_SET[v] 
        
        for v in range(1,65) :
             CQn_BLOCK_BOX_SET[v] = 0               
             CUML_BLOCK_BOX_SET[v] = 0
             CUML_VALID_BOX_SET[v] = 0        
#-----------------------------------------------------------------------------------------------------------
# 2-DIMENTIONAL ARRAY --> Qn_WISE_BLOCK_BOX_SET[Cqno][v]  STORES   Qn-WISE  BLOCK BOX SET OF RESPECTIVE ALL QnS OF THE SET             
# HERE INITIALIZE BY MAKING 0   ALL ENTRIES IN THIS  2-DIMENTIONAL ARRAY --> Qn_WISE_BLOCK_BOX_SET[Cqno][v]  OF CURRENT  Qn NO            
        Qn_WISE_BLOCK_BOX_SET[Cqno][0] = 0
        for v in range(1,65) :
             Qn_WISE_BLOCK_BOX_SET[Cqno][v] = 0
#-----------------------------------------------------------------------------------------------------------             
# 2-DIMENTIONAL ARRAY --> Qn_WISE_VALID_BOX_SET[Cqno][v]  STORES   Qn-WISE  VALID BOX SET OF RESPECTIVE ALL QnS OF THE SET
# 2-DIMENTIONAL ARRAY --> Qn_WISE_CUML_VALID_BOX_SET[Cqno][v]  STORES   Qn-WISE  CUML. VALID BOX SET OF RESPECTIVE ALL QnS OF THE SET
# HERE INITIALIZE BY MAKING 0   ALL  ENTRIES IN THIS  2-DIMENTIONAL ARRAY --> Qn_WISE_VALID_BOX_SET[Cqno][v]  and  Qn_WISE_CUML_VALID_BOX_SET[Cqno][v] OF CURRENT  Qn NO  
        Qn_WISE_VALID_BOX_SET[Cqno][0] = 0
        Qn_WISE_CUML_VALID_BOX_SET[Cqno][0] = 0
        for v in range(1,65) :
             Qn_WISE_VALID_BOX_SET[Cqno][v] = 0 
             Qn_WISE_CUML_VALID_BOX_SET[Cqno][v] = 0   
             
#TASKS[A]: WE STORES, INSTANTLY  CALCULATED EACH  BLOCK BOX OF CURRENT Qn,  IN  CQn_BLOCK_BOX_SET[v]
#TASKS[B]: HERE USING  CQn_BLOCK_BOX_SET[v] --> WE FILL UP  Qn_WISE_BLOCK_BOX_SET[Cqno][0]  / Qn_WISE_BLOCK_BOX_SET[Cqno][v]   WITH TOTAL BLOCK BOX NO / EACH BLOCK BOX VALUE         
#TASKS[C]: HERE USING  THE ARRAY  CQn_BLOCK_BOX_SET[i]  STORE  Qn_WISE_VALID_BOX_SET[][] FOR THIS CURRENT Qn [Cqno] 
#TASKS[D]: HERE USING  RESPECTVE ARRAY--> Qn_WISE_BLOCK_BOX_SET[Qn][X], STORE CUML-BLOCK-BOX VALUES OF ALL THE Qn-NO,FROM 1ST TO CURRENT ONE , IN GENERAL ARRAY --> CUML_BLOCK_BOX_SET[]
#TASKS[E]: HERE USING  CUML_BLOCK_BOX_SET[] STORE CUML-VALID BOX VALUES UP TO TO CURRENT-Qn, IN GENERAL ARRAY --> CUML_VALID_BOX_SET[j]             
#TASKS[F]: HERE USING  CUML_VALID_BOX_SET[j],  STORE CUML-VALID BOX VALUES UP TO TO CURRENT-Qn, IN SPECIFIC ARRAY --> Qn_WISE_CUML_VALID_BOX_SET[QnNO][J]  
            
#-----------------------------------------------------------------------------------------------------------             
#  For Horizontal directions :
         
        R = r0
        C = 0
        C_NO=8
        for i in range(C_NO):      # Implies  for  i =  0  to  C_NO-1   ===  C_NO no of  iterrations
            C = C + 1
            BLOCK_BOX_NO =  (R-1) * 8 + C
            CQn_BLOCK_BOX_SET[BLOCK_BOX_NO] = BLOCK_BOX_NO   
        #print("After Step A :  r0,c0 = ", r0, c0)   
        ##print(CHESS_BOX)  
      
#  For Vertical directions directions :
        R = 0
        C = c0
        R_NO = 8 
        for j in range(R_NO):      # Implies  for  i =  0  to  R_NO-1   ===  R_NO no of  iterrations
            R = R + 1
            BLOCK_BOX_NO = (R-1) * 8 + C      # CHESS_BOX[R-1][C-1] =  (R-1) * 8 + C   
            CQn_BLOCK_BOX_SET[BLOCK_BOX_NO]  = BLOCK_BOX_NO 
        ##print("After Step B :  r0,c0 = ", r0, c0)      
        ##print(CHESS_BOX)  
     
# For [A] Left Upper  Portion    
        R = r0   
        C = c0 
        while R > 0 :
            R = R - 1
            if R == 0 :
               break
            if R > 0 :
               C = C - 1
               if C == 0 :
                   break
            BLOCK_BOX_NO =   (R-1) * 8 + C                         #  CHESS_BOX[R-1][C-1] =  (R-1) * 8 + C 
            CQn_BLOCK_BOX_SET[BLOCK_BOX_NO]  = BLOCK_BOX_NO 
        ##print("After Step C1  :  r0,c0 = ", r0, c0)    
        ##print(CHESS_BOX)  
       
# For [B] Left DOWN  Portion    
        R = r0  
        C = c0  
        while R > 0 :
            R = R + 1
            if R > 8 :
               break   
            if R > 0 :
               C = C - 1
               if C == 0 :
                   break
            BLOCK_BOX_NO = (R-1) * 8 + C   
            CQn_BLOCK_BOX_SET[BLOCK_BOX_NO]  = BLOCK_BOX_NO           #  CHESS_BOX[R-1][C-1] =  (R-1) * 8 + C   
        ##print("After Step C2 :  r0,c0 = ", r0, c0)     
        ##print(CHESS_BOX)   
        
# For [C] Right Upper  Portion    
        R = r0   
        C = c0 
        while R > 0 :
            R = R - 1
            if R == 0 :
               break
            if R > 0 :
               C = C + 1
               if C > 8 :
                   break
            BLOCK_BOX_NO = (R-1) * 8 + C   
            CQn_BLOCK_BOX_SET[BLOCK_BOX_NO]  = BLOCK_BOX_NO      #  CHESS_BOX[R-1][C-1] =  (R-1) * 8 + C 
        ##print("After Step C3  :  r0,c0 = ", r0, c0)    
        ##print(CHESS_BOX)  
        
# For [D] Right DOWN  Portion    
        R = r0  
        C = c0  
        while R > 0 :
            R = R + 1
            if R > 8 :
               break   
            if R > 0 :
               C = C + 1
               if C > 8 :
                   break
            BLOCK_BOX_NO =  (R-1) * 8 + C   
            CQn_BLOCK_BOX_SET[BLOCK_BOX_NO]  = BLOCK_BOX_NO      #  CHESS_BOX[R-1][C-1] =  (R-1) * 8 + C 
    
#            #print("CHESS_BOX  After Step C4  :  r0,c0 = ", r0, c0)    
#            #print(CHESS_BOX) 
            
# [A] EACH  BLOCK BOX-NO, AGAINST  THIS CURRENT Qn [CQn], IS COLLECTED ABOVE IN GENERAL ARRAY--> CQn_BLOCK_BOX_SET[] 
            
# [B] NOW WE STORE BLOCK BOX-NO  IN SPECIFIC ARRAY--> Qn_WISE_BLOCK_BOX_SET[][] AGAINST THIS CURRENT Qn [Cqno]  USING  THE  GENERAL ARRAY --> CQn_BLOCK_BOX_SET[i]
        j = 0            
        for i in range(1,65):
            if CQn_BLOCK_BOX_SET[i] > 0 :
                 j = j + 1
                 Qn_WISE_BLOCK_BOX_SET[Cqno][j] = CQn_BLOCK_BOX_SET[i]   # STORE EACH BLOCK BOX NO  IN subsequent  BOX SL-NO [j] in  Qn_WISE_BLOCK_BOX_SET[Cqno][j]
       
        Qn_WISE_BLOCK_BOX_SET[Cqno][0] = j    # STORE TOTAL NO  OF   BLOCK BOX  AGAINST THIS  SPECIFIC CURRENT Qn [Cqno]  
        
# [C] NOW WE STORE EACH  VALID_BOX NO [OTHER THAN  BLOCK BOX-NO WITH 0 VALUES]  IN SPECIFIC ARRAY--> Qn_WISE_VALID_BOX_SET[][] AGAINST THIS CURRENT Qn [Cqno] USING  THE ARRAY  CQn_BLOCK_BOX_SET[i] 
        j = 0            
        for i in range(1,65):
            if CQn_BLOCK_BOX_SET[i] == 0 :
                 j = j + 1
                 Qn_WISE_VALID_BOX_SET[Cqno][j] = CQn_BLOCK_BOX_SET[i]    # STORE EACH  VALID BOX NO  IN subsequent  BOX SL-NO [j] in  Qn_WISE_VALID_BOX_SET[Cqno][j]
        
        Qn_WISE_VALID_BOX_SET[Cqno][0] = j    # STORE TOTAL NO  OF  VALID BOX  AGAINST THIS  SPECIFIC CURRENT Qn [Cqno]    

# [D] HERE WE STORE CUML-BLOCK-BOX VALUES OF ALL THE Qn-NO, FROM 1ST-Qn TO CURRENT-Qn, IN GENERAL ARRAY --> CUML_BLOCK_BOX_SET[]
# NOTE THAT SOME Qns MUST HAVE COMMON BLOCK-BOX-NO. SO CUML. TOT BLOCK-BOX-NO SHOUD BE CALCULATED LATER INDIRECTLY FROM CUML.TOT-VALID-BOX-NOS                
        for i in range(1, Cqno+1) :                                            # SELECT  EACH  Qn NO FROM SL NO 1 TO Cqno
            Qn_WISE_TOT_BLOCK_BOX_NO = Qn_WISE_BLOCK_BOX_SET[i][0]
            for j in range(1, Qn_WISE_TOT_BLOCK_BOX_NO + 1) :
                ARRAY_BLOCK_BOX_NO = Qn_WISE_BLOCK_BOX_SET[i][j]               # COLLECT FROM ARRAY  EACH  BLOCK_BOX_NO OF SELECTED Cqno
                CUML_BLOCK_BOX_SET[ARRAY_BLOCK_BOX_NO] = ARRAY_BLOCK_BOX_NO    # STORE  EACH  BLOCK_BOX_NO  IN THE BOX OF THAT BOX-SL-NO 
                  
# [E] HERE WE STORE CUML-VALID BOX VALUES UP TO TO CURRENT-Qn, IN GENERAL ARRAY --> CUML_VALID_BOX_SET[j]  USING  CUML_BLOCK_BOX_SET[]                  
        TOT_VBOX = 0 
        for i in range(1, 65) :
             ARRAY_BLOCK_BOX_NO = CUML_BLOCK_BOX_SET[i]                  # COLLECT FROM ARRAY  EACH  BLOCK_BOX_NO OF SELECTED Cqno
             if ARRAY_BLOCK_BOX_NO == 0 :
                  TOT_VBOX = TOT_VBOX + 1
                  CUML_VALID_BOX_SET[TOT_VBOX] = i                              # STORE  EACH  VALID_BOX_NO  IN IN subsequent  BOX SL-NO [j]  
                    
                  
# STORE CUML VALID BOX (TOT_VBOX])   IN ARRAY --> CUML_VALID_BOX_SET[0]     AND  CUML  BLOCK  BOX (TOT_BBOX)  IN ARRAY --> CUML_BLOCK_BOX_SET[0]
        CUML_VALID_BOX_TOT = TOT_VBOX
        CUML_BLOCK_BOX_TOT = 64 - TOT_VBOX
        CUML_VALID_BOX_SET[0] = CUML_VALID_BOX_TOT
        CUML_BLOCK_BOX_SET[0] = CUML_BLOCK_BOX_TOT 
        
        Qn_WISE_BLOCK_BOX_SET[Cqno][0] = CUML_BLOCK_BOX_TOT
        Qn_WISE_CUML_VALID_BOX_SET[Cqno][0] = TOT_VBOX 
        for j in range(64) :
             Qn_WISE_CUML_VALID_BOX_SET[Cqno][j] = CUML_VALID_BOX_SET[j]       
      
# DISPLAY  CUML TOTAL  BLOCK  BOX / VALID  BOX  UPTO THE CURRENT Qn -----------       
        #print("CUML_BLOCK_BOX_TOT =", CUML_BLOCK_BOX_TOT, "==", Qn_WISE_BLOCK_BOX_SET[Cqno][0]) 
        #for j in range(1, 65) :
        #    if Qn_WISE_BLOCK_BOX_SET[Cqno][j] > 0 :
                ##print(Qn_WISE_BLOCK_BOX_SET[Cqno][j] , "  ", end='' )
       
        ##print()
        #print("** CUML_VALID_BOX_TOT =", CUML_VALID_BOX_TOT, "==", Qn_WISE_CUML_VALID_BOX_SET[Cqno][0])  
        #for j in range(1, 65) :
        #    if Qn_WISE_CUML_VALID_BOX_SET[Cqno][j] > 0 :
                ##print(Qn_WISE_CUML_VALID_BOX_SET[Cqno][j] , "  ", end='' )
                
        ##print()
        return(CUML_VALID_BOX_TOT)
            
# --------------BLOCK-BOX / VALID-BOX ---  Function   EVALUATE_BLOCKED_BOXES() -  ENDS ----------------------------------
#  AT  STARTING OF  EACH  SET  ALL  64  BOXES ARE VALID  WITH  0  VALUES            
VALID_SET_NO = 0  
BOX_SL_NO1 = 0
BOX_SL_NO2 = 0
BOX_SL_NO3 = 0

#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@-------   Qn_NO = 1   STARTS -------------------------------------
for Qn1_BOX in range(1,33) :  
    
#***************************
# BEFORE STARTING EACH  NEW SET WITH Qn-1st,  WE  MUST  INITIALISE  ALL  ARRAYS  USED FOR EVALUATE_BLOCKED_BOXES
     
    for i in range(1,8): 
       for j in range(1,65):
           Qn_WISE_BLOCK_BOX_SET[i][j] = 0  
    
    Qn_WISE_BLOCK_BOX_SET[1][0] = 0     
       
    for i in range(1,8):
       for j in range(1,65):
           Qn_WISE_VALID_BOX_SET[i][j] = 0  
         
    Qn_WISE_VALID_BOX_SET[1][0] = 64   
    
    # STORE ALL CHESS BOX NO AS  VALID BOX IN Qn_WISE_VALID_BOX_SET[0]]B]
    BOX_NO = 0
    for j in range(1,65):
             BOX_NO = BOX_NO + 1
             Qn_WISE_VALID_BOX_SET[0][j] = BOX_NO 
             
    Qn_WISE_VALID_BOX_SET[0][0] = BOX_NO
    
#****************************
    Qn_NO = 1 
    
    DAY_TIME = time.localtime() # get struct_time
    TIME_string = time.strftime("%H:%M:%S", DAY_TIME) 
    print(TIME_string)  
    
    BOX_NO = Qn1_BOX   
    
    Qn1_BOX_NO =  BOX_NO
                                                         
    DEV = int(BOX_NO / 8)
    REM =  BOX_NO % 8
    if REM == 0 :
              BOX_r0 = DEV    
              BOX_c0 = 8   # LAST  COL.
    else :
              BOX_r0 = DEV + 1   
              BOX_c0 = REM  
              
    SET_Qn_BOX_NO[Qn_NO] = BOX_NO     
        
    # TASK-1.2 & 1.3 : AFTER  PLACMENT OF 1ST Qn, CALL FUNCTION  <EVALUATE_BLOCKED_BOXES(BOX_r0, BOX_c0, Qn_NO)> TO  FILL UP  THE  ALL CONCERNED  CHESS TABLE  / STORE ALL  VALID BOX  IN ARRAY  
    EVALUATE_BLOCKED_BOXES(BOX_r0, BOX_c0, Qn_NO)       
    CUML_VALID_BOX_TOT =  Qn_WISE_CUML_VALID_BOX_SET[Qn_NO][0]  
   
    #@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@-------   Qn_NO = 2   STARTS -------------------------------------
    for Qn2_BOX in range(1, Qn_WISE_CUML_VALID_BOX_SET[1][0]+1): 
        BOX_NO  =   Qn_WISE_CUML_VALID_BOX_SET[1][Qn2_BOX]   
        
        Qn2_BOX_NO =  BOX_NO
            
        if BOX_NO > 0 : #   VALID BOX  AVAILABLE  
                Qn_NO = 2                                            
                DEV = int(BOX_NO / 8)
                REM =  BOX_NO % 8
                if REM == 0 :
                          BOX_r0 = DEV    
                          BOX_c0 = 8   # LAST  COL.
                else :
                          BOX_r0 = DEV + 1   
                          BOX_c0 = REM  
                          
                SET_Qn_BOX_NO[Qn_NO] = BOX_NO
                
                # TASK-2.2 & 2.3 : AFTER  PLACMENT OF 2nd Qn, CALL FUNCTION  <EVALUATE_BLOCKED_BOXES(BOX_r0, BOX_c0, Qn_NO)> TO  FILL UP  THE  ALL CONCERNED  CHESS TABLE  / STORE ALL  VALID BOX  IN ARRAY        
                EVALUATE_BLOCKED_BOXES(BOX_r0, BOX_c0, Qn_NO)    
                CUML_VALID_BOX_TOT =  Qn_WISE_CUML_VALID_BOX_SET[Qn_NO][0] 
                
                REST_Qn_NO = 8 - Qn_NO 
                
                if CUML_VALID_BOX_TOT < REST_Qn_NO : 
                      continue  
                else :                                     
                      c=0 
        #@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@-------   Qn_NO = 3   STARTS -------------------------------------         
        for Qn3_BOX in range(1,Qn_WISE_CUML_VALID_BOX_SET[2][0]+1):  
          
            BOX_NO  = Qn_WISE_CUML_VALID_BOX_SET[2][Qn3_BOX]   
            
            Qn3_BOX_NO =  BOX_NO
                  
            if BOX_NO > 0 : #   VALID BOX  AVAILABLE                                                           
                    Qn_NO = 3  
                    DEV = int(BOX_NO / 8)
                    REM =  BOX_NO % 8
                    if REM == 0 :
                              BOX_r0 = DEV    
                              BOX_c0 = 8   # LAST  COL.
                    else :
                              BOX_r0 = DEV + 1   
                              BOX_c0 = REM  
                              
                    SET_Qn_BOX_NO[Qn_NO] = BOX_NO   
                   
                    # TASK-3.2 & 3.3 : AFTER  PLACMENT OF 3rd Qn, CALL FUNCTION  <EVALUATE_BLOCKED_BOXES(r0, c0)> TO  FILL UP  THE  ALL CONCERNED  CHESS TABLE  / STORE ALL  VALID BOX  IN ARRAY  
                    EVALUATE_BLOCKED_BOXES(BOX_r0, BOX_c0, Qn_NO) 
                    CUML_VALID_BOX_TOT =  Qn_WISE_CUML_VALID_BOX_SET[Qn_NO][0] 
                      
                    REST_Qn_NO = 8 - Qn_NO 
                  
                    # HERE WE RE CHECK IF CUML_VALID_BOX_TOT < REST_Qn_NO, IF SO -- HERE WE RE-FILL CUML_BLOCK_BOX_SET[64] WITH  BLOCK-BOX-NO-SET  OF PREV.-Qn &  BREAK loop  HERE   
                    if CUML_VALID_BOX_TOT < REST_Qn_NO :   
                          continue  
                    else :         
                          c=0
            
            #@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@-------   Qn_NO = 4   STARTS -------------------------------------             
            for Qn4_BOX in range(1,Qn_WISE_CUML_VALID_BOX_SET[3][0]+1):  
                BOX_NO  =  Qn_WISE_CUML_VALID_BOX_SET[3][Qn4_BOX]    
                
                Qn4_BOX_NO =  BOX_NO 
                
                if BOX_NO > 0 : #   VALID BOX  AVAILABLE 
                        Qn_NO = 4                                                     
                        DEV = int(BOX_NO / 8)
                        REM =  BOX_NO % 8
                        if REM == 0 :
                                  BOX_r0 = DEV    
                                  BOX_c0 = 8   # LAST  COL.
                        else :
                                  BOX_r0 = DEV + 1   
                                  BOX_c0 = REM   
                      
                        SET_Qn_BOX_NO[Qn_NO] = BOX_NO      
                       
                        # TASK-4.2 & 4.3 : AFTER  PLACMENT OF 4th Qn, CALL FUNCTION  <EVALUATE_BLOCKED_BOXES(r0, c0)> TO  FILL UP  THE  ALL CONCERNED  CHESS TABLE  / STORE ALL  VALID BOX  IN ARRAY  
                        EVALUATE_BLOCKED_BOXES(BOX_r0, BOX_c0, Qn_NO)    
                        CUML_VALID_BOX_TOT =  Qn_WISE_CUML_VALID_BOX_SET[Qn_NO][0] 
                     
                        REST_Qn_NO = 8 -Qn_NO 
                        # HERE WE RE CHECK IF CUML_VALID_BOX_TOT < REST_Qn_NO, IF SO -- HERE WE RE-FILL CUML_BLOCK_BOX_SET[64] WITH  BLOCK-BOX-NO-SET  OF PREV.-Qn &  BREAK loop  HERE                  
                        if CUML_VALID_BOX_TOT < REST_Qn_NO  : 
                              continue        
                        else :                              
                              c=0  
                
                #@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@-------   Qn_NO = 5   STARTS ------------------------------------- 
                for Qn5_BOX in range(1,Qn_WISE_CUML_VALID_BOX_SET[4][0]+1): 
                    BOX_NO  =  Qn_WISE_CUML_VALID_BOX_SET[4][Qn5_BOX ]    
                    
                    Qn5_BOX_NO =  BOX_NO
                  
                    if BOX_NO > 0 : #   VALID BOX  AVAILABLE 
                            Qn_NO = 5                                                     
                            DEV = int(BOX_NO / 8)
                            REM =  BOX_NO % 8
                            if REM == 0 :
                                      BOX_r0 = DEV    
                                      BOX_c0 = 8   # LAST  COL.
                            else :
                                      BOX_r0 = DEV + 1   
                                      BOX_c0 = REM  
                      
                            SET_Qn_BOX_NO[Qn_NO] = BOX_NO  
                                        
                            # TASK-5.2 & 5.3 : AFTER  PLACMENT OF 5th Qn, CALL FUNCTION  <EVALUATE_BLOCKED_BOXES(r0, c0)> TO  FILL UP  THE  ALL CONCERNED  CHESS TABLE  / STORE ALL  VALID BOX  IN ARRAY  
                            EVALUATE_BLOCKED_BOXES(BOX_r0, BOX_c0, Qn_NO)
                            CUML_VALID_BOX_TOT =  Qn_WISE_CUML_VALID_BOX_SET[Qn_NO][0] 
                            
                            REST_Qn_NO = 8 -Qn_NO 
                           
                            # HERE WE RE CHECK IF CUML_VALID_BOX_TOT < REST_Qn_NO, IF SO -- HERE WE RE-FILL CUML_BLOCK_BOX_SET[64] WITH  BLOCK-BOX-NO-SET  OF PREV.-Qn &  BREAK loop  HERE   
                            if CUML_VALID_BOX_TOT < REST_Qn_NO  :
                                   continue  
                            else :   
                                   c=0  
                    
                    #@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@-------   Qn_NO = 6   STARTS ------------------------------------- 
                    for Qn6_BOX in range(1,Qn_WISE_CUML_VALID_BOX_SET[5][0]+1): 
                        BOX_NO  =  Qn_WISE_CUML_VALID_BOX_SET[5][Qn6_BOX ]    
                      
                        Qn6_BOX_NO =  BOX_NO 
                     
                        if BOX_NO > 0 : #   VALID BOX  AVAILABLE 
                                Qn_NO = 6                                                          
                                DEV = int(BOX_NO / 8)
                                REM =  BOX_NO % 8
                                if REM == 0 :
                                          BOX_r0 = DEV    
                                          BOX_c0 = 8   # LAST  COL.
                                else :
                                          BOX_r0 = DEV + 1   
                                          BOX_c0 = REM  
                      
                                SET_Qn_BOX_NO[Qn_NO] = BOX_NO            
                                                  
                                # TASK-6.2 & 6.3 : AFTER  PLACMENT OF 6th Qn, CALL FUNCTION  <EVALUATE_BLOCKED_BOXES(BOX_r0, BOX_c0, Qn_NO)> TO  FILL UP  THE  ALL CONCERNED  CHESS TABLE  / STORE ALL  VALID BOX  IN ARRAY  
                                EVALUATE_BLOCKED_BOXES(BOX_r0, BOX_c0, Qn_NO)    
                                CUML_VALID_BOX_TOT =  Qn_WISE_CUML_VALID_BOX_SET[Qn_NO][0] 
                                    
                                REST_Qn_NO = 8 -Qn_NO 
                                # HERE WE RE CHECK IF CUML_VALID_BOX_TOT < REST_Qn_NO, IF SO -- HERE WE RE-FILL CUML_BLOCK_BOX_SET[64] WITH  BLOCK-BOX-NO-SET  OF PREV.-Qn &  BREAK loop  HERE   
                                if CUML_VALID_BOX_TOT < REST_Qn_NO :
                                      continue       
                                else :                                     
                                      c=0  
              
                        #@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@-------   Qn_NO = 7   STARTS -------------------------------------         
                        for Qn7_BOX in range(1,Qn_WISE_CUML_VALID_BOX_SET[6][0]+1): 
                            BOX_NO  =  Qn_WISE_CUML_VALID_BOX_SET[6][Qn7_BOX ]    
                            
                            Qn7_BOX_NO =  BOX_NO
                          
                            if BOX_NO > 0 : #   VALID BOX  AVAILABLE 
                                    Qn_NO = 7                                                     
                                    DEV = int(BOX_NO / 8)
                                    REM =  BOX_NO % 8
                                    if REM == 0 :
                                              BOX_r0 = DEV    
                                              BOX_c0 = 8   # LAST  COL.
                                    else :
                                              BOX_r0 = DEV + 1   
                                              BOX_c0 = REM  
                              
                                    SET_Qn_BOX_NO[Qn_NO] = BOX_NO  
                                                 
                                    # TASK-5.2 & 5.3 : AFTER  PLACMENT OF 5th Qn, CALL FUNCTION  <EVALUATE_BLOCKED_BOXES(BOX_r0, BOX_c0, Qn_NO)> TO  FILL UP  THE  ALL CONCERNED  CHESS TABLE  / STORE ALL  VALID BOX  IN ARRAY  
                                    EVALUATE_BLOCKED_BOXES(BOX_r0, BOX_c0, Qn_NO)
                                    CUML_VALID_BOX_TOT =  Qn_WISE_CUML_VALID_BOX_SET[Qn_NO][0]
                                  
                                    REST_Qn_NO = 8 -Qn_NO 
                                    # HERE WE RE CHECK IF CUML_VALID_BOX_TOT < REST_Qn_NO, IF SO -- HERE WE RE-FILL CUML_BLOCK_BOX_SET[64] WITH  BLOCK-BOX-NO-SET  OF PREV.-Qn &  BREAK loop  HERE   
                                    if CUML_VALID_BOX_TOT < REST_Qn_NO  :
                                           continue  
                                    else :  
                                           c=0  
                            
                            #@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@-------   Qn_NO = 8   STARTS -------------------------------------          
                            for Qn8_BOX in range(1, Qn_WISE_CUML_VALID_BOX_SET[7][0] + 1):         
                                BOX_NO  =  Qn_WISE_CUML_VALID_BOX_SET[7][Qn7_BOX]
                                
                                Qn8_BOX_NO =  BOX_NO
                              
                                if BOX_NO > 0 :  #VALID BOX  AVAILABLE 
                               
                                        Qn_NO = 8
                                          
                                        SET_Qn_BOX_NO[Qn_NO] = BOX_NO 
                                        TOT_SET_NO = TOT_SET_NO + 1
                                        THIS_SET_REPEAT_COUNT = 0
                                        
                                        #print("[TASK-8.1]-Placed Qn8 at BOX NO:", BOX_NO , "   TOT_SET_NO = ",TOT_SET_NO )
                                         
                                        if TOT_SET_NO == 1:
                                            VALID_SET_NO = 1 
                                            PREV_VALID_SET_NO = 0 
                                            k=0
                                            print("SET_NO  = " , VALID_SET_NO , " : "  ,  end='' )  #"[MAIN][TASK-5A] **  VALID_
                                            for k in range(1,9) : 
                                                VALID_SET_Qn_BOX[VALID_SET_NO][k] = SET_Qn_BOX_NO[k]   
                                                print(VALID_SET_Qn_BOX[VALID_SET_NO][k] , "  " ,  end='')    
                                         
                                            print(TIME_string)   #time.ctime()) 
                                                
                                        if TOT_SET_NO > 1:
                                         #***********************************************
                                            # [TASK-5B] : COMPLETE  SET--- FOR OTHER  SETS  [TOT_SET_NO > 1],  CHECK IF  CURRENT  SET IS ORIGINAL OR NOT                           
                                             
                                            if TOT_SET_NO > 1 :    # FOR SUCH  SETS  CONSTRUCTED  AFTER  1ST  SET
                                                    IS_SET_VALID = 1 
                                                    for i in range(1, VALID_SET_NO + 1) :     # SELECT  EACH  OLD  VALID_SET_NO  ONE  BY  ONE
                                                        MATCHED_Qn_NO = 0 
                                                        for j in range(1,9) :                                             
                                                            Qn_BOX_NO_OLD_SET = VALID_SET_Qn_BOX[i,j]     # ASSIGN  EACH  Qn-BOX-NO  OF OLD-SET
                                                          
                                                            for k in range(1,9) :
                                                                 Qn_BOX_NO_NEW_SET = SET_Qn_BOX_NO[k]   
                                                                 # NOW  COMPARE  EACH  OLD-SET  Qn BOX-NO    WITH  THAT OF  SELECTED   Qn BOX-NO  OF  NEW  SET        
                                                                 if Qn_BOX_NO_OLD_SET == Qn_BOX_NO_NEW_SET :
                                                                      MATCHED_Qn_NO = MATCHED_Qn_NO + 1
                                                                      if MATCHED_Qn_NO == 8 :
                                                                            IS_SET_VALID = 0   
                                                                                 
                                            #print("[MAIN-LAST][TASK-5B.3]  Duplicate  Set *  IS_SET_VALID =  0 ??   ==  ", IS_SET_VALID    )
                                            #*********************************************** 
                                            if IS_SET_VALID  == 1 : 
                                                DAY_TIME = time.localtime() # get struct_time
                                                TIME_string = time.strftime("%H:%M:%S", DAY_TIME) 
                                                VALID_SET_NO = VALID_SET_NO + 1    
                                                
                                                print("SET_NO  = " , VALID_SET_NO ,"/", TOT_SET_NO, " : "  ,  end='' )  #[MAIN][TASK-6] **  VALID_
                                                k=0
                                                VALID_SET_BOXES = ""
                                                for k in range(1,9) : 
                                                       #Qn_BOX_NO  = int(SET_Qn_BOX_NO[k] )
                                                       #VALID_SET_BOXES = VALID_SET_BOXES, Qn_BOX_NO 
                                                       
                                                       VALID_SET_Qn_BOX[VALID_SET_NO][k] = SET_Qn_BOX_NO[k]  
                                                       print(VALID_SET_Qn_BOX[VALID_SET_NO][k] , "  " ,  end='')    
                                         
                                                print(TIME_string)   #time.ctime())
                                           
                                            #if VALID_SET_NO == 2:
                                            #    continue
                                            if IS_SET_VALID  == 0 : 
                                                THIS_SET_REPEAT_COUNT = THIS_SET_REPEAT_COUNT + 1
                                                TOT_SET_REPEAT_COUNT = TOT_SET_REPEAT_COUNT + 1 
                                                # print("[MAIN-LAST] TOT_SET_REPEAT_COUNT =",TOT_SET_REPEAT_COUNT, "   THIS_SET_REPEAT_COUNT = ", THIS_SET_REPEAT_COUNT)
                                                if THIS_SET_REPEAT_COUNT > 0 : 
                                                    #@22222222222222222
                                                    #"SET_REPEAT_COUNT  > 2  GOING  TO    B2_LOOP_END  " 
                                                    BACK_TO_Qn = 2 
                                                    #@22222222222222222
                                                    break 
                            #print("BLOCK FOR-LOOP-Qn8---ENDS" ) 
                            
                            if BACK_TO_Qn == 2 :
                                break 
                        #print("BLOCK FOR-LOOP-Qn7---ENDS" ) 
                        
                        if BACK_TO_Qn == 2 :
                            break
                                  
                    #print("BLOCK FOR-LOOP-Qn6---ENDS" ) 
                    
                    if BACK_TO_Qn == 2 :
                        break
                                  
                #print("BLOCK FOR-LOOP-Qn5---ENDS" ) 
                
                if BACK_TO_Qn == 2 :
                    break
            #print("BLOCK FOR-LOOP-Qn4---ENDS" ) 
            if BACK_TO_Qn == 2 :
                break
        #print("BLOCK FOR-LOOP-Qn3---ENDS" ) 
        
        if BACK_TO_Qn == 2 : 
            #'HERE  KEEP  THE  PREVIOUS     QUEEN  Q1  AT  THEIR PREVIOUS  BOXES
            #BOX_NO = QUEEN_WISE_CUM_NON_BLOCK_BOX(1, 0)
            #Txt_CHESS_BOX(BOX_NO) = "Q1"
            #QUEEN_PLACED_BOX_NO = QUEEN_WISE_CUM_NON_BLOCK_BOX(Qn_NO, 0)
            BACK_TO_Qn = 0
            continue
    #print("BLOCK FOR-LOOP-Qn2---ENDS" ) 
    
#print("BLOCK FOR-LOOP-Qn1---ENDS" )  

# STARTS : 22:04:53   ENDS : 22:27:27