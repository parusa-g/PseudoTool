import sys
sys.path.append('../')
from ReadPseudoXml import readxml
import numpy as np
import matplotlib.pyplot as plt
import xml.etree.ElementTree as ET
#================================================================
def PlotData(x,y,xlabel='',ylabel='',title=''):
    fig, ax = plt.subplots(figsize=(8,8))
    
    ydim = y.ndim
    
    if ydim == 1:
        ax.plot(x,y)
    elif ydim == 2:
        for i in range(y.shape[1]):
            ax.plot(x,y[:,i])
    
    if len(xlabel) > 0:
        ax.set_xlabel(xlabel)
        
    if len(ylabel) > 0:
        ax.set_ylabel(ylabel)
        
    if len(title) > 0:
        ax.set_title(title)
        
    plt.show()
#================================================================
def main(xml_file):
    tree = ET.parse(xml_file)
    root = tree.getroot()
    pp = readxml(root)
    
    # List of possible items:
    # ---------------------------------------------------------------
    # (1) Get the rmesh
    rr = pp.get_data('pp_rmesh')
    
    # (2) Get the dr = r_{i+1/2} - r_{i-1/2}
    dr = pp.get_data('pp_rab')
    
    # (3) Get the atomic local potential
    Vloc = pp.get_data('pp_local')
    
    # (4) Get the Vanderbilt projectors for the non-local potential
    pp_beta = pp.get_data('pp_beta')
    
    # (5) Get the Vanderbilt eigen-values
    pp_dij = pp.get_data('pp_dij')
    
    # (6) Get the pseudo-wavefunctions
    pp_pswfc = pp.get_data('pp_pswfc')
    
    # (7) Get the non-linear core correction
    pp_nlcc = pp.get_data('pp_nlcc')
    
    # (8) Get the pseudo-atomic charge density
    pp_rho = pp.get_data('pp_rhoatom')
    
    # Plotting the quantitites
    # ---------------------------------------------------------------
    xlabel = 'r [Bohr]'
    
    PlotData(rr, Vloc, xlabel, ylabel=r'V$_{loc}$ [Ha]', title='Atomic local potential')
    PlotData(rr, pp_beta, xlabel, ylabel=r'$\beta_{\ell}$', title='Vanderbilt projectors')
    PlotData(rr, pp_pswfc, xlabel, ylabel=r'$\phi_{\ell}$', title='Pseudo-wavefunctions')
    PlotData(rr, pp_nlcc, xlabel, ylabel=r'$V_{nlcc}$', title='Non-linear core correction')
    PlotData(rr, pp_rho, xlabel, ylabel=r'$\rho_{\ell}$', title='Pseudo-atomic charge density')
#===============================================================================================
if __name__ == '__main__':
    xml_file = 'Mo.xml'
    main(xml_file)


