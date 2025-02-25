try:
    import textual
    import textual.binding
    import textual.containers
    import textual.widgets
    from textual.app import App, ComposeResult
except ImportError as e:
    raise ImportError(
        "Please install textual with 'pip install textual' "
        "or 'pip install essimaging[gui]' to use the GUI."
    ) from e

from typing import ClassVar


class FileExplorer(textual.containers.Horizontal):
    def compose(self) -> ComposeResult:
        yield textual.widgets.DirectoryTree(path=".")
        yield textual.containers.Container(textual.widgets.Pretty(''))


class ESSImagingApp(App):
    BINDINGS: ClassVar = [("q", "quit", "Exit the app")]

    def compose(self) -> ComposeResult:
        yield textual.widgets.Header(show_clock=True)
        yield FileExplorer()
        yield textual.widgets.Footer()


def main():
    app = ESSImagingApp()
    app.run()
