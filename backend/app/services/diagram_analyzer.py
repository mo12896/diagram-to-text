from pathlib import Path
from typing import List

import cv2
from loguru import logger

from ..strategies import RelationshipCalculator
from ..strategies.detectors.base import FeatureDetector, FeatureDetectors
from ..strategies.preprocessors.base import ImagePreprocessor, ImagePreprocessors


class DiagramAnalyzer:
    """
    The main class to analyze diagrams.

    Methods:
        analyze: Process and analyze an input diagram.
    """

    def __init__(
        self,
        preprocessors: List[ImagePreprocessor],
        detectors: List[FeatureDetector],
        relationship_calculator: RelationshipCalculator,
    ):
        """
        Initialize the DiagramAnalyzer.

        Args:
            preprocessors: A list of preprocessing strategies.
            detectors: A list of feature detection strategies.
            relationship_calculator: A strategy to calculate relationships between features.
            img_processor: A pipeline of preprocessing strategies.
            feature_detector: A pipeline of feature detection strategies.
        """
        self.preprocessors = preprocessors
        self.detectors = detectors
        self.relationship_calculator = relationship_calculator
        self.img_processor = ImagePreprocessors(steps=self.preprocessors)
        self.feature_detector = FeatureDetectors(steps=self.detectors)

    async def analyze(self, image_path: Path) -> dict:
        """
        Analyze a given diagram image.

        Args:
            image_path: Path to the image file.

        Returns:
            A tuple of the processed image and a list of detected features.
        """
        try:
            original_image = cv2.imread(str(image_path))
            if original_image is None:
                logger.error(f"Failed to load image from {image_path}")
                return

            processed_image = self.img_processor.preprocess_image(original_image)
            features = self.feature_detector.detect_features(processed_image)
            relationships = self.relationship_calculator.calculate(features)

            return relationships

        except Exception as e:
            logger.error(f"An error occurred: {e}")
            raise


if __name__ == "__main__":
    # Usage
    preprocessors = [GrayscalePreprocessor(), AdaptiveThresholdPreprocessor()]

    detectors = [
        TesseractTextDetector(),
        SimpleBoxDetector(),
        HoughTransformArrowDetector(),
    ]

    relationship_calculator = RelationshipCalculator()

    analyzer = DiagramAnalyzer(preprocessors, detectors, relationship_calculator)
    image_path = Path("path_to_image.jpg")
    processed_image, relationships = analyzer.analyze(image_path)
