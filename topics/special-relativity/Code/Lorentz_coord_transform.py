import Paths as path
import SR_Functions as SR
import matplotlib.pyplot as plt
import numpy as np
import time
start_time = time.time()
filename_prefix = "coord_transform_"
### Set up ####################################################################
c = 1
V = np.array([ 0 , 0.9 ])
Gamma = 1 / np.sqrt( 1 - ( V[1] / c )**2 )

N_r = 11
coords_max = 10
y = np.linspace(-coords_max, coords_max, N_r)
z = np.linspace(-coords_max, coords_max, N_r)
yv, zv = np.meshgrid(y, z)
zv_prime, yv_prime = np.meshgrid(y, z)

### Plots #####################################################################
### Format ####################################################################
sc =  0.7/3 #arrow scale
zlim = 24
zlim_neg = 13
ylim = 13
def PlotStyle(y_name,z_name, axis_color):
    #plt.figure(frameon=False)
    plt.axis('equal')
    plt.axis('off')
    plt.axis('square')
    plt.xlim([-ylim, ylim])
    plt.ylim([-zlim_neg,zlim])
    plt.arrow(-ylim, 0, 2*ylim, 0, lw = 1, head_width=1.3, head_length=1, overhang = sc,
              length_includes_head= True, color = axis_color)
    plt.arrow(0, -zlim_neg, 0, zlim+zlim_neg ,lw = 1, head_width=1.3, head_length=1, overhang = sc,
              length_includes_head= True, color = axis_color)
    plt.annotate(y_name, xy=(0, 0), xytext=(ylim-1,1),color = axis_color)
    plt.annotate(z_name, xy=(0, 0), xytext=(1,zlim-2),color = axis_color)

def v_arrow():
    plt.arrow(-ylim +1, 0, 0, 4, lw = 1, head_width=1.3, head_length=1, overhang = sc,
          length_includes_head= True, color = "grey")
    plt.arrow(-ylim +1, 0, 0, 3, lw = 1, head_width=1.3, head_length=1, overhang = sc,
          length_includes_head= True, color = "grey")
    plt.annotate("v", xy=(0, 0), xytext=(-ylim,5), color = "grey")

plt.figure(1) ################################################################

PlotStyle("y","z","black")
plt.ylim([-zlim,zlim])
v_arrow()
plt.plot(yv, zv, marker='o', color='black', linestyle='none',ms=1)
for I_R in range(N_r):
    plt.annotate("t = 0", xy=(0, 0), xytext=(15,z[I_R]-0.4))

plt.savefig(path.svg + filename_prefix + "initial.svg",bbox_inches='tight', format='svg',transparent=True) # changed from svg
plt.savefig(path.pdf + filename_prefix + "initial.pdf",bbox_inches='tight', format='pdf',transparent=True) # changed from svg

plt.figure(2) ################################################################

PlotStyle("y'","z'","grey")
plt.ylim([-zlim,zlim])
tcolour = np.zeros((N_r,N_r))

for I_y in range(N_r):
    zv_prime[I_y] = SR.TRANS_Z(zv[I_y], V[1], 0)

    for I_z in range(N_r):
        tcolour[I_y,I_z] = Gamma * ( zv[I_y,I_z] * V[1] )

    t_prime = round( SR.TRANS_1Time(zv[I_y,0], V[1], 0),1)
    plt.annotate("t' = %s" %t_prime, xy=(0, 0), xytext=(15,zv_prime[I_y,0]-0.4))

plt.quiver(yv, zv_prime, 0, -0.7, tcolour, cmap = 'jet' ,
                angles="xy" , zorder=1, pivot="mid",
                alpha=1,width=0.005, scale=5, scale_units='inches', headwidth=5
                )#,headwidth=1)   #)

plt.savefig(path.svg + filename_prefix + "primed.svg",bbox_inches='tight', format='svg',transparent=True) # changed from svg
plt.savefig(path.pdf + filename_prefix + "primed.pdf",bbox_inches='tight', format='pdf',transparent=True) # changed from svg

plt.figure(3) ################################################################

PlotStyle("y'","z'","grey")
plt.ylim([-zlim,zlim])
for I_R in range(N_r):
    zv[I_R] = SR.TRANS_Z_simul(zv[I_R], V[1], -V[1], 0)

plt.quiver(yv, zv, 0, -0.7, angles="xy" , zorder=1, pivot="mid", alpha=1,width=0.005,
           scale=5, scale_units='inches', headwidth=5)#,headwidth=1)   #)

plt.annotate("$t' = 0$" , xy=(0, 0), xytext=(15,5))

plt.savefig(path.svg + filename_prefix + "primed_sychronised.svg",bbox_inches='tight', format='svg',transparent=True) # changed from svg
plt.savefig(path.pdf + filename_prefix + "primed_sychronised.pdf",bbox_inches='tight', format='pdf',transparent=True) # changed from svg

plt.figure(4) ################################################################

