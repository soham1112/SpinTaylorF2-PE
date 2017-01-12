#======================================================================
# Code to explore the bounds on H0/H2 using psiJ--thetaJ--kappa values.
# SM 1/2017
#======================================================================

"""
Here's what I'm doing. We know SNR_2/SNR_0(chi1, thetaJ, kappa).

Then we can find the 3D array of the scalar product(chi1, thetaJ, kappa)
for a fixed value of psiJ (here 0.001) such that 
SNR_2/SNR_0(chi1, thetaJ, kappa) = scalar product(chi1, thetaJ, kappa) * H0/H2(thetaJ, psiJ = 0.0001)

Having done this, we can now compute SNR_2/SNR_0(chi1, thetaJ, kappa, *psiJ*) using
SNR_2/SNR_0(chi1, thetaJ, kappa, *psiJ*) = scalar product(chi1, thetaJ, kappa) * H0/H2(thetaJ, psiJ = 0.0001).

And then you can find the points in the thetaJ, psiJ parameter space which correspond to the SNR ratio between 0.75 
and 1.25 from which we compute the bounds on H0/H2.

At least this is what I understood Archana meant. 
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib
from scipy import interpolate
import glob

def HRATIO(cube, _thetaJ, psiJ=0.001, A0 = 1, F = 1):
	thetaJ = DATA["THETAJ"][_thetaJ]
	H0 = (3.0/4.0)*A0*F*np.cos(2.0*psiJ)*np.sin(thetaJ)**2.0
	H2 = A0*F*np.power(np.power((1.0 + np.cos(thetaJ)**2.0)/2.0, 2.0)*np.cos(2*psiJ)**2.0 + (np.cos(thetaJ)*np.sin(2*psiJ))**2.0, 0.5)
	return H0/H2

def HRATIO_PSIJ(cube, PSIJ, _thetaJ, _psiJ, A0 = 1, F = 1):
	thetaJ = DATA["THETAJ"][_thetaJ]
	psiJ   = PSIJ[_psiJ]

	H0 = (3.0/4.0)*A0*F*np.cos(2.0*psiJ)*np.sin(thetaJ)**2.0
	H2 = A0*F*np.power(np.power((1.0 + np.cos(thetaJ)**2.0)/2.0, 2.0)*np.cos(2*psiJ)**2.0 + (np.cos(thetaJ)*np.sin(2*psiJ))**2.0, 0.5)
	return H0/H2

FILES = glob.glob("../../output/datasets/output-2016_10_19_19_24_50/overlaps*")
PSIJ  = np.linspace(0, 2*np.pi, 50) 

SNR_RATIO_GENERIC_PSIJ = np.zeros((50, 50, 50, 50, 4))

for index_file, _file in enumerate(FILES):
	DATA  = np.load(_file)
	print "ETA", DATA["ETA"]
	print "------------------------------"
	
	SNR_2 = DATA["SNR_02"]
	SNR_0 = DATA["SNR_00"]

	SRATIO = SNR_2/SNR_0

	"""
	Defining a matrix that will hold the scalar product matrix.
	This matrix will have entries for each chi and kappa. The indexing
	therefore would remain the same as mentioned below.
	"""

	SPMATRIX = np.zeros(np.shape(SRATIO))
	
	"""
	Here we are only choosing the 
	points that are between 0.75 and 1.25. 
	the indexing is [_chi][_thetaJ][kappa]
	"""

	for index, value in np.ndenumerate(SRATIO):
		if np.abs(value - 1.0) > 0.25:
			SPMATRIX[index] = np.nan
		else:
			SPMATRIX[index] = value*HRATIO(DATA, index[1])

	"""
	Having generated the scalar product matrix, we now compute
	SNR_2/SNR_0(chi1, thetaJ, kappa, *psiJ*) for a particular value 
	of eta. Thus the indexing now would be: [_chi][_thetaJ][kappa][psiJ]
	"""


	for index_psiJ, _psiJ in enumerate(PSIJ):
		print "Working on iteration: ", index_psiJ
		for index, value in np.ndenumerate(SRATIO):
			SNR_RATIO_GENERIC_PSIJ[index[0], index[1], index[2], index_psiJ, index_file] = SPMATRIX[index]*HRATIO_PSIJ(DATA, PSIJ, index[1], index_psiJ)




np.savez("./SNR_RATIO_GENERIC_PSIJ",
	SNR_RATIO_GENERIC_PSIJ_GRID = SNR_RATIO_GENERIC_PSIJ)












