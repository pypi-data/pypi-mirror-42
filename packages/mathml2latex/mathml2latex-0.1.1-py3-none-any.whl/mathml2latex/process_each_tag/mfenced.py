#! /usr/bin/env python3
# -*- coding:utf-8 -*-


#  <mfenced open="{" close="}" separators=";;,">  => 属性から区切り記号を取ってくる必要あり
def process_mfenced(descendant, insertion_list):
    determine_list = [x.string for x in list(descendant.children) if x.name]

    temp_list = []
    i = 0
    for x_string in determine_list:
        if x_string is None:
            temp_list.append(insertion_list[i])
            i += 1
        else:
            temp_list.append(x_string)

    try:
        fence_left = descendant['open']
    except Exception as e:
        # print(e)
        fence_left = '('
    try:
        fence_right = descendant['close']
    except Exception as e:
        # print(e)
        fence_right = ')'

    try:
        separators = list(descendant['separators'])

        try:
            last_separator = separators[-1]
        except Exception as e:
            # print(e)
            last_separator = ','

        length1 = len(determine_list)
        length2 = len(separators)

        if length1 > length2:
            num = length1 - length2
            separators += [last_separator] * num

        mfenced = ''.join([x + y for x, y in zip(temp_list, separators)])

    except Exception as e:
        mfenced = ''.join(temp_list)

    mfenced = fence_left + mfenced + fence_right

    return mfenced
