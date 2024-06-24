import cv2
import numpy as np

class ImagePreprocesser:
    def __init__(self, imagePath):
        self.imgPath = imagePath
        self.img = cv2.imread(self.imgPath)
    
    @staticmethod
    def histogramAdjustment(image):
        image[:, :, 2] = cv2.equalizeHist(image[:, :, 2])
        return image
    
    @staticmethod
    def grayScaleConverter(image):
        red = image[:, :, 0]
        green = image[:, :, 1]
        blue = image[:, :, 2]
        return (0.3 * red + 0.59 * green + 0.11 * blue).astype(np.uint8)

    @staticmethod
    def unSharpMask(image):
        blurredImg = cv2.GaussianBlur(image, (3, 3), 0)
        return cv2.addWeighted(image, 1.5, blurredImg, -0.5, 0)
    
    @staticmethod
    def thresholdImg(image):
        image_8bit = cv2.convertScaleAbs(image)
        thresholdValue, img = cv2.threshold(image_8bit, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        return img
    
    def processImage(self):
        self.img = self.histogramAdjustment(self.img)
        self.img = self.grayScaleConverter(self.img)
        self.img = self.unSharpMask(self.img)
        self.img = self.thresholdImg(self.img)
        cv2.imwrite(self.imgPath, self.img)
        return self.img