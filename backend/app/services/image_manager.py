from dataclasses import dataclass
from pathlib import Path

import aiofiles
from loguru import logger
from werkzeug.utils import secure_filename

# Configure logger
logger.add("file_manager_logs.log", rotation="1 day", compression="zip")


@dataclass
class ImageMetadata:
    """
    A dataclass representing metadata of the stored file.

    Attributes:
    - filename: The name of the file.
    - filepath: The full path to the file on the server.
    """

    filename: str
    filepath: Path


class ImageManager:
    # Define the upload folder and allowed extensions
    UPLOAD_FOLDER = Path("app/static/uploads")
    ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg"}

    @staticmethod
    def allowed_file(filename: str) -> bool:
        """
        Check if the file has an allowed extension.

        :param filename: Name of the file.
        :return: Boolean indicating if file extension is allowed.
        """
        return (
            "." in filename
            and filename.rsplit(".", 1)[1].lower() in ImageManager.ALLOWED_EXTENSIONS
        )

    @staticmethod
    async def save_file(image) -> ImageMetadata:
        """
        Asynchronously save the uploaded file to the server.

        :param file: The uploaded file object from Flask.
        :return: Metadata of the saved file.
        """
        if image and ImageManager.allowed_file(image.filename):
            filename = secure_filename(image.filename)
            file_path = ImageManager.UPLOAD_FOLDER / filename

            # Asynchronously save the file
            async with aiofiles.open(file_path, "wb") as f:
                await f.write(image.read())

            logger.info(f"File {filename} saved to {file_path}.")
            return ImageMetadata(filename, file_path)
        else:
            logger.error("Invalid file type")
            raise ValueError("Invalid file type")

    @staticmethod
    async def delete_file(filepath: Path):
        """
        Asynchronously delete a file from the server.

        :param filepath: The path to the file to be deleted.
        """
        if filepath.exists():
            await aiofiles.os.remove(filepath)
            logger.info(f"File {filepath} deleted.")
        else:
            logger.warning(f"File {filepath} not found. Skipping deletion.")
