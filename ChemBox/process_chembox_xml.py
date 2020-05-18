import re
import csv
import json
import xml.dom.minidom
from xml.dom.minidom import parse

def parse_xml_get_elements(filename):
    '''
    Parameters
    ----------
    Input : File Path
    Output: Dictionary {Chem_Names: DOM Element}
    '''     
    elemDict = {}

    DOMTree = parse(filename)
    elemName = DOMTree.getElementsByTagName('title')
    elemText = DOMTree.getElementsByTagName('text')
    for idx, elem in enumerate(elemName):
        name = elem.firstChild.data
        elemDict[name] = elemText[idx]
    return elemDict


def chemical_dict_to_csv(chemDict, filename='chembox_data.csv'):
    '''
    Parameters
    ----------
    chemDict: {}
    filename: csv file name
    '''
    chemicals = chemDict.keys()
    csv_columns = [
        'Name',
        'Formula',
        'Property',
        'Value',
        'Unit',
    ]

    csv_file = filename
    with open(csv_file, 'w') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
        writer.writeheader()

        for chemical in chemicals:
            try:
                formula = chemDict[chemical]['Formula']
            except KeyError:
                formula = None

            record = {
                'Name': chemical,
                'Formula': formula,
                'Property': None,
                'Value': None,
                'Unit': None
            }

            properties = [
                prop for prop in chemDict[chemical].keys() if prop != 'Formula'
            ]

            for prop in properties:
                record['Property'] = prop
                record['Value'] = chemDict[chemical][prop]['Value']

                try:
                    unit = chemDict[chemical][prop]['Unit']
                except KeyError:
                    unit = None

                record['Unit'] = unit
                writer.writerow(record)



