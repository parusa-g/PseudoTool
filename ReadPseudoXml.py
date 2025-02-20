import sys
import numpy as np
import xml.etree.ElementTree as ET

class parse(object):
    def __init__(self,xml_file):
        
        tree = ET.parse(xml_file)
        root = tree.getroot()
        
        self.root = root
        self.keys = self.get_keys()
        self.labels = self.get_labels()
        self.llpswfc = self.get_ll_pswfc()
        self.llbeta = self.get_ll_beta()

    def get_keys(self):
        keys = {}
        # Get keys from every xml data's child
        for i,item in enumerate(self.root):
            keys[item.tag] = i

        return keys
        
    def get_labels(self):
        # Get the labels from PP header
        k = self.keys['pp_header']
        lbl = {}
        for i,item in enumerate(self.root[k]):
            lbl[item.tag] = item.text

        return lbl
    
    def get_ll_pswfc(self):
        ll = []
        ii = self.keys['pp_pswfc']
        nwf = int(self.labels['number_of_wfc'])
        for i in range(nwf):
            l = self.root[ii][i].attrib['l']
            ll.append(int(l))
        
        return ll
    
    def get_ll_beta(self):
        ll = []
        ii = self.keys['pp_nonlocal']
        nproj = int(self.labels['number_of_proj'])
        for i in range(nproj):
            l = self.root[ii][i].attrib['angular_momentum']
            ll.append(int(l))
            
        return ll
    
    def get_data(self,item_name):
        
        if item_name == 'pp_rmesh':
            ii = self.keys['pp_mesh']
            sz = int(self.labels['mesh_size'])

            raw = self.root[ii][0].text.split()
            tmp = [np.float128(s) for s in raw]
            tmp = np.array(tmp)
            
        elif item_name == 'pp_rab':
            ii = self.keys['pp_mesh']
            sz = int(self.labels['mesh_size'])
            
            raw = self.root[ii][1].text.split()
            tmp = [np.float128(s) for s in raw]
            tmp = np.array(tmp)
            
        elif item_name == 'pp_dij':
            nproj = int(self.labels['number_of_proj'])
            ii = self.keys['pp_nonlocal']
            raw = self.root[ii][-1].text.split()
            tmp = [np.float128(s) for s in raw]
            tmp = 0.5 * np.array(tmp).reshape((nproj,nproj))
            
        elif item_name == 'pp_beta':
            ii = self.keys['pp_nonlocal']
            size = int(self.labels['mesh_size'])
            nproj = int(self.labels['number_of_proj'])
            tmp = np.zeros((size,nproj))
            for i in range(nproj):
                raw = self.root[ii][i].text.split()
                dat = [np.float128(s) for s in raw]
                tmp[:,i] = np.array(dat)
                
        elif item_name == 'pp_pswfc':
            ii = self.keys[item_name]
            size = int(self.labels['mesh_size'])
            nwf = int(self.labels['number_of_wfc'])
            tmp = np.zeros((size,nwf))
            for i in range(nwf):
                raw = self.root[ii][i].text.split()
                dat = [np.float128(s) for s in raw]
                tmp[:,i] = np.array(dat)
        else:
            ii = self.keys[item_name]
            raw = self.root[ii].text.split()
            tmp = [np.float128(s) for s in raw]
            tmp = np.array(tmp)

        # Check dimension 
        if item_name != 'pp_dij':
            dim = int(self.labels['mesh_size'])
            if tmp.shape[0] != dim:
                raise ValueError('Dimension incorrect')

        return tmp

    def save_to_file(self,item_name,fname):

        if item_name != 'pp_dij':
            x = self.get_data('pp_rmesh')
            y = self.get_data(item_name)
            dim = y.ndim

            if dim == 1:
                y = y.reshape(-1,1)
                fmt = ['%12.9f', '%12.9f']
            else:
                nn = y.shape[-1] + 1
                fmt = []
                for i in range(nn):
                    fmt.append('%12.9f')

            dat = np.concatenate((x,y), axis=1)
        else:
            dat = self.get_data(item_name)
            fmt = []
            nn = int(self.labels['number_of_proj'])
            for i in range(nn):
                fmt.append('%12.9f')

        np.savetxt(fname, dat, fmt=fmt)
# -----------------------------------------------------------------
def main(xml_file,item):
    # Parse xml file
    pp = parse(xml_file)

    # Save the data to a file
    file_out = item + '.dat'
    pp.save_to_file(item,file_out)
# -----------------------------------------------------------------
if __name__ == '__main__':
    # Usage: python ReadPseudoXml.py <path/to/xml_file> <pp_item>
    # List of <pp_item>: see the examples in ReadPseudo.py
    
    main(sys.argv[1], sys.argv[2])