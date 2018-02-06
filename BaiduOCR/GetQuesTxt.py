from BaiduOCR.Funcs import *


imgName = 'xg.jpg'
saveName = 'xg_crop.jpg'
# get_img(imgName)
# crop_img(imgName, saveName)

# for i in range(1, 8):
#     crop_img(f'xg0{i}.png')

ques_txt = get_image_arry(saveName)
ques_txt = ['湄公河不经过以下哪个国家', '印度', '缅甸', '老挝']
print(ques_search(ques_txt))
# print(option_search(ques_txt))


