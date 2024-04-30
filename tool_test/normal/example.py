def find_earliest_time_slot(a_availability, b_availability, meeting_duration):
    '''
    查找两个数据中均没有占用的时间
    假设a_availability为张三开会时间["0830-0900", "1000-1030"]
    b_availability为李四开会时间["0800-0930", "1000-1030"]
    返回结果为：张三和李四均不开会的时间组['00:00-08:00', '09:30-10:00','10:30-24:00']
    meeting_duration: 过滤返回结果大于该时间段的条目
    '''
    def cut_available_time(old_available_time, start_time, end_time):
        new_available_time = []
        for avail_item in old_available_time:
            avi_start = avail_item[0]
            avi_end = avail_item[1]
            # 当前时间不占用空闲时间
            if avi_start >= end_time or avi_end <= start_time:
                new_available_time.append(avail_item)
                continue
            if start_time <= avi_start < end_time <= avi_end:
                new_available_time.append((end_time, avi_end))
            elif end_time >= avi_end > start_time >= avi_start:
                new_available_time.append((avi_start, start_time))
            elif avi_start < start_time and avi_end > end_time:
                new_available_time.append((avi_start, start_time))
                new_available_time.append((end_time, avi_end))
        return new_available_time

    available_time = [(0, 1440)]
    for item_duration in a_availability + b_availability:
        start_str = item_duration.split("-")[0]
        end_str = item_duration.split("-")[1]
        start_hour = int(start_str[:2])
        start_minute = int(start_str[2:])
        end_hour = int(end_str[:2])
        end_minute = int(end_str[2:])
        start = start_hour * 60 + start_minute
        end = end_hour * 60 + end_minute
        available_time = cut_available_time(available_time, start, end)

    result_availability = []
    for time_item in available_time:
        start = int(time_item[0])
        end = int(time_item[1])
        if end - start >= meeting_duration:
            result_str = "%02d:%02d-%02d:%02d" % (start / 60, start % 60, end / 60, end % 60)
            result_availability.append(result_str)

    return result_availability if len(result_availability) > 0 else None


def find_availability_time_slot(a_availability, b_availability, meeting_duration):
    '''
    查找两个数据中均可用的时间
    假设a_availability为张三空闲时间["0830-0900", "1000-1030"]
    b_availability为李四空闲时间["0800-0930", "1000-1030"]
    返回结果为：张三和李四都空闲的时间组['08:30-09:00', '10:00-10:30']
    meeting_duration: 过滤返回结果大于该时间段的条目
    '''
    def extra_time(time_info_str):
        start_str = time_info_str.split("-")[0]
        end_str = time_info_str.split("-")[1]
        start_hour = int(start_str[:2])
        start_minute = int(start_str[2:])
        end_hour = int(end_str[:2])
        end_minute = int(end_str[2:])
        start_num = start_hour * 60 + start_minute
        end_num = end_hour * 60 + end_minute
        return start_num, end_num

    def intersect_available_time(old_available_time, start_time, end_time):
        new_available_time = []
        for avail_item in old_available_time:
            avi_start = avail_item[0]
            avi_end = avail_item[1]
            if avi_start > end_time or avi_end < start_time:
                continue
            elif start_time <= avi_start <= end_time <= avi_end:
                new_available_time.append((avi_start, end_time))
            elif avi_start <= start_time and avi_end >= end_time:
                new_available_time.append((start_time, end_time))
            elif end_time >= avi_end >= start_time >= avi_start:
                new_available_time.append((start_time, avi_end))
            elif avi_start >= start_time and avi_end <= end_time:
                new_available_time.append((avi_start, avi_end))
        return new_available_time

    available_time = []
    for item_duration in a_availability:
        available_time.append(extra_time(item_duration))

    result_time = []
    for item_duration in b_availability:
        start, end = extra_time(item_duration)
        result_time = result_time + (intersect_available_time(available_time, start, end))

    result_availability = []
    for time_item in result_time:
        start = int(time_item[0])
        end = int(time_item[1])
        if end - start >= meeting_duration:
            result_str = "%02d:%02d-%02d:%02d" % (start / 60, start % 60, end / 60, end % 60)
            result_availability.append(result_str)

    return result_availability if len(result_availability) > 0 else None


if __name__ == '__main__':
    a_availability = ["0830-0900", "1000-1030", "1100-1300", "1330-1530", "1630-1730"]
    b_availability = ["0800-0930", "1000-1030", "1100-1130", "1200-1430", "1500-1600", "1630-1700"]
    result = find_earliest_time_slot(a_availability, b_availability, 30)
    print(result)
    result1 = find_availability_time_slot(a_availability, b_availability, 30)
    print(result1)
