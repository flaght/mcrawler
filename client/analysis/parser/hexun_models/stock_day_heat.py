# -*- coding: utf-8 -*-

import xml.etree.ElementTree as ET
from analysis.base.mlog import mlog

"""
Created on 201601015

@author kerry
"""

class StockDayHeat():

    def quarter_heat(self, content):
        symbol = ""
        tlist = []
        try:
            tree = ET.fromstring(content)
            lst_node = tree.getiterator('Title')
            for node in lst_node:
                if node.attrib.has_key("id") > 0:
                    symbol = node.attrib['id']
            lst_node = tree.getiterator('Individual')
            for node in lst_node:
                for c in node:
                    if c.attrib.has_key("d") > 0:
                        d = c.attrib["d"]
                        dlist = d.split(' ')
                        date = dlist[0]
                        hour = dlist[1]
                        v = c.attrib["v"]
                        changerate = c.attrib["changerate"]
                        tlist.append((d, int(v), changerate))
        except Exception, e:
            mlog.log().error("error content")
        return {"symbol": symbol, "tlist": tlist}

    def day_heat(self,content):
        symbol = ""
        tlist = []
        try:
            tree = ET.fromstring(content)
            lst_node = tree.getiterator('Title')
            for node in lst_node:
                if node.attrib.has_key("id") > 0:
                    symbol = node.attrib['id']
            lst_node = tree.getiterator('Individual')
            for node in lst_node:
                for c in node:
                    if c.attrib.has_key("d") > 0:
                        d = c.attrib["d"]
                        v = c.attrib["v"]
                        tlist.append((d,int(v)))
        except Exception, e:
            mlog.log().error("error content")

        return {"symbol":symbol,"tlist":tlist}

hx_dayheat = StockDayHeat()