"""Build and test portable SRecord executables from the upstream 1.65.0 source."""

import hashlib
import platform
import shutil
import stat
import subprocess
import sys
import tarfile
import tempfile
import urllib.request
import zipfile
from pathlib import Path

REVISION = "5844fa801cf4e9749202cff86ea1ed67f0cacbbf"
SOURCE_SHA256 = "9e2cc90cf95499edb70c86c339733c2811d243a8b89d6667577cf5945cf5ad51"
SOURCE_URL = f"https://codeload.github.com/sierrafoxtrot/srecord/tar.gz/{REVISION}"
TOOLS = ("srec_cat", "srec_cmp", "srec_info")
PLATFORM = {"Windows": "win32-x64", "Linux": "linux-x64", "Darwin": "darwin-arm64"}


def run(*args, **kwargs):
    return subprocess.run(args, check=True, **kwargs)


def smoke_test(binaries, directory):
    """Exercise the Intel HEX conversion and merge used by the FLPR build."""
    cat, cmp, info = binaries
    for tool in binaries:
        version = run(tool, "-VERSion", capture_output=True, text=True).stdout
        if "version 1.65.0" not in version:
            raise RuntimeError(f"Unexpected {tool.name} version: {version}")
    fixture = directory / "application.hex"
    fixture.write_text(":048000000102030472\n:00000001FF\n", encoding="ascii")
    launcher = directory / "launcher.hex"
    launcher.write_text(":0400000005060708E2\n:00000001FF\n", encoding="ascii")
    raw = directory / "application.bin"
    merged = directory / "merged.hex"
    expected = directory / "expected.hex"
    expected.write_text(":0400000005060708E2\n:048000000102030472\n:00000001FF\n", encoding="ascii")

    run(cat, fixture, "-Intel", "-offset", "-", "-minimum-addr", fixture, "-Intel", "-o", raw, "-Binary")
    if raw.read_bytes() != bytes([1, 2, 3, 4]):
        raise RuntimeError("Unexpected binary conversion")
    run(cat, launcher, "-Intel", raw, "-Binary", "-offset", "0x00008000", "-o", merged, "-Intel")
    run(cmp, merged, "-Intel", expected, "-Intel")
    run(info, merged, "-Intel")


def package(destination):
    host = platform.system()
    arch = platform.machine().lower()
    expected = {"Windows": {"amd64", "x86_64"}, "Linux": {"x86_64"}, "Darwin": {"arm64", "aarch64"}}
    if arch not in expected.get(host, set()):
        raise RuntimeError(f"Unsupported host: {host} {arch}")
    destination.mkdir(parents=True, exist_ok=True)
    output = destination / (PLATFORM[host] + ".zip")

    with tempfile.TemporaryDirectory(prefix="srecord-") as tmp:
        directory = Path(tmp)
        source_archive = directory / "source.tar.gz"
        request = urllib.request.Request(SOURCE_URL, headers={"User-Agent": "emscript-releng"})
        with urllib.request.urlopen(request, timeout=45) as source, source_archive.open("wb") as local:
            shutil.copyfileobj(source, local)
        with source_archive.open("rb") as local:
            if hashlib.file_digest(local, "sha256").hexdigest() != SOURCE_SHA256:
                raise RuntimeError("SRecord source archive digest mismatch")
        with tarfile.open(source_archive, "r:gz") as source:
            source.extractall(directory, filter="data")

        upstream = directory / f"srecord-{REVISION}"
        build = directory / "build"
        options = ["-DHAVE_GCRYPT_H=OFF", "-DHAVE_LIBGCRYPT=OFF"]
        if host == "Windows":
            options += ["-DCMAKE_EXE_LINKER_FLAGS=-static", "-DCMAKE_CXX_FLAGS=-include cstdint"]
        if host == "Darwin":
            options += ["-DCMAKE_OSX_DEPLOYMENT_TARGET=13.0"]
        run("cmake", "-S", upstream, "-B", build, "-G", "Ninja", *options)
        run("cmake", "--build", build, "--target", *TOOLS, "--parallel", "4")
        executable = ".exe" if host == "Windows" else ""
        binaries = [build / name / (name + executable) for name in TOOLS]
        smoke_test(binaries, directory)

        with zipfile.ZipFile(output, "x", zipfile.ZIP_DEFLATED) as archive:
            for binary in binaries:
                entry = zipfile.ZipInfo("bin/" + binary.name)
                entry.create_system = 3
                entry.external_attr = (stat.S_IFREG | 0o755) << 16
                archive.writestr(entry, binary.read_bytes(), compress_type=zipfile.ZIP_DEFLATED)
            archive.write(upstream / "LICENSE", "LICENSE")
            archive.write(source_archive, "source/srecord-1.65.0.tar.gz")
            archive.write(Path(__file__), "source/build-srecord.py")
        with zipfile.ZipFile(output) as archive:
            if archive.testzip() is not None:
                raise RuntimeError("SRecord ZIP integrity check failed")
    print(f"Verified {output}")


if __name__ == "__main__":
    package(Path(sys.argv[1]).resolve())
