import cv2
# print(cv2.__version__)  verifico se opencv è installato o meno

array = cv2.imread("image.png")

print(array.shape)
print(array)
