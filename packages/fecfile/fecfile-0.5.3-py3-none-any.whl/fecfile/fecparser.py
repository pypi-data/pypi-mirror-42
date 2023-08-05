from datetime import datetime
from pytz import timezone
import csv
import json
import os
import warnings

from .cache import getTypeMapping, getMapping


class FecParserTypeWarning(UserWarning):
    """when data in an FEC filing doesn't match types.json"""
    pass


this_file = os.path.abspath(__file__)
this_dir = os.path.dirname(this_file)
mappings_file = os.path.join(this_dir, 'mappings.json')
types_file = os.path.join(this_dir, 'types.json')
mappings = {}
types = {}
with open(mappings_file) as data_file:
    mappings = json.loads(data_file.read())
with open(types_file) as data_file:
    types = json.loads(data_file.read())
eastern = timezone('US/Eastern')


comma_versions = ['1', '2', '3', '5']


def include_line(line, filter_list):
    for f in filter_list:
        if line.startswith(f) or line.startswith('"' + f):
            return True
    return False


def loads(input, options={}):
    version = None
    lines = input.split('\n')
    out = {'itemizations': {}, 'text': [], 'header': {}, 'filing': {}}
    out['header'], version, header_length = parse_header(lines)
    text_section = False
    for i in range(header_length, len(lines)):
        line = lines[i]
        if i > header_length and 'filter_itemizations' in options:
            if not include_line(line, options['filter_itemizations']):
                continue
        stripped_line = line.strip().upper()
        if stripped_line == '[BEGINTEXT]' or stripped_line == '[BEGIN TEXT]':
            text_section = True
            continue
        if stripped_line == '[ENDTEXT]' or stripped_line == '[END TEXT]':
            text_section = False
            continue
        if text_section:
            if 'F99_text' in out:
                out['F99_text'] += '\n' + line
            else:
                out['F99_text'] = line
            continue
        parsed = parse_line(line, version, i)
        if i < header_length + 1:
            out['filing'] = parsed
        elif parsed:
            if 'form_type' in parsed:
                form_type = parsed['form_type']
                if form_type[0] == 'S':
                    form_type = 'Schedule ' + parsed['form_type'][1]
                if form_type in out['itemizations']:
                    out['itemizations'][form_type].append(parsed)
                else:
                    out['itemizations'][form_type] = [parsed]
            else:
                out['text'].append(parsed)
    return out


def fields_from_line(line, use_ascii_28=False):
    if (chr(0x1c) in line) or use_ascii_28:
        fields = line.split(chr(0x1c))
    else:
        reader = csv.reader([line])
        fields = next(reader)
    for field in fields:
        if field.startswith('"') and field.endswith('"'):
            field = field[1:-1]
    return list(map(
        lambda x: x[1:-1] if (x.startswith('"') and x.endswith('"')) else x,
        fields
    ))


def parse_header(lines):
    if lines[0].startswith('/*'):
        header_size = 1
        header = {'schedule_counts': {}}
        schedule_counts = False
        while not lines[header_size].startswith('/*'):
            this_line = lines[header_size]
            if this_line.lower().startswith('schedule_counts'):
                schedule_counts = True
            else:
                header_fields = this_line.split('=')
                k = header_fields[0].strip().lower()
                v = header_fields[1].strip().lower()
                if schedule_counts:
                    header['schedule_counts'][k] = int(v)
                else:
                    header[k] = v
            header_size += 1
        return header, header['fec_ver_#'], header_size + 1
    fields = fields_from_line(lines[0])
    if fields[1] == 'FEC':
        parsed = parse_line(lines[0], fields[2], 0)
        return parsed, fields[2], 1
    parsed = parse_line(lines[0], fields[1], 0)
    return parsed, fields[1], 1


def parse_line(line, version, line_num=None):
    ascii_separator = True
    if version is None or version[0] in comma_versions:
        ascii_separator = False
    fields = fields_from_line(line, use_ascii_28=ascii_separator)
    if len(fields) < 2:
        return None
    form = fields[0].strip()
    this_version_mapping = getMapping(mappings, form, version)
    out = {}
    for i in range(len(this_version_mapping)):
        val = fields[i] if i < len(fields) else ''
        k = this_version_mapping[i]
        out[k] = getTyped(form, version, k, val, line_num)
    return out


nones = ['none', 'n/a']


def getTyped(form, version, field, value, line_num):
    prop = getTypeMapping(types, form, version, field)
    if prop:
        try:
            if prop['type'] == 'integer':
                return int(value)
            if prop['type'] == 'float':
                stripped = value.strip()
                if stripped == '' or stripped.lower() in nones:
                    return None
                sanitized = stripped.replace('%', '')
                return float(sanitized)
            if prop['type'] == 'date':
                format = prop['format']
                stripped = value.strip()
                if stripped == '':
                    return None
                parsed_date = datetime.strptime(
                    stripped,
                    format)
                return eastern.localize(parsed_date)
        except ValueError:
            warnings.warn(
                'cannot parse value: {v}, as type: {t}, '
                'for field: {f}, in form: {o}, '
                'version: {r} (line {n})'.format(
                    v=value,
                    t=prop['type'],
                    f=field,
                    o=form,
                    r=version,
                    n='unknown' if line_num is None else line_num + 1,
                ),
                FecParserTypeWarning,
            )
            return None
    return value


def print_example(parsed):
    out = {'filing': parsed['filing'], 'itemizations': {}}
    for k in parsed['itemizations'].keys():
        out['itemizations'][k] = parsed['itemizations'][k][0]
    print(json.dumps(out, sort_keys=True, indent=2, default=str))
