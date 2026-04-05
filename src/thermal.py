import os
from dataclasses import dataclass
from pathlib import Path

LOCAL_CAPABILITIES_FILE = Path(__file__).parent.parent / "capabilities.json"

os.environ["ESCPOS_CAPABILITIES_FILE"] = str(LOCAL_CAPABILITIES_FILE)
from escpos.printer import Network, Usb

type Printer = Network | Usb

@dataclass
class PrinterConfig:
    ip: str
    port: int
    pixel_width: int
    profile: str | None = None


class PrintJob:
    def __init__(self):
        pass



class ConfiguredPrinter:
    def __init__(self, config:PrinterConfig):
        self.config = config
        self.printer = self._configure_printer(self.config)
    
        pass

    def reset(self):
        self.printer.hw("INIT")
    
    def send_job(self, job: PrintJob) -> None:
        self.reset()
        for line in PrintJob.render():
            self.printer.textln(line)
        self.printer.ln(2)
        self.printer.cut()
    
