# coding=utf-8
import os


def get_DirWayDict(fileWay: str) -> dict:
    """
    该函数负责以字典形式整理目标文件夹下的所有文件
    :param fileWay: 文件夹路径
    :return: {'拓展名1': ['该类型下文件名1', '该类型下文件名2', ...], '拓展名2': [...], ...}
    """
    fileNamesSplitByTypes = {}
    fileTypes = []
    for item in os.listdir(fileWay):
        if os.path.isfile(os.path.join(fileWay, item)):             # 确定操作对象为文件而非文件夹
            fileType = os.path.splitext(item)[-1][1:]       # 提取文件拓展名
            if fileType == 'vsmeta':                        # 如果是已经在VS station处理过信息，生成过vsmeta文件的话
                fileType = item.split('.')[-2] + '.vsmeta'      # 对应拓展名就应该是视频拓展名+.vsmeta
            if fileType not in fileTypes:                   # 当该文件类型为第一次出现时
                fileTypes.append(fileType)                      # 添加该文件拓展名到fileTypes列表里
                fileNamesSplitByTypes[fileType] = list()        # 在字典中新建键值对，拓展名为键，对应值初始化为列表
            fileNamesSplitByTypes[fileType].append(item)            # 将文件路径添加到字典值对应的值列表里

    print("目标文件夹路径内情况如下：")
    for key in fileNamesSplitByTypes:
        print("存在{}个拓展名为{}的文件".format(len(fileNamesSplitByTypes[key]), key))

    return fileNamesSplitByTypes


def get_ColoredElement(element: str) -> str:
    """
    该函数决定新文件名里的所有元素以什么样的方式连接在一起
    :param element: 新文件名里的单个元素
    :return: ‘[元素]’
    """
    return '[' + element + ']'


def get_NewRuleFilesName(maxNum: int, newElementList: list) -> list:
    """
    该函数负责生成最终的文件名（不包含拓展名）列表，之所以要生成列表是由于存在拓展名不同但文件名必须相同的情况
    :param maxNum: 要更改多少集的文件，取决于之前检查的结果
    :param newElementList: 含有所有新名称元素的列表
    :return: ['新文件名1', '新文件名2', '新文件名3', ...]
    """
    newRuleList = []
    for m in range(maxNum):
        finalNewName = ''
        num = str(m + 1)
        if int(num) < 10:
            num = '0' + num
        for item in newElementList:
            finalNewName += get_ColoredElement(item) if item else get_ColoredElement(num)
        newRuleList.append(finalNewName)

    return newRuleList


if __name__ == "__main__":
    "① 输入要更改的目标文件夹路径"
    # noinspection SpellCheckingInspection
    fileW = '\\\\DS220plus\\anime\\秘密内幕～女警的反击～'
    "② 扫描目标文件夹内状况并打印"
    oldFilesDict = get_DirWayDict(fileW)
    "③ 输入总集数"
    episodeNum = int(input("输入总集数："))
    "④ 修改要更改成格式的元素，并通过函数检查"
    "注意：此处的 0 值为“集数”存放的位置"
    # noinspection SpellCheckingInspection
    newNameRuleList = ["CXRAW", "假面骑士W", 0, "1080P", "HEVC Main10P FLAC MKV"]
    newFilesList = get_NewRuleFilesName(episodeNum, newNameRuleList)
    "⑤ 正式更改前的确认"
    for k in oldFilesDict:
        if len(oldFilesDict[k]) == episodeNum:
            for i in range(episodeNum):
                print("{} 将更改为-> {}".format(oldFilesDict[k][i], newFilesList[i] + '.' + k))

    if input("是否确定更改？（Y/N）") == "Y":
        for k in oldFilesDict:
            if len(oldFilesDict[k]) == episodeNum:
                for i in range(episodeNum):
                    os.rename(os.path.join(fileW, oldFilesDict[k][i]), os.path.join(fileW, newFilesList[i] + '.' + k))
    else:
        print("已更改")
