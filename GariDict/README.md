# Garifuna Dictionary / Translator


### BACKGROUND
The Garífuna are a mix of West/Central African, Arawak, and Carib ancestry. Garifuna is a language widely spoken in villages of Garifuna people on the coasts of Central America. Today, the global population of Garifunas stands at upwards of **300,000** people, many of whom live in the U.S. and Canada.

This project an attempt at language preservation by:
1. Digitizing existing physical dictionaries (**Tesseract OCR** – Optical Character Recognition)
2. Building a "flexible" Search Engine (**Whoosh**)
> When exact matches are not found, the search engine should return suggestions


### CONTENTS OF THIS DIRECTORY
* GariDict.ipynb (Main)
* translator.py (Give search_word & lang: return english-garifuna-spanish)
* create_and_load_schema_ix.py
* batch_ocr.py (process multiple images PyTesseract)
* settings.py (constants)
* utils.py (helper funcs)
* schema/
	- whoosh schema index object
* images/
	- batch_images.txt (list of image files)
* data/
	- tab separated output data