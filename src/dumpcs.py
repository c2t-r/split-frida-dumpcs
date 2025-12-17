import re
from dataclasses import dataclass
from pathlib import Path


@dataclass
class Entry:
    namespace: str
    code: str


class Dumpcs:
    """Parser for frida-il2cpp-bridge dump.cs files"""

    path: Path
    code: str
    entries: dict[str, list[Entry]]

    def __init__(self, path: str | Path) -> None:
        self.path = Path(path)
        self.code = ""
        self.entries = {}
        self._load()

    def _load(self) -> None:
        """Load and parse dump.cs file"""
        self.code = self.path.read_text(encoding="utf-8")
        self.code = re.sub(r"// 0x[0-9a-f]{8}", "// 0x00000000", self.code)  # remove address for git diff
        self._parse()
        print(f"Found {len(self.entries)} namespaces\n")

    def _parse(self) -> None:
        """Parse the dump.cs content into entries grouped by namespace"""
        # Original simple pattern: r"//(.+?)\n[\s\S]+?^\}"
        pattern = re.compile(r"^//\s*(.+?)\n([\s\S]+?^\})", re.MULTILINE)

        for match in pattern.finditer(self.code):
            namespace = match.group(1).strip()
            code = match.group(2)

            entry = Entry(
                namespace=namespace,
                code=code,
            )

            if namespace not in self.entries:
                self.entries[namespace] = []
            self.entries[namespace].append(entry)

    def split(self, output_dir: str | Path) -> None:
        """Split dump.cs into multiple files by namespace"""
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)

        for namespace, entries in self.entries.items():
            # Sanitize namespace for filename
            filename = self._sanitize_filename(namespace) + ".cs"
            filepath = output_path / filename

            # Combine all entries for this namespace
            content = "\n\n".join(entry.code for entry in entries)

            filepath.write_text(content, encoding="utf-8")
            print(f"  {filename} ({len(entries)} entries)")

        print(f"\nTotal: {len(self.entries)} namespaces, {sum(len(e) for e in self.entries.values())} entries")

    def _sanitize_filename(self, name: str) -> str:
        """Sanitize a string for use as a filename"""
        # Replace invalid characters
        invalid_chars = r'<>:"/\|?*'
        for char in invalid_chars:
            name = name.replace(char, "_")
        return name
