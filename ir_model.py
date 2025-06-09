import llvmlite.binding as llvm

class IRModel:
    def __init__(self):
        llvm.initialize()
        llvm.initialize_native_target()
        llvm.initialize_native_asmprinter()
        self.module = None
        self._raw = ""

    def load_ir(self, path: str):
        with open(path, 'r') as f:
            asm = f.read()
        try:
            self.module = llvm.parse_assembly(asm)
            self.module.verify()
        except RuntimeError as e:
            print(f"Warning: failed to parse IR – {e}")
            self.module = None
        self._raw = asm

    def text(self) -> str:
        return self._raw

    def functions(self):
        funcs = []
        for i, line in enumerate(self._raw.splitlines()):
            if line.startswith("define "):
                name = line.split('@')[1].split('(')[0]
                funcs.append((name, i))
        return funcs

    def globals(self):
        globals = []
        for i, line in enumerate(self._raw.splitlines()):
            if line.startswith("@") and "=" in line:
                name = line.split()[0]
                globals.append((name, i))
        return globals

    def symbols(self):
        return {
            "Functions": self.functions(),
            "Globals": self.globals(),
        }