import cv2
import pytesseract

img = cv2.imread('./stored_frames/500.jpg')
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

text = pytesseract.image_to_string(gray)
print(text)

cv2.imshow('frame', img)
cv2.waitKey(0)
cv2.destroyAllWindows()