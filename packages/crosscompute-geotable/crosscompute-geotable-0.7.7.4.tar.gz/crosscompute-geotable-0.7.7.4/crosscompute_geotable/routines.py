import numpy as np
import pandas as pd
import re
from crosscompute.exceptions import DataTypeError
from invisibleroads_macros.calculator import define_normalize
from invisibleroads_macros.geometry import drop_z, flip_xy
from invisibleroads_macros.table import normalize_key
from math import floor

from .fallbacks import parse_geometry, rgb2hex, COLOR_CONVERTER


# These color schemes are courtesy of http://colorbrewer2.org
HEX_ARRAY_BY_COLOR_SCHEME = {
    'bugn': [
        '#f7fcfd', '#e5f5f9', '#ccece6', '#99d8c9', '#66c2a4', '#41ae76',
        '#238b45', '#006d2c', '#00441b'],
    'bupu': [
        '#f7fcfd', '#e0ecf4', '#bfd3e6', '#9ebcda', '#8c96c6', '#8c6bb1',
        '#88419d', '#810f7c', '#4d004b'],
    'gnbu': [
        '#f7fcf0', '#e0f3db', '#ccebc5', '#a8ddb5', '#7bccc4', '#4eb3d3',
        '#2b8cbe', '#0868ac', '#084081'],
    'orrd': [
        '#fff7ec', '#fee8c8', '#fdd49e', '#fdbb84', '#fc8d59', '#ef6548',
        '#d7301f', '#b30000', '#7f0000'],
    'pubu': [
        '#fff7fb', '#ece7f2', '#d0d1e6', '#a6bddb', '#74a9cf', '#3690c0',
        '#0570b0', '#045a8d', '#023858'],
    'pubugn': [
        '#fff7fb', '#ece2f0', '#d0d1e6', '#a6bddb', '#67a9cf', '#3690c0',
        '#02818a', '#016c59', '#014636'],
    'purd': [
        '#f7f4f9', '#e7e1ef', '#d4b9da', '#c994c7', '#df65b0', '#e7298a',
        '#ce1256', '#980043', '#67001f'],
    'rdpu': [
        '#fff7f3', '#fde0dd', '#fcc5c0', '#fa9fb5', '#f768a1', '#dd3497',
        '#ae017e', '#7a0177', '#49006a'],
    'ylgn': [
        '#ffffe5', '#f7fcb9', '#d9f0a3', '#addd8e', '#78c679', '#41ab5d',
        '#238443', '#006837', '#004529'],
    'ylgnbu': [
        '#ffffd9', '#edf8b1', '#c7e9b4', '#7fcdbb', '#41b6c4', '#1d91c0',
        '#225ea8', '#253494', '#081d58'],
    'ylorbr': [
        '#ffffe5', '#fff7bc', '#fee391', '#fec44f', '#fe9929', '#ec7014',
        '#cc4c02', '#993404', '#662506'],
    'ylorrd': [
        '#ffffcc', '#ffeda0', '#fed976', '#feb24c', '#fd8d3c', '#fc4e2a',
        '#e31a1c', '#bd0026', '#800026'],
    'blues': [
        '#f7fbff', '#deebf7', '#c6dbef', '#9ecae1', '#6baed6', '#4292c6',
        '#2171b5', '#08519c', '#08306b'],
    'greens': [
        '#f7fcf5', '#e5f5e0', '#c7e9c0', '#a1d99b', '#74c476', '#41ab5d',
        '#238b45', '#006d2c', '#00441b'],
    'greys': [
        '#ffffff', '#f0f0f0', '#d9d9d9', '#bdbdbd', '#969696', '#737373',
        '#525252', '#252525', '#000000'],
    'oranges': [
        '#fff5eb', '#fee6ce', '#fdd0a2', '#fdae6b', '#fd8d3c', '#f16913',
        '#d94801', '#a63603', '#7f2704'],
    'purples': [
        '#fcfbfd', '#efedf5', '#dadaeb', '#bcbddc', '#9e9ac8', '#807dba',
        '#6a51a3', '#54278f', '#3f007d'],
    'reds': [
        '#fff5f0', '#fee0d2', '#fcbba1', '#fc9272', '#fb6a4a', '#ef3b2c',
        '#cb181d', '#a50f15', '#67000d'],
    'brbg': [
        '#8c510a', '#bf812d', '#dfc27d', '#f6e8c3', '#f5f5f5', '#c7eae5',
        '#80cdc1', '#35978f', '#01665e'],
    'piyg': [
        '#c51b7d', '#de77ae', '#f1b6da', '#fde0ef', '#f7f7f7', '#e6f5d0',
        '#b8e186', '#7fbc41', '#4d9221'],
    'prgn': [
        '#762a83', '#9970ab', '#c2a5cf', '#e7d4e8', '#f7f7f7', '#d9f0d3',
        '#a6dba0', '#5aae61', '#1b7837'],
    'puor': [
        '#b35806', '#e08214', '#fdb863', '#fee0b6', '#f7f7f7', '#d8daeb',
        '#b2abd2', '#8073ac', '#542788'],
    'rdbu': [
        '#b2182b', '#d6604d', '#f4a582', '#fddbc7', '#f7f7f7', '#d1e5f0',
        '#92c5de', '#4393c3', '#2166ac'],
    'rdgy': [
        '#b2182b', '#d6604d', '#f4a582', '#fddbc7', '#ffffff', '#e0e0e0',
        '#bababa', '#878787', '#4d4d4d'],
    'rdylbu': [
        '#d73027', '#f46d43', '#fdae61', '#fee090', '#ffffbf', '#e0f3f8',
        '#abd9e9', '#74add1', '#4575b4'],
    'rdylgn': [
        '#d73027', '#f46d43', '#fdae61', '#fee08b', '#ffffbf', '#d9ef8b',
        '#a6d96a', '#66bd63', '#1a9850'],
    'spectral': [
        '#d53e4f', '#f46d43', '#fdae61', '#fee08b', '#ffffbf', '#e6f598',
        '#abdda4', '#66c2a5', '#3288bd'],
    'paired': [
        '#a6cee3', '#1f78b4', '#b2df8a', '#33a02c', '#fb9a99', '#e31a1c',
        '#fdbf6f', '#ff7f00', '#cab2d6'],
    'pastel1': [
        '#fbb4ae', '#b3cde3', '#ccebc5', '#decbe4', '#fed9a6', '#ffffcc',
        '#e5d8bd', '#fddaec', '#f2f2f2'],
    'set1': [
        '#e41a1c', '#377eb8', '#4daf4a', '#984ea3', '#ff7f00', '#ffff33',
        '#a65628', '#f781bf', '#999999'],
    'set3': [
        '#8dd3c7', '#ffffb3', '#bebada', '#fb8072', '#80b1d3', '#fdb462',
        '#b3de69', '#fccde5', '#d9d9d9'],
}
SUMMARY_TYPE_EXPRESSION = r'(?: from (mean|sum))?'
FILL_COLOR_COLUMN_PATTERN = re.compile(r'fill (color|%s)' % '|'.join(
    HEX_ARRAY_BY_COLOR_SCHEME) + SUMMARY_TYPE_EXPRESSION)
