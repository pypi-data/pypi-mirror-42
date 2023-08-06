#! /usr/bin/env python3
# -*- coding:utf-8 -*-


# Problem !! => LaTeX形式で表記するときに、数式装飾記号が複雑すぎる………
# cf. http://www.latex-cmd.com/equation/accent.html
def inspect_mover(child, insertion_list, index):

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


def process_mover(descendant, insertion_list):
    # Syntax: `<mover> base overscript </mover>`
    child_list = [x for x in descendant.children if x.name]

    index = 0

    temp_list   = inspect_mover(child_list[0], insertion_list, index)
    base        = temp_list[0]
    index       += temp_list[1]

    temp_list   = inspect_mover(child_list[1], insertion_list, index)
    overscript  = temp_list[0]

    mover = r'\mover{{{}}}^{{{}}}'.format(base, overscript)

    return mover
