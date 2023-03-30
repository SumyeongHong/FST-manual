import os
import string
from ast import literal_eval
import json

### 10000개 파일 처리하는데 40초 ~ 1분 정도 소요될 수 있습니다.
### 아래 두 경로를 잘 맞춰주세요
folder_relative_path = './HSC_Feature_Vector 2'
image_data_path = './image (4).json'
export_path = './hsc_result.json'


file_list = os.listdir(folder_relative_path)
imageIdMap = {}
result = []

def flatten(arr):
    result = []
    for item in arr:
        if isinstance(item, list):
            result.extend(flatten(item))
        else:
            result.append(item)
    return result

# image 정보로부터 파일 이름 -> ID 매핑하는 파트
with open(image_data_path) as json_file:
    a = json.load(json_file)
    for each in a:
        imageIdMap[each['image'].split('.')[0]] = each['image_id']

# 각 파일에 대해 처리하는 파트
for file_name in file_list:
    path = folder_relative_path + '/' + file_name
    f = open(path, 'r')
    text = f.read()
    text = text.translate({ord(c): None for c in string.whitespace})
    text = text.split(',device')[0].split('tensor(')[1]
    array = literal_eval(text)
    flat_array = flatten(array)
    id = imageIdMap[file_name.split('.')[0]]
    result.append({
        "image_id": id,
        "vector": flat_array
    })
    f.close()

# 파일 출력하는 파트
with open(export_path, 'w', encoding='UTF-8') as file:
    file.write(json.dumps(result, indent=2, ensure_ascii=False))