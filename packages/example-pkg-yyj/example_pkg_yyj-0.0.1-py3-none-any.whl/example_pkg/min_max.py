def ins():
    x = input("请输入：")
    return x

def min_max(list):
    min = list[0]
    max = list[0]
    for i in list:
        if min >= i:
            min = i
    for j in list:
        if max <= j:
            max = j
    print(str(min) + "," + str(max))

if __name__=='__main__':

    list=ins()
    list=list.split(',')
    min_max(list)



