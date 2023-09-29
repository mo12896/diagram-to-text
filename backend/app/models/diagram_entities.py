from dataclasses import dataclass
from typing import List

import numpy as np


@dataclass
class Image:
    """Image dataclass to represent an image with its content.

    Attributes:
    - content: The image content represented as a numpy array.
    """

    content: np.ndarray


@dataclass
class Point:
    """Represents a point in 2D space.

    Attributes:
    - x: x-coordinate of the point.
    - y: y-coordinate of the point.
    """

    x: float
    y: float


@dataclass
class Rectangle:
    """Represents a rectangle using top-left and bottom-right points.

    Attributes:
    - top_left: Top-left corner of the rectangle.
    - bottom_right: Bottom-right corner of the rectangle.
    """

    top_left: Point
    bottom_right: Point


@dataclass
class TextBlock:
    """Represents a block of text and its location in a diagram.

    Attributes:
    - text: The actual text content.
    - coordinates: The bounding rectangle of the text block.
    """

    text: str
    coordinates: Rectangle


@dataclass
class Arrow:
    """Represents an arrow using starting and ending points.

    Attributes:
    - start: The starting point of the arrow.
    - end: The end point of the arrow.
    """

    start: Point
    end: Point


@dataclass
class Relationship:
    """Represents a relationship between two entities (typically boxes) in a diagram.

    Attributes:
    - source: The source entity of the relationship.
    - destination: The destination entity of the relationship.
    """

    source: Rectangle
    destination: Rectangle


@dataclass
class AnalysisResult:
    """Encapsulates the result of a diagram analysis.

    Attributes:
    - texts: List of detected text blocks.
    - boxes: List of detected rectangles (or boxes).
    - arrows: List of detected arrows.
    - relationships: List of detected relationships.
    """

    texts: List[TextBlock]
    boxes: List[Rectangle]
    arrows: List[Arrow]
    relationships: List[Relationship]
