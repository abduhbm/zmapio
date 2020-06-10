import pytest

from zmapio import ZMAPGrid

z_text = """! File created by DMBTools2.GridFileFormats.ZmapPlusFile
!
@GRID FILE, GRID, 4
20, -9999.0000000, , 7, 1
6, 4, 0, 200, 0, 300
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


@pytest.fixture
def zmap_object(tmpdir):
    x = tmpdir.join("test.dat")
    x.write(z_text)
    z_obj = ZMAPGrid(x.strpath)
    yield z_obj
