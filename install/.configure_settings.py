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
    settings['longest_desc'] = 0
    settings['longest_clas'] = 0
    settings['classes'] = [0, 1, 2]
    json.dump(settings, open('settings/settings.json', 'w+'))

    print('\t-Open settings/settings.json and configure the following fields:')
    print('\t\t-api')
    print('\t\t-url')
    print('\t\t-classes')
