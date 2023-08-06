#! /usr/bin/env python3
# -*- coding:utf-8 -*-


def process_mtext(descendant, child_list, insertion_list):
    # child_list, insertion_listだけでは、
    # それらをどのように組み合わせればいいのかについての情報がない
    mtext_list = []
    i = 0
    j = 0
    # 親タグ要素の塊がある場合
    if insertion_list:
        determine_list = [x.string for x in list(descendant.children) if x.name]
        for x_string in determine_list:
            if x_string:  # 親タグのかたまりではない場合
                mtext_list.append(x_string)
                i += 1
            else:  # 親タグのかたまりである場合
                mtext_list.append(insertion_list[j])
                j += 1

        mtext = ''.join(mtext_list)
    # 親タグ要素の塊がない場合
    else:
        mtext = ''.join(child_list)

    return mtext
