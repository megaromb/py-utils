import argparse
import glob
import logging
import os
import shutil
from pathlib import Path

import common

LOGGER_NAME = common.get_file_name_without_ext(__file__)
DESCRIPTION = \
    "Copies files defined by a pattern from source to destination directory. In case of file name collision, " \
    "both files are placed in destination directory and renamed using the tags provided "


class CmdOptions:

    def __init__(self, args):
        self.src_dir: str = args.src_dir
        self.dst_dir: str = args.dst_dir
        self.src_tag: str = args.src_tag
        self.file_pattern: str = args.file_pattern
        self.src_tag_all: bool = args.src_tag_all

    def __str__(self):
        return f"src_dir: '{self.src_dir}', "\
               f"dst_dir: '{self.dst_dir}', "\
               f"src_tag: '{self.src_tag}', "\
               f"file_pattern: '{self.file_pattern}', "\
               f"src_tag_all: '{self.src_tag_all}'"

    @staticmethod
    def parse():
        parser = argparse.ArgumentParser(description=DESCRIPTION)
        parser.add_argument(
            "--src-dir",
            required=True,
            help="Source directory to copy files from")
        parser.add_argument(
            "--dst-dir",
            required=True,
            help="Destination directory to copy files to")
        parser.add_argument(
            "--src-tag",
            required=True,
            help="Suffix used to rename source file when there is file with the same name in a destination directory")
        parser.add_argument(
            "--file-pattern",
            default="*.*",
            help="Pattern to filter files to copy")
        parser.add_argument(
            "--src-tag-all",
            type=bool,
            default=True,
            help="If True, means tagging all source files")
        return CmdOptions(parser.parse_args())


def tag_file_name(file_name: str, tag: str):
    file_name_without_ext = Path(file_name).stem
    _, file_ext = os.path.splitext(file_name)
    return f"{file_name_without_ext}-{tag}{file_ext}"


def copy(cmd_options: CmdOptions, logger: logging.Logger):
    separator = "" if cmd_options.src_dir.endswith("/") else "/"
    src_file_list = glob.glob(f"{cmd_options.src_dir}{separator}{cmd_options.file_pattern}", recursive=False)
    logger.info(f"{len(src_file_list)} files found in '{cmd_options.src_dir}' directory")

    for src_file_path in src_file_list:
        _, file_name = os.path.split(src_file_path)
        dst_file_path = os.path.join(cmd_options.dst_dir, file_name)
        logger.info(f"'{file_name}': copying started ...")

        if os.path.exists(dst_file_path):
            logger.warning(f"file with '{file_name}' name already exists in target directory")
            dst_file_size = os.path.getsize(dst_file_path)
            src_file_size = os.path.getsize(src_file_path)
            if dst_file_size == src_file_size:
                logger.warning(f"files are of the same size ({src_file_size:,d} bytes). skipping.")
                continue

            new_file_name = tag_file_name(file_name, cmd_options.src_tag)
            os.rename(dst_file_path, os.path.join(cmd_options.dst_dir, new_file_name))
            logger.warning(f"existing '{file_name}' file was renamed to '{new_file_name}'")

        shutil.copy(src_file_path, dst_file_path)
        logger.info(f"'{file_name}': copying completed.")


def main():
    cmd_options = CmdOptions.parse()
    logger = common.init_logger(LOGGER_NAME)
    logger.info(DESCRIPTION)
    logger.info(f"cmd_options: {cmd_options}")
    copy(cmd_options, logger)


if __name__ == "__main__":
    main()