RADIUS_COLUMN_PATTERN = re.compile(
    r'radius in pixels(?: (range) (\d+) (\d+))?' + SUMMARY_TYPE_EXPRESSION)


class DisplayTable(pd.DataFrame):

    _metadata = ['display_bundle']

    def __init__(self, *args, **kw):
        is_abbreviated = kw.pop('is_abbreviated')
        super(DisplayTable, self).__init__(*args, **kw)
        # Prepare display bundle in constructor to capture data type errors
        self.display_bundle = get_display_bundle(self)
        self.is_abbreviated = is_abbreviated
        self.ignored_count = len(self) - len(self.display_bundle[0])


def get_display_bundle(table):
    packs, properties = [], {}
    if not len(table):
        return packs, properties
    geometry_column_names = get_geometry_column_names(table.columns)
    if not geometry_column_names:
        raise DataTypeError(
            'geometry columns missing (%s)' % ', '.join(table.columns))
    elif len(geometry_column_names) > 1:
        parse = parse_point_from_tuple
    else:
        parse = parse_geometry
        wkt_column_name = geometry_column_names[0]
        table[wkt_column_name] = table[wkt_column_name].astype(str)
        bad_mask = table[wkt_column_name].str.contains('EMPTY')
        for label, row in table[bad_mask].iterrows():
            print(
                f'geometry_wkt.warning = '
                f'skipping {row[wkt_column_name]} at loc[{label}]')
        table = table[~bad_mask]
    t = table.dropna(subset=geometry_column_names)
    # !!! Quickfix
    local_ts = []
    geometry_packs = []
    for geometry_value, local_t in t.groupby(geometry_column_names):
        try:
            geometry_pack = parse(geometry_value)
        except Exception:
            print(f'geometry_value.warning = skipping {geometry_value}')
            continue
        geometry_packs.append(geometry_pack)
        local_ts.append(local_t)
    t = pd.concat(local_ts)

    transforms = []
    for get_transform in [
            get_fill_color_transform,
            get_radius_transform]:
        transform = get_transform(t, geometry_column_names)
        if not transform:
            continue
        transforms.append(transform)

    for geometry_pack, local_t in zip(geometry_packs, local_ts):
        geometry_type_id, geometry_coordinates = geometry_pack
        geometry_coordinates = normalize_coordinates(
            geometry_type_id, geometry_coordinates)
        local_properties = {}
        for transform in transforms:
            local_properties, local_t = transform(local_properties, local_t)
        local_t = local_t.drop(geometry_column_names, axis=1)
        packs.append((
            geometry_type_id, geometry_coordinates, local_properties, local_t))
    return packs, properties


