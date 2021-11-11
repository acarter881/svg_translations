import csv
import os
import xml.etree.ElementTree as ET

class Translate:
    def __init__(self, csv) -> None:
        self.IGNORED_CHARACTERS = ['-',
                    '.',
                    ',',
                    ';',
                    '\\',
                    '/',
                    'BD',
                    'BodyGuard',
                    'BD BodyGuard',
                    'TM',
                    'T',
                    'Monoject',
                    'BD Plastipak',
                    'TXXXXXXX']         # Characters to ignore? This is taken from a text file from Gianni
        self.no_translation = set()     # Create empty set for terms that don't have a translation
        self.the_dict = dict()          # Create empty dictionary for the English to Italian (or whichever language) terms
        self.csv = csv                  # Take the csv file's name
        self.log = './RU/logs/log.txt'  # The log file that displays terms that don't have a translation

    def __repr__(self) -> str:
        return 'This is a script that translates the text inside of SVG files and saves as new files.'

    def eng_to_foreign(self):
        # Open the csv file and populate the dictionary
        with open(file=self.csv, mode='r', newline='', encoding='utf-8-sig') as csvfile:
            my_reader = csv.reader(csvfile, delimiter=',')

            for row in my_reader:
                if row[0].strip() != '':                                 # Exclude the rows with only spaces or no value in them
                    self.the_dict.setdefault(row[0].strip(), row[1].strip()) 

    def create_svgs(self):
        # Iterate over SVG files in the current working directory
        for file in os.listdir('.'):
            if file.endswith('.svg'):
                tree = ET.parse(file)
                root = tree.getroot()

                # Iterate recursively over the entire sub-tree, looking for "text" tags
                for child in root.iter(r'{http://www.w3.org/2000/svg}text'):
                    if child.tag.endswith('text'):
                        eng_text = child.text

                    if self.the_dict.get(eng_text):                      # Check if a translation exists.
                        translated_text = self.the_dict.get(eng_text)
                    elif eng_text in self.IGNORED_CHARACTERS:            # Check if the text is in the IGNORED_CHARACTERS list
                        translated_text = eng_text
                    else:                                                # If the translation doesn't exist, maintain original word and add English term to "no_translation" set
                        self.no_translation.add(eng_text)
                        translated_text = eng_text

                    # Update the translated text
                    child.text = translated_text

                # Write the new SVG to disk
                tree.write(f'./RU/{file}')

    def to_log(self):
        # Log the English terms that do not have a translation
        with open(file=self.log, mode='w', encoding='utf-8-sig') as f:
            for term in self.no_translation:
                f.write(f'No translation for: {term}' + '\n')

# Instantiate the class and run the necessary functions
if __name__ == '__main__':
    c = Translate(csv='./EN-IT.csv')
    c.eng_to_foreign()
    c.create_svgs()
    c.to_log()
