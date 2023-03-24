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
}

def parse_enum_definitions(filepath: Path):
    with open(filepath, "r") as f:
        file_content = f.read()

    enum_pattern = r"enum\s+(\w+)\s*{([\s\S]*?)}"
    enum_defs = re.findall(enum_pattern, file_content)

    return {name: parse_enum_members(members_str) for name, members_str in enum_defs}

def parse_enum_members(members_str: str):
    field_pattern = r"\n\s+(\w+),?"
    members = re.findall(field_pattern, members_str)
    return [(member.strip(), i) for i, member in enumerate(members)]

def to_python_enums(enums):
    output = []
    for name, members in enums.items():
        members_str = ",\n    ".join(f'{member} = {i}' for member, i in members)
        enum_str = dedent(
            f"""
class {name}(Enum):
    {members_str}
"""
        )
        output.append(enum_str.strip())

    return "\n\n".join(output)

# The previous functions for structs remain unchanged

def main():
    input_file = Path("src/enums.sol")  # Replace with your input file path
    
    enums = parse_enum_definitions(input_file)
    enums_str = to_python_enums(enums)

    output_file = Path("output.py")  # Replace with your desired output file path
    with open(output_file, "w") as f:
        f.write(f"{enums_str}")

if __name__ == "__main__":
    main()
