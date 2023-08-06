
def print_list_and_type(the_list):
    if 'cnt' not in print_list_and_type.__dict__:
        print_list_and_type.cnt = 0
        print(the_list,'Level 0')
    else:
        print_list_and_type.cnt += 1
        print(the_list, 'Level ', print_list_and_type.cnt)
    for each_item in the_list:
        if not isinstance(each_item, list):
            print(each_item, type(each_item))
        else:
            print_list_and_type(each_item)


