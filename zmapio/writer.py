import numpy as np


def chunks(x, n):
    for i in range(0, len(x), n):
        yield x[i : i + n]


def write(zmap, file_object, nodes_per_line):
    lines = []

    if not zmap.null_value_2:
        zmap.null_value_2 = ""

    for c in zmap.comments:
        lines.append("!" + c)

    lines.append("@{}, {}, {}".format(zmap.name, zmap.z_type, nodes_per_line))
    lines.append(
        "{}, {}, {}, {}, {}".format(
            zmap.field_width,
            zmap.null_value,
            zmap.null_value_2,
            zmap.decimal_places,
            zmap.start_column,
        )
    )
    lines.append(
        "{}, {}, {}, {}, {}, {}".format(
            zmap.no_rows, zmap.no_cols, zmap.min_x, zmap.max_x, zmap.min_y, zmap.max_y
        )
    )
    lines.append("0.0, 0.0, 0.0")
    lines.append("@")

    file_object.write("\n".join(lines))
    file_object.write("\n")

    fmt = "{0:>{1}.{2}f}".format
    width = zmap.field_width
    precision = zmap.decimal_places

    zmap.z_values = np.nan_to_num(zmap.z_values, nan=zmap.null_value)

    def write_lines(r):
        line_gen = (
            "".join(line) + "\n"
            for line in chunks(
                [fmt(val, width, precision) for val in r], nodes_per_line
            )
        )
        file_object.writelines(line_gen)

    [write_lines(row) for row in zmap.z_values]

    file_object.writelines([""])
