import argparse
import asyncio
import logging
import shutil
from pathlib import Path

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

logger = logging.getLogger(__name__)


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Asynchronously sort files from a source folder "
            "into subfolders by file extension."
        )
    )

    parser.add_argument(
        "source",
        type=Path,
        help="Path to the source folder",
    )

    parser.add_argument(
        "output",
        type=Path,
        help="Path to the output folder",
    )

    return parser.parse_args()


async def copy_file(file_path: Path, output_folder: Path) -> None:
    try:
        extension = file_path.suffix.lower().lstrip(".")

        if not extension:
            extension = "no_extension"

        destination_folder = output_folder / extension

        await asyncio.to_thread(
            destination_folder.mkdir,
            parents=True,
            exist_ok=True,
        )

        destination_file = destination_folder / file_path.name

        await asyncio.to_thread(
            shutil.copy2,
            file_path,
            destination_file,
        )

        logger.info(
            "Copied: %s -> %s",
            file_path,
            destination_file,
        )

    except (OSError, shutil.Error) as error:
        logger.error(
            "Failed to copy %s: %s",
            file_path,
            error,
        )


async def read_folder(
    source_folder: Path,
    output_folder: Path,
) -> None:
    try:
        if not source_folder.exists():
            logger.error(
                "Source folder does not exist: %s",
                source_folder,
            )
            return

        if not source_folder.is_dir():
            logger.error(
                "Source path is not a directory: %s",
                source_folder,
            )
            return

        await asyncio.to_thread(
            output_folder.mkdir,
            parents=True,
            exist_ok=True,
        )

        files = await asyncio.to_thread(
            lambda: [path for path in source_folder.rglob("*") if path.is_file()]
        )

        if not files:
            logger.info(
                "No files found in source folder: %s",
                source_folder,
            )
            return

        logger.info(
            "Found %d file(s). Starting asynchronous copy.",
            len(files),
        )

        tasks = [copy_file(file_path, output_folder) for file_path in files]

        await asyncio.gather(*tasks)

        logger.info(
            "Sorting completed successfully. Output folder: %s",
            output_folder,
        )

    except OSError as error:
        logger.error(
            "Failed to read folder %s: %s",
            source_folder,
            error,
        )


async def main() -> None:
    args = parse_arguments()

    source_folder: Path = args.source.resolve()
    output_folder: Path = args.output.resolve()

    logger.info("Source folder: %s", source_folder)
    logger.info("Output folder: %s", output_folder)

    await read_folder(
        source_folder,
        output_folder,
    )


if __name__ == "__main__":
    asyncio.run(main())
