#======================================================================
# Code to plot the bounds on chi and kappa with high res plot
# SM 12/2016
#======================================================================

import numpy as np
import matplotlib.pyplot as plt
import matplotlib
from scipy import interpolate
from scipy.interpolate import griddata
import glob

goldenratio = 2. / (1 + 5**.5)
# matplotlib.rcParams.update({
#         "font.size": 18.0,
#         "axes.titlesize": 18.0,
#         "axes.labelsize": 18.0,
#         "xtick.labelsize": 18.0,
#         "ytick.labelsize": 18.0,
#         "legend.fontsize": 18.0,
#         "figure.figsize": (10.3, 10.3*goldenratio),
#         "figure.dpi": 300,
#         "savefig.dpi": 300,
#         "text.usetex": True
# })

def HRATIO(CUBE, _chi1, psiJ = 0.001, A0 = 1, F = 1):

        """
        # thetaJ = DATA["THETAJ"]
        # H0 = (3.0/4.0)*A0*F*np.cos(2.0*psiJ)*np.sin(thetaJ)**2.0
        # H2 = A0*F*np.power(np.power((1.0 + np.cos(thetaJ)**2.0)/2.0, 2.0)*np.cos(2*psiJ)**2.0 + (np.cos(thetaJ)*np.sin(2*psiJ))**2.0, 0.5)
        # return H0/H2
        """

        H2H0 = np.linspace(-1.5, 1.5, 200)
        return H0H2[_chi1]

DATA = np.load("/Users/apple/Documents/Mars/output/datasets/output-2017_01_10_17_08_30/overlaps_eta_0.06_chi1_1.72_N_200.npz")

SNR_2 = DATA["SNR_02"]
SNR_0 = DATA["SNR_00"]
SRATIO = SNR_2/SNR_0

for index, value in np.ndenumerate(SRATIO):
      if np.abs(value - 1.0) > 0.25:
        SRATIO[index] = np.nan
      else:
        SRATIO[index] = value*0.83      #directly adding this here.

print "Finished modidying the array."

SLICE = SRATIO

KAPPA = np.linspace(-0.5, 1.0, 200) 
CHI1  = np.linspace(0.2, 0.8, 200) 

plt.contourf(KAPPA, CHI1, SRATIO, cmap='viridis_r')

#plotting the lines for the bounds
plt.axhline(CHI1[np.isfinite(SLICE[:, 0])][-1], linestyle='-.' ,color='k',alpha=0.5)
plt.axhline(CHI1[np.isfinite(SLICE[:, 0])][0] , linestyle='-.' ,color='k',alpha=0.5)
plt.axvline(KAPPA[np.isfinite(SLICE[-1])][-1], linestyle='--' ,color='k',alpha=0.5)
plt.axvline(KAPPA[np.isfinite(SLICE[-1])][0] , linestyle='--' ,color='k',alpha=0.5)

plt.xlabel(r"$\kappa$")
plt.ylabel(r"$\chi_{1}$")
plt.title(r"$\eta = %1.3f, H_{0}/H_{2}=0.83$"%(DATA["ETA"]))
plt.colorbar()
plt.tight_layout()
plt.show()
# plt.savefig("./test_regions.pdf")
# plt.close()
















