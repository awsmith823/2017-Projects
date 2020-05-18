import re
import csv
import json
import xml.dom.minidom
from xml.dom.minidom import parse


class ChemBox(object):

    # SectionX is where you can find the main chemical data
    chemical_properties_section = 'Section2'

    def __init__(
        self,
        chemical_dom_element=None,
        chemical_formula=None,
        chemical_data={}
    ):

        self.chemical_dom_element = chemical_dom_element
        self.chemical_formula = chemical_formula
        self.chemical_data = {}

    def get_text_data_from_element_TagName(self):
        '''
        Extract the data from DOM object

        Parameters
        ----------
        DOM text object

        Output
        ------
        Text from DOM object: str
        '''
        return self.chemical_dom_element.firstChild.data

    def get_section_tuples_lst_from_text(self):
        '''
        Get iterable of section pairs from chemical info text
        obtained from DOM object

        Parameters
        ----------
        DOM text element

        Output
        ------
        List of section-pairs identified in the text
           e.g [(Section2, Section3), (Section3, Section5)]
        '''
        # REGEX
        section_pattern = r'(Section\d*)\s*=\s*{{'

        # EXTRACT chemical_text from dom_element
        chemical_info_text = self.get_text_data_from_element_TagName()

        # SEARCH FOR SECTIONS
        sections_lst = re.compile(
            section_pattern,
            flags=re.DOTALL
        ).findall(chemical_info_text)

        return list(zip(sections_lst, (sections_lst + ["\'\'\'"])[1:]))

    def get_properties_section_tuple(self, section_tuples_lst):
        '''
        This function used to extract start and end of properties section
        from a list of tuples with sequential sections.

        Parameters
        ----------
        section_tuples_lst: iterable of section pairs (tuples)
            e.g [('Section2', 'Section3'), ('Section3', 'Section5')]

        Output
        ------
        Filtered list with the properties section tuple
           e.g [(Section2, Section3)]
        '''

        properties_section_tuple = [
            tup for tup in section_tuples_lst if
            tup[0] == self.chemical_properties_section
        ]

        return properties_section_tuple

    def get_clean_section_text(self, section_text):
        '''
        Use REGEX patterns to clean text
        '''

        # Remove Reference Texts
        reference_pattern = r'<ref(.+?)</ref>'  # <ref name=str2> ... </ref>
        section_text = re.sub(reference_pattern, '',
                              section_text, flags=re.DOTALL)

        # Transform breakline lists into single line
        breakline_pattern = r'<br />\n'
        section_text = re.sub(breakline_pattern, ' ',
                              section_text, flags=re.DOTALL)

        # Remove HTML Tags and Declarations
        html_pattern = r'(<!--.*?-->|<[^>]*>)'
        section_text = re.sub(html_pattern, '', section_text, flags=re.DOTALL)

        # Search for unbulleted list in section_text
        list_pattern = r'{{(.*)list(.+?)}}'
        unbulleted_list = re.search(
            list_pattern, section_text, flags=re.DOTALL)

        if unbulleted_list:
            # Substitute newline
            group = re.sub('\n', '', unbulleted_list.group(0), flags=re.DOTALL)
            # Re-insert unbulleted list as one-line
            section_text = re.sub(list_pattern, group,
                                  section_text, flags=re.DOTALL)

        return section_text  # section_text.encode('utf-8')

    def get_section_text(self, chemical_info_text, section_pair):
        '''
        Parameters
        ----------
        chemical_info_text: str
        section_pair: (start, end) of the section of interest
         e.g ('Section3', 'Section5')

        Output
        ------
        section_text: str        
        '''
        # REGEX
        section_pair_pattern = r'%s\s*=\s*{{(.+?)%s'  # % (Section1, Section2)

        # get section start & end
        section_start, section_end = section_pair

        # REGEX TO FIND SECTION TEXT
        section_text = re.compile(
            section_pair_pattern % (section_start, section_end),
            flags=re.DOTALL
        ).findall(chemical_info_text.replace('\n\n', '\n'))[0]

        # CLEAN TEXT
        section_text = self.get_clean_section_text(section_text)
        return section_text

    def get_chemical_formula(self, properties_section_text):
        '''
        Extract formula from properties_section text

        Parameters
        ----------
        properties_section_text: str Section text that contains
        primary chemical properties info
        '''
        # REGEX
        new_line_pattern = r'Formula\s*=\s*\n(.+?)\n'
        in_line_pattern = r'Formula\s*=\s*(.+?)\n'

        if bool(re.search(new_line_pattern, properties_section_text)):
            chemical_formula = re.compile(
                new_line_pattern,
                flags=re.DOTALL
            ).findall(properties_section_text)[0]

        elif bool(re.search(in_line_pattern, properties_section_text)):
            chemical_formula = re.compile(
                in_line_pattern,
                flags=re.DOTALL
            ).findall(properties_section_text)[0]

        else:  # FORMULA IN 2ND LINE OF SECTION
            chemical_formula = properties_section_text.split('\n')[1]

        chemical_formula = \
            chemical_formula.strip('|').strip().replace('  ', ' ')

        # store chemical formula
        self.chemical_formula = chemical_formula
        self.chemical_data['Formula'] = self.chemical_formula

    def remove_chemical_formula_from_section_text(
        self,
        properties_section_text
    ):
        '''
        Parameters
        ----------
        properties_section_text: str properties section 
        (contains chemical formula)

        Output
        ------
        section_text_no_formula: str substitue formula with '\n'
        '''
        # REGEX
        new_line_pattern = r'Formula\s*=\s*\n(.+?)\n'
        in_line_pattern = r'Formula\s*=\s*(.+?)\n'

        if bool(re.search(new_line_pattern, properties_section_text)):
            section_text_no_formula = re.sub(
                new_line_pattern, '\n', properties_section_text
            )

        elif bool(re.search(in_line_pattern, properties_section_text)):
            section_text_no_formula = re.sub(
                in_line_pattern, '\n', properties_section_text
            )

        else:  # FORMULA IN 2ND LINE OF SECTION
            properties_section_text_lst = properties_section_text.split('\n')
            del properties_section_text_lst[1]
            section_text_no_formula = '\n'.join(properties_section_text_lst)

        return section_text_no_formula

    def get_itemized_properties(self, section_text):
        '''
        Parameters
        ----------
        section_text: str

        Output
        ------
        itemized_text: list of properties and values
            e.g ['MolarMass = 101.9031 g/mol', 'Appearance = orange crystals', ... , etc]
        '''
        itemized_properties = section_text.split('\n')[1:]
        # Line starts with |
        itemized_properties = filter(
            lambda item: (item and item[0] ==
                          '|'), section_text.split('\n')[1:]
        )
        # Remove | and white-space
        itemized_properties = map(
            lambda item: item.strip('|').strip(), itemized_properties
        )
        # Line has text that is not '}}'
        itemized_properties = filter(
            lambda item: (item != '}}' and item), itemized_properties
        )

        return list(itemized_properties)

    def get_chemical_property_and_value(self, item):
        '''
        Parameters
        ----------
        item: str e.g 'MolarMass = 266.69 g/mol'

        Output
        ------
        (property, value): tuple e.g ('MolarMass', '266.69 g/mol')
        '''
        prop, value_str = item.split('=', 1)
        return (prop.strip(), value_str.strip())

    def get_chemical_value_and_unit(self, value_str):
        '''
        Parameters
        ----------
        value_str: str e.g '266.69 g/mol'

        Output
        ------
        (value, unit): tuple e.g ('266.69',  'g/mol')
        '''
        # REGEX
        value_unit_pattern = r'(\-*)(\d+(?:\.\d+)?) '  # e.g '266.69 g/mol'

        searched_text = re.search(value_unit_pattern, value_str)

        if bool(searched_text):
            searched_text = searched_text.group(0)
            _, value, units = value_str.partition(searched_text)
            return (value.strip(), units.strip())
        else:
            return (value_str, None)

    def get_chemical_property_value_unit(self, item):
        '''
        Parameters
        ----------
        item: str e.g 'MolarMass = 266.69 g/mol'

        Output
        ------
        (property, value, unit): tuple e.g ('MolarMass', '266.69',  'g/mol')
        '''

        prop, value_str = self.get_chemical_property_and_value(item)
        value, unit = self.get_chemical_value_and_unit(value_str)

        if value:
            self.chemical_data[prop] = {'Value': value}
            if unit:
                self.chemical_data[prop]['Unit'] = unit

    def get_chemical_data(self):
        '''
        Chains all the above functions to get chemical
        data for a specified chemical
        '''

        # Get the chemical info text
        chemical_info_text = self.get_text_data_from_element_TagName()

        # Get section pairs from chemical info text
        section_tuples_lst = self.get_section_tuples_lst_from_text()

        # Get section_start & section_end for main chemical properties
        properties_section = self.get_properties_section_tuple(
            section_tuples_lst)

        # Extract data from each section
        for section_tuple in section_tuples_lst:

            # Get text between section_start & section_end
            section_text = self.get_section_text(
                chemical_info_text=chemical_info_text,
                section_pair=section_tuple
            )

            # Get chemical formula if properties section text
            if properties_section and (properties_section[0] == section_tuple):

                self.get_chemical_formula(section_text)

                # Remove chemical formula from section text
                section_text = self.remove_chemical_formula_from_section_text(
                    section_text)

            # Itemized Properties from section
            itemized_properties = self.get_itemized_properties(section_text)

            # CHEMICAL < PROPERTY - VALUE - UNIT >
            for item in itemized_properties:

                # Get prop-val-unit and store in dictionary
                self.get_chemical_property_value_unit(item=item)
        return self.chemical_data
