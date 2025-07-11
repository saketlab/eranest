import pytest
import json
import os
from shapely.geometry import shape, Polygon
from eranest.util import (
    extract_coords_from_geometry,
    get_bounding_box,
    load_json_with_encoding,
    is_valid_geojson,
    convert_to_geojson,
    create_geojson_from_bbox
)

def test_extract_coords_from_geometry(sample_geojson):
    geometry = sample_geojson['features'][0]['geometry']
    coords = extract_coords_from_geometry(geometry)
    assert isinstance(coords, list)
    assert len(coords) > 0

def test_get_bounding_box(sample_geojson):
    bbox = get_bounding_box(sample_geojson)
    assert len(bbox) == 4
    assert bbox[0] == -122.5  # west
    assert bbox[1] == 37.5    # south
    assert bbox[2] == -122.0  # east
    assert bbox[3] == 38.0    # north

def test_load_json_with_encoding(sample_geojson_file):
    data = load_json_with_encoding(sample_geojson_file)
    assert isinstance(data, dict)
    assert 'features' in data

def test_is_valid_geojson(sample_geojson):
    assert is_valid_geojson(sample_geojson) is True
    assert is_valid_geojson({"invalid": "data"}) is False

def test_convert_to_geojson():
    # Test with a simple polygon
    poly = {
        "type": "Polygon",
        "coordinates": [[[0, 0], [1, 0], [1, 1], [0, 1], [0, 0]]]
    }
    geojson = convert_to_geojson(poly)
    print(geojson)
    assert is_valid_geojson(geojson)

def test_create_geojson_from_bbox():
    geojson = create_geojson_from_bbox(-122.5, 37.5, -122.0, 38.0)
    assert is_valid_geojson(geojson)
    bbox = get_bounding_box(geojson)
    assert bbox == (-122.5, 37.5, -122.0, 38.0)