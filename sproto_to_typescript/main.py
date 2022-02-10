import re
import os


def transferSprotoToTypeScript(file_name, name):
    namespace = name + "Struct"
    output_name = namespace + ".ts"
    output_data = []
    mapping_data = {}

    # 前言


    output_data.append("namespace " + namespace + "\n")
    output_data.append("{\n")
    with open(file_name, "r", encoding="utf-8") as f:
        line = f.readline()
        while line:
            line = line.replace("\n", "")
            if len(line) > 0:
                value = ""
                if line[0] == ".":
                    line = line.replace(".", "export type ")
                    line = line.replace("{", " ={")
                elif line[0] != "\t" and line[0] != "}" and line[0] != "#" and line[0] != " ":
                    value = re.match("[^ ]+", line).group()
                    line = "export namespace " + line

                r1 = re.findall(" +\d+ *", line)
                if len(r1) > 0:
                    print(line)
                    print(line[line.index(r1[0])])
                    line = line.replace(r1[0], "")
                    if value != "":
                        mapping_data[r1[0].strip()] = value

                line = line.replace("*integer", "number[]")

                line = line.replace("integer", "number")
                line = line.replace("request", "export type request = ")
                line = line.replace("response", "export type response = ")
                if line.find("*") >= 0:
                    line = line.replace("*", namespace + ".")
                    line = line + "[]"
                if line.find("#") >= 0:
                    line = line.replace("#", "/**")
                    line = line + "*/"

                # print(line)
                output_data.append(line + "\n")
            line = f.readline()

    output_data.append("\texport let mapping = {\n")
    i = 0
    for k in mapping_data:
        if i == 0:
            output_data.append("\t\t\"" + k + "\":\"" + mapping_data[k] + "\"\n")
            i = i + 1
        else:
            output_data.append("\t\t,\"" + k + "\":\"" + mapping_data[k] + "\"\n")

    output_data.append("\t}\n")

    output_data.append("}")

    try:
        os.remove(output_name)
    except OSError as e:
        print(e)
    else:
        print("File is deleted successfully")

    with open(output_name, "a", encoding="utf-8") as f:
        f.writelines(output_data)

    with open("Proto.ts", "a", encoding="utf-8") as f:
        output_data = []
        # 前言

        output_data.append("class " + name + "ProtoType{\n")
        for k in mapping_data:
            output_data.append("\tpublic static readonly " + mapping_data[k] + ":number=" + k + ";\n")
        output_data.append("}\n")

        output_data.append("class " + name + "ProtoInterface{\n")
        for k in mapping_data:
            output_data.append(
                "\tpublic call" + mapping_data[k] + "(result:" + namespace + "." + mapping_data[
                    k] + ".response){console.log(\"call" + mapping_data[k] + " do nothing\")}\n")
        output_data.append("}\n")
        f.writelines(output_data)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    try:
        os.remove("Proto.ts")
    except OSError as e:
        print(e)
    else:
        print("File is deleted successfully")

    transferSprotoToTypeScript("login.sproto", "Login")