PlotStyle("y","z","black")
v_arrow()
yv, zv = np.meshgrid(y, z)
#R_mag = np.sqrt( yv**2 + zv**2 )
#R_mag_norm = R_mag / R_mag.max()
plt.plot(yv, zv, marker='o', color='black', linestyle='none',ms=1)
#plt.scatter(yv, zv, c=R_mag_norm, cmap='turbo', marker='o', s=6)
#plt.colorbar(label='retarded time')

plt.savefig(path.svg + filename_prefix + "initial_with_retarded_time.svg",bbox_inches='tight', format='svg',transparent=True) # changed from svg
plt.savefig(path.pdf + filename_prefix + "initial_with_retarded_time.pdf",bbox_inches='tight', format='pdf',transparent=True) # changed from svg

plt.figure(5) ################################################################

PlotStyle("y'","z'","grey")
for I_R in range(N_r):
    zv[I_R] = Gamma * ( zv[I_R] + V[1] * np.sqrt( zv[I_R]**2 + yv[I_R]**2) )

plt.quiver(yv, zv, 0, -0.7, angles="xy" , zorder=1, pivot="mid", alpha=1,width=0.005,
           scale=5, scale_units='inches', headwidth=5, color='black')#,headwidth=1)   #)

#plt.annotate("$t' = t'_{ret}$" , xy=(0, 0), xytext=(15,5))

plt.savefig(path.svg + filename_prefix + "primed_retarded.svg",bbox_inches='tight', format='svg',transparent=True)
plt.savefig(path.pdf + filename_prefix + "primed_retarded.pdf",bbox_inches='tight', format='pdf',transparent=True)

plt.figure(6) ################################################################

PlotStyle("y'","z'","grey")
#plt.annotate("Aberrated" , xy=(0, 0), xytext=(15,5))

y = np.linspace(-coords_max, coords_max, N_r)
z = np.linspace(-coords_max, coords_max, N_r)
yv, zv = np.meshgrid(y, z)

R_mag = np.sqrt( yv**2 + zv**2 ) +0.0001
Cos = zv / R_mag
Sin = yv / R_mag
AA = Gamma * ( 1 - V[1]* Cos )

Cos_PRM = - ( Cos - V[1] ) / ( 1 - V[1] *Cos )
Sin_PRM = Sin / AA

plt.plot(R_mag * Sin_PRM, R_mag * Cos_PRM, marker='o', color='black', linestyle='none',ms=1)

plt.savefig(path.svg + filename_prefix + "aberrated.svg",bbox_inches='tight', format='svg',transparent=True) # changed from svg
plt.savefig(path.pdf + filename_prefix + "aberrated.pdf",bbox_inches='tight', format='pdf',transparent=True) # changed from svg

plt.figure(7) ################################################################

PlotStyle("y'","z'","grey")
#plt.annotate("Aberrated \n and \n scaled" , xy=(0, 0), xytext=(15,5))

plt.quiver(AA * R_mag * Sin_PRM, AA *  R_mag * Cos_PRM, 0, -0.7, angles="xy" , zorder=1, pivot="mid", alpha=1,width=0.005,
           scale=5, scale_units='inches', headwidth=5, color='black')#,headwidth=1)   #)

plt.savefig(path.svg + filename_prefix + "aberrated_and_scaled.svg",bbox_inches='tight', format='svg',transparent=True) # changed from svg
plt.savefig(path.pdf + filename_prefix + "aberrated_and_scaled.pdf",bbox_inches='tight', format='pdf',transparent=True) # changed from svg



##############################################################################
##############################################################################
# plt.figure(7) ################################################################

# plt.axis('equal')
# plt.axis('off')
# plt.axis('square')
# plt.xlim([-ylim, ylim])
# plt.ylim([-ylim,ylim])
# plt.arrow(-ylim, 0, 2*ylim, 0, lw = 1, head_width=1.3, head_length=1, overhang = sc,
#             length_includes_head= True, color = 'grey')
# plt.arrow(0, -zlim, 0, 2*zlim ,lw = 1, head_width=1.3, head_length=1, overhang = sc,
#             length_includes_head= True, color = 'grey')
# plt.annotate("y'", xy=(0, 0), xytext=(ylim-1,1),color = 'grey')
# plt.annotate("z'", xy=(0, 0), xytext=(1,zlim-2),color = 'grey')


# plt.quiver(AA * R_mag * Sin_PRM, AA *  R_mag * Cos_PRM, 0, -0.7, angles="xy" , zorder=1, pivot="mid", alpha=1,width=0.005,
#            scale=5, scale_units='inches', headwidth=5, color='black')#,headwidth=1)   #)

# plt.savefig(path.svg + filename_prefix + "aberrated_and_scaled.svg",bbox_inches='tight', format='svg',transparent=True) # changed from svg
# plt.savefig(path.pdf + filename_prefix + "aberrated_and_scaled.pdf",bbox_inches='tight', format='pdf',transparent=True) # changed from svg

###
plt.show()
print(" Run time: %s seconds" % (time.time() - start_time))
