from multiprocessing import Pool
import numpy as np

def E_FIELD(n,X_p_FRMp,loop_FRMp, CC_dE,Ea_FRMp_x,Ea_FRMp_y,X_p,CC_FRMe1,CC_FRMe2,Ve,gamma_Ve,T0,c,\
            CC_FRMep,Vp_FRMe,gamma_Vep,loop_FRMep,Ee_FRMep_x,Ee_FRMep_y):
    for j in range(n):
            for i in range(n):
                ##################################################################
                ### Atoms Field ###! CHECKED !###
                disp = X_p_FRMp[i,j,:] - loop_FRMp
                dE_a = - CC_dE * ( disp / np.linalg.norm(disp)**3 )
                Ea_FRMp_x[i,j] = Ea_FRMp_x[i,j] + dE_a[0]
                Ea_FRMp_y[i,j] = Ea_FRMp_y[i,j] + dE_a[1]
    
                ##################################################################
                ### Electrons field ###
                ### <lab> --> <e> ###
                X_p_FRMe = X_p[i,j] + ( CC_FRMe1 * np.dot(Ve,X_p[i,j]) - CC_FRMe2 ) * Ve
                T_FRMe = gamma_Ve * ( T0 - np.dot(Ve,X_p[i,j])/c**2 ) # for all points
                
                ### <e> --> <p> ###
                X_p_FRMep = X_p_FRMe + ( CC_FRMep * np.dot(Vp_FRMe,X_p_FRMe) - gamma_Vep * T_FRMe ) * Vp_FRMe                 
    
                ### Electron E-field: Frame <ep> ###! CHECKED !###
                disp = X_p_FRMep - loop_FRMep #X_p - loop
                dE_e = CC_dE * ( disp / np.linalg.norm(disp)**3 )
                Ee_FRMep_x[i,j] = Ee_FRMep_x[i,j] + dE_e[0]
                Ee_FRMep_y[i,j] = Ee_FRMep_y[i,j] + dE_e[1]  
                
    return Ea_FRMp_x, Ea_FRMp_y, Ee_FRMep_x, Ee_FRMep_y      
                
def E_FIELD_mp(k,n,X_p_FRMp,loop_FRMp, CC_dE,Ea_FRMp_x,Ea_FRMp_y,X_p,CC_FRMe1,CC_FRMe2,Ve,gamma_Ve,T0,c,\
            CC_FRMep,Vp_FRMe,gamma_Vep,loop_FRMep,Ee_FRMep_x,Ee_FRMep_y):
    
    if k == 1:
        p = Pool()
        Ea_FRMp_x, Ea_FRMp_y, Ee_FRMep_x, Ee_FRMep_y = p.map(E_FIELD, n,X_p_FRMp,loop_FRMp, CC_dE,Ea_FRMp_x,Ea_FRMp_y,X_p,CC_FRMe1,CC_FRMe2,Ve,gamma_Ve,T0,c,\
                CC_FRMep,Vp_FRMe,gamma_Vep,loop_FRMep,Ee_FRMep_x,Ee_FRMep_y)
        p.close()
        p.join()
    
    return Ea_FRMp_x, Ea_FRMp_y, Ee_FRMep_x, Ee_FRMep_y

    
    
# =============================================================================
# 
# def E_FIELD_mp(numbers):
#     start_time = time.time()
#     result = []
#     for i in numbers:
#         result.append(add(i))
#     #print(result)
#     end_time = time.time() - start_time
#     print(end_time)
# =============================================================================
