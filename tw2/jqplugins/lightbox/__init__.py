# -*- coding: utf-8 -*-
#
# tw2.jqplugins.lightbox - a jQuery Lightbox widget
#
# Copyright © 2016 Nils Philippsen <nils@tiptoe.de>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with this program; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.

from __future__ import unicode_literals

from tw2.core import Widget, JSLink, CSSLink, DirLink, Param
from tw2.core import js_function, js_symbol
from tw2.jquery.base import jquery_js


lightbox_js = JSLink(
    modname=__name__, filename="static/js/lightbox.js")

lightbox_css = CSSLink(
    modname=__name__, filename="static/css/lightbox.css")

static_resources = DirLink(modname=__name__, filename="static")


class Lightbox(Widget):

    resources = [jquery_js, lightbox_js, lightbox_css, static_resources]

    options = Param("Dictionary with options to the Lightbox widget.",
                    default=None)

    template = ""

    def prepare(self):
        super(Lightbox, self).prepare()

        copy_img_alt_src = """jQuery('a[data-lightbox]:not([data-title])>img[alt]:only-child').each(
    function(i, elem) {
        elem.parentElement.setAttribute(
            'data-title', elem.getAttribute('alt'));
    });"""
        self.add_call(copy_img_alt_src)
        if self.options:
            self.add_call(js_function("lightbox.option")(self.options))

    def generate_output(self, displays_on):
        return ""
