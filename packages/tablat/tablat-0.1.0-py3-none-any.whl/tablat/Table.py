# -*- coding: utf-8 -*-
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
        self.headers = list(map(str, headers))
        self._num_columns = len(headers)
        self._column_max = self._update_columns_maxlenght()
        self._colspace = 3

    def __getitem__(self, i):
            return self._table_data[i * self._num_columns:i * self._num_columns + self._num_columns]

    def _update_columns_maxlenght(self):
        """
        Calculates max lenght of each column based on data input
        """
        column_max = []
        for head in self.headers:
            column_max.append(len(head))

        for i, data in enumerate(self._table_data):
            if len(str(data)) > column_max[i % self._num_columns]:
                column_max[i % self._num_columns] = len(str(data))

        self._column_max = column_max

    def _print_hsep(self, char='_', borders=' '):
        """
        Print horizontal separator
        """
        print('{b}{l}{b}'.format(b=borders, l=char*(sum(self._column_max) + (self._num_columns + 1) * self._colspace)))

    def print_table(self):
        """
        Prints a table with the data.
        """

        # Print init
        self._update_columns_maxlenght()
        col_space = ' '*self._colspace

        # Print separator line
        self._print_hsep()

        # Print headers
        headers_line = '|{s}{d:<{l}}{s}'.format(d=self.headers[0], l=self._column_max[0], s=col_space)
        for (col_lenght, header) in zip(self._column_max[1:], self.headers[1:]):
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
