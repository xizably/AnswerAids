from BaiduOCR.Funcs import *


imgName = 'xg.jpg'
saveName = 'xg_crop.jpg'
get_img(imgName)
# print(Image.open(saveName).size)
# print(Image.open(imgName).mode)
crop_img(imgName, saveName)
# print(Image.open(saveName).mode)

# for i in range(1, 8):
#     crop_img(f'xg0{i}.png')

imgPath = saveName
print(get_image_txt(imgPath))




