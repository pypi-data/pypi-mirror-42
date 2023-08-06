#  n进制 转 m进制，m和n均为正整数
# n-->10
# 10-->m


def bs(ten, m):
    '''
    十进制转m进制
    :param ten: 十进制数
    :param m: 转换进制数
    :return: 无
    '''
    while ten:
        yield str(ten % m)
        ten = ten // m


def start(num, n, m):
    '''

    :param num:输入数：输入小写字母和数字
    :param n:输入数的进制数：必须整数
    :param m:输出数的进制数，必须整数
    :return:返回输出数字符串
    '''
    # if n>1 and m>1:raise ValueError("必须输入大于1的整数")
    # elif not isinstance(num,(int,str)):raise ValueError('num必须为int型或小写字母')
    # elif num>1:raise ValueError('num必须大于1')
    # elif isinstance(num,str):num=str(num)
    ten = int(str(num), n)  # n-->10
    bs_num = bs(ten, m)
    # bs_num01=[str(87+i) if int(i)>9 else -i for i in bs_num]
    return ''.join(bs_num)[::-1]


if __name__ == '__main__':
    print(start(1000111, 2, 16))
