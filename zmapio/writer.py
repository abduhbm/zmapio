import math


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

    for i in zmap.z_values:
        for j in chunks(i, nodes_per_line):
            j_fmt = "0.{}f".format(zmap.decimal_places)
            j_fmt = "{0:" + j_fmt + "}"
            j = [
                j_fmt.format(float(x))
                if not math.isnan(x)
                else j_fmt.format(float(zmap.null_value))
                for x in j
            ]
            line = "{:>" + "{}".format(zmap.field_width) + "}"
            lines.append("".join([line] * len(j)).format(*tuple(j)))

    file_object.write("\n".join(lines))
    file_object.write("\n")
