# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import re
from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter
import sys
from codecs import open
from itertools import izip_longest


def get_widths(table, formats, padding):
    columns = izip_longest(*table, fillvalue="")
    return [max(len(format_entry(entry, format_string, padding))
                for entry in column)
            for column, format_string in zip(columns, formats)]


def add_widths(formats, widths, padding):
    return [add_width(format_string, width - sum(padding))
            for format_string, width in zip(formats, widths)]


def top_rule(widths, corners, hor):
    return (corners[0] + corners[1].join(hor * width for width in widths)
            + corners[2])


def inner_rule(widths, corners, hor):
    return (corners[3] + corners[4].join(hor * width for width in widths)
            + corners[5]) + "\n"


def bottom_rule(widths, corners, hor):
    return (corners[6] + corners[7].join(hor * width for width in widths)
            + corners[8])


def format_entry(entry, format_string, padding):
    format_string = "{0:" + format_string + "}"
    return " " * padding[0] + format_string.format(entry) + " " * padding[1]


def format_row(row, formats, padding, ver):
    return (ver + ver.join(format_entry(entry, format_string, padding)
                           for entry, format_string in zip(row, formats))
            + ver) + "\n"


def add_width(format_string, width):
    regexp = r",?(\.\d+)?(b|c|d|e|E|f|F|g|G|n|o|s|x|X|%)?"
    match = re.match(regexp, format_string)
    begin, end = match.span()
    if end - begin > 0:
        return format_string[:begin] + str(width) + format_string[begin:]
    else:
        return format_string + str(width)


def print_table(table, formats=None, padding=(1, 1), corners="┌┬┐├┼┤└┴┘",
                header_corners="╒╤╕╞╪╡", header_hor="═", header_ver="│",
                header=False, hor="─", ver="│"):
    if not formats:
        formats = [""] * len(table[-1])
    elif type(formats) is str:
        formats = formats * len(table[-1])
    if len(corners) == 1:
        corners = corners * 9
    widths = get_widths(table, formats, padding)
    formats = add_widths(formats, widths, padding)
    if header:
        print top_rule(widths, header_corners, header_hor)
        print format_row(table[0], formats, padding, header_ver),
        print inner_rule(widths, header_corners, header_hor),
        table = table[1:]
    else:
        print top_rule(widths, corners, hor)
    print inner_rule(widths, corners, hor).join(format_row(row, formats,
                                                           padding, ver)
                                                for row in table),
    print bottom_rule(widths, corners, hor)


def main():
    parser = ArgumentParser(formatter_class=ArgumentDefaultsHelpFormatter,
                            description="Render tab separated data as \
                            a table.")
    parser.add_argument("--hor", help="horizontal line character",
                        metavar="CHAR", default="─")
    parser.add_argument("--ver", help="vertical line character",
                        metavar="CHAR", default="│")
    parser.add_argument("--corners", help="corner characters", metavar="CHARS",
                        default="┌┬┐├┼┤└┴┘")
    parser.add_argument("--padding", help="left and right horizontal padding \
                        lenghts", nargs=2, type=int, metavar="<n>",
                        default=[1, 1])
    parser.add_argument("--format", help="format string for the table entries",
                        default="", dest="formats", metavar="FORMAT")
    parser.add_argument("--header", help="format first row as header",
                        action="store_true")
    parser.add_argument("--hhor", help="horizontal line character \
                        for the header row", metavar="CHAR", dest="header_hor",
                        default="═")
    parser.add_argument("--hver", help="vertical line character \
                        for the header row", metavar="CHAR", dest="header_ver",
                        default="│")
    parser.add_argument("--hcorners", help="corner characters for \
                        the header row", metavar="CHARS",
                        dest="header_corners", default="╒╤╕╞╪╡")
    parser.add_argument("file", help="file to render or - to read from STDIN",
                        nargs="?", default="-", metavar="FILE")
    parser.add_argument("--version", "-v", action="version",
                        version="%(prog)s 0.1")
    args = parser.parse_args()

    if args.file == "-":
        args.file = sys.stdin
    else:
        args.file = open(args.file, encoding="utf-8")

    table = [line.strip().split("\t") for line in args.file.readlines()]
    args = vars(args)
    del args["file"]
    print_table(table, **args)

if __name__ == "__main__":
    main()
