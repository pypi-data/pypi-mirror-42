import pyFAI, pyFAI.detectors
import fabio, subprocess
import numpy as np

detector = pyFAI.detectors.Detector(pixel1=2e-4, pixel2=2e-4)
#ai = pyFAI.AzimuthalIntegrator(dist=0.217021892746, poni1= 0.204888745042, poni2=0.206345510462,
#                               rot1=5.85676487728e-05, rot2=0.000251840753446, rot3=7.37486050006e-09,
#                               pixel1=0.00019999999999999998, pixel2=0.00019999999999999998,
#                               splineFile=None, detector=None, wavelength=2.0696999999999997e-11)
#print(ai)
#ai = pyFAI.AzimuthalIntegrator(splineFile='Dioptas.poni')
#ai.setFit2D  # Sets the configuration to Fit2D
#print'\n',(ai)


aii = pyFAI.AzimuthalIntegrator(wavelength=2.0696999999999997e-11)  # Wavelength is needed for Fit2D
ai = pyFAI.AzimuthalIntegrator()  # Wavelength is not needed if giving poni file

### Fit2D

aii.setFit2D(217.0219, 1031.664, 1024.717, tilt=1.481447e-2,
            tiltPlanRotation=103.0919, pixelX=200, pixelY=200)  # Sets the configuration to Fit2D
imgflip = np.flipud(fabio.open('WOEtH_RT-00001.tif').data)  # Tif files are flipped

print 'Fit2D:\n', aii
res = aii.integrate1d(imgflip, 2000, filename='moke0.dat', correctSolidAngle=True, mask=None, unit='q_A^-1')  # Setup integration parameters

### Dioptas poni

ai = pyFAI.load("Dioptas.poni")
img = fabio.open('WOEtH240-00111.tif').data  # Gives the same if you import with scipy.ndimage.imread
mask = np.asanyarray('Dioptas.mask', order='C').data  # Loading mask array into picture

print '\nDioptas poni:\n', ai
res = ai.integrate1d(img, 2048, filename='methodcsr.dat', correctSolidAngle=True, mask=mask, polarization_factor=0.990,unit='q_A^-1')  # Setup integration parameters

'''
If correctSolidAngle is False for dioptas and Pyfai then i get same results. 
But they to correct for it in different ways.

It is possible to correct or not the powder diffraction pattern using the correctSolidAngle parameter. 
The weight of a pixel is ponderate by its solid angle.
'''
### Dioptas setting

ai = pyFAI.AzimuthalIntegrator(dist=0.217021892746, poni1= 0.204888745042, poni2=0.206345510462,
                               rot1=5.85676487728e-05, rot2=0.000251840753446, rot3=7.37486050006e-09,
                               pixel1=0.00019999999999999998, pixel2=0.00019999999999999998,
                               splineFile=None, detector=None, wavelength=2.0696999999999997e-11)

print '\nDioptas:\n', ai
res = ai.integrate1d(img, 2000, filename='moke2.dat', correctSolidAngle=True, mask=None, unit='q_A^-1')  # Setup integration parameters

### Mask

#mask_call = 'pyFAI-drawmask ' + 'WOEtH_RT-00001.tif'  # Masks ave_files
#print mask_call
#subprocess.call(mask_call)
