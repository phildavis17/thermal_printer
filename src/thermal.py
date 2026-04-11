import os
import tomllib
from dataclasses import dataclass
from pathlib import Path

LOCAL_CAPABILITIES_FILE = Path(__file__).parent.parent / "capabilities.json"

os.environ["ESCPOS_CAPABILITIES_FILE"] = str(LOCAL_CAPABILITIES_FILE)
from escpos.printer import Network, Usb

DEFAULT_CONFIG_PATH = Path(__file__).parent.parent / "printer_config.toml"

type Printer = Network | Usb

@dataclass
class PrinterConfig:
    ip: str
    port: int
    pixel_width: int
    profile: str | None = None

    @staticmethod
    def parse_from_config(config_data: dict[str, str | int]):
        return PrinterConfig(**config_data)


class PrintJob:
    def __init__(self, lines: list[str]):
        self.lines = lines


class ConfiguredPrinter:
    def __init__(self, config:PrinterConfig):
        self.config = config
        self.printer = self._configure_printer(self.config)
    
    @staticmethod
    def _configure_printer(config: PrinterConfig):
        p = Network(
            host = config.ip,
            port = config.port,
            profile=config.profile
        )
        p.hw("INIT")
        return p

    def reset(self):
        self.printer.hw("INIT")
    
    def send_job(self, job: PrintJob) -> None:
        self.reset()
        for line in job.lines:
            self.printer.textln(line)
        self.printer.ln(2)
        self.printer.cut()

def load_configs(config_path: Path) -> dict:
    with open(config_path, "rb") as config_file:
        return tomllib.load(config_file)
    
def get_configured_printer(
    config_path: Path | None = None,
    printer_name: str | None = None,
):
    if config_path is None:
        config_path = DEFAULT_CONFIG_PATH
    config = load_configs(config_path)
    if printer_name is not None:
        config_data = config[printer_name]
    config_data = list(config.values()).pop()
    printer_config = PrinterConfig.parse_from_config(config_data)
    return ConfiguredPrinter(printer_config)

    

if __name__ == "__main__":
    cp = get_configured_printer()

    l = [
        "This",
        "is",
        "a",
        "test",
    ]
    pj = PrintJob(l)
    cp.send_job(pj)
