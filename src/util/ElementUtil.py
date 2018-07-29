#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/7/28 18:18
# @Author  : ganliang
# @File    : ElementUtil.py
# @Desc    : xml解析

def getElement(element, tag_name, attribute_name):
    elements = element.getElementsByTagName(tag_name)
    if elements:
        element = elements[0]
        value = element.getAttribute(attribute_name)
        return value
    return ""


def getTagElement(element, tag, tag_name, attribute_name):
    elements = element.getElementsByTagName(tag)
    if elements:
        tagElements = element.getElementsByTagName(tag_name)
        if tagElements:
            element = elements[0]
            value = element.getAttribute(attribute_name)
            return value
    return ""
