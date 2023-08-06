#!/usr/bin/env python

import argparse
import sys
import os.path
import re
import json
import yaml
import mistune
from subprocess import Popen, PIPE
# from var_dump import var_dump

version = '0.4'

cfg_yml = '.tf_readme_validator.yml'

cfg = {
    'readme': {
        'Description':                  {'type': 'header',
                                         'level': 2},
        'Usage':                        {'type': 'header',
                                         'level': 2},
        'Conditional creation':         {'type': 'header',
                                         'level': 3,
                                         'optional': True},
        'Known issues / Limitations':   {'type': 'header',
                                         'level': 3,
                                         'optional': True},
        'Code included in this module': {'type': 'header',
                                         'level': 3,
                                         'optional': True},
        'Examples':                     {'type': 'header',
                                         'level': 3,
                                         'optional': True},
        'Inputs':                       {'type': 'header',
                                         'level': 2},
        'inputs table':                 {'type': 'table',
                                         'parent': 'Inputs'},
        'Outputs':                      {'type': 'header',
                                         'level': 2},
        'outputs table':                {'type': 'table',
                                         'parent': 'Outputs'},
        'Tests':                        {'type': 'header',
                                         'level': 2,
                                         'optional': True},
        'Terraform versions':           {'type': 'header',
                                         'level': 2},
        'Contributing':                 {'type': 'header',
                                         'level': 2},
        'License':                      {'type': 'header',
                                         'level': 2},
        'Authors':                      {'type': 'header',
                                         'level': 2},
    },
    'options': {
        'optional_validate': True,
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
    for key in cfg['readme']:
        if 'ok' not in cfg['readme'][key]:
            print(key + ' absent (E101)')
            code = 1
        elif not cfg['readme'][key]['ok']:
            print(key + ' - ' + cfg['readme'][key]['error'])
            code = 1
    return code


class CustomRenderer(mistune.Renderer):
    def __init__(self):
        self.last_seen = ''
        self.tables = {'Inputs': [], 'Outputs': []}
        mistune.Renderer.__init__(self)

    def header(self, text, level, raw):
        if text in cfg['readme']:
            if not cfg['options']['optional_validate'] and \
                    'optional' in cfg['readme'][text] and \
                    cfg['readme'][text]['optional']:
                return ''
            if cfg['readme'][text]['type'] != 'header':
                cfg['readme'][text]['ok'] = False
                cfg['readme'][text]['error'] = 'wrong header type (E102)'
            elif cfg['readme'][text]['level'] != level:
                cfg['readme'][text]['ok'] = False
                cfg['readme'][text]['error'] = \
                    'wrong header level (E103)'
            else:
                cfg['readme'][text]['ok'] = True
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

    if cfg['inputs']['validate']:
        diff = validate_inputs_outputs(cfg['inputs']['json'],
                                       rndr.tables['Inputs'])
        if len(diff) > 0:
            cfg['readme']['inputs table']['ok'] = False
            cfg['readme']['inputs table']['error'] = \
                'divergent elements: ' + ', '.join(diff) + ' (E201)'
        else:
            cfg['readme']['inputs table']['ok'] = True
    else:
        cfg['readme']['inputs table']['ok'] = True

    if cfg['outputs']['validate']:
        diff = validate_inputs_outputs(cfg['outputs']['json'],
                                       rndr.tables['Outputs'])
        if len(diff) > 0:
            cfg['readme']['outputs table']['ok'] = False
            cfg['readme']['outputs table']['error'] = \
                'divergent elements: ' + ', '.join(diff) + ' (E301)'
        else:
            cfg['readme']['outputs table']['ok'] = True
    else:
        cfg['readme']['outputs table']['ok'] = True


def initialize():
    if not cfg['options']['optional_validate']:
        for key in cfg['readme']:
            if 'optional' in cfg['readme'][key] and \
                    cfg['readme'][key]['optional']:
                cfg['readme'][key]['ok'] = True


def load_inputs_outputs(data, name):
    if os.path.isfile(data['path']):
        process = Popen(['terraform-docs', 'json', data['path']], stdout=PIPE)
        (json_data, err) = process.communicate()
        code = process.wait()
        if code > 0:
            raise Exception('terraform-docs json ' + data['path'] + ' failed')
        json_loaded = json.loads(json_data)
        data['json'] = []
        if json_loaded[name] is not None:
            data['json'] = list(map(lambda x: x['Name'], json_loaded[name]))
    else:
        print 'WARNING: cannot open ' + data['path'] + ' for reading'
        data['json'] = []


def load_config():
    with open(cfg_yml) as stream:
        data = yaml.load(stream)
        if 'replace' in data:
            for section in data['replace']:
                if section not in cfg:
                    print('WARNING: in config skipping replace/' + section)
                    continue
                cfg[section] = data['replace'][section]
        elif 'update' in data:
            for section in data['update']:
                if section not in cfg:
                    print('WARNING: in config skipping update/' + section)
                    continue
                for item in data['update'][section]:
                    cfg[section][item] = data['update'][section][item]
        elif 'remove' in data:
            for section in data['remove']:
                if section not in cfg:
                    print('WARNING: in config skipping remove/' + section)
                    continue
                for item in data['remove'][section]:
                    cfg[section].pop(item, None)


def main():
    parser = argparse.ArgumentParser(
        description="""
    Validates README.md file against the default specification.
    The config file (.tf_readme_validator.yml), README.md, variables.tf
    and outputs.tf are looked for only in the current directory.
    """)
    parser.add_argument('-v', '--version', help='show version and exit',
                        action="store_true")
    args = parser.parse_args()
    if args.version:
        print(version)
        return 0

    if os.path.isfile(cfg_yml):
        load_config()
    if cfg['inputs']['validate']:
        load_inputs_outputs(cfg['inputs'], 'Inputs')
    if cfg['outputs']['validate']:
        load_inputs_outputs(cfg['outputs'], 'Outputs')
    initialize()
    with open('README.md') as md:
        validate(md.read())
    return print_results()


if __name__ == '__main__':
    sys.exit(main())
