#!/usr/bin/python3

import sys
import os
import argparse
import tarfile

import config

def parse_arguements():
     parser = argparse.ArgumentParser()
     parser.add_argument("artifactName", type=str)
     parser.add_argument("artifactLocation", type=str)
     parser.add_argument("artifactVersion", type=str)
     parser.add_argument("unpackDestination", type=str)
     return parser.parse_args()

def main():
    args = parse_arguements()

    # Check if there is an artifact that matches the arguements
    artifactPath = os.path.join(config.repositoryPath, args.artifactLocation, args.artifactName, args.artifactVersion)
    artifactFileName = args.artifactName + ".tgz"
    artifactFilePath = os.path.join(artifactPath, artifactFileName)

    archive_exists = tarfile.is_tarfile(artifactFilePath)
    if not archive_exists:
        print("can't find archive at path: " + artifactFilePath)
        sys.exit(1)

    # Make the staging area if needed
    os.makedirs(args.unpackDestination, exist_ok=True)

    # Extract arifact to this folder
    print("extracting artifact from: " + str(artifactFilePath) + " to: " + args.unpackDestination)
    with tarfile.open(artifactFilePath, 'r') as tar:
        tar.extractall(args.unpackDestination)

if __name__ == "__main__":
    main()