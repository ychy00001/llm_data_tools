import os

if __name__ == '__main__':
    # deduplicate_file = [f"aaa/{i}" for i in os.listdir("./")]
    # print(deduplicate_file)
    # print(f"{round(1 / len(deduplicate_file), 3) * 100}%")

    # g = os.walk("../")
    # for path, dir_list, file_list in g:
    #     for file_name in file_list:
    #         print(os.path.join(path, file_name))

    dirs = './test_make_dir/joseph/work/python/aaa.txt'
    print(os.path.dirname(dirs))
    if not os.path.exists(dirs):
        os.makedirs(dirs)