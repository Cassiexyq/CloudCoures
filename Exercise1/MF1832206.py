
import sys

# 获得输入的文件参数
# input_file = sys.argv[1]
input_file = 'evaluate.txt'
# print(input_file)


# ============================================
# 最快方式读取文件内容返回内容和top k值
def readfromtxt(file):
    content = []
    # 读取方式
    # 1.一次性读取文件返回行的list 最快
    with open(file, 'r') as f:
        k = int(f.readline())
        # print(K)
        # 获得每行数值，以.作为分隔符分别存储
        for line in f.readlines():
            line = float(line.strip())
            content.append(line)

    # 2. 使用numpy包读入
    # lines = np.loadtxt(file, dtype='str')
    # k = lines[0].astype('int')
    # content = lines[1:].astype('float')
    return k, content


# ===========================================
# 普通快排算法
# 1. 从list中跳出一个元素，称之“基准”
# 2. 分区: 重新排列list，所有元素比基准小的放右边，大的放右边。结束后，基准处于中间位置
# 3. 递归把小于基准的子列和大于基准的子列排序
# 时间复杂度O(nlogn)， 空间复杂度O(n)
# 基于该算法，改进，只找到前k个数，就不用对所有子序列排序，找到第前k大的数
# 1. 切分后的右边长度 > k, 说明基准太小，前k个数包含在右序列里
# 2. 切分后的右边长度 = k，则右边这个序列就是要找的前k个数
# 3. 切分后的右边 < k，说明基准太大，左边有要找的前k数
# 直到找到长度刚好等于k，说明此时的基准就是要找的k，可以返回
def get_K(content, k):

    # 以此前序列的最后一个元素作为基准
    pivot = content[-1]
    # right = [pivot]
    right = []
    left = []
    # 把大于基准的放右边，小于基准的放左边
    for x in content[:-1]:
        if x >= pivot:
            right.append(x)
        else:
            left.append(x)
    # 把基准放在左边，在第二种情况下要继续递归，不能放右边，会一直以该基准作为基准，要注意。
    right = [pivot] + right
    # right.extend(temp)
    len_R = len(right)
    # 判断右序列是否刚好包含前k大元素
    if len_R == k:
        # 当相同时说明right序列包含了前k数，且此时基准最小
        return pivot
    elif len_R > k:
        # 当len大说明right序列过长，必包含前k，继续递归
        return get_K(right, k)
    else:
        # 当len小说明right序列太短，必包含大于此时k的前k中的某几个，在左边找出剩下的，减掉此时找到的数
        return get_K(left, k-len_R)


if __name__ == '__main__':
    k, content = readfromtxt(input_file)
    # print(k)
    # print(content)
    result = []
    # 得到每个前K值
    for i in range(1, k+1):
        result.append(str(get_K(content, i)))
    print(','.join(result), end='')




