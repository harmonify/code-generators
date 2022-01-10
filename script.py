import re


class StructureGenerator:
    def __init__(self) -> None:
        self.supportedLangs = self.mapLangs()
        self.input = self.getInputFile()
        self.outputLangs = self.getOutputLangs()
        self.fileName = self.setFileName()
        self.generateOutput()

    def mapLangs(self) -> dict:
        return {
            'ts': self.generateTs,
            'cpp': self.generateCpp,
        }

    def getInputFile(self) -> list[str]:
        with open(input("Enter the input file name: "), 'r') as f:
            print()
            # Remove comments, empty lines and trailing spaces
            return [line.strip() for line in f.readlines() if line.strip() and not line.startswith('#')]

    def getOutputLangs(self) -> list[str]:
        print("Supported languages are:")
        for lang in self.supportedLangs:
            print(f"{lang}")
        print()

        outputLangs = []
        desiredOutputLangs = input(
            "How many languages you want to generate the output to?\n'*' for all supported languages\n: ")

        try:
            if desiredOutputLangs == '*':
                print()
                return self.supportedLangs.keys()
            elif desiredOutputLangs.isdigit():
                for i in range(int(desiredOutputLangs)):
                    outputLangs.append(input(f"Language {i+1}: "))
                print()
                return outputLangs
            else:
                raise ValueError("Unsupported value.")
        except ValueError as e:
            print(e)

    def setFileName(self) -> str:
        return input("Enter the output file name (no suffix): ")
        # return re.split(r'\s+', self.input[0])[1]

    def generateOutput(self) -> None:
        conditions = []
        for lang in self.outputLangs:
            conditions.append(self.supportedLangs[lang]())
        if all(conditions) is True:
            print("The operations was successful.")
        else:
            print("Errors occured.")

    def generateTs(self) -> bool:
        tsTypes = {
            "int": "number",
            "float": "number",
            "double": "number",
            "string": "string",
            "char": "string",
            "char[]": "string",
            "wchar_t": "string",
            "wchar_t[]": "string",
            "bool": "boolean",
            "void": "void"
        }

        with open(f"{self.fileName}.ts", 'w') as f:
            try:
                for line in self.input:
                    if line.startswith('M'):
                        _, structureName = re.split(r'\s+', line)
                        f.write(f"export interface {structureName} {'{'}\n")
                    elif line.startswith('F'):
                        _, fieldName, fieldType = re.split(r'\s+', line)
                        # if fieldType is char({size}) or wchar_t({size}), remove ({size}) and substitute with string
                        if re.search(r'char\(.*\)|wchar_t\(.*\)', fieldType):
                            f.write(f"  {fieldName}: {tsTypes['string']};\n")
                        # if fieldType is array, add [] to the end of the type
                        elif re.match(r'\w+\(.*\)', fieldType):
                            fieldType = re.sub(r'\(.*\)', '', fieldType)
                            f.write(
                                f"  {fieldName}: {tsTypes[fieldType]}[];\n")
                        else:
                            f.write(f"  {fieldName}: {tsTypes[fieldType]};\n")
                    elif line.startswith('E'):
                        f.write(f"{'}'}\n")
                    else:
                        raise ValueError
                return True
            except ValueError as e:
                print(e)
                return False

    def generateCpp(self) -> bool:
        with open(f"{self.fileName}.cpp", 'w') as f:
            try:
                for line in self.input:
                    if line.startswith('M'):
                        _, structureName = re.split(r'\s+', line)
                        f.write('typedef struct {\n')
                    elif line.startswith('F'):
                        _, fieldName, fieldType = re.split(r'\s+', line)
                        f.write(f"  {fieldType} {fieldName};\n")
                    elif line.startswith('E'):
                        f.write(f"{'}'} {structureName};\n")
                    else:
                        raise ValueError("Unsupported values.")
                return True
            except ValueError as e:
                print(e)
                return False


def main(args=None):
    try:
        StructureGenerator()
    except KeyboardInterrupt as e:
        print("\nExiting...")
        exit()


if __name__ == '__main__':
    main()
