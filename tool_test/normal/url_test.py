import os
base_dir = "../../data/falcon_web"
format_dir = base_dir + "_format/"
back_dir = base_dir + "_back/"
if __name__ == '__main__':
    # url = "https://stackoverflow.com/questions/70123567/index-row-size-2712-exceeds-btree-version-4-maximum-2704-for-index-while-doing"
    # print(url[:1800])
    # print(os.listdir(back_dir))
    skip_dict= {}
    back_list = os.listdir(back_dir)
    for list_item in back_list:
        skip_dict[list_item] = "all"
    print(skip_dict)
