#! /usr/bin/env python3
# -*- coding:utf-8 -*-


# そもそもどこでPhantomなんて使うのか？利用方法がわからない
def process_mphantom(descendant, insertion_list):

    determine_list = [x.string for x in list(descendant.children) if x.name]
    temp_list = []
    i = 0
    for x_string in determine_list:
        if x_string is None:
            temp_list.append(insertion_list[i])
            i += 1
        else:
            temp_list.append(x_string)
    mphantom = ''.join(temp_list)
    return mphantom
