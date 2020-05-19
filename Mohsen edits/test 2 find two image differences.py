import pyautogui, time, cv2
import numpy as np

train_image = cv2.imread("testing images/game00.jpg")
query_card = cv2.imread("testing images/game1.jpg")

difference_image = cv2.absdiff(query_card, train_image)
difference_amount = int(np.sum(difference_image)/255)

cv2.imwrite('color_img.jpg', difference_image)
cv2.imshow("image", difference_image)
print(difference_amount)

cv2.waitKey()
cv2.destroyAllWindows()