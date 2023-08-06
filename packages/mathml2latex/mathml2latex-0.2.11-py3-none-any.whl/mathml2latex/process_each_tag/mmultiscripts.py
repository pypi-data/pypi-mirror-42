#! /usr/bin/env python3
# -*- coding:utf-8 -*-

import re


def convert2latex(inspected_child_list):

    temp_list = []
    i = 0

    for child in inspected_child_list:
        if child == 'nnnn':
            continue
        elif child == '':
            continue
        elif i % 2:
            temp_list.append('_{{{}}}'.format(child))
        else:
            temp_list.append('^{{{}}}'.format(child))
        i += 1

    return temp_list


def inspect_mmultiscripts(child_list, insertion_list, index):

    inspected_list = []
    count = 0
    for child in child_list:
        # mprescripts を含まない場合、child_list の要素はすべて空文字列(str)であるはず => 処理する必要がないのでそのままSkip
        if type(child) == str:
            return [child_list, count]

        x_string = child.string

        if child.name == 'none':  # <none /> タグのとき
            x_string = 'nnnn'
            inspected_list.append(x_string)
        elif x_string:  # childが子タグか親タグか検証
            # 子タグであれば、要素をそのまま返す
            inspected_list.append(x_string)
        else:
            # 親タグであれば、insertion_listから要素を取ってくる
            inspected_list.append(insertion_list[index])
            index += 1
            count += 1  # 親タグに遭遇した回数

    return [inspected_list, count]


def process_mmultiscripts(descendant, insertion_list):
    # Syntax: `<mmultiscripts>base postsubscript postsuperscript
    # <mprescripts /> presubscript presuperscript </mmultiscripts>`
    # ただし、任意の要素が`<none />`に置き換わることもある

    temp_list = []

    child_list = [x for x in descendant.children if x.name]

    base_list = child_list[:1]
    child_list_without_base = child_list[1:-1]

    i = 0
    index_of_mprescript = 0
    for child in child_list_without_base:
        if child.name == 'mprescripts':
            index_of_mprescript = i
        else:
            i += 1

    # <mprescripts /> が存在するかどうかの分岐フラグ
    if index_of_mprescript:  # 存在しなければ 0 のままなはずである
        mprescripts_exist = True
    else:
        mprescripts_exist = False

    # postscripts, prescripts に分離してリストを保持
    if mprescripts_exist:
        # postscript に含まれる childだけで構成されるリストを作る
        postscript_list = child_list_without_base[0:index_of_mprescript]
        # prescript に含まれる childだけで構成されるリストを作る
        index_of_mprescript += 1  # `mprescripts` を取り除く
        prescript_list = child_list_without_base[index_of_mprescript:-1]
    else:
        # prescripts が存在しない場合、postscriptのみリストとする
        postscript_list = child_list_without_base
        prescript_list  = [''] * len(postscript_list)  # postscript_list と同じ要素数の空文字列リストを作成

    counter = 0
    inspected_base_list        = inspect_mmultiscripts(base_list, insertion_list, counter)
    base = inspected_base_list[0][0]
    counter += inspected_base_list[1]

    inspected_prescripts_list  = inspect_mmultiscripts(prescript_list, insertion_list, counter)
    prescript = convert2latex(inspected_prescripts_list[0])
    counter += inspected_prescripts_list[1]

    inspected_postscripts_list = inspect_mmultiscripts(postscript_list, insertion_list, counter)
    postscript = convert2latex(inspected_postscripts_list[0])

    temp_list = ['{}']
    temp_list.extend(prescript)
    temp_list.append(base)
    temp_list.extend(postscript)

    mmultiscripts = re.sub('nnnn', '', ''.join(temp_list))

    return mmultiscripts
