import time

if __name__ == '__main__':
    line_count = 2685029
    percent_step = 5
    current_percent = 0
    for current_line in range(line_count):
        percent = current_line / line_count * 100
        print(f"current: {current_line}, percent:{percent}")
        if percent > current_percent:
            print(f"已完成{int(percent)}%")
            current_percent += percent_step
        if percent == 100:
            print(f"处理完成!")
        time.sleep(1)
