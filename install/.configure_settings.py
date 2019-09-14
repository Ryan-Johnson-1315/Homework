import os
import json

print('\nChecking for settings file')

if os.path.exists('settings/settings.json'):
    print('\t-Settings file already exists')
else:
    print('\t-Creating settings file')
    settings = dict()
    settings['api'] = "Set up api key"
    settings['url'] = "Set up url link"
    settings['longest_desc'] = "Do not edit - Used for formatting"
    settings['longest_clas'] = "Do not edit - Used for formatting"
    settings['classes'] = [0, 2, 3, 4, 5]
    json.dump(settings, open('settings/settings.json', 'w+'))

    print('\t-Open settings/settings.json and configure the following fields:')
    print('\t\t-api')
    print('\t\t-url')
    print('\t\t-classes')
