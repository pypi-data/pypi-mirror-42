import pyFAI, pyFAI.detectors
import fabio, subprocess
import numpy as np

class calibration():
	def __init__(self):
		pass

	def setDetector(self, pix1=2e-4, pix2=2e-4):
		pyFAI.detectors.Detector(pixel1=2e-4, pixel2=2e-4)

	def setfit2DCalib(self, wavelength):
		self.ai = pyFAI.AzimuthalIntegrator(wavelength=wavelength)	
		self.ai.setFit2D(217.0219, 1031.664, 1024.717, tilt=1.481447e-2,
                         tiltPlanRotation=103.0919, pixelX=200, pixelY=200)
		self.imgflip = np.flipud(fabio.open('WOEtH_RT-00001.tif').data)	
		self.ai.integrate1d(self.imgflip, 2000, filename='moke0.dat', correctSolidAngle=True, mask=None, unit='q_A^-1')

	def setMask(self, maskName):
		self.mask = np.asanyarray(maskName, order='C').data

	def setDioptasPoniCalib(self):
		self.ai = pyFAI.load("Dioptas.poni")

	def setImg(self, imgName):
		self.img = fabio.open(imgName).data		

	def setDioptasCalib(self):
		self.ai = pyFAI.AzimuthalIntegrator(dist=0.217021892746, poni1= 0.204888745042, poni2=0.206345510462,
		                               rot1=5.85676487728e-05, rot2=0.000251840753446, rot3=7.37486050006e-09,
		                               pixel1=0.00019999999999999998, pixel2=0.00019999999999999998,
		        	                   splineFile=None, detector=None, wavelength=2.0696999999999997e-11)

	def dioptasIntegrate(self):
		ai.integrate1d(self.img, 2048, filename='methodcsr.dat', correctSolidAngle=True, mask=self.mask, polarization_factor=0.990,unit='q_A^-1')  # Setup integration parameters

	def __str__:(self):
		print self.ai




if __name__ == '__main__':
	pass
