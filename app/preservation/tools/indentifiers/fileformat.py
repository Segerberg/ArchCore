from typing import Optional, List, Tuple
from fido.fido import Fido
from fido.versions import get_local_versions
from xml.etree.ElementTree import Element

class FormatIdentifier:
    _fido: Optional[Fido] = None
    format_name: Optional[str] = None
    format_version: Optional[str] = None
    format_registry_key: Optional[str] = None
    use_fido_pronom_formats: bool
    use_fido_extension_formats: bool

    def __init__(self, use_fido_pronom_formats: bool = True, use_fido_extension_formats: bool = True) -> None:
        self.use_fido_pronom_formats = use_fido_pronom_formats
        self.use_fido_extension_formats = use_fido_extension_formats

    @property
    def fido(self) -> Fido:
        if self._fido is None:
            format_files: List[str] = []
            if self.use_fido_pronom_formats or self.use_fido_extension_formats:
                versions = get_local_versions()
                if self.use_fido_pronom_formats:
                    format_files.append(versions.pronom_signature)
                if self.use_fido_extension_formats:
                    format_files.append(versions.fido_extension_signature)

            self._fido = Fido(
                handle_matches=self.handle_matches,
                nocontainer=True,
                format_files=format_files,
            )

        return self._fido

    def handle_matches(self, fullname: str, matches: List[Tuple[Element, str]], delta_t: float, matchtype: str = '') -> None:
        if len(matches) == 0:
            if self.allow_unknown_file_types:
                self.format_name = 'Unknown File Format'
                self.format_version = None
                self.format_registry_key = None
                return

            raise ValueError(f"No matches for {fullname}")

        f, _ = matches[-1]

        try:
            self.format_name = f.find('name').text
        except AttributeError:
            self.format_name = None

        try:
            self.format_version = f.find('version').text
        except AttributeError:
            self.format_version = None

        try:
            self.format_registry_key = f.find('puid').text
        except AttributeError:
            self.format_registry_key = None

    def identify_file_format(self, filename: str) -> Tuple[Optional[str], Optional[str], Optional[str]]:
        """
        Identifies the format of the given file using the fido library.

        Args:
            filename (str): The path to the file whose format is to be identified.

        Returns:
            Tuple[Optional[str], Optional[str], Optional[str]]:
                A tuple containing:
                - The format name (str or None) if identified, or None if unknown.
                - The format version (str or None) if applicable, or None if unavailable.
                - The format registry key (str or None), typically the PRONOM PUID, or None if not found.
        """

        self.fido.identify_file(filename)
        return self.format_name, self.format_version, self.format_registry_key
