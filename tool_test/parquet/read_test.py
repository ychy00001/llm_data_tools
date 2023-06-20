import pyarrow as pa
import pyarrow.parquet as pq
import sys
import re
base_dir = "/data/project/llm_data_tools/data/falcon_web"

if __name__ == '__main__':
    i = "train-02578-of-05534-2a111086cb4b97fd.parquet"
    file_item = f"{base_dir}/{i}"
    df = pq.read_table(file_item).to_pandas()
    print(f'行数：{len(df)}')
    for index, row in df.iterrows():
        url = row['url']
        content = row['content']
        dump = row['dump']
        dump_year = re.search(r'[0-9]{4}', dump, re.M|re.I)
        if dump_year:
            print(f'dump_group:{dump_year.group()}')
            if dump_year.group() != "2020":
                print("no!!!")
            else:
                print(f"{dump_year.group()}")
        else:
            print("Nothing found!")
        print(f'url:{url}, dump:{dump}, content{content[:20]}')
        sys.exit()


