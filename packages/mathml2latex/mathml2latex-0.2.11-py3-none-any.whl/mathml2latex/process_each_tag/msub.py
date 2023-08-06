#! /usr/bin/env python3
# -*- coding:utf-8 -*-


def inspect_msub(child, insertion_list, index):

    x_string = child.string
    count = 0

    if x_string:  # childが子タグか親タグか検証
        # 子タグであれば、要素をそのまま返す
        inspected_child = x_string
    else:
        # 親タグであれば、insertion_listから要素を取ってくる
        inspected_child = insertion_list[index]
        count = 1  # 親タグに遭遇した回数

    return [inspected_child, count]


def process_msub(descendant, insertion_list):
    # Syntax: `<msubsup> base subscript</msubsup>`

    child_list = [x for x in descendant.children if x.name]

    if len(child_list) < 2:
        print(child_list)
        print(descendant)
        print(insertion_list)
        print('This is `IndexError	list index out of range`')

    index = 0

    temp_list   = inspect_msub(child_list[0], insertion_list, index)
    base        = temp_list[0]
    index       += temp_list[1]

    temp_list   = inspect_msub(child_list[1], insertion_list, index)
    subscript   = temp_list[0]

    msub = r'{}_{{{}}}'.format(base, subscript)

    return msub
