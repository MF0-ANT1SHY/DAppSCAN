import os
import json
import csv


def process_csv(input_csv_path, output_csv_path, dict_dir, output_dir):
    # 读取CSV文件
    with open(input_csv_path, "r") as csvfile:
        reader = csv.DictReader(csvfile)
        rows = list(reader)
        fieldnames = reader.fieldnames

    # 处理每一行数据
    for row in rows:
        file_name = row["File Name"].split("/")[-1]
        source_path = (
            row["Source Path"].split("rce/contracts/")[-1]
            if "rce/contracts/" in row["Source Path"]
            else row["Source Path"]
        )

        # 在dict目录中查找对应的文件
        json_file = find_file(dict_dir, file_name)
        # print(f"Processing {json_file}...")
        if json_file:
            with open(json_file, "r") as f:
                data = json.load(f)

            # 遍历contracts字段
            for contract_name, contract_data in data.get("contracts", {}).items():
                if source_path in contract_name:
                    bin_runtime = contract_data.get("bin-runtime", "")
                    if bin_runtime:
                        # 创建以SourcePath命名的.code文件
                        code_file_name = f"{source_path}.code".split("/")[-1]
                        code_file_path = os.path.join(output_dir, code_file_name)

                        # 确保输出目录存在
                        os.makedirs(os.path.dirname(code_file_path), exist_ok=True)

                        # 将bin-runtime内容写入.code文件
                        with open(code_file_path, "w") as code_file:
                            code_file.write(bin_runtime)

                        print(f"Created {code_file_path}")
                    break
        else:
            print(f"Could not find {file_name} in {dict_dir}")


def find_file(directory, filename):
    for root, dirs, files in os.walk(directory):
        if filename in files:
            return os.path.join(root, filename)
    return None


# 使用示例
dict_directory = "./DAppSCAN-bytecode/bytecode"  # 指定目录
input_csv_file = "2csv.csv"  # 输入CSV文件名
output_csv_file = "processed_test.csv"  # 输出CSV文件名
output_directory = "./bytecode"

process_csv(input_csv_file, output_csv_file, dict_directory, output_directory)
