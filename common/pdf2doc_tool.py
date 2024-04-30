from pdf2docx import Converter
import os
import subprocess


def make_file_dir(file_path):
    '''
    根据文件创建其路径的目录
    '''
    file_dir = os.path.dirname(file_path)
    if not os.path.exists(file_dir):
        os.makedirs(file_dir)


def get_all_files(file_dir, suffix1="_doc"):
    '''
    获取所有文件，同时返回文件对应的格式化以及清楚的脏数据
    return: [(file_path, file_format_path, file_dirty_path), ()....]
    '''
    files = []
    g = os.walk(file_dir)
    for path, dir_list, file_list in g:
        for file_name in file_list:
            file_path = os.path.join(path, file_name)
            format_path = file_path.replace(file_dir, file_dir + suffix1)
            if format_path.endswith(".md.pdf"):
                format_path = format_path.replace(".md.pdf", ".docx")
            elif format_path.endswith(".pdf"):
                format_path = format_path.replace(".pdf", ".docx")
            else:
                continue
            make_file_dir(format_path)
            files.append((file_path, format_path))
    return files


def get_all_files_md(file_dir, suffix1="_md"):
    '''
    获取所有文件，同时返回文件对应的格式化以及清楚的脏数据
    return: [(file_path, file_format_path, file_dirty_path), ()....]
    '''
    files = []
    g = os.walk(file_dir)
    for path, dir_list, file_list in g:
        for file_name in file_list:
            file_path = os.path.join(path, file_name)
            format_path = file_path.replace(file_dir, file_dir + suffix1)
            if format_path.endswith(".docx"):
                media_path = format_path.replace(".docx", "_img")
                format_path = format_path.replace(".docx", ".md")
            else:
                continue
            make_file_dir(format_path)
            make_file_dir(media_path)
            files.append((file_path, format_path, media_path))
    return files


def pdfToWorld(base_dir):
    jobs = get_all_files(base_dir)
    for item in jobs:
        pdf_file = item[0]
        docx_file = item[1]
        try:
            cv = Converter(pdf_file)
            cv.convert(docx_file)  # all pages by default
            cv.close()
        except RuntimeError:
            print(f"异常文件：{pdf_file}")
            with open("/Users/rain/Downloads/convert_err_file", "a", encoding='utf-8') as f:
                f.write(pdf_file)
                f.write("\n")


def worldToMarkDown(base_dir):
    "pandoc -f docx -t markdown --extract-media ./ -o svn.md 11-SVN_k.docx"
    jobs = get_all_files_md(base_dir)
    for item in jobs:
        world_file = item[0]
        md_file = item[1]
        img_dir = item[2]
        p = subprocess.Popen(f"pandoc -f docx -t markdown --extract-media '{img_dir}' -o '{md_file}' '{world_file}'",
                             shell=True, encoding="utf8", stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        for line in p.stdout.readlines():
            print(line)
        p.wait()


if __name__ == '__main__':
    #pdfToWorld("/Users/rain/Downloads/wz_export_pdf")
    # pdfToWorld("E:\game\wz_export_pdf")
     worldToMarkDown("/Users/rain/Downloads/wz_export_pdf_doc")
    # worldToMarkDown("E:\game\wz_export_pdf_doc")
