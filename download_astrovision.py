"""Script for downloading AstroVision datasets from Hugging Face.

Author: Travis Driver
"""

import sys
import os
import json
from pathlib import Path

import argparse
import zipfile

from huggingface_hub import hf_hub_download


DEFAULT_DATA_ROOT = str(Path(__file__).resolve().parent / "data")


def unzip_file(in_path: str, out_dirpath: str) -> None:
    """Unzips the file at `in_path` to the directory specified in `dirpath`"""
    with zipfile.ZipFile(in_path, "r") as zip_ref:
        sys.stdout.write(f"\rUnzipping {in_path}...")
        zip_ref.extractall(out_dirpath)
        sys.stdout.write(f"\rUnzipping {in_path}... Done.\n")
        sys.stdout.flush()


def main(argv: None = None) -> None:  # pylint: disable=unused-argument
    """Program entrance."""
    # Parse arguments.
    parser = argparse.ArgumentParser("Download AstroVision datasets.")
    parser.add_argument("--local_dir", type=str, default=DEFAULT_DATA_ROOT, help="Path where data will be saved.")
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
    args = parser.parse_args()

    # Initialize download URLs.
    dataset_urls_dict = {}
    if args.test:  # download testing data
        download_root = ""
        with open(os.path.join("lists", "test.json")) as fin:
            dataset_urls_dict = json.load(fin)
    elif args.train:  # download training data
        download_root = ""
        with open(os.path.join("lists", "train.json")) as fin:
            dataset_urls_dict = json.load(fin)
    elif args.clusters:  # download clusters
        download_root = "clusters"
        with open(os.path.join("lists", "clusters.json")) as fin:
            dataset_urls_dict = json.load(fin)
        if args.dataset_name is not None:
            train_clusters = {"train/" + args.dataset_name: dataset_urls_dict["train"][args.dataset_name]}
            test_clusters = {"test/" + args.dataset_name: dataset_urls_dict["test"][args.dataset_name]}
            dataset_urls_dict = {**train_clusters, **test_clusters}
            if args.cluster_name is not None:
                if args.cluster_name in train_clusters["train/" + args.dataset_name]:
                    dataset_urls_dict = {"train/" + args.dataset_name: [args.cluster_name]}
                elif args.cluster_name in test_clusters["test/" + args.dataset_name]:
                    dataset_urls_dict = {"test/" + args.dataset_name: [args.cluster_name]}
                else:
                    raise ValueError(f"No cluster with name {args.cluster_name} exists in {args.dataset_name}.")
        else:  # download all clusters
            train_clusters = {"train/" + dname: clusters for (dname, clusters) in dataset_urls_dict["train"].items()}
            test_clusters = {"test/" + dname: clusters for (dname, clusters) in dataset_urls_dict["test"].items()}
            dataset_urls_dict = {**train_clusters, **test_clusters}
    elif args.segments:  # download segments
        download_root = "segments"
        with open(os.path.join("lists", "segments.json")) as fin:
            dataset_urls_dict = json.load(fin)
        if args.dataset_name is not None:
            if args.dataset_name not in dataset_urls_dict:
                raise ValueError(
                    f"No dataset with name {args.dataset_name}. See lists/segments.json for available datasets."
                )
            dataset_urls_dict = {args.dataset_name: dataset_urls_dict[args.dataset_name]}
            if args.segment_name is not None:
                if args.segment_name in dataset_urls_dict[args.dataset_name]:
                    dataset_urls_dict = {args.dataset_name: [args.segment_name]}
                else:
                    raise ValueError(f"No segment with name {args.segment_name} exists in {args.dataset_name}.")

    # Loop through URLs and download.
    os.makedirs(args.local_dir, exist_ok=True)
    for dataset_name, segment_names in dataset_urls_dict.items():
        for sname in segment_names:
            fpath = os.path.join(download_root, dataset_name, sname + ".zip")
            hf_hub_download(
                repo_id="travisdriver/astrovision-data",
                filename=fpath,
                repo_type="dataset",
                local_dir=args.local_dir,
                local_dir_use_symlinks=False,
            )
            if not args.unpack_off:
                unzip_file(os.path.join(args.local_dir, fpath), os.path.dirname(os.path.join(args.local_dir, fpath)))


if __name__ == "__main__":
    main()
