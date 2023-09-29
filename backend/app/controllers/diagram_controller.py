from app.services.diagram_analyzer import DiagramAnalyzer
from app.services.image_manager import ImageManager
from app.strategies import RelationshipCalculator
from app.strategies.detectors import (
    HoughTransformArrowDetector,
    SimpleBoxDetector,
    TesseractTextDetector,
)
from app.strategies.preprocessors import (
    AdaptiveThresholdPreprocessor,
    GrayscalePreprocessor,
)
from flask import Blueprint, jsonify, request, send_from_directory

# Define blueprint
diagram_bp = Blueprint("diagram", __name__)

# TODO: The specific data processors should later the put by the client!
# Instantiate your preprocessors, detectors, and relationship calculator
preprocessors = [GrayscalePreprocessor(), AdaptiveThresholdPreprocessor()]
detectors = [
    TesseractTextDetector(),
    SimpleBoxDetector(),
    HoughTransformArrowDetector(),
]
relationship_calculator = RelationshipCalculator()

# Instantiate the diagram analyzer with the above strategies
analyzer = DiagramAnalyzer(preprocessors, detectors, relationship_calculator)


@diagram_bp.route("/analyze_diagram", methods=["POST"])
def analyze_diagram():
    """
    Endpoint to analyze a diagram. It expects a file upload with the name 'diagram'.
    Returns a JSON representation of the AnalysisResult.
    """
    try:
        # Get the uploaded diagram file
        image_file = request.files.get("diagram")
        if not image_file:
            return jsonify({"error": "No file provided"}), 400

        # Save the uploaded file using the ImageManager
        image_metadata = ImageManager.save_file(image_file)

        # Analyze the saved image
        result = analyzer.analyze(image_metadata.filepath)

        # Cleanup: Optionally delete the image from the server after processing
        ImageManager.delete_file(image_metadata.filepath)

        return jsonify(result), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@diagram_bp.route("/uploads/<filename>")
def uploaded_file(filename):
    """
    Endpoint to retrieve uploaded files. This can be useful if you want to show the uploaded image back to the user.
    """
    return send_from_directory(ImageManager.UPLOAD_FOLDER, filename)
