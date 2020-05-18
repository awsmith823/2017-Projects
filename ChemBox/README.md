# Wiki ChemBox


### BACKGROUND
This project is an exercise in `data wrangling` where we take a raw XML file of chemical data from Wikipedia and transform it to more usable data formats (e.g Dictionary, DataFrame). From each chemical we extract a name, formula, and any chemical property-value-unit that we find within the file. 


### CONTENTS OF THIS DIRECTORY
* Parsing Wiki Chembox.ipynb
* process_chembox_xml.py
* chembox.py
* data
	- ../wiki_chembox.xml (Raw)
	- ../chembox_data.csv (Derived)
	- ../chembox_data.json (Derived)


### DATA SUMMARY
* `wiki_chembox.xml` Has over 600 chemicals
* parse_xml_get_elements() UDF in `process_chembox_xml.py`  uses xml.dom.minidom to extract chemical name and Document Object Model (DOM) from the XML file.
* `chembox.py` contains class **ChemBox** used to process DOM object for each chemical