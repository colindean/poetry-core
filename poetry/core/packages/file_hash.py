import hashlib
import io

from dataclasses import dataclass
from pathlib import Path
from typing import Dict
from typing import Optional
from typing import Set


@dataclass(frozen=True)
class HashValue:
    algorithm: str
    digest: str

    def __str__(self) -> str:
        return f"{self.algorithm}:{self.digest}"

    @classmethod
    def from_str(cls, algo_digest: str, separator: str = ":") -> "HashValue":
        algo, digest = algo_digest.split(separator, 1)
        return cls(algo, digest)


class FileHash:
    def __init__(self, path: Path, known_hashes: Optional[Set[HashValue]] = None):
        if known_hashes is None:
            known_hashes = set()
        self.path = path
        self.hash_cache = known_hashes

    def __eq__(self, other):
        if isinstance(other, FileHash):
            shared = self.hash_cache.intersection(other.hash_cache)
            return bool(shared)

    def sha256(self) -> HashValue:
        return self.other("sha256")

    def md5(self) -> HashValue:
        return self.other("md5")

    def _hashes_by_algo(self) -> Dict[str, HashValue]:
        return dict([(hashval.algorithm, hashval) for hashval in list(self.hash_cache)])

    def other(self, algorithm: str) -> HashValue:
        algos_cached = self._hashes_by_algo()
        if algorithm not in algos_cached:
            hash_val = self._hash(algorithm, self.path)
            self.hash_cache.add(hash_val)
            return hash_val
        else:
            return algos_cached[algorithm]

    @classmethod
    def _hash(cls, hash_name: str, file_path: Path) -> HashValue:
        h = hashlib.new(hash_name)
        with file_path.open("rb") as fp:
            for content in iter(lambda: fp.read(io.DEFAULT_BUFFER_SIZE), b""):
                h.update(content)

        return HashValue(h.name, h.hexdigest())
