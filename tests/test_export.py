import json
import warnings

import pandas as pd
import pytest


def test_export_to_csv(zmap_object, tmpdir):
    x = tmpdir.join("output.csv")
    zmap_object.to_csv(x.strpath)
    lines = x.readlines()
    assert len(lines) == 25
    assert lines[0] == "# X,Y,Z\n"
    assert lines[1] == "0.0,300.0,nan\n"


def test_export_to_csv_pixel_is_point(zmap_object_pixel_is_point, tmpdir):
    x = tmpdir.join("output.csv")
    zmap_object_pixel_is_point.to_csv(x.strpath)
    lines = x.readlines()
    assert len(lines) == 25
    assert lines[0] == "# X,Y,Z\n"
    assert lines[1] == "25.0,275.0,nan\n"


def test_export_to_geojson(zmap_object, tmpdir):
    x = tmpdir.join("output.json")
    zmap_object.to_geojson(x.strpath)
    d = json.load(x)
    assert sorted(list(d.keys())) == ["coordinates", "type"]
    assert d.get("type") == "MultiPoint"
    assert len(d.get("coordinates")) == 24
    assert [0.0, 60.0, 88.0] in d.get("coordinates")


def test_export_to_geojson_pixel_is_point(zmap_object_pixel_is_point, tmpdir):
    x = tmpdir.join("output.json")
    zmap_object_pixel_is_point.to_geojson(x.strpath)
    d = json.load(x)
    assert sorted(list(d.keys())) == ["coordinates", "type"]
    assert d.get("type") == "MultiPoint"
    assert len(d.get("coordinates")) == 24
    assert [25.0, 175.0, 3.0] in d.get("coordinates")


def test_export_to_wkt(zmap_object, tmpdir):
    x = tmpdir.join("output.wkt")
    zmap_object.to_wkt(x.strpath)
    with open(x.strpath) as f:
        line = f.readline()
    assert line.startswith("MULTIPOINT ((0.0000000 300.0000000 nan),")


def test_export_to_wkt_pixel_is_point(zmap_object_pixel_is_point, tmpdir):
    x = tmpdir.join("output.wkt")
    zmap_object_pixel_is_point.to_wkt(x.strpath)
    with open(x.strpath) as f:
        line = f.readline()
    assert line.startswith("MULTIPOINT ((25.0000000 275.0000000 nan),")


def test_export_to_wkt_with_precision(zmap_object, tmpdir):
    x = tmpdir.join("output.wkt")
    zmap_object.to_wkt(x.strpath, precision=2)
    with open(x.strpath) as f:
        line = f.readline()
    assert line.startswith("MULTIPOINT ((0.00 300.00 nan),")


def test_export_to_dataframe(zmap_object):
    with pytest.warns(UserWarning, match="to_dataframe was renamed to to_pandas"):
        zmap_object.to_dataframe()


def test_export_to_pandas(zmap_object):
    df = zmap_object.to_pandas()
    assert type(df) == pd.DataFrame
    assert df.describe().loc["mean"]["X"] == 100.0


def test_export_to_dataframe_capture_warning(zmap_object):
    with pytest.warns(UserWarning):
        warnings.warn("renamed to to_pandas", UserWarning)
