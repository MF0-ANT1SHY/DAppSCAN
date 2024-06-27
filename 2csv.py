# extract bytecode to csv
import os
import json
import csv
from pathlib import Path


def process_json_files(directory):
    results = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(".json"):
                file_path = os.path.join(root, file)
                with open(file_path, "r") as f:
                    data = json.load(f)
                    if "SWCs" in data:
                        for swc in data["SWCs"]:
                            if swc.get("category") == "SWC-107-Reentrancy":
                                print(swc)
                                results.append(
                                    [
                                        file_path,
                                        swc["category"],
                                        swc.get("sourcePath", ""),
                                    ]
                                )
    return results


def save_to_csv(data, output_file):
    with open(output_file, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["File Name", "Category", "Source Path"])
        writer.writerows(data)


def main():
    directory = "./DAppSCAN-bytecode/SWCbytecode"
    output_file = "2csv.csv"

    results = process_json_files(directory)
    save_to_csv(results, output_file)
    print(f"the result has been saved in {output_file}")


if __name__ == "__main__":
    main()
