import numpy as np
from scipy.interpolate import interp1d  
from initialize import Tables
from Results import Result
import matplotlib.pyplot as plt
import random
import sys

class Theoretical_prediction(Tables,Result):
    def __init__(self):
        Tables.__init__(self)
        Result.__init__(self)
        self.MT_theo = None
        self.CS_pp_TT = None
        self.CS_pp_Tbq = None
        self.CS_pp_Ttq = None
        self.BR_T_bW = None
        self.BR_T_tZ = None
        self.BR_T_tH = None
        self.width_mass_ratio = None 
        self.coupling_to_Top = None
        self.sin_left = None
        self.sin_right = None
        self.coupling_TbW_L = None   
        self.coupling_TZt_L =None   
        self.coupling_TtH_L = None
        self.coupling_TbW_R = None   
        self.coupling_TZt_R =None   
        self.coupling_TtH_R = None
    def Set_Model(self,model):
      self.model = model
    
    def Set_width_to_mass_ratio(self,width_mass_ratio):
     self.width_mass_ratio = width_mass_ratio
    
    def Coupling_Inputs(self,coupling_to_Top,sin_left,sin_right,coupling_TbW_L,coupling_TZt_L,coupling_TtH_L,coupling_TbW_R,coupling_TZt_R,coupling_TtH_R):
     self.coupling_to_Top = coupling_to_Top
     self.sin_left = sin_left
     self.sin_right = sin_right    
     self.coupling_TbW_L = coupling_TbW_L
     self.coupling_TZt_L = coupling_TZt_L
     self.coupling_TtH_L = coupling_TtH_L
     self.coupling_TbW_R = coupling_TbW_R
     self.coupling_TZt_R = coupling_TZt_R
     self.coupling_TtH_R = coupling_TtH_R
    
    def complete_CS_Calc(self):
      if self.model == 'Pure': 
        CS_TTbar_bW = self.CS_pp_TT*self.BR_T_bW*self.BR_T_bW
        CS_TTbar_tZ = self.CS_pp_TT*self.BR_T_tZ*self.BR_T_tZ
        CS_TTbar_tH = self.CS_pp_TT*self.BR_T_tH*self.BR_T_tH
        #single production of T associated with bq (pp->Tbq)
        CS_Tbq_tZ = self.CS_pp_Tbq*self.BR_T_tZ
        CS_Tbq_bW = self.CS_pp_Tbq*self.BR_T_bW
        CS_Tbq_tH = self.CS_pp_Tbq*self.BR_T_tH
        #single production of T associated with tq (pp->Ttq)
        CS_Ttq_tZ = self.CS_pp_Ttq*self.BR_T_tZ
        CS_Ttq_bW = self.CS_pp_Ttq*self.BR_T_bW
        CS_Ttq_tH = self.CS_pp_Ttq*self.BR_T_tH
        
        #pp_TTbar_comb =  CS_TTbar_bW + CS_TTbar_tZ + CS_TTbar_tH
        
        return CS_TTbar_bW, CS_TTbar_tZ, CS_TTbar_tH, CS_Tbq_tZ, CS_Tbq_bW, CS_Tbq_tH, CS_Ttq_tZ, CS_Ttq_bW, CS_Ttq_tH#, pp_TTbar_comb
      
      elif self.model == 'Singlet':
       
       self.BR_T_bW = 0.5
       self.BR_T_tZ = 0.25
       self.BR_T_tH = 0.25
       BR_t_Wb = 1
       BR_H_bb = 0.58
       
       BR_W_lnu = 0.3
       BR_W_qq = 0.6832
       BR_Z_ll = 0.1
       BR_Z_nunu = 0.2
       BR_Z_qq = 0.7
       
       pp_TTbar_bW_plus_X =   self.CS_pp_TT*self.BR_T_bW*(self.BR_T_bW + self.BR_T_tZ + self.BR_T_tH)
       pp_TTbar_tZ_plus_X =   self.CS_pp_TT*self.BR_T_tZ*(self.BR_T_tZ + self.BR_T_bW + self.BR_T_tH)
       pp_TTbar_tH_plus_X =   self.CS_pp_TT*self.BR_T_tH*(self.BR_T_tZ + self.BR_T_bW + self.BR_T_tH)
     
       pp_Tbq_bW = self.CS_pp_Tbq*self.BR_T_bW
       pp_Tbq_tZ = self.CS_pp_Tbq*self.BR_T_tZ
       pp_Tbq_tH = self.CS_pp_Tbq*self.BR_T_tH
     
       pp_Ttq_bW = self.CS_pp_Ttq*self.BR_T_bW
       pp_Ttq_tZ = self.CS_pp_Ttq*self.BR_T_tZ
       pp_Ttq_tH = self.CS_pp_Ttq*self.BR_T_tH
       
       pp_TTbar_one_lepton = self.CS_pp_TT*self.BR_T_tH*self.BR_T_tH*BR_t_Wb*BR_t_Wb*BR_H_bb*BR_H_bb*BR_W_lnu*BR_W_qq #TT -> HtHt -> HWbHWb     H -> bb, WW -> lnuqq 
       
       pp_TTbar_dileptons_same_sign = self.CS_pp_TT*self.BR_T_tZ*self.BR_T_bW*BR_t_Wb*BR_Z_ll*BR_W_qq*BR_W_lnu  #TT -> ZtWb -> ZWbWb      Z -> bb, WW -> lnuqq 
       
       #opposite sign leptons final state involving a Z boson
       opposite_1 = self.CS_pp_TT*self.BR_T_tZ*self.BR_T_bW*BR_Z_ll*BR_t_Wb*BR_W_qq**2   #TT -> ZtWb -> ZWbWb     Z -> ll, W -> qq
       opposite_2 = self.CS_pp_TT*self.BR_T_tZ*self.BR_T_tH*(BR_t_Wb**2)*BR_Z_ll*(BR_W_qq**2)*BR_H_bb       #TT -> ZttH -> ZWbWbH     Z -> ll, H -> qq
       opposite_3 = self.CS_pp_TT*self.BR_T_tZ*self.BR_T_tZ*(BR_t_Wb**2)*BR_Z_ll*(BR_W_qq**2)*(BR_Z_nunu+BR_Z_qq)   #TT -> ZttH -> ZWbWbZ     Z -> ll, Z -> qq/nunu
       
       pp_TTbar_dileptons_opposite_sign_Z = opposite_1 + opposite_2 + opposite_3
              
       #trileptons final state involving a Z boson
       trileptons_1 = self.CS_pp_TT*self.BR_T_tZ*self.BR_T_bW*BR_t_Wb*BR_Z_ll*BR_W_qq*BR_W_lnu  #TT -> ZtWb ->ZWbWb     Z->ll, WW ->lnuqq
       trileptons_2 = self.CS_pp_TT*self.BR_T_tZ*self.BR_T_tH*(BR_t_Wb**2)*BR_Z_ll*BR_H_bb*BR_W_qq*BR_W_lnu  #TT->tZtH->WbZWbH      Z->ll, H->qq, WW -> qqlnu
       trileptons_3 = self.CS_pp_TT*self.BR_T_tZ*self.BR_T_tH*(BR_t_Wb**2)*BR_Z_ll*BR_Z_nunu*BR_W_qq*BR_W_lnu #TT->tZtZ->WbWbZZ    Z->ll, W->qq,lnu, Z->nunu
       
       pp_TTbar_trileptons = trileptons_1 + trileptons_2 + trileptons_3
       
       #fourleptons final state involving a Z boson
       fourleptons_1 = self.CS_pp_TT*self.BR_T_tZ*self.BR_T_bW*BR_t_Wb*BR_Z_ll*BR_W_lnu**2        # TT -> ZtbW -> ZbWbW    Z -> ll, W -> lnu
       fourleptons_2 = self.CS_pp_TT*self.BR_T_tZ*self.BR_T_tH*(BR_t_Wb**2)*BR_Z_ll*BR_H_bb*BR_W_lnu**2   # TT -> ZttH -> ZWbWbH    Z -> ll, W -> lnu, H->bb
       fourleptons_3 = self.CS_pp_TT*self.BR_T_tZ*self.BR_T_tZ*(BR_t_Wb**2)*BR_Z_ll*BR_Z_nunu*BR_W_lnu**2    # TT -> ZttZ -> ZWbWbZ    Z -> ll, W -> lnu, H->bb
       
       pp_TTbar_fourleptons = fourleptons_1 + fourleptons_2 + fourleptons_3
       
       pp_TTbar_comb_one_ss_trifour =  pp_TTbar_one_lepton + pp_TTbar_dileptons_same_sign + pp_TTbar_trileptons + pp_TTbar_fourleptons
       
       pp_TTbar_comb_dileptons_opposite_trilepton = pp_TTbar_dileptons_opposite_sign_Z + pp_TTbar_trileptons #opposite sign dileptons final state + trileptons final state
       
       pp_TTbar_comb_ss_tri = pp_TTbar_dileptons_same_sign + pp_TTbar_trileptons
       
       return pp_TTbar_bW_plus_X, pp_TTbar_tZ_plus_X, pp_TTbar_tH_plus_X, pp_Tbq_tZ, pp_Tbq_bW, pp_Tbq_tH, pp_Ttq_tZ, pp_Ttq_bW, pp_Ttq_tH, pp_TTbar_comb_one_ss_trifour, pp_TTbar_comb_dileptons_opposite_trilepton, pp_TTbar_comb_ss_tri, pp_TTbar_one_lepton
       
      elif self.model == 'Doublet':
       
       self.BR_T_bW = 0
       self.BR_T_tZ = 0.5
       self.BR_T_tH = 0.5
       
       BR_t_Wb = 1
       BR_H_bb = 0.58
       BR_W_lnu = 0.3
       BR_W_qq = 0.6832
       BR_Z_ll = 0.1
       BR_Z_nunu = 0.2
       BR_Z_qq = 0.7
       
       pp_TTbar_bW_plus_X =   self.CS_pp_TT*self.BR_T_bW*(self.BR_T_bW + self.BR_T_tZ + self.BR_T_tH)
       pp_TTbar_tZ_plus_X =   self.CS_pp_TT*self.BR_T_tZ*(self.BR_T_tZ + self.BR_T_bW + self.BR_T_tH)
       pp_TTbar_tH_plus_X =   self.CS_pp_TT*self.BR_T_tH*(self.BR_T_tZ + self.BR_T_bW + self.BR_T_tH)
     
       pp_Tbq_bW = self.CS_pp_Tbq*self.BR_T_bW
       pp_Tbq_tZ = self.CS_pp_Tbq*self.BR_T_tZ
       pp_Tbq_tH = self.CS_pp_Tbq*self.BR_T_tH
     
       pp_Ttq_bW = self.CS_pp_Ttq*self.BR_T_bW
       pp_Ttq_tZ = self.CS_pp_Ttq*self.BR_T_tZ
       pp_Ttq_tH = self.CS_pp_Ttq*self.BR_T_tH
       
       pp_TTbar_one_lepton = self.CS_pp_TT*self.BR_T_tH*self.BR_T_tH*BR_t_Wb*BR_t_Wb*BR_H_bb*BR_H_bb*BR_W_lnu*BR_W_qq #TT -> HtHt -> HWbHWb     H -> bb, WW -> lnuqq 
       
       pp_TTbar_dileptons_same_sign = self.CS_pp_TT*self.BR_T_tZ*self.BR_T_bW*BR_t_Wb*BR_Z_ll*BR_W_qq*BR_W_lnu  #TT -> ZtWb -> ZWbWb      Z -> bb, WW -> lnuqq 
       
       #opposite sign leptons final state involving a Z boson
       opposite_1 = self.CS_pp_TT*self.BR_T_tZ*self.BR_T_bW*BR_Z_ll*BR_t_Wb*BR_W_qq**2   #TT -> ZtWb -> ZWbWb     Z -> ll, W -> qq
       opposite_2 = self.CS_pp_TT*self.BR_T_tZ*self.BR_T_tH*(BR_t_Wb**2)*BR_Z_ll*(BR_W_qq**2)*BR_H_bb       #TT -> ZttH -> ZWbWbH     Z -> ll, H -> qq
       opposite_3 = self.CS_pp_TT*self.BR_T_tZ*self.BR_T_tZ*(BR_t_Wb**2)*BR_Z_ll*(BR_W_qq**2)*(BR_Z_nunu+BR_Z_qq)   #TT -> ZttH -> ZWbWbZ     Z -> ll, Z -> qq/nunu
       
       pp_TTbar_dileptons_opposite_sign_Z = opposite_1 + opposite_2 + opposite_3
              
       #trileptons final state involving a Z boson
       trileptons_1 = self.CS_pp_TT*self.BR_T_tZ*self.BR_T_bW*BR_t_Wb*BR_Z_ll*BR_W_qq*BR_W_lnu  #TT -> ZtWb ->ZWbWb     Z->ll, WW ->lnuqq
       trileptons_2 = self.CS_pp_TT*self.BR_T_tZ*self.BR_T_tH*(BR_t_Wb**2)*BR_Z_ll*BR_H_bb*BR_W_qq*BR_W_lnu  #TT->tZtH->WbZWbH      Z->ll, H->qq, WW -> qqlnu
       trileptons_3 = self.CS_pp_TT*self.BR_T_tZ*self.BR_T_tH*(BR_t_Wb**2)*BR_Z_ll*BR_Z_nunu*BR_W_qq*BR_W_lnu #TT->tZtZ->WbWbZZ    Z->ll, W->qq,lnu, Z->nunu
       
       pp_TTbar_trileptons = trileptons_1 + trileptons_2 + trileptons_3
       
       #fourleptons final state involving a Z boson
       fourleptons_1 = self.CS_pp_TT*self.BR_T_tZ*self.BR_T_bW*BR_t_Wb*BR_Z_ll*BR_W_lnu**2        # TT -> ZtbW -> ZbWbW    Z -> ll, W -> lnu
       fourleptons_2 = self.CS_pp_TT*self.BR_T_tZ*self.BR_T_tH*(BR_t_Wb**2)*BR_Z_ll*BR_H_bb*BR_W_lnu**2   # TT -> ZttH -> ZWbWbH    Z -> ll, W -> lnu, H->bb
       fourleptons_3 = self.CS_pp_TT*self.BR_T_tZ*self.BR_T_tZ*(BR_t_Wb**2)*BR_Z_ll*BR_Z_nunu*BR_W_lnu**2    # TT -> ZttZ -> ZWbWbZ    Z -> ll, W -> lnu, H->bb
       
       pp_TTbar_fourleptons = fourleptons_1 + fourleptons_2 + fourleptons_3
       
       pp_TTbar_comb_one_ss_trifour =  pp_TTbar_one_lepton + pp_TTbar_dileptons_same_sign + pp_TTbar_trileptons + pp_TTbar_fourleptons
       
       pp_TTbar_comb_dileptons_opposite_trilepton = pp_TTbar_dileptons_opposite_sign_Z + pp_TTbar_trileptons # opposite sign dileptons final state + trileptons final state
       
       pp_TTbar_comb_ss_tri = pp_TTbar_dileptons_same_sign + pp_TTbar_trileptons
       
       return pp_TTbar_bW_plus_X, pp_TTbar_tZ_plus_X, pp_TTbar_tH_plus_X, pp_Tbq_tZ, pp_Tbq_bW, pp_Tbq_tH, pp_Ttq_tZ, pp_Ttq_bW, pp_Ttq_tH, pp_TTbar_comb_one_ss_trifour, pp_TTbar_comb_dileptons_opposite_trilepton, pp_TTbar_comb_ss_tri, pp_TTbar_one_lepton
      
      else:
       print("Error in model choice") 
 
    def numerator(self,i):
    
     #cs_bW, cs_tZ, cs_tH, cs_Tbq_Zt, cs_Tbq_bW, cs_Tbq_tH, cs_Ttq_tZ, cs_Ttq_bW, cs_Ttq_tH, pp_TTbar_comb_1234, pp_TTbar_comb_23, pp_TTbar_comb_ss_tri, pp_TTbar_1l = self.complete_CS_Calc()
  
     
     if self.model == 'Singlet' : 
      cs_bW, cs_tZ, cs_tH, cs_Tbq_Zt, cs_Tbq_bW, cs_Tbq_tH, cs_Ttq_tZ, cs_Ttq_bW, cs_Ttq_tH, pp_TTbar_comb_1234, pp_TTbar_comb_23, pp_TTbar_comb_ss_tri, pp_TTbar_1l = self.complete_CS_Calc()
      if  i < 9 :
          
        if self.process[i] == 'pp --> TTbar --> Zt + X -> 1l + E_miss' :  
          num = cs_tZ
          return num
        
        elif self.process[i] == 'pp --> TTbar --> l + 2l + >= 3leptons' :  
          num = pp_TTbar_comb_1234
          return num 
       
        elif self.process[i] == 'pp --> TTbar --> WbWb' :  
          num = cs_bW
          return num
          
        elif self.process[i] == 'pp --> TTbar --> Zt + X -> l+l- + 3l':
         num = pp_TTbar_comb_23
         return num 
         
        elif self.process[i] == 'pp --> TTbar --> 2l + 3leptons':
         num = pp_TTbar_comb_ss_tri
         return num
       
        elif self.process[i] == 'pp --> TTbar --> 1l':
         num = pp_TTbar_1l
         return num   
               
        else:
         return -1  
      
      elif self.width_mass_ratio is not None  :  
        
        if (i == 9 and self.width_mass_ratio <= 0.05) or (i == 10 and self.width_mass_ratio == 0.1) or (i == 11 and self.width_mass_ratio == 0.2)  or (i == 12 and self.width_mass_ratio == 0.3) :#or i == 13 or i==14 :
         num = cs_Tbq_Zt
         return num 
        
       # if (i==15 and self.width_mass_ratio <= 0.05)\
       #       or (i==16 and self.coupling_TbW_L==0.5):
       #  num = cs_Tbq_tH
       #  return num
        
        else:
         return -1
      else:
       return -1
        
     elif  self.model == 'Doublet':
        cs_bW, cs_tZ, cs_tH, cs_Tbq_Zt, cs_Tbq_bW, cs_Tbq_tH, cs_Ttq_tZ, cs_Ttq_bW, cs_Ttq_tH, pp_TTbar_comb_1234, pp_TTbar_comb_23, pp_TTbar_comb_ss_tri, pp_TTbar_1l = self.complete_CS_Calc()
        if self.process[i] == 'pp --> TTbar --> l + 2l + >= 3leptons' :  
          num = pp_TTbar_comb
          return num 
        
        elif self.process[i] == 'pp --> TTbar --> Zt + X -> 1l + E_miss' :
          num = cs_tZ
          return num
        
        elif self.process[i] == 'pp --> Ttq --> tHtq'  :
          num = cs_Ttq_tH
          return num   
        
        elif self.process[i] == 'pp --> Ttq --> tZtq'  :
          num = cs_Ttq_tZ
          return num 
        
        elif self.process[i] == 'pp --> TTbar --> Zt + X -> l+l- + 3l':
         num = pp_TTbar_comb_23
         return num
        
        else:
         return -1
     elif self.model == 'Pure':
       
       cs_bW, cs_tZ, cs_tH, cs_Tbq_Zt, cs_Tbq_bW, cs_Tbq_tH, cs_Ttq_tZ, cs_Ttq_bW, cs_Ttq_tH = self.complete_CS_Calc()
       
       if self.process[i] == 'pp --> TTbar --> tZtZ' :  
          num = cs_tZ
          return num 
       elif self.process[i] == 'pp --> TTbar --> tHtH' :
          num = cs_tH
          return num
       elif self.process[i] == 'pp --> TTbar --> WbWb' :
          num = cs_bW
          return num
       elif self.process[i] == 'pp --> Tbq --> bWbq' :
          num = cs_Tbq_bW
          return num
       else :
        return -1
    def denominator(self, num,index,t):
        if num >= 0 and min(self.MT[index]) <= self.MT_theo and max(self.MT[index]) >= self.MT_theo:
         expected_or_observed = interp1d(self.MT[index], t[index], 'linear')  
         Denominator = expected_or_observed(self.MT_theo) #donne l'observed limit qui correspont à la masse théorique entrée par l'utilisateur
         return Denominator         
        else:
         d = -1
         return d

    def Expected_Ratio_Cal(self):
     try:
      maximum = -1000000
      for index,Id in enumerate(self.Id):  
        n = self.numerator(index)
        d = self.denominator(n,index,self.exp)
        if d == -1:
         continue
        rat = n/d    
        if rat > maximum :
           maximum = rat
           pos = index
      return pos
     except UnboundLocalError:
      sys.exit(f"The mass {self.MT_theo} is not in the range of included experiment files")
    
    def check_channel(self):
      position = self.Expected_Ratio_Cal()
      numerator = self.numerator(position)
      deno = self.denominator(numerator,position,self.obs) 
      observed_ratio = numerator/deno
      self.obsratio = observed_ratio
      if self.obsratio >= 1 :
       self.allowed = 0
       self.channel = position
      else :
       self.allowed = 1
       self.channel = position
    
    def Find_Singlet_Limit(self,MT,pp_TTbar,pp_Tbq,pp_Ttq):
     self.CS_pp_TT = pp_TTbar
     self.CS_pp_Tbq = pp_Tbq
     self.CS_pp_Ttq = pp_Ttq
     self.MT_theo = MT
     self.initialize_tables_CMS_AND_ATLAS()
     self.check_channel()
    
    def Find_Doublet_Limit(self,MT,pp_TTbar,pp_Tbq,pp_Ttq):
     self.CS_pp_TT = pp_TTbar
     self.CS_pp_Tbq = pp_Tbq
     self.CS_pp_Ttq = pp_Ttq
     self.MT_theo = MT
     self.initialize_tables_CMS_AND_ATLAS()
     self.check_channel()
    
    def Pure_decay_input(self,MT,pp_TTbar,pp_Tbq,pp_Ttq,BR_T_bW,BR_T_tZ,BR_T_tH):
        self.MT_theo = MT
        self.CS_pp_TT = pp_TTbar
        self.CS_pp_Tbq = pp_Tbq
        self.CS_pp_Ttq = pp_Ttq
        self.BR_T_bW = BR_T_bW
        self.BR_T_tZ = BR_T_tZ
        self.BR_T_tH = BR_T_tH
        self.initialize_tables_CMS_AND_ATLAS()
        self.check_channel()
        
        
    
