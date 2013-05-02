# -*- coding: utf-8 -*-
"""
    Copyright (C) 2013 Kouhei Maeda <mkouhei@palmtb.net>

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""


def generate_url(partial_uri_list):
    """
    Argument:

        partial_uri_list: patial string of generating URL
                          ex. ["https://swift.example.org", "auth", "v1.0"]

    Return: URL
            ex. "https://swift.example.org/auth/v1.0"
    """
    url = ""
    for i, partial_uri in enumerate(partial_uri_list):
        if i + 1 == len(partial_uri_list):
            url += partial_uri
        else:
            url += partial_uri + "/"
    return url
