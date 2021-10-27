import csv
import os
import xml.etree.ElementTree as ET

# Characters to ignore? This is taken from a text file
IGNORED_CHARACTERS = ['-',
                    '.',
                    ',',
                    ';',
                    '\\',
                    '/',
                    ]

# Create empty set for terms that don't have a translation
no_translation = set()

# Create empty dictionary
the_dict = {}

# Open the csv file and populate the dictionary
with open(file='EN-IT.csv', mode='r', newline='', encoding='utf-8-sig') as csvfile:
    my_reader = csv.reader(csvfile, delimiter=',')

    for row in my_reader:
        if row[0].strip() != '':                            # Exclude the rows with only spaces or no value in them
            the_dict.setdefault(row[0].strip(), row[1].strip())

# Iterate over SVG files in the current working directory
for file in os.listdir('.'):
    if file.endswith('.svg'):
        tree = ET.parse(file)
        root = tree.getroot()

        # Iterate recursively over the entire sub-tree, looking for "text" tags
        for child in root.iter(r'{http://www.w3.org/2000/svg}text'):
            if child.tag.endswith('text'):
                eng_text = child.text

            if the_dict.get(eng_text):                      # Check if a translation exists.
                translated_text = the_dict.get(eng_text)
            elif eng_text in IGNORED_CHARACTERS:            # Check if the text is in the IGNORED_CHARACTERS list
                translated_text = eng_text
            else:                                           # If the translation doesn't exist, maintain same word
                translated_text = eng_text

            # Update the translated text
            child.text = translated_text
        
        # Create new SVG file name
        f_name = file.split('.')
        f_name = f_name[0] + '_new.' + f_name[1]

        # Write the new SVG to disk
        tree.write(f'./Translated Files/{f_name}')
