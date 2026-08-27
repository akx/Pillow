from __future__ import annotations

import sys

import fuzzers
import packaging
import pytest

from PIL import Image, features
from Tests.helper import list_test_fonts, list_test_images, skip_unless_feature

TYPE_CHECKING = False
if TYPE_CHECKING:
    import pathlib

if sys.platform.startswith("win32") or sys.platform == "ios":
    pytest.skip("Fuzzer doesn't run on Windows or iOS", allow_module_level=True)

libjpeg_turbo_version = features.version("libjpeg_turbo")
if libjpeg_turbo_version is not None:
    version = packaging.version.parse(libjpeg_turbo_version)
    if version.major == 2 and version.minor == 0:
        pytestmark = pytest.mark.valgrind_known_error(
            reason="Known failing with libjpeg_turbo 2.0"
        )


@pytest.mark.parametrize("path", list(list_test_images()))
def test_fuzz_images(path: pathlib.Path) -> None:
    fuzzers.enable_decompressionbomb_error()
    try:
        fuzzers.fuzz_image(path.read_bytes())
        assert True
    except (
        # Known exceptions from Pillow
        OSError,
        SyntaxError,
        MemoryError,
        ValueError,
        NotImplementedError,
        OverflowError,
        # Known Image.* exceptions
        Image.DecompressionBombError,
        Image.DecompressionBombWarning,
    ):
        assert True
    finally:
        fuzzers.disable_decompressionbomb_error()


@skip_unless_feature("freetype2")
@pytest.mark.parametrize("path", list(list_test_fonts()))
def test_fuzz_fonts(path: pathlib.Path) -> None:
    try:
        fuzzers.fuzz_font(path.read_bytes())
    except (Image.DecompressionBombError, Image.DecompressionBombWarning, OSError):
        pass
    assert True
