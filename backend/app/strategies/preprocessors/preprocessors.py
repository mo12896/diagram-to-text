import cv2
from app.models.diagram_entities import Image
from loguru import logger

from .base import ImagePreprocessors

# Configure logger
logger.add("preprocessors_logs.log", rotation="1 day", compression="zip")


class GrayscalePreprocessor:
    """Converts an image to grayscale."""

    def __call__(self, image: Image) -> Image:
        """Convert the given image to grayscale asynchronously.

        Args:
            image (Image): The original image.

        Returns:
            Image: Grayscale image.
        """
        try:
            gray_image = cv2.cvtColor(image.content, cv2.COLOR_BGR2GRAY)
            return Image(content=gray_image)
        except Exception as e:
            logger.error(f"Grayscale conversion failed: {e}")
            raise


class AdaptiveThresholdPreprocessor:
    """Applies adaptive thresholding to an image."""

    def __call__(self, image: Image) -> Image:
        """Apply adaptive thresholding to the given image asynchronously.

        Args:
            image (Image): The original image.

        Returns:
            Image: Thresholded image.
        """
        try:
            thresholded_image = cv2.adaptiveThreshold(
                image.content,
                255,
                cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                cv2.THRESH_BINARY,
                11,
                2,
            )
            return Image(content=thresholded_image)
        except Exception as e:
            logger.error(f"Adaptive thresholding failed: {e}")
            raise


def main(image_path: str):
    """Main asynchronous function to preprocess an image.

    Args:
        image_path (str): Path to the input image.
    """
    image_content = cv2.imread(image_path)
    image = Image(content=image_content)

    # Initialize the preprocessors
    preprocessors = [
        GrayscalePreprocessor(),
        AdaptiveThresholdPreprocessor(),
    ]
    image_preprocessors = ImagePreprocessors(steps=preprocessors)
    result_image = image_preprocessors.preprocess_image(image)

    # Save the result image
    cv2.imwrite("result.jpg", result_image.content)


# Use asyncio to run the main function.
if __name__ == "__main__":
    main("/home/moritz/Workspace/diagram2text/artifacts/mermaid_diagram.png")