def get_geometry_column_names(column_names):
    wkt_column_names = [x for x in column_names if is_wkt(x)]
    if wkt_column_names:
        # Assume WKT coordinate order is (longitude, latitude)
        return [wkt_column_names[0]]
    longitude_column_names = [x for x in column_names if is_longitude(x)]
    latitude_column_names = [x for x in column_names if is_latitude(x)]
    if longitude_column_names and latitude_column_names:
        return [longitude_column_names[0], latitude_column_names[0]]


def parse_point_from_tuple(point_xy):
    return 1, list(point_xy)


def get_fill_color_transform(table, geometry_column_names):
    column_name, name_parts = prepare_column_name(
        FILL_COLOR_COLUMN_PATTERN, table.columns)
    if not column_name:
        return
    color_scheme, summary_type = name_parts
    if color_scheme == 'color':
        summarize = define_summarize_colors(summary_type or 'mean')
        normalize = rgb2hex
    else:
        hex_array = get_hex_array(color_scheme)
        summarize = define_summarize_numbers(summary_type or 'sum')
        normalize_number = define_normalize(get_summary_domain(
            table, geometry_column_names, column_name, summarize), [0, 8.9999])

        def normalize(x):
            index_string = floor(normalize_number(x))
            try:
                index = int(index_string)
            except ValueError:
                index = 0
            return hex_array[index]

    return define_transform(column_name, 'fillColor', normalize, summarize)


def get_radius_transform(table, geometry_column_names):
    column_name, name_parts = prepare_column_name(
        RADIUS_COLUMN_PATTERN, table.columns)
    if not column_name:
        return
    has_range, y_min, y_max, summary_type = name_parts
    summarize = define_summarize_numbers(summary_type or 'sum')
    normalize = define_normalize(get_summary_domain(
        table, geometry_column_names, column_name, summarize,
    ), [float(y_min), float(y_max)]) if has_range else lambda x: x
    return define_transform(
        column_name, 'radius_in_pixels', normalize, summarize)


def normalize_coordinates(geometry_type_id, geometry_coordinates):

    def f(xyz):
        return list(flip_xy(drop_z(xyz)))

    if geometry_type_id == 1:
        geometry_coordinates = f(geometry_coordinates)
    elif geometry_type_id in (2, 3, 4):
        geometry_coordinates = [
            f(x) for x in geometry_coordinates]
    elif geometry_type_id in (5, 6):
        geometry_coordinates = [[
            f(x) for x in l] for l in geometry_coordinates]
    return geometry_coordinates


def is_wkt(column_name):
    column_name = column_name.lower()
    return column_name.endswith('wkt')


def is_latitude(column_name):
    column_name = column_name.lower()
    return column_name.endswith('latitude') or column_name == 'lat'


def is_longitude(column_name):
    column_name = column_name.lower()
    return column_name.endswith('longitude') or column_name == 'lon'


def prepare_column_name(pattern, column_names):
    for column_name in column_names:
        match = pattern.match(normalize_key(
            column_name, separate_camel_case=True, separate_letter_digit=True))
        if match:
            return column_name, match.groups()
    return None, ()


def define_summarize_colors(summary_type):

    def get_rgb_array(x):
        try:
            return np.array(COLOR_CONVERTER.to_rgb(x))
        except ValueError:
            raise DataTypeError('color not recognized (%s)' % x)

    def summarize(string_series):
        rgb_arrays = string_series.apply(get_rgb_array)
        x = getattr(rgb_arrays, summary_type)()
        return np.clip(x, 0, 1)

    return summarize


def get_hex_array(color_scheme):
    try:
        return HEX_ARRAY_BY_COLOR_SCHEME[color_scheme]
    except KeyError:
        raise DataTypeError('color scheme not supported (%s)' % color_scheme)


def define_summarize_numbers(summary_type):

    def summarize(number_series):
        return getattr(number_series, summary_type)()

    return summarize


def get_summary_domain(table, geometry_column_names, column_name, summarize):
    x_min, x_max = float('inf'), -float('inf')
    for geometry_value, local_table in table.groupby(geometry_column_names):
        x = summarize(local_table[column_name])
        if x < x_min:
            x_min = x
        if x > x_max:
            x_max = x
    return x_min, x_max


def define_transform(column_name, local_property_name, normalize, summarize):

    def transform(local_properties, local_table):
        xs = local_table.pop(column_name)
        local_properties[local_property_name] = normalize(summarize(xs))
        return local_properties, local_table

    return transform
