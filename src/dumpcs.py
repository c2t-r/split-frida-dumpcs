from dataclasses import dataclass
import re

""" dumpcs format
// Panda.Script
class <Module> : 
{
    
    
}

// Panda.Script
class Microsoft.CodeAnalysis.EmbeddedAttribute : System.Attribute
{
    
    System.Void .ctor(); // 0x00a39870
}
...
"""


@dataclass
class Entry:
    satrt: int  # line
    end: int  # line
    namespace: str
    code: str


class dumpcs:
    code: str
    entries: map[str, list[Entry]]

    def __init__(self) -> None:
        pass

    def load(self) -> None:
        pattarn = r"//(.+?)\n[/s/S]+?^\}"
        self.entries  # key is namespace

    def split(self, path) -> None:
        # split by [namespace].py
        sp = {}
        for entry in self.entries:
            pass
        pass
