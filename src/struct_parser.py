import re
from pathlib import Path
from textwrap import dedent

TYPE_MAPPING = {
    "address": "str",
    "uint256": "int",
    "uint8": "int",
    "bytes32": "str",
    "bytes": "bytes",
    "bool": "bool",
    "payable": "str",
    "uint120": "int",
    "bytes": "str"
}


def parse_struct_definitions(filepath: Path):
    with open(filepath, "r") as f:
        file_content = f.read()
    print(file_content)

    struct_pattern = r"struct\s+(\w+)\s*\{([\s\S]*?)\}"
    struct_defs = re.findall(struct_pattern, file_content)
    print(struct_defs)
    ret: dict[str,list[tuple[str,str]]] = {}

    for name, fields_str in struct_defs:
        TYPE_MAPPING[name] = name
        ret[name] = parse_fields(fields_str)
    return ret


def escape_list(s) -> str:
    print(s)
    if s.endswith("[]"):
        stripped_type = s[:-2]
        subtype = TYPE_MAPPING.get(stripped_type, stripped_type)
        return escape_list('List[' + subtype + ']')
    return TYPE_MAPPING.get(s, s)

def parse_fields(fields_str: str) -> list[tuple[str, str]]:
    field_pattern = r"([\w\[\]]+)\s+(\w+);"
    return re.findall(field_pattern, fields_str)


def map_type(solidity_type:str) -> str:
    return escape_list(solidity_type)


def to_python_dataclasses(structs: dict[str, list[tuple[str, str]]]):
    output = []
    for name, fields in structs.items():
        field_str = "\n    ".join([f"{fname}: {map_type(ftype)}" for ftype, fname in fields])
        dataclass_str = dedent(
            f"""
@dataclass
class {name}:
    {field_str}
"""
        )
        output.append(dataclass_str.strip())

    return "\n\n".join(output)


def main():
    input_file = Path("src/structs.sol")  # Replace with your input file path
    structs = parse_struct_definitions(input_file)
    dataclasses_str = to_python_dataclasses(structs)

    output_file = Path("output.py")  # Replace with your desired output file path
    with open(output_file, "w") as f:
        f.write(dataclasses_str)


if __name__ == "__main__":
    main()
