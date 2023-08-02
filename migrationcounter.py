import json


def fileMigrationCounter(jsonFilePath, outputFilePath):
    try:
        with open(jsonFilePath, "r") as documents_json:
            try:
                documents_read = json.load(documents_json)
            except:
                print(f"Error: {jsonFilePath} is empty or not formatted correctly :(")
                return

    except FileNotFoundError as e:
        print(e)
        return

    all_files_and_keys = {}

    for file in documents_read["data"]:
        document_format = str(file["asset"]["documentFormat"])
        filename = str(file["filename"])

        all_files_and_keys.setdefault(document_format, []).append(filename)

    with open(outputFilePath, "w") as outfile:
        for doc_type, filenames in all_files_and_keys.items():
            doc_type_count = len(filenames)
            outfile.write(f"Number of {doc_type} documents: {doc_type_count}\n")
            outfile.write(f"\tAll {doc_type} files:\n")
            for file_name in filenames:
                outfile.write(f"\t\t{file_name}\n")
            outfile.write("\n**********************************\n\n")
