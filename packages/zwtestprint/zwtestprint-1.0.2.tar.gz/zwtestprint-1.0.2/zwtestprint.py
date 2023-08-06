'''测试一下注释
来个多行的
哈哈'''
def print_log(list_info,width):
    for item in list_info:
        if isinstance(item,list):
            '''如果是集合递归打印'''
            #print('-----------------')
            print_log(item,width+5)
        else:
            for i in range(width):
                print('\t',end='')
            print(item)

