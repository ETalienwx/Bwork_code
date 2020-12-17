from PIL import Image, ImageSequence
import numpy as np
np.set_printoptions(threshold=np.inf)


def print_to_txt(x, cur):
    filename = str(cur) + ".txt"
    f = open(filename, "w")
    for tmp in x:
        count_1 = tmp.count(1)
        count_0 = tmp.count(0)
        # f.write(str(tmp))
        f.write("1:" + str(count_1) + " " + "0:" + str(count_0))
        f.write('\n')
    f.close()


def freme_binary(img):
    try:
        img = Image.open(img)
    except IOError:
        print("Fail to open image")

    cur = 1
    for frame in ImageSequence.Iterator(img):
        width, height = frame.size
        image_list = []
        for x in range(height):
            px_line = []
            for y in range(width):
                px = frame.getpixel((y, x))
                px_line.append(px)
            image_list.append(px_line)
        print_to_txt(image_list, cur)
        # print(image_list)
        cur += 1


if __name__ == '__main__':
    freme_binary("test.gif")
