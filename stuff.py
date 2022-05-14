def temp_axis_temp_list(start: int=0, end: int=40) -> list: 
    temp_list = []
    start_temp = start
    temp = start_temp

    while temp <= end:
        temp_list.append(temp)
        temp += 2

    return temp_list

print(temp_axis_temp_list(-8, 40))