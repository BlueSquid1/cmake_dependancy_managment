#!/usr/bin/python3

import os
import argparse
import tarfile
import json
import hashlib

import config

def parse_arguements():
     parser = argparse.ArgumentParser()
     parser.add_argument("artifactName", type=str)
     parser.add_argument("artifactLocation", type=str)
     parser.add_argument("artifactDestination", type=str)
     parser.add_argument("artifactVersion", type=str)
     return parser.parse_args()

def main():
    args = parse_arguements()

    # Make path to artifact repository if needed
    outputFolder = os.path.join(config.repositoryPath, args.artifactDestination, args.artifactName, args.artifactVersion)
    os.makedirs(outputFolder, exist_ok=True)

    # Tar artifact to be uploaded
    artifactFileName = args.artifactName + ".tgz"
    artifactFilePath = os.path.join(outputFolder, artifactFileName)
    print("uploading artifact to: " + str(artifactFilePath) + " from source: " + str(args.artifactLocation))
    with tarfile.open(artifactFilePath, "w:gz") as tar:
        tar.add(args.artifactLocation, arcname=os.path.sep)

    # Calculate Sha1Sum
    bufferSize = 0x10000
    sha1 = hashlib.sha1()
    with open(artifactFilePath, 'rb') as f:
        data = f.read(bufferSize)
        while data:
            sha1.update(data)
            data = f.read(bufferSize)
    has1sum = sha1.hexdigest()
    # Generate metadata file
    jsonMeta = {
                    'name' : artifactFileName,
                    'version' : args.artifactVersion,
                    'path' : args.artifactDestination,
                    'sha1sum' : has1sum
                }
    print("artifact metadata is: " + str(jsonMeta))
    metadataFilePath = os.path.join(outputFolder, "pom.json")
    with open(metadataFilePath, 'w') as f:
        json.dump(jsonMeta, f, sort_keys=True, indent=4)

if __name__ == "__main__":
    main()