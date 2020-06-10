import json


def test_export_to_csv(zmap_object, tmpdir):
    x = tmpdir.join("output.csv")
    zmap_object.to_csv(x.strpath)
    lines = x.readlines()
    assert len(lines) == 24
    assert lines[0] == "0.0,300.0,nan\n"


def test_export_to_geojson(zmap_object, tmpdir):
    x = tmpdir.join("output.json")
    zmap_object.to_geojson(x.strpath)
    d = json.load(x)
    assert sorted(list(d.keys())) == ["coordinates", "type"]
    assert d.get("type") == "MultiPoint"
    assert len(d.get("coordinates")) == 24
    assert [0.0, 60.0, 88.0] in d.get("coordinates")


def test_export_to_wkt(zmap_object, tmpdir):
    x = tmpdir.join("output.wkt")
    zmap_object.to_wkt(x.strpath)
    with open(x.strpath) as f:
        line = f.readline()
    assert line.startswith("MULTIPOINT ((0.0000000 300.0000000 nan),")


def test_export_to_wkt_with_precision(zmap_object, tmpdir):
    x = tmpdir.join("output.wkt")
    zmap_object.to_wkt(x.strpath, precision=2)
    with open(x.strpath) as f:
        line = f.readline()
    assert line.startswith("MULTIPOINT ((0.00 300.00 nan),")
