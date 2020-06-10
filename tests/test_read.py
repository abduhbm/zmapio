def test_read_comments_section(zmap_object):
    assert len(zmap_object.comments) == 2
    assert zmap_object.comments[0].startswith(
        " File created by DMBTools2.GridFileFormats"
    )


def test_columns_rows_count(zmap_object):
    assert zmap_object.no_cols == 4
    assert zmap_object.no_rows == 6


def test_max_min_values(zmap_object):
    assert zmap_object.max_x == 200.0
    assert zmap_object.min_x == 0.0
    assert zmap_object.max_y == 300.0
    assert zmap_object.min_y == 0.0


def test_decimal_places(zmap_object):
    assert zmap_object.decimal_places == 7


def test_nodes_per_line(zmap_object):
    assert zmap_object.nodes_per_line == 4


def test_null_values(zmap_object):
    assert zmap_object.null_value == -9999
    assert zmap_object.null_value_2 == ""


def test_start_column(zmap_object):
    assert zmap_object.start_column == 1


def test_x_values(zmap_object):
    assert zmap_object.x_values.shape == (6, 4)


def test_y_values(zmap_object):
    assert zmap_object.y_values.shape == (6, 4)


def test_z_values(zmap_object):
    assert zmap_object.z_values.shape == (4, 6)


def test_z_type(zmap_object):
    assert zmap_object.z_type == "GRID"
