# -*- coding: utf-8 -*-
# tabletext 0.1
#
# Copyright (C) 2014  Thibaut Horel <thibaut.horel@gmail.com>

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from __future__ import unicode_literals
import re
from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter,\
    RawDescriptionHelpFormatter
import sys
from codecs import open, getwriter
from itertools import izip_longest


__all__ = ["to_text"]


def _get_widths(table, formats, padding):
    columns = izip_longest(*table, fillvalue="")
    return [max(len(_format_entry(entry, format_string, padding))
                for entry in column)
            for column, format_string in zip(columns, formats)]


def _add_widths(formats, widths, padding):
    return [_add_width(format_string, width - sum(padding))
            for format_string, width in zip(formats, widths)]


def _top_rule(widths, corners, hor):
    return (corners[0] + corners[1].join(hor * width for width in widths)
            + corners[2])


def _inner_rule(widths, corners, hor):
    return (corners[3] + corners[4].join(hor * width for width in widths)
            + corners[5])


def _bottom_rule(widths, corners, hor):
    return (corners[6] + corners[7].join(hor * width for width in widths)
            + corners[8])


def _format_entry(entry, format_string, padding):
    format_string = "{0:" + format_string + "}"
    return " " * padding[0] + format_string.format(entry) + " " * padding[1]


def _format_row(row, formats, padding, ver):
    return (ver + ver.join(_format_entry(entry, format_string, padding)
                           for entry, format_string
                           in izip_longest(row, formats, fillvalue=""))
            + ver)


def _add_width(format_string, width):
    if width == 0:
        return format_string
    regexp = r",?(\.\d+)?(b|c|d|e|E|f|F|g|G|n|o|s|x|X|%)?"
    match = re.match(regexp, format_string)
    begin, end = match.span()
    if end - begin > 0:
        return format_string[:begin] + str(width) + format_string[begin:]
    else:
        return format_string + str(width)


def to_text(table, formats=None, padding=(1, 1), corners="┌┬┐├┼┤└┴┘",
            header_corners="╒╤╕╞╪╡", header_hor="═", header_ver="│",
            header=False, hor="─", ver="│"):
    n_columns = max(len(row) for row in table)
    if not formats:
        formats = [""] * n_columns
    elif type(formats) is unicode:
        formats = [formats] * n_columns
    if len(corners) == 1:
        corners = corners * 9
    if len(header_corners) == 1:
        header_corners = header_corners * 6
    widths = _get_widths(table, formats, padding)
    formats = _add_widths(formats, widths, padding)
    r = []
    if header:
        r.append(_top_rule(widths, header_corners, header_hor))
        r.append(_format_row(table[0], formats, padding, header_ver))
        r.append(_inner_rule(widths, header_corners, header_hor))
        table = table[1:]
    else:
        r.append(_top_rule(widths, corners, hor))
    r.append(("\n" + _inner_rule(widths, corners, hor)
              + "\n").join(_format_row(row, formats, padding, ver)
                           for row in table))
    r.append(_bottom_rule(widths, corners, hor))
    return "\n".join(r)


def main():
    class MyFormatter(ArgumentDefaultsHelpFormatter,
                      RawDescriptionHelpFormatter):
        pass

    parser = ArgumentParser(formatter_class=MyFormatter,
                            description="""
Format the input into a table with borders, writing the result to standard
output. Each TAB separated line from FILE will become a row in the output.""",
                            epilog="""
For more details and bug reports, see: https://github.com/Thibauth/tabletext"""
                            )
    parser.add_argument("--hor", help="horizontal line character",
                        metavar="CHAR", default="─")
    parser.add_argument("--ver", help="vertical line character",
                        metavar="CHAR", default="│")
    parser.add_argument("--corners", help="corner characters", metavar="CHARS",
                        default="┌┬┐├┼┤└┴┘")
    parser.add_argument("--padding", help="left and right padding lengths",
                        nargs=2, type=int, metavar="<n>",
                        default=[1, 1])
    parser.add_argument("--format", help="format string for the table entries",
                        default="", dest="formats", metavar="FORMAT",
                        type=unicode)
    parser.add_argument("--header", help="format first row as header",
                        action="store_true")
    parser.add_argument("--hhor", help="horizontal line character \
                        for the header", metavar="CHAR", dest="header_hor",
                        default="═")
    parser.add_argument("--hver", help="vertical line character \
                        for the header row", metavar="CHAR", dest="header_ver",
                        default="│")
    parser.add_argument("--hcorners", help="corner characters for \
                        the header row", metavar="CHARS",
                        dest="header_corners", default="╒╤╕╞╪╡")
    parser.add_argument("-s", "--sep", help="interpret CHAR as column\
                        separator in the input", metavar="CHAR", default=r"\t")
    parser.add_argument("file", help="file to format. When FILE is absent\
                        or -, read from STDIN",
                        nargs="?", default="-", metavar="FILE")
    parser.add_argument("--version", "-v", action="version",
                        help="output version information and exit",
                        version="""
%(prog)s 0.1
Copyright (C) 2014 Thibaut Horel <thibaut.horel@gmail.com>
License GPLv3+: GNU GPL version 3 or later <http://gnu.org/licenses/gpl.html>.
This is free software: you are free to change and redistribute it.
There is NO WARRANTY, to the extent permitted by law.  """)
    args = parser.parse_args()

    if args.file == "-":
        args.file = sys.stdin
    else:
        args.file = open(args.file, encoding="utf-8")
    sep = args.sep.replace(r"\t", "\t")
    table = [line.strip().split(sep) for line in args.file.readlines()]
    args = vars(args)
    del args["file"]
    del args["sep"]
    if sys.version < '3':
        sys.stdout = getwriter('utf8')(sys.stdout)
    print to_text(table, **args)

if __name__ == "__main__":
    main()
