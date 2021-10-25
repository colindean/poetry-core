from pathlib import Path

from poetry.core.packages.file_hash import FileHash
from poetry.core.packages.file_hash import HashValue


DIST_PATH = Path(__file__).parent.parent / "fixtures" / "distributions"
TEST_FILE = "demo-0.1.0.tar.gz"
TEST_FILE_FULL_PATH = DIST_PATH / TEST_FILE
TEST_FILE_SHA256 = HashValue(
    "sha256", "72e8531e49038c5f9c4a837b088bfcb8011f4a9f76335c8f0654df6ac539b3d6"
)
TEST_FILE_MD5 = HashValue("md5", "80a46fca8b73ee10f12a92765448c47f")


def test_sha256_hash():
    file_hash = FileHash(TEST_FILE_FULL_PATH)
    assert file_hash.sha256() == TEST_FILE_SHA256


def test_md5_hash():
    file_hash = FileHash(TEST_FILE_FULL_PATH)
    assert file_hash.md5() == TEST_FILE_MD5


def test_same_file_hash():
    file_hash = FileHash(TEST_FILE_FULL_PATH)
    assert file_hash is file_hash


def deserialize_hash():
    actual = HashValue.from_str(
        "sha256:72e8531e49038c5f9c4a837b088bfcb8011f4a9f76335c8f0654df6ac539b3d6"
    )
    assert actual == TEST_FILE_SHA256
