"""Script for downloading AstroVision datasets.

Adapted from https://raw.githubusercontent.com/IntelVCL/TanksAndTemples/master/python_toolbox/download_t2_dataset.py

Author: Travis Driver
"""

import sys
import os
import json
import requests

import argparse
import zipfile
import hashlib

CHUNK_SIZE = 32768


def download_file_from_dropbox(url: str, destination: str) -> None:
    """Downloads the file from `url` into the file path specified by `destination`."""
    response = requests.get(url, stream=True)
    if not os.path.exists(os.path.dirname(destination)):
        os.makedirs(os.path.dirname(destination))
    total_filesize = 0
    with open(destination, "wb") as f:
        for chunk in response.iter_content(CHUNK_SIZE):
            if chunk:  # filter out keep-alive new chunks
                f.write(chunk)
                total_filesize += CHUNK_SIZE
                sys.stdout.write("\r%5.0f MB downloaded" % (float(total_filesize) / 1000000))
                sys.stdout.flush()
    sys.stdout.write(f"\rDownload complete to {destination}.\n")
    sys.stdout.flush()


def unzip_file(in_path: str, out_dirpath: str) -> None:
    """Unzips the file at `in_path` to the directory specified in `dirpath`"""
    with zipfile.ZipFile(in_path, "r") as zip_ref:
        sys.stdout.write(f"\rUnzipping {in_path}...")
        zip_ref.extractall(out_dirpath)
        sys.stdout.write(f"\rUnzipping {in_path}... Done.\n")
        sys.stdout.flush()


def generate_file_md5(fpath: str, blocksize: int = 2 ** 20) -> str:
    """Calculates MD5 checksum for the input file, which is used to verify that the file was properly downloaded"""
    m = hashlib.md5()
    with open(fpath, "rb") as f:
        while True:
            buf = f.read(blocksize)
            if not buf:
                break
            m.update(buf)
    return m.hexdigest()


def main(argv: None = None) -> None:  # pylint: disable=unused-argument
    """Program entrance."""
    # Parse arguments.
    parser = argparse.ArgumentParser("Download AstroVision datasets.")
    parser.add_argument("--test", action="store_true", help="Download test clusters.")
    parser.add_argument("--train", action="store_true", help="Download train clusters.")
    parser.add_argument(
        "--clusters", action="store_true", help="Download clusters (see lists/clusters.json for valid cluster names)."
    )
    parser.add_argument(
        "--segments", action="store_true", help="Download segments (see lists/segments.json for valid segment names)."
    )
    parser.add_argument(
        "--dataset_name", type=str, default=None, help="Name of dataset to download (e.g., `dawn_vesta`)."
    )
    parser.add_argument(
        "--segment_name", type=str, default=None, help="Name of segment to download (e.g., `2011205_rc3`)."
    )
    parser.add_argument(
        "--cluster_name", type=str, default=None, help="Name of cluster to download (e.g., `00000007`)."
    )
    parser.add_argument("--unpack_off", action="store_true", help="Do not un-zip the folders after download.")
    parser.add_argument("--calc_md5_off", action="store_true", help="Do not calculate md5sum after download.")
    args = parser.parse_args()

    # Read in MD5 checksums.
    if not args.calc_md5_off:
        with open(os.path.join("lists", "md5.json")) as fin:
            md5_checksums = json.load(fin)

    os.makedirs("data", exist_ok=True)

    # Initialize download URLs.
    dataset_urls_dict = {}
    if args.test:  # download testing data
        download_root = os.path.join("data", "test")
        os.makedirs(download_root, exist_ok=True)
        with open(os.path.join("lists", "test.json")) as fin:
            dataset_urls_dict = json.load(fin)
    elif args.train:  # download training data
        download_root = os.path.join("data", "train")
        os.makedirs(download_root, exist_ok=True)
        with open(os.path.join("lists", "train.json")) as fin:
            dataset_urls_dict = json.load(fin)
    elif args.clusters:  # download clusters
        download_root = os.path.join("data", "clusters")
        os.makedirs(download_root, exist_ok=True)
        with open(os.path.join("lists", "clusters.json")) as fin:
            dataset_urls_dict = json.load(fin)
        if args.dataset_name is not None:
            dataset_urls_dict = {args.dataset_name: dataset_urls_dict[args.dataset_name]}
            if args.cluster_name is not None:
                dataset_urls_dict = {
                    args.dataset_name: {args.cluster_name: dataset_urls_dict[args.dataset_name][args.cluster_name]}
                }
    elif args.segments:  # download segments
        download_root = os.path.join("data", "segments")
        os.makedirs(download_root, exist_ok=True)
        with open(os.path.join("lists", "segments.json")) as fin:
            dataset_urls_dict = json.load(fin)
        if args.dataset_name is not None:
            dataset_urls_dict = {args.dataset_name: dataset_urls_dict[args.dataset_name]}
            if args.segment_name is not None:
                dataset_urls_dict = {
                    args.dataset_name: {args.segment_name: dataset_urls_dict[args.dataset_name][args.segment_name]}
                }

    # Loop through URLs and download.
    for dataset_name, segment_urls in dataset_urls_dict.items():
        dataset_root = os.path.join(download_root, dataset_name)
        os.makedirs(dataset_root, exist_ok=True)
        for segment_name, url in segment_urls.items():
            download_file_from_dropbox(url, os.path.join(dataset_root, segment_name + ".zip"))
            md5_tmp = generate_file_md5(os.path.join(dataset_root, segment_name + ".zip"))
            print(f"File checksum: {md5_tmp}")
            if not args.calc_md5_off:
                assert md5_tmp == md5_checksums[dataset_name][segment_name]
            if not args.unpack_off:
                unzip_file(os.path.join(dataset_root, segment_name + ".zip"), dataset_root)


if __name__ == "__main__":
    main()
