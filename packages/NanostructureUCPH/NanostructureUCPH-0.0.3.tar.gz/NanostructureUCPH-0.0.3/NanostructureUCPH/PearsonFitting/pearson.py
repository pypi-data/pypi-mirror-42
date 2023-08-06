import os
import string
import numpy as np
import matplotlib.pyplot as plt

from tqdm import tqdm
from scipy import stats
from scipy.optimize.minpack import leastsq
from diffpy.Structure import loadStructure, Structure
from diffpy.srreal.pdfcalculator import PDFCalculator
from pyobjcryst import loadCrystal
from diffpy.srfit.fitbase import Profile, FitResults, initializeRecipe, FitContribution, FitRecipe
from diffpy.srfit.pdf.characteristicfunctions import sphericalCF
from diffpy.srfit.pdf import PDFParser, PDFGenerator

def create_array(arr, fields):
	"""
	Creating and exstending an numpy array.

	Parameter
	---------
		arr : an numpy array.

		fields : an array containing strings e.g. ['x', 'y', 'z'].

	Return
	------
		None.
	"""

    dtype2 = np.dtype({name:arr.dtype.fields[name] for name in fields})
    return np.ndarray(arr.shape, dtype2, arr, 0, arr.strides)


def scipyOptimize(recipe):
	"""
	Fitting with scipy stats' leastsq function.

	Parameter
	---------
		recipe : recipe from diffpy.

	Return
	------
		None.
	"""

    leastsq(recipe.residual, recipe.getValues())
    return


def plotRecipe(recipe):
	"""
	Used for plotting recipe.

	Parameter
	---------
		recipe : recipe from diffpy.

	Return
	------
		None.
	"""

    r = recipe.pdf.profile.x
    g = recipe.pdf.profile.y
    gcalc = recipe.pdf.evaluate()
    diffzero = -0.8 * max(g) * np.ones_like(g)
    diff = g - gcalc + diffzero
    plt.plot(r,g,'bo',label="G(r) Data")
    plt.plot(r, gcalc,'r-',label="G(r) Fit")
    plt.plot(r,diff,'g-',label="G(r) diff")
    plt.plot(r, diffzero,'k-')
    plt.xlabel("$r (\AA)$")
    plt.ylabel("$G (\AA^{-2})$")
    plt.legend(loc=1)


