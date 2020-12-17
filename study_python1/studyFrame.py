# ---------------------------------打印在控制台---------------------------------
# from PIL import Image, ImageSequence

# try:
#     img = Image.open("test.gif")
# except IOError:
#     print("Fail to open image")

# px_arr = []  # 存放像素点标记的列表
# for frame in ImageSequence.Iterator(img):
#     width, height = img.size
#     image_list = []
#     for x in range(height):
#         px_line = []
#         for y in range(width):
#             px = img.getpixel((y, x))
#             px_line.append(px)
#         image_list.append(px_line)
#     px_arr.append(image_list)
# print(px_arr)
# -----------------------------------------------------------------------------

# ------------------------------------------------------------------------------------------------------------------------------------
# txt = open("open.txt", "w")
# width, height = img.size
# image_list =[]
# for x in range(height):
#     px_line = []
#     for y in range(width):
#         px = img.getpixel((y, x))
#         px_line.append(px)
#     image_list.append(px_line)
# for px in image_list:
#     txt.write(str(px))
# txt.close()
# ------------------------------------------------------------------------------------------------------------------------------------

# ---------------------------------输出至文件---------------------------------
# from PIL import Image, ImageSequence


# def print_to_txt(x, cur):
#     filename = str(cur) + ".txt"
#     f = open(filename, "w")
#     for tmp in x:
#         f.write(str(tmp))
#         f.write('\n')
#     f.close()


# try:
#     img = Image.open("test.gif")
# except IOError:
#     print("Fail to open image")

# px_arr = []  # 存放像素点标记的列表
# cur = 1
# for frame in ImageSequence.Iterator(img):
#     width, height = img.size
#     image_list = []
#     for x in range(height):
#         px_line = []
#         for y in range(width):
#             px = img.getpixel((y, x))
#             px_line.append(px)
#         image_list.append(px_line)
#     print_to_txt(image_list, cur)
#     cur += 1
# ------------------------------------------------------------------------------------------------------------------------------------

# -----------------------------------------------------------------------------
# from PIL import Image
# import os
# gifFileName = "test.gif"
# im = Image.open(gifFileName)  # 使用Image打开test.gif图像
# pngDir = gifFileName[:-4]  # 创建存放每帧图片的文件夹
# os.mkdir(pngDir)
# try:
#     while True:
#         current = im.tell()
#         im.save(pngDir+'/'+str(current)+'.png')
#         im.seek(current+1)
# except EOFError:
#     pass
# -----------------------------------------------------------------------------

# ----------------------------保存每一帧-----------------------------------
# from PIL import Image, ImageSequence
# im = Image.open("test.gif")
# index = 1
# for frame in ImageSequence.Iterator(im):
#     frame.save("frame%d.png" % index)
#     index += 1
# ---------------------------------------------------------------

# ----------------------------RGB-----------------------------------
# from PIL import Image
# im = Image.open('0.png')
# width = im.size[0]  # 1920
# height = im.size[1]  # 1080
# im = im.convert('RGB')
# array = []
# for x in range(width):
#     for y in range(height):
#         r, g, b = im.getpixel((x,y))
#         rgb = (r, g, b)
#         array.append(rgb)
# print(array)
# ---------------------------------------------------------------

# ----------------------------打印每一点的像素-----------------------------------
# px = image.load()
# print (px[4,4])
# ---------------------------------------------------------------

# ----------------------------统计每个颜色的数量-----------------------------------
# im1 = Image.Image.getcolors(img)
# print(im1)
# ---------------------------------------------------------------

# ----------------------------打印成一维数组-----------------------------------
# image = Image.open('45.png')
# width = image.width
# height = image.height
# image_list = []
# for x in range(height):
#     scanline_list = []
#     for y in range(width):
#         pixel = image.getpixel((y, x))
#         scanline_list.append(pixel)
#     image_list.append(scanline_list)
# print(image_list)
# ---------------------------------------------------------------

# ----数据可视化matplotlib-----------------------------------------------------
# from PIL import Image
# import matplotlib.pyplot as plt
# img = Image.open("test.gif")
# plt.imshow(img)
# plt.show()
# data = img.getdata()
# seq = list(data)
# print(seq[345])
# ---------------------------------------------------------------

# ---------第一版代码（放到数组里面）------------------------------------------------------
# from PIL import Image, ImageSequence


# def print_to_txt(x, cur):
#     filename = str(cur) + ".txt"
#     f = open(filename, "w")
#     for tmp in x:
#         f.write(str(tmp))
#         f.write('\n')
#     f.close()


# def freme_binary(img):
#     try:
#         img = Image.open(img)
#     except IOError:
#         print("Fail to open image")

#     # px_arr = []  # 存放像素点标记的列表
#     cur = 1
#     for frame in ImageSequence.Iterator(img):
#         width, height = frame.size
#         image_list = []
#         for x in range(height):
#             px_line = []
#             for y in range(width):
#                 px = frame.getpixel((y, x))
#                 px_line.append(px)
#             image_list.append(px_line)
#         print_to_txt(image_list, cur)
#         cur += 1


# if __name__ == '__main__':
#     freme_binary("test.gif")
# ---------------------------------------------------------------

# --------第二版（使用numpy进行数组操作）-----------------------------------------------
# from PIL import Image, ImageSequence
# import numpy as np
# np.set_printoptions(threshold=np.inf)


# def print_to_txt(x, cur):
#     filename = str(cur) + ".txt"
#     f = open(filename, "w")
#     for tmp in x:
#         f.write(str(tmp))
#         f.write('\n')
#     f.close()


# def freme_binary(img):
#     try:
#         img = Image.open(img)
#     except IOError:
#         print("Fail to open image")

#     cur = 1
#     for frame in ImageSequence.Iterator(img):
#         width, height = frame.size
#         frame.convert("L")
#         frame.point(lambda x: 1 if x > 100 else 0)
#         data = frame.getdata()
#         print(data)
#         new_data = np.reshape(data, (height, width))
#         print_to_txt(new_data, cur)
#         cur += 1


# if __name__ == '__main__':
#     freme_binary("test.gif")
# ---------------------------------------------------------------
