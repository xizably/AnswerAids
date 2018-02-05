from BaiduOCR.Funcs import *


imgName = 'xg.jpg'
saveName = 'xg_crop.jpg'
# get_img(imgName)
# print(Image.open(saveName).size)
# print(Image.open(imgName).mode)
crop_img(imgName, saveName)
# print(Image.open(saveName).mode)

# for i in range(1, 8):
#     crop_img(f'xg0{i}.png')

imgPath = saveName
# {'log_id': 5182755660894572553, 'words_result_num': 5, 'words_result':
# [{'words': '8.我们吃的洋芋是植物的哪个部', 'probability': {'variance': 0.000133, 'average': 0.995295, 'min': 0.962865}},
# {'words': '分?', 'probability': {'variance': 0, 'average': 0.999945, 'min': 0.999903}},
# {'words': '茎', 'probability': {'variance': 0, 'average': 0.995819, 'min': 0.995819}},
# {'words': '叶', 'probability': {'variance': 0, 'average': 0.999013, 'min': 0.999013}},
# {'words': '果实', 'probability': {'variance': 1e-06, 'average': 0.998826, 'min': 0.998002}}]}

ques_txt = get_image_arry(imgPath)
# for i in range(0, len(result_txt)):
#     print(result_txt[i])

print(ques_search(ques_txt))


