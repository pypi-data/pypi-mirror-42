# # 列表
# cast = ["a", 'b', "c", 'd']
#
# print(cast)
#
# print(len(cast))
#
# print(cast[1])
#
# # 列表末尾增加数据
# cast.append('e')
#
# print(cast)
#
# # 列表末尾删除数据
# cast.pop()
#
# print(cast)
#
# # 列表末尾增加数据项集合
# cast.extend(['a', 'f'])
# print(cast)
#
# # 列表找到并删除一个特定数据项(只能删掉第一个)
# cast.remove('a')
#
# print(cast)
#
# # 列表特定位置前面增加一个数据
# cast.insert(1, 'g')
#
# print(cast)
#
# # 循环
# for each_flick in cast:
#     print(each_flick)

import nester

# 列表，电影
# movies = ["The Holy Grail", 1975, "Terrry Jones & Terry Gilliam", 91,
#           ["Graham Chapman", ["Micheal Palin", "John Cleese", "Terry Gilliam", "Eric Idle", "Terry Jones"]]]

# print(movies)
#
# for each_item in movies:
#     print(each_item)
#
# print("----------------------------------")

# BIF（内置函数)允许检查某个特定标识符是否包含某个特定类型的数据，isinstance()
# names = ["Alice", "Bob"]
# print(isinstance(names, list))
# num_name = len(names)
# print(isinstance(num_name, list))

# 重构1
# for each_item in movies:
#     if isinstance(each_item, list):
#         for nest_item in each_item:
#             # print(nest_item)
#             if isinstance(nest_item, list):
#                 for deeper_item in nest_item:
#                     print(deeper_item)
#             else:
#                 print(nest_item)
#     else:
#         print(each_item)

# 重构2
"""这是“nester.py"模块，提供了一个名为 print_lol() 的函数，
这个函数的作用是打印列表，其中有可能包含（也可能不包含) 嵌套列表。"""


def print_lol(the_list, level):
    """这个函数取一个位置参数，名为“the_list”，这可以是任何 Python 列表（也可以是包含嵌套列表的列表）。
    所指定的列表中的每个数据项会（递归地）输出到屏幕上，各数据各占一行。"""
    for every_item in the_list:
        if isinstance(every_item, list):
            print_lol(every_item, level)
        else:
            for tab in range(level):
                print("\t", end='')
            print(every_item)

# print_lol(movies)
