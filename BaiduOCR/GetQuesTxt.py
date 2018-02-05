from BaiduOCR.Funcs import *


imgName = 'xg.jpg'
saveName = 'xg_crop.jpg'
# get_img(imgName)
# crop_img(imgName, saveName)

# for i in range(1, 8):
#     crop_img(f'xg0{i}.png')

ques_txt = get_image_arry(saveName)
print(ques_search(ques_txt))


