from typing import List, Protocol

from ...models.diagram_entities import Image


class ImagePreprocessor(Protocol):
    def __call__(self, image: Image) -> Image:
        """
        Preprocess the image.

        Args:
            image (cv2.cv2): Image to preprocess

        Returns:
            cv2.cv2: Preprocessed image
        """
        ...


class ImagePreprocessors:
    def __init__(self, steps: List[ImagePreprocessor]):
        """Constructor for the ImagePreprocessor class.

        Args:
            steps (list[ImagePreProcessor]): List of preprocessing steps
        """
        self.steps = steps

    def preprocess_image(self, image: Image) -> Image:
        """Pipeline for preprocessing the image.

        Args:
            image (cv2.cv2): Image to preprocess

        Returns:
            cv2.cv2: Preprocessed image
        """
        for step in self.steps:
            image = step(image)
        return image
