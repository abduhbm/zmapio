from zmapio import ZMAPGrid

z_text = """!this is
!a test
@test, GRID, 4
20, -9999.0, , 7, 1
6, 4, 0.0, 200.0, 0.0, 300.0
0.0, 0.0, 0.0
@
       -9999.0000000       -9999.0000000           3.0000000          32.0000000
          88.0000000          13.0000000
       -9999.0000000          20.0000000           8.0000000          42.0000000
          75.0000000           5.0000000
           5.0000000         100.0000000          35.0000000          50.0000000
          27.0000000           1.0000000
           2.0000000          36.0000000          10.0000000           6.0000000
           9.0000000       -9999.0000000
"""


def test_write_zmap_file(zmap_object, tmpdir):
    x = tmpdir.join("output.dat")
    z = ZMAPGrid(
        z_values=zmap_object.z_values, min_x=0.0, max_x=200.0, min_y=0.0, max_y=300.0
    )
    z.comments = ["this is", "a test"]
    z.nodes_per_line = 4
    z.field_width = 20
    z.decimal_places = 7
    z.name = "test"
    z.null_value = -9999.0
    z.write(x.strpath)

    with open(x.strpath) as f:
        data = f.read()
        assert data == z_text
