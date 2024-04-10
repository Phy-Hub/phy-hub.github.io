import SR_Functions as SR

V_p = 0.8
GAM_Vp = SR.Gamma(V_p)
x = 20
x_FRMp = SR.TRANS_Coords(x, 0, V_p, V_p, GAM_Vp, x*V_p)

V_e = 0.4
GAM_Ve = SR.Gamma(V_e)
x_FRMe = SR.TRANS_Coords(x, 0, V_e, V_e, GAM_Ve, x*V_e)

Vp_FRMe = SR.TRANS_Velocity(V_p, V_e, V_e, GAM_Ve, V_e*V_p)
GAM_Vp_FRMe = SR.Gamma(Vp_FRMe)
T_FRMe = SR.TRANS_Time(x, 0, V_e, GAM_Ve, x*V_e)

x_FRMep = SR.TRANS_Coords(x_FRMe, T_FRMe, Vp_FRMe, Vp_FRMe, GAM_Vp_FRMe, x_FRMe*Vp_FRMe)

print(x,x_FRMp, x_FRMep)