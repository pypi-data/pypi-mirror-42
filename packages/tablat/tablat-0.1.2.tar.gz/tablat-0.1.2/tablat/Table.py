# -*- coding: utf-8 -*-
import warnings


class Table(object):
    """
    Basic class to print data in a table format.

    Prints a table with a provided headers and data. The number of header titles
        establishes the number of columns in the table.

    Attributes:
        table_data: An iterable containing the data to print in the table.
                    By default an empty list
        headers: Title of each column in the table. By default an empty list.
    """

    def __init__(self, table_data=[], headers=[]):
        self._table_data = table_data
        self._headers = list(map(str, headers))
        self._num_columns = len(headers)
        self._colspace = 3
        self._calc_columns_max_lenght()

    def __getitem__(self, i):
        return self._table_data[i * self._num_columns:i * self._num_columns + self._num_columns]

    def __str__(self):
        self.print_table()

    def __repr__(self):
        print('{\n\t"headers":{},\n\t"data":{},\n\n"columns_lenght":{}\n}'.format(self.headers,
                                                                                  self.table_data,
                                                                                  self._column_max))

    def _calc_columns_max_lenght(self):
        """
        Calculates max lenght of each column based on data in `_table_data` and `_headers`
        """
        if self._num_columns == 0:
            return

        column_max = []
        for head in self._headers:
            column_max.append(len(head))

        for i, data in enumerate(self._table_data):
            if len(str(data)) > column_max[i % self._num_columns]:
                column_max[i % self._num_columns] = len(str(data))

        self._column_max = column_max

    def _update_columns_max_lenght(self, data_list, start_index=0):
        """
        Updates max lenght of columns from a data list.
        """
        if self._num_columns == 0:
            return

        for i, data in enumerate(data_list, start=start_index):
            if len(str(data)) > self._column_max[i % self._num_columns]:
                self._column_max[i % self._num_columns] = len(str(data))

    def _print_hsep(self, char='_', borders=' '):
        """
        Print horizontal separator
        """
        print('{b}{l}{b}'.format(b=borders, l=char*(sum(self._column_max) + (self._num_columns + 1) * self._colspace)))

    def print_table(self):
        """
        Prints a table with the data.
        """

        if not self._num_columns:
            warnings.warn("Unable to calculate the number of columns, you need"
                          "to provide a 'headers' list to generate table layout."
                          "Use headers attribute", UserWarning)
            return

        # Print init
        col_space = ' '*self._colspace

        # Print separator line
        self._print_hsep()

        # Print headers
        headers_line = '|{s}{d:<{l}}{s}'.format(d=self._headers[0], l=self._column_max[0], s=col_space)
        for (col_lenght, header) in zip(self._column_max[1:], self._headers[1:]):
            headers_line += '{d:>{l}}{s}'.format(l=col_lenght, d=header, s=col_space)

        headers_line += '|'
        print(headers_line)
        self._print_hsep('-', '|')

        # Print lines
        for i, data in enumerate(self._table_data):
            if i % self._num_columns == 0:
                data_line = '|{s}{d:<{l}}{s}'.format(d=data, l=self._column_max[i % self._num_columns], s=col_space)

            else:
                data_line += '{d:>{l}}{s}'.format(d=data, l=self._column_max[i % self._num_columns], s=col_space)

            if i % self._num_columns == self._num_columns - 1:
                data_line += '|'
                print(data_line)

        self._print_hsep(borders='|')

    def add_data(self, data):
        """
        Add more data to the table.

        Args:
            data (list): List of data to add to the `Table`
        """
        current_index = len(self._table_data)
        self._update_columns_max_lenght(data, current_index)
        self._table_data.extend(data)

    @property
    def headers(self):
        """
        Headers of the table. If changed the number of columns will be recalculated.
        """
        return self._headers

    @headers.setter
    def headers(self, new_headers):
        self._headers = new_headers
        self._num_columns = len(new_headers)
        self._calc_columns_max_lenght()

    @property
    def table_data(self):
        """
        Change the data list to in the `Table`.
        """
        return self._table_data

    @table_data.setter
    def table_data(self, tab_data):
        self._table_data
        self._calc_columns_max_lenght()
