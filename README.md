# PseudoTool
A code to parse a standard UPF pseudo-potential file.

To use this module you need to have the xml-python module installed. This can be done by running the 
following command.

```
pip install xml-python
```

For more information, visit https://docs.python.org/3/library/xml.etree.elementtree.html.

This script in principle reads a UPF pseudo-potential file in xml format. Hence, one needs to convert the file
into an xml file. In Quantum Espresso distribution, this can be achieved by running, 

```
upfconv.x -x file.upf
```
