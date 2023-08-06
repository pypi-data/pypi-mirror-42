#!/usr/bin/env python

import sys
import os.path
import re
import json
import yaml
import mistune
from subprocess import Popen, PIPE
# from var_dump import var_dump

cfg_yml = '.tf_readme_validator.yml'

structure = {
    'readme': {
        'Description':                  {'type': 'header',
                                         'level': 2},
        'Usage':                        {'type': 'header',
                                         'level': 2},
        'Conditional creation':         {'type': 'header',
                                         'level': 3},
        'Known issues / Limitations':   {'type': 'header',
                                         'level': 3},
        'Code included in this module': {'type': 'header',
                                         'level': 3},
        'Examples':                     {'type': 'header',
                                         'level': 3},
        'Inputs':                       {'type': 'header',
                                         'level': 2},
        'inputs table':                 {'type': 'table',
                                         'parent': 'Inputs'},
        'Outputs':                      {'type': 'header',
                                         'level': 2},
        'outputs table':                {'type': 'table',
                                         'parent': 'Outputs'},
        'Tests':                        {'type': 'header',
                                         'level': 2},
        'Terraform versions':           {'type': 'header',
                                         'level': 2},
        'Contributing':                 {'type': 'header',
                                         'level': 2},
        'License':                      {'type': 'header',
                                         'level': 2},
        'Authors':                      {'type': 'header',
                                         'level': 2},
    },
    'inputs': {
        'validate': True,
        'path': 'variables.tf',
    },
    'outputs': {
        'validate': True,
        'path': 'outputs.tf',
    },
}


def print_results():
    code = 0
    for key in structure['readme']:
        if 'ok' not in structure['readme'][key]:
            print(key + ' absent (E101)')
            code = 1
        elif not structure['readme'][key]['ok']:
            print(key + ' - ' + structure['readme'][key]['error'])
            code = 1
    return code


class CustomRenderer(mistune.Renderer):
    def __init__(self):
        self.last_seen = ''
        self.tables = {'Inputs': [], 'Outputs': []}
        mistune.Renderer.__init__(self)

    def header(self, text, level, raw):
        if text in structure['readme']:
            if structure['readme'][text]['type'] != 'header':
                structure['readme'][text]['ok'] = False
                structure['readme'][text]['error'] = 'wrong header type (E102)'
            elif structure['readme'][text]['level'] != level:
                structure['readme'][text]['ok'] = False
                structure['readme'][text]['error'] = \
                    'wrong header level (E103)'
            else:
                structure['readme'][text]['ok'] = True
            self.last_seen = text
        return ''

    def table_row(self, content):
        header = re.match('<th>(.*)</th>', content)
        if header:
            self.tables[self.last_seen] = []
        column = re.match('<td>(.*)</td>', content)
        if column:
            self.tables[self.last_seen].append(column.groups()[0])
        return ''


def validate_inputs_outputs(source, readme):
    union = set(source) | set(readme)
    intersection = set(source) & set(readme)
    diff = union - intersection
    return diff


def validate(readme):
    rndr = CustomRenderer()
    markdown = mistune.Markdown(renderer=rndr)
    markdown(readme)

    if structure['inputs']['validate']:
        diff = validate_inputs_outputs(structure['inputs']['json'],
                                       rndr.tables['Inputs'])
        if len(diff) > 0:
            structure['readme']['inputs table']['ok'] = False
            structure['readme']['inputs table']['error'] = \
                'divergent elements: ' + ', '.join(diff) + ' (E201)'
        else:
            structure['readme']['inputs table']['ok'] = True
    else:
        structure['readme']['inputs table']['ok'] = True

    if structure['outputs']['validate']:
        diff = validate_inputs_outputs(structure['outputs']['json'],
                                       rndr.tables['Outputs'])
        if len(diff) > 0:
            structure['readme']['outputs table']['ok'] = False
            structure['readme']['outputs table']['error'] = \
                'divergent elements: ' + ', '.join(diff) + ' (E301)'
        else:
            structure['readme']['outputs table']['ok'] = True
    else:
        structure['readme']['outputs table']['ok'] = True


def load_inputs_outputs(data, name):
    if os.path.isfile(data['path']):
        process = Popen(['terraform-docs', 'json', data['path']], stdout=PIPE)
        (json_data, err) = process.communicate()
        code = process.wait()
        if code > 0:
            raise Exception('terraform-docs json ' + data['path'] + ' failed')
        data['json'] = list(map(lambda x: x['Name'],
                            json.loads(json_data)[name]))
    else:
        print 'WARNING: cannot open ' + data['path'] + ' for reading'
        data['json'] = []


def load_config():
    with open(cfg_yml) as stream:
        data = yaml.load(stream)
        if 'replace' in data:
            for section in data['replace']:
                if section not in structure:
                    print('WARNING: in config skipping replace/' + section)
                    continue
                structure[section] = data['replace'][section]
        elif 'update' in data:
            for section in data['update']:
                if section not in structure:
                    print('WARNING: in config skipping update/' + section)
                    continue
                for item in data['update'][section]:
                    structure[section][item] = data['update'][section][item]
        elif 'remove' in data:
            for section in data['remove']:
                if section not in structure:
                    print('WARNING: in config skipping remove/' + section)
                    continue
                for item in data['remove'][section]:
                    structure[section].pop(item, None)


def main():
    if os.path.isfile(cfg_yml):
        load_config()
    if structure['inputs']['validate']:
        load_inputs_outputs(structure['inputs'], 'Inputs')
    if structure['outputs']['validate']:
        load_inputs_outputs(structure['outputs'], 'Outputs')
    with open('README.md') as md:
        validate(md.read())
    return print_results()


if __name__ == '__main__':
    sys.exit(main())
