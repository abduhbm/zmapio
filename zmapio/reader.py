import numpy as np

try:
    import cStringIO as StringIO
except ImportError:
    try:
        import StringIO
    except ImportError:
        from io import StringIO
    else:
        from StringIO import StringIO
else:
    from StringIO import StringIO


def open_file(file_ref):
    if isinstance(file_ref, str):
        lines = file_ref.splitlines()

        if len(lines) > 1:
            file_ref = StringIO(file_ref)

        else:
            file_ref = open(lines[0], "r")

    return file_ref


def read_file_contents(file_obj):
    comments = []
    headers = None
    data = None
    data_flag = False
    lines = file_obj.readlines()
    lines = [line for line in lines if not line.startswith("+")]

    for i in range(len(lines)):
        line = lines[i].strip()
        if not line:
            continue

        if line.startswith("!"):
            comments.append(line[1:])

        elif line.startswith("@") and not data_flag:
            data_flag = True
            headers = read_headers(i, lines)

        elif line.startswith("@") and data_flag:
            data = read_data(i, lines)
            break

        else:
            continue

    return comments, headers, data


def read_headers(index, lines):
    rows = []
    for line in lines[index : index + 4]:
        line = line.strip()
        rows.append(line.split(","))

    header = {
        "name": rows[0][0].strip()[1:],
        "z_type": rows[0][1].strip(),
        "nodes_per_line": int(rows[0][2]),
        "field_width": int(rows[1][0]),
        "null_value": rows[1][1].strip(),
        "null_value_2": rows[1][2].strip(),
        "decimal_places": int(rows[1][3]),
        "start_column": int(rows[1][4]),
        "no_rows": int(rows[2][0]),
        "no_cols": int(rows[2][1]),
        "min_x": np.float64(rows[2][2]),
        "max_x": np.float64(rows[2][3]),
        "min_y": np.float64(rows[2][4]),
        "max_y": np.float64(rows[2][5]),
    }

    return header


def read_data(index, lines):
    data = []
    for line in lines[index + 1 :]:
        line = line.strip()
        data.append(line)

    return data
