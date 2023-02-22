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


def test_1bit_transparency():
    with Image.open("Tests/images/cur_259.cur") as im:
        assert im.size == (32, 32) and im.mode == "RGBA"
        assert im.getpixel((0, 0)) == (0, 0, 0, 255)  # pointy bit is black
        assert im.getpixel((1, 0)) == (0, 0, 0, 255)  # and its neighbor is black
        assert im.getpixel((2, 0)) == (0, 0, 0, 0)  # third pixel in the upper row is transparent though
        assert im.getpixel((1, 1)) == (255, 255, 255, 255)  # cursor body is white
