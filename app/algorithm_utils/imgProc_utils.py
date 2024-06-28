import cv2
import numpy as np
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ImagePreprocesser:
    def __init__(self, imagePath):
        """
        Initialize the ImagePreprocesser with the given image path.

        Args:
            imagePath (str): The path to the image to be processed.
        """
        self.imgPath = imagePath
        self.img = cv2.imread(self.imgPath)
        if self.img is None:
            logger.error(f"Failed to read image from path: {imagePath}")
            raise FileNotFoundError(f"Image not found at path: {imagePath}")

    @staticmethod
    def histogramAdjustment(image):
        """
        Adjust the histogram of the image's red channel.

        Args:
            image (numpy.ndarray): The input image.

        Returns:
            numpy.ndarray: The image with adjusted histogram.
        """
        logger.info("Adjusting histogram...")
        image[:, :, 2] = cv2.equalizeHist(image[:, :, 2])
        return image

    @staticmethod
    def grayScaleConverter(image):
        """
        Convert the image to grayscale using the weighted sum method.

        Args:
            image (numpy.ndarray): The input image.

        Returns:
            numpy.ndarray: The grayscale image.
        """
        logger.info("Converting to grayscale...")
        red = image[:, :, 0]
        green = image[:, :, 1]
        blue = image[:, :, 2]
        return (0.3 * red + 0.59 * green + 0.11 * blue).astype(np.uint8)

    @staticmethod
    def unSharpMask(image, alpha=1.5, beta=-0.5, gamma=0):
        """
        Apply an unsharp mask to the image to enhance edges.

        Args:
            image (numpy.ndarray): The input image.
            alpha (float): Weight of the original image.
            beta (float): Weight of the blurred image.
            gamma (float): Scalar added to each sum.

        Returns:
            numpy.ndarray: The image with enhanced edges.
        """
        logger.info("Applying unsharp mask...")
        blurredImg = cv2.GaussianBlur(image, (3, 3), 0)
        return cv2.addWeighted(image, alpha, blurredImg, beta, gamma)

    @staticmethod
    def thresholdImg(image):
        """
        Apply Otsu's thresholding to convert the image to a binary image.

        Args:
            image (numpy.ndarray): The input image.

        Returns:
            numpy.ndarray: The binary image.
        """
        logger.info("Applying thresholding...")
        image_8bit = cv2.convertScaleAbs(image)
        _, img = cv2.threshold(image_8bit, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        return img

    def processImage(self):
        """
        Process the image by applying histogram adjustment, grayscale conversion,
        unsharp masking, and thresholding. Saves the processed image to the original path.

        Returns:
            numpy.ndarray: The processed image.
        """
        try:
            logger.info(f"Processing image: {self.imgPath}")
            self.img = self.histogramAdjustment(self.img)
            self.img = self.grayScaleConverter(self.img)
            self.img = self.unSharpMask(self.img)
            self.img = self.thresholdImg(self.img)
            cv2.imwrite(self.imgPath, self.img)
            logger.info(f"Image processed and saved: {self.imgPath}")
            return self.img
        except Exception as e:
            logger.error(f"Error processing image: {e}")
            raise

# Example usage:
# imagePreprocessor = ImagePreprocesser("path/to/image.jpg")
# processed_image = imagePreprocessor.processImage()
