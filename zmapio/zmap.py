import csv
import json

import numpy as np

from . import reader
from . import writer


class ZMAPGrid(object):
    def __init__(
        self,
        file_ref=None,
        comments=None,
        name=None,
        z_type="GRID",
        nodes_per_line=None,
        field_width=None,
        null_value=1e30,
        decimal_places=None,
        start_column=1,
        min_x=None,
        max_x=None,
        min_y=None,
        max_y=None,
        z_values=None,
        **kwargs
    ):
        self.comments = comments
        self.name = name
        self.z_type = z_type
        self.nodes_per_line = nodes_per_line
        self.field_width = field_width
        self.null_value = null_value
        self.null_value_2 = ""
        self.decimal_places = decimal_places
        self.start_column = start_column
        self.z_values = z_values
        self.min_x = min_x
        self.max_x = max_x
        self.min_y = min_y
        self.max_y = max_y

        if file_ref:
            x, y, z = self.read(file_ref, **kwargs)
            self.x_values = x
            self.y_values = y
            self.z_values = z

        elif all(
            v is not None
            for v in [self.z_values, self.min_x, self.max_x, self.min_y, self.max_y]
        ):
            self.no_cols, self.no_rows = self.z_values.shape
            x = np.linspace(self.min_x, self.max_x, self.no_cols)
            y = np.linspace(self.max_y, self.min_y, self.no_rows)
            self.x_values, self.y_values = np.meshgrid(x, y)

    def read(self, file_ref, dtype=np.float64):
        file_obj = reader.open_file(file_ref)
        comments, headers, data = reader.read_file_contents(file_obj)

        if not headers:
            raise ValueError("Header section is not defined")

        for key in headers:
            setattr(self, key, headers[key])

        self.comments = comments

        if hasattr(file_obj, "close"):
            file_obj.close()

        try:
            self.null_value = np.float64(self.null_value)
        except TypeError:
            try:
                self.null_value = np.float64(self.null_value_2)
            except TypeError:
                raise ValueError("Null value is not defined in header")

        z = np.zeros(self.no_rows * self.no_cols, dtype=dtype)
        i = 0
        for nodes in data:
            for n in nodes.split():
                if n == self.null_value or dtype(n) == dtype(self.null_value):
                    z[i] = np.nan
                else:
                    z[i] = dtype(n)
                i += 1

        z = z.reshape((self.no_cols, self.no_rows))
        x = np.linspace(self.min_x, self.max_x, self.no_cols)
        y = np.linspace(self.max_y, self.min_y, self.no_rows)
        x, y = np.meshgrid(x, y)

        return x, y, z

    def plot(self, **kwargs):
        try:
            import matplotlib.pyplot as plt
        except ImportError:
            raise ImportError("matplotlib needs to be installed for plotting.")

        ax = plt.pcolormesh(
            self.x_values, self.y_values, self.z_values.swapaxes(0, 1), **kwargs
        )

        return ax

    def to_csv(self, file_ref, **kwargs):
        opened_file = False
        if isinstance(file_ref, str) and not hasattr(file_ref, "write"):
            opened_file = True
            file_ref = open(file_ref, "w")

        if "lineterminator" not in kwargs:
            kwargs["lineterminator"] = "\n"

        writer = csv.writer(file_ref, **kwargs)
        for j in range(self.no_cols):
            for i in range(self.no_rows):
                x = self.x_values[i, j]
                y = self.y_values[i, j]
                z = self.z_values[j, i]
                writer.writerow([x, y, z])

        if opened_file:
            file_ref.close()

    def to_wkt(self, file_ref, precision=None):
        opened_file = False
        if isinstance(file_ref, str) and not hasattr(file_ref, "write"):
            opened_file = True
            file_ref = open(file_ref, "w")

        if not precision:
            if self.decimal_places:
                precision = self.decimal_places
            else:
                precision = 4

        nodes = []
        for j in range(self.no_cols):
            for i in range(self.no_rows):
                x = self.x_values[i, j]
                y = self.y_values[i, j]
                z = self.z_values[j, i]
                nodes.append(
                    "({} {} {})".format(
                        np.format_float_positional(
                            x, precision=precision, unique=False
                        ),
                        np.format_float_positional(
                            y, precision=precision, unique=False
                        ),
                        np.format_float_positional(
                            z, precision=precision, unique=False
                        ),
                    )
                )
        file_ref.write("MULTIPOINT (" + ", ".join(nodes) + ")")

        if opened_file:
            file_ref.close()

    def to_geojson(self, file_ref):
        opened_file = False
        if isinstance(file_ref, str) and not hasattr(file_ref, "write"):
            opened_file = True
            file_ref = open(file_ref, "w")

        nodes = []
        for j in range(self.no_cols):
            for i in range(self.no_rows):
                x = self.x_values[i, j]
                y = self.y_values[i, j]
                z = self.z_values[j, i]
                nodes.append([x, y, z])

        json.dump({"type": "MultiPoint", "coordinates": nodes}, file_ref)

        if opened_file:
            file_ref.close()

    def to_dataframe(self):
        try:
            import pandas as pd
        except ImportError:
            raise ImportError(
                "pandas package needs to be installed for dataframe conversion."
            )

        from collections import defaultdict

        nodes_dict = defaultdict(list)
        for j in range(self.no_cols):
            for i in range(self.no_rows):
                nodes_dict["X"].append(self.x_values[i, j])
                nodes_dict["Y"].append(self.y_values[i, j])
                nodes_dict["Z"].append(self.z_values[j, i])
        return pd.DataFrame(nodes_dict)

    def write(self, file_ref, nodes_per_line=None):
        opened_file = False
        if isinstance(file_ref, str) and not hasattr(file_ref, "write"):
            opened_file = True
            file_ref = open(file_ref, "w")

        if not nodes_per_line:
            nodes_per_line = self.nodes_per_line

        writer.write(self, file_ref, nodes_per_line)
        if opened_file:
            file_ref.close()
