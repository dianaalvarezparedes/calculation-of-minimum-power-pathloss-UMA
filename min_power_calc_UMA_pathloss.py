import math
#import matplotlib.pyplot as plt
def pathloss_UMA_LOS_auxiliar(d2D,fc,hBS,hUT):
    c=299792458
    hE=1
    hBS1=hBS-hE
    hUT1=hUT-hE
    dBP1=4*hBS1*hUT1*fc*1000000000/c
    d3D=math.sqrt(pow(d2D,2)+math.pow(hBS-hUT,2))
    PL11=28.0+22*math.log10(d3D)+20*math.log10(fc)
    PL21=28.0+40*math.log10(d3D)+20*math.log10(fc)-9*math.log10(pow(dBP1,2)+math.pow(hBS-hUT,2))
    #resp=PL21; gamma_SF=4
    
    if d2D>10 or d2D==10:
         if d2D<dBP1 or d2D==dBP1:
             resp=PL11
             gamma_SF=4
         elif d2D<5000 or d2D==dBP1:
             resp=PL21
             gamma_SF=4
         else:
             print("The model UMA LOS does not work for more than 10km")
             return
    else:
         print("The model UMA LOS does not work for less than 10m")
         return
    return resp, gamma_SF

#resp, gamma_SF = pathloss_UMA_LOS_auxiliar(30,3.5,15,1.6)
#print(resp)
#print(gamma_SF)

def minimum_received_power(d2D,fc,hBS,hUT,gnb_antenna_gain_dbi,beamforming_gain,LOS_NLOS_flag):
#function [min_power_ue_ant_sensib] = minimum_received_power(d2D,fc,hBS,hUT)
    trans_power_db = 53
    #gnb_antenna_gain_dbi = 10
    if LOS_NLOS_flag==0:
        path_loss_db, gamma_SF = pathloss_UMA_LOS_auxiliar(d2D,fc,hBS,hUT)
    else:
        path_loss_db, gamma_SF = pathloss_UMA_NLOS(d2D,fc,hBS,hUT)
       
    ue_antena_gain_db = 0
    min_power_ue_ant_sensib_db = trans_power_db + gnb_antenna_gain_dbi - path_loss_db - ue_antena_gain_db + beamforming_gain
    min_power_ue_ant_sensib = math.pow(10,((min_power_ue_ant_sensib_db-30)/10))
    return min_power_ue_ant_sensib

#min_power_ue_ant_sensib = minimum_received_power(30,3.5,15,1.6)
#print(min_power_ue_ant_sensib)

def pathloss_UMA_NLOS(d2D,fc,hBS,hUT):

    PL_UMA_LOS, gamma_SF = pathloss_UMA_LOS_auxiliar(d2D,fc,hBS,hUT)
    d3D=math.sqrt(math.pow(d2D,2)+math.pow(hBS-hUT,2))
    PL1_UMA_NLOS1=13.54+39.08*math.log10(d3D)+20*math.log10(fc)-0.6*(hUT-1.5)
    
    if d2D>10 or d2D==10:
        if d2D<5000 or d2D==5000:
            PL1_UMA_NLOS=PL1_UMA_NLOS1
        else:
            print("The model UMA LOS does not work for more than 5km")
            return
    else:
        print("The model UMA LOS does not work for less than 10m")
        return
    
    PL1_UMA_NLOS=PL1_UMA_NLOS1
    PL_RMA_NLOS=max(PL_UMA_LOS,PL1_UMA_NLOS)
    resp=PL_RMA_NLOS
    gamma_SF=6
    return resp, gamma_SF


