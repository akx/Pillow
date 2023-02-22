import pytest

from PIL import CurImagePlugin, Image


def test_sanity():
    with Image.open("Tests/images/deerstalker.cur") as im:
        assert im.size == (32, 32)
        assert isinstance(im, CurImagePlugin.CurImageFile)
        # Check some pixel colors to ensure image is loaded properly
        assert im.getpixel((10, 1)) == (0, 0, 0, 0)
        assert im.getpixel((11, 1)) == (253, 254, 254, 1)
        assert im.getpixel((16, 16)) == (84, 87, 86, 255)


def test_invalid_file():
    with pytest.raises(SyntaxError):
        CurImagePlugin.CurImageFile("Tests/images/flower.jpg")

    with pytest.raises(SyntaxError, match="No images were found"):
        CurImagePlugin.CurImageFile("Tests/images/no_cursors.cur")