class pearsonFitting:
    """
    Pearson Fitting Class for Pair Distribution Function analysis.
    
    Parameter
    ---------
        None.

    Return
    ------
        None.
    """


    def __init__(self):
        """
        Creates an object. 
        """

        self.__params = False


    def loadDataPDF(self, dataDir):
        """
        Load G(r) of measured data.

        Parameter
        ---------
            dataDir : The directory where the datafiles should be imported.

        Return
        ------
            None.
        """

        self.dataDir = dataDir
        os.chdir(self.dataDir)
        self.allData = os.listdir(self.dataDir)
        self.PDFfiles = []
        for i in self.allData:
            self.PDFfiles.append(np.loadtxt(i, dtype={'names': ('r_val', 'int_val'), 
                                                      'formats': ('f4', 'f4')}))
    

    def loadCIF(self, CIFdir):
        """
        Simple function that gets the names of all files within a folder.
        There can not be subfolders within this folder!

        Parameter
        ---------
            CIFdir : Desired directory.

        Return
        ------
            None.
        """

        self.CIFdir = CIFdir
        os.chdir(self.CIFdir)
        self.allCIF = os.listdir(self.CIFdir)

           
    def setPDF(self, rmin='', rmax='', qmin=0.0, qmax=20.0, qdamp=0.04, delta2=2.0, psize=20.0, atomBiso=[''], Biso=[0.005]):
        """
        Used for changing the standart parameters when generating the PDFs.
        All PDFs will be calculated using the same parameters.

        Parameter
        ---------
            rmin : Takes float as input. If none is given rmin is set to data sets starting value.

            rmax : Takes float as input. If none is given rmax is set to data sets ending value.

			qmin : Takes float as input. If none is given qmin is set to 0.0.

			qmax : Takes float as input. If none is given qmax is set to 20.0.

            qdamp : Takes float as input. If none is given qdamp is set to 0.04.
            
            delta2 : Takes float as input. If none is given delta2 is set to 2.0.

            psize : Takes float as input. If none is given psize is set to 20.0.

            atomBiso : Takes a list a atom names e.g. ['W', 'O']. Atoms will have their Biso set to corresponding index of Bios.
            		   If no input is given all atoms Biso is changed.

            Biso : Takes a list of floats, must have same length as atomBios e.g. [0.005, 0.003].
                   If no value is given all atoms Biso i set to 0.005. 

        Return
        ------
            None
        """

        self.rmin      = rmin
        self.rmax      = rmax
        self.qdamp     = qdamp
        self.qmin      = qmin
        self.qmax      = qmax
        self.delta2    = delta2
        self.psize     = psize
        self.atomBiso  = atomBiso
        self.Biso      = Biso
        self.__params  = True    
      

    def setSaveDir(self, saveDir):
    	"""
    	Parameter
    	---------
			saveDir : Directory where files will be stored 

    	Return
    	------
    		None.
    	"""
        self.saveDir = saveDir


    def genPDF(self, data='', CIF='', savePDF=False, saveDir=''):
        """
        Generates and saves the PDFs of the CIFs.

        Parameter
        ---------
			data : Name of data file the CIF should be generated from.
				   If none is defined all data files will be used.

			CIF : Name of CIF files that should be used to generate PDF.
				  If none is defined all CIFs will be calculated.

            savePDF : Takes in a boolean. If 'True' calculated PDFs will be saved. 

            saveDir : Directory for where the PDFs should be saved. 
                      Only used if savePDF is set to 'True'.

        Return
        ------
            None.
        """

        if self.__params == True:
            if self.rmin == '' and self.rmax =='':
                pass
            elif self.rmin == '':
                pdfprofile.setCalculationRange(xmax = self.rmax)
            elif self.rmax == '':
                pdfprofile.setCalculationRange(xmin = self.rmin)
            else: 
                pdfprofile.setCalculationRange(xmin = self.rmin, xmax = self.rmax)
        else:
            self.qdamp    = 0.04
            self.delta2   = 2.0
            self.qmin     = 0.0
            self.qmax     = 20.0
            self.psize    = 20.0
            self.atomBiso = ['']
            self.Biso     = [0.005]

        if data!='' or CIF!='':
            os.chdir(self.dataDir)
            pdf_file = np.loadtxt(data, dtype={'names': ('r_val', 'int_val'), 
                                               'formats': ('f4', 'f4')})
            pdfprofile = Profile()
            pdfparser = PDFParser()
            pdfparser.parseFile(data)
            pdfprofile.loadParsedData(pdfparser)

            os.chdir(self.CIFdir)
            pdfgenerator = PDFGenerator("G1")
            pdfgenerator.qdamp.value = self.qdamp
            pdfgenerator.delta2.value = self.delta2
            pdfgenerator.setQmin(self.qmin)
            pdfgenerator.setQmax(self.qmax)
            pdfgenerator._calc.evaluatortype = 'OPTIMIZED'

            structure_crystal = loadCrystal(CIF)
            pdfgenerator.setStructure(structure_crystal, periodic = True)
            pdfcontribution = FitContribution("pdf")
            pdfcontribution.setProfile(pdfprofile, xname="r")
            pdfcontribution.addProfileGenerator(pdfgenerator)
            pdfcontribution.registerFunction(sphericalCF, name = "f")
            pdfcontribution.setEquation('mc1*G1*f')
            pdfcontribution.psize.value = self.psize

            recipe = FitRecipe()
            recipe.addContribution(pdfcontribution)
            recipe.clearFitHooks()

            recipe.addVar(pdfgenerator.delta2, tag = "delta2")
            recipe.addVar(pdfcontribution.psize, tag = "psize")
            recipe.addVar(pdfcontribution.mc1, 1, tag = "scale")

            if self.atomBiso[0] == '':
                for atom in pdfgenerator.phase.getScatterers():
                    try:
                        recipe.newVar("Atom_Biso", self.Biso, tag = 'adp_atom')
                        recipe.constrain(atom.Biso, self.Biso)                      
                    except:
                        pass
            else:
                d = {}
                for atom in pdfgenerator.phase.getScatterers():
                    for i in range(len(Atoms)): 
                        if atom.element.title().startswith(Atoms[i]) == True:
                            try:
                                d[str(Atoms[i])+"_Biso"] = recipe.newVar(str(Atoms[i])+"_Biso", BISO[i], tag = 'adp_'+str(Atoms[i]))
                                recipe.constrain(atom.Biso, d.values()[i])                      
                            except:
                                pass

            for par in pdfgenerator.phase.sgpars.latpars:
                recipe.addVar(par, tag='cell')

            for par in pdfgenerator.phase.sgpars.xyzpars:
                lclabel = par.par.obj.GetName().lower()
                lcsymbol = lclabel.rstrip(string.digits)
                name="{}_{}".format(par.par.name, lclabel)
                tags = ['xyz', 'xyz_' + lclabel, 'xyz_' + lcsymbol]
                recipe.addVar(par, name=name, tags=tags)

                
            if savePDF == False:
                pass
            else:
                os.chdir(saveDir)
                for i in range(len(self.allCIF)):
                    np.savetxt(str(name[i][:-4])+'.gr', pdfsave[i])
            return recipe

        else:
            PDF = []
            print '\nGenerating PDFs:'
            for i in tqdm(range(len(self.allData)), desc='Data Files', leave=True):
                for j in tqdm(range(len(self.allCIF)), desc='CIFs tested', leave=False):
                    os.chdir(self.dataDir)
                    pdf_file = np.loadtxt(self.allData[i], dtype={'names': ('r_val', 'int_val'), 
                                                       'formats': ('f4', 'f4')})
                    pdfprofile = Profile()
                    pdfparser = PDFParser()
                    pdfparser.parseFile(self.allData[i])
                    pdfprofile.loadParsedData(pdfparser)

                    os.chdir(self.CIFdir)
                    pdfgenerator = PDFGenerator("G1")
                    pdfgenerator.qdamp.value = self.qdamp
                    pdfgenerator.delta2.value = self.delta2
                    pdfgenerator.setQmin(self.qmin)
                    pdfgenerator.setQmax(self.qmax)
                    pdfgenerator._calc.evaluatortype = 'OPTIMIZED'

                    structure_crystal = loadCrystal(self.allCIF[j])
                    pdfgenerator.setStructure(structure_crystal, periodic = True)
                    pdfcontribution = FitContribution("pdf")
                    pdfcontribution.setProfile(pdfprofile, xname="r")
                    pdfcontribution.addProfileGenerator(pdfgenerator)
                    pdfcontribution.registerFunction(sphericalCF, name = "f")
                    pdfcontribution.setEquation('mc1*G1*f')
                    pdfcontribution.psize.value = self.psize

                    recipe = FitRecipe()
                    recipe.addContribution(pdfcontribution)
                    recipe.clearFitHooks()

                    recipe.addVar(pdfgenerator.delta2, tag = "delta2")
                    recipe.addVar(pdfcontribution.psize, tag = "psize")
                    recipe.addVar(pdfcontribution.mc1, 1, tag = "scale")

                    if self.atomBiso[0] == '':
                        for atom in pdfgenerator.phase.getScatterers():
                            try:
                                recipe.newVar("Atom_Biso", self.Biso, tag = 'adp_atom')
                                recipe.constrain(atom.Biso, self.Biso)                      
                            except:
                                pass
                    else:
                        d = {}
                        for atom in pdfgenerator.phase.getScatterers():
                            for i in range(len(Atoms)): 
                                if atom.element.title().startswith(Atoms[i]) == True:
                                    try:
                                        d[str(Atoms[i])+"_Biso"] = recipe.newVar(str(Atoms[i])+"_Biso", BISO[i], tag = 'adp_'+str(Atoms[i]))
                                        recipe.constrain(atom.Biso, d.values()[i])                      
                                    except:
                                        pass

                    PDF.append(recipe.pdf.evaluate())
            self.PDF = PDF
       

    def calcPear(self):
		"""
		Calculates the Pearson correlation between CIF files and measured data.

		Parameter
		---------
			None.

		Return
		------
			pearlist : Structured array with data file, CIF file, Pearson and P-value.
		"""

		print '\nCalculating Pearson:'      
		self.pearlist = []
		self.rankList = []
		for i in tqdm(range(len(self.allData)), desc='Data Files', leave=True):
		    data_info = np.zeros(len(self.allCIF), dtype=[('Data file', np.unicode_, 32),
		                                                  ('Cif file', np.unicode_, 64),
		                                                  ('Pearson', float),
		                                                  ('p-value', float)])
		    for j in tqdm(range(len(self.allCIF)), desc='CIFs tested', leave=False):
		        pear_coef = stats.pearsonr(self.PDFfiles[i]['int_val'], self.PDF[j])  
		        v1 = create_array(data_info, ['Data file','Cif file', 'Pearson', 'p-value'])
		        v1[j] = str(self.allData[i]), str(self.allCIF[j]), pear_coef[0], pear_coef[1]
		    data_info.sort(order='Pearson')
		    data_info = data_info[::-1]                 
		    self.pearlist.append(data_info)
		    self.rankList.append(data_info['Cif file'])
		return self.pearlist

    def printPearson(self):
    	"""
		Prints Pearson.

    	Parameter
    	---------
			None.

    	Return
    	------
    		None.
    	"""
        for i in range(len(self.pearlist)):
            print self.pearlist[i][0]['Data file']+str(':')
            for j in range(len(self.pearlist[i])):
                print "\t{:30.30} - {:+7.5f}".format(self.pearlist[i][j]['Cif file'], self.pearlist[i][j]['Pearson'])
            print ''
    

    def savePearson(self):
    	"""
		Saves Pearson in saveDir.

    	Parameter
    	---------
			None.

    	Return
    	------
    		None.
    	"""
        os.chdir(self.saveDir)
        f= open("PearCor.txt","w+")    
        for i in range(len(self.pearlist)):
            f.write(self.pearlist[i][0]['Data file']+str(':\n'))
            for j in range(len(self.pearlist[i])):
                f.write("\t{:3}) {:30.30} - {:+7.5f}\n".format(j, self.pearlist[i][j]['Cif file'], self.pearlist[i][j]['Pearson']))
            f.write('\n')
        f.close()    


    def fitScale(self, rank='all', save=False):
        """
        Fits PDFs scaling factor.

        Parameter
        ---------
            rank : Takes an integer. If not defined all PDFs will be fitted. 
                   If an integer is given only top models will be fitted. 
                   Top models are determined from Pearson. 

            save : Takes a boolean. False as default. If True files will be saved in saveDir. 

        Return
        ------
            rwList : Structured array containing Data files, CIFs, Rw and Scale.
        """

        print '\nFitting Scale:'
        if rank == 'all':
            rank = len(self.allCIF)
        elif rank > len(self.allCIF):
            rank = len(self.allCIF)
            print 'Rank is larger than number of CIFs!'
        else:
            pass

        rwList = []
        rankList_ph = []
        for i in tqdm(range(len(self.allData)), desc='Data Files', leave=True):
            data_info = np.zeros(len(self.rankList[i][:rank]), dtype=[('Data file', np.unicode_, 32),
                                                      ('Cif file', np.unicode_, 64),
                                                      ('Rw', float),
                                                      ('Scale', float)])
            for j in tqdm(range(len(self.rankList[i][:rank])), desc='CIFs tested', leave=False):
                recipe = self.genPDF(self.allData[i], self.rankList[i][j])
                recipe.fix('all')
                recipe.free('mc1')
                scipyOptimize(recipe)
                #print FitResults(recipe).rw

                v1 = create_array(data_info, ['Data file','Cif file', 'Rw', 'Scale'])
                v1[j] = self.allData[i], self.rankList[i][j], FitResults(recipe).rw, recipe.getValues()
            data_info.sort(order='Rw')
            rwList.append(data_info)
            rankList_ph.append(data_info['Cif file'])

        if save==True:
            os.chdir(self.saveDir)
            f=open("RwScale.txt","w+")    
            for i in range(len(rwList)):
                f.write(rwList[i][0]['Data file']+str(':\n'))
                f.write("\t{:>3.3}) {:30.30} - {:7.7} - {:9.9}\n".format('#', 'CIF', 'Rw', 'Scale'))
                for j in range(len(rwList[i])):
                    f.write("\t{:3}) {:30.30} - {:7.5f} - {:9.5f}\n".format(j, rwList[i][j]['Cif file'], rwList[i][j]['Rw'], rwList[i][j]['Scale']))
                f.write('\n')
            f.close()                  
        return rwList


    def fitCell(self, rank='All', save=False):
        """
        Fits PDFs scaling factor and unit cell.

        Parameter
        ---------
            rank : Takes an integer. If not defined all PDFs will be fitted. 
                   If an integer is given only top models will be fitted. 
                   Top models are determined from Pearson. 

            save : Takes a boolean. False as default. If True files will be saved in saveDir. 

        Return
        ------
            rwList : Structured array containing Data files, CIFs, Rw, Scale, a, b and c.
        """

        print '\nFitting Cell:'
        if rank == 'all':
            rank = len(self.allCIF)
        elif rank > len(self.allCIF):
            rank = len(self.allCIF)
            print 'Rank is larger than number of CIFs!'
        else:
            pass

        rwList = []
        for i in tqdm(range(len(self.allData)), desc='Data Files', leave=True):
            data_info = np.zeros(len(self.rankList[i][:rank]), dtype=[('Data file', np.unicode_, 32),
                                                      ('Cif file', np.unicode_, 64),
                                                      ('Rw', float),
                                                      ('Scale', float),
                                                      ('a', float),
                                                      ('b', float),
                                                      ('c', float)])
            for j in tqdm(range(len(self.rankList[i][:rank])), desc='CIFs tested', leave=False):
                recipe = self.genPDF(self.allData[i], self.rankList[i][j])
                recipe.fix('all')
                recipe.free('mc1')
                scipyOptimize(recipe)
                recipe.free('cell')
                scipyOptimize(recipe)

                v1 = create_array(data_info, ['Data file','Cif file', 'Rw', 'Scale','a','b','c'])
                values = recipe.getValues()
                names  = recipe.getNames()
                a = -1
                b = -1
                c = -1
                if len(values) == 4:
                	scaling = values[0]
                	a = values[1] 
                	b = values[2]
                	c = values[3]
                elif len(values) == 3:
                	scaling = values[0]
                	if names[1] == 'a':
                		a = values[1]
                	elif names[1] == 'b':
                		b = values[1]
                	if names[2] == 'b':
                		b = values[2]
                	elif names[2] == 'c':
                		c = values[2]
                else:
                	if names[1] == 'a':
                		a = values[1]
                	if names[1] == 'b':
                		b = values[1]
                	if names[1] == 'c':
                		c = values[1]

                v1[j] = self.allData[i], self.rankList[i][j], FitResults(recipe).rw, scaling, a,b,c
            data_info.sort(order='Rw')
            rwList.append(data_info)

        if save==True:
            os.chdir(self.saveDir)
            f=open("RwCell.txt","w+")    
            for i in range(len(rwList)):
                f.write(rwList[i][0]['Data file']+str(':\n'))
                f.write("\t{:>3.3}) {:30.30} - {:7.7} - {:9.9} - {:9.9} - {:9.9} - {:9.9}\n".format('#', 'CIF', 'Rw', 'Scale', 'a', 'b', 'c'))
                for j in range(len(rwList[i])):
                    f.write("\t{:3}) {:30.30} - {:7.5f} - {:9.5f} - {:9.5f} - {:9.5f} - {:9.5f}\n".format(j, rwList[i][j]['Cif file'], rwList[i][j]['Rw'], rwList[i][j]['Scale'],rwList[i][j]['a'],rwList[i][j]['b'],rwList[i][j]['c']))
                f.write('\n')
            f.close()   
        return rwList

### Testing ###

if __name__ == '__main__':
    testObj = pearsonFitting()
    testObj.setSaveDir('/home/emilkjaer/School/Pear_cor/ModulePearson')        
    testObj.loadCIF('/home/emilkjaer/School/Pear_cor/preface/TestCIF')
    testObj.loadDataPDF('/home/emilkjaer/School/Pear_cor/preface/TestData') 
    testObj.setPDF()
    testObj.genPDF() 
    testObj.calcPear()
    testObj.savePearson()
    #testObj.printPearson()
    testObj.fitScale(rank=20, save=True)
    testObj.fitCell(rank=5, save=True)
