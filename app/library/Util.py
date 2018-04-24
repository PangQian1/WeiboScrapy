
# 从列表中提取某个key
def extractVal(dictionary, key, default = ''):
    result = default
    if key in dictionary:
      result = dictionary[key]

    return  result