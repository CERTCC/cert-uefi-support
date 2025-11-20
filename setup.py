from setuptools import setup, Extension
from pathlib import Path
import sys

BaseToolsDir = Path("edk2/BaseTools")

if not Path(BaseToolsDir).exists():
    print("The edk2 submodule has not been populated.")
    print("Populate it using \"git submodule update --init --recursive\"")
    sys.exit(1)

edk2Module = Extension(
    'uefi_support.EfiCompressor',
    sources=[
        str(Path(BaseToolsDir, 'Source', 'C', 'Common', 'Decompress.c')),
        str(Path('uefi_support', 'EfiCompressor.c'))
    ],
    include_dirs=[
        str(Path(BaseToolsDir, 'Source', 'C', 'Include')),
        str(Path(BaseToolsDir, 'Source', 'C', 'Include', 'Ia32')),
        str(Path(BaseToolsDir, 'Source', 'C', 'Common'))
    ]
)

LzmaSDK = Path(BaseToolsDir, 'Source', 'C', 'LzmaCompress', 'Sdk', 'C')
LzmaSDKFiles = [str(Path(LzmaSDK, x)) for x in ['Alloc.c', 'LzFind.c', 'LzmaDec.c', 'LzmaEnc.c', '7zFile.c', '7zStream.c', 'Bra86.c']]

lzmaModule = Extension(
    "uefi_support.LzmaCompressor",
    sources = LzmaSDKFiles + [str(Path('uefi_support', 'LzmaCompressor.c'))],
    include_dirs = [ str(LzmaSDK) ],
    define_macros = [('_7ZIP_ST', None)]
)

HuffmanPath = Path('unhuffme')
HuffmanFiles = [str(Path(HuffmanPath, x))
                for x in ['dict_cpt_1.c', 'dict_cpt_2.c',
                          'dict_pch_1.c', 'dict_pch_2.c', 'huffman.c']]
huffmanModule = Extension(
    "uefi_support.HuffmanCompressor",
    sources = HuffmanFiles + [str(Path('uefi_support', 'HuffmanCompressor.c'))],
    include_dirs = [ str(HuffmanPath) ])

mspackPath = Path("libmspack/libmspack/mspack")
mspackFiles = [str(Path(mspackPath, x))
               for x in ['system.c', 'cabd.c', 'lzxd.c', 'mszipd.c', 'qtmd.c']]

cabModule = Extension(
    "uefi_support.Cab",
    sources = mspackFiles + [str(Path('uefi_support', 'Cab.c'))],
    include_dirs = [ str(mspackPath) ],
    extra_compile_args = [])

setup(name="uefi_support",
      version="1.0",
      ext_modules=[edk2Module, lzmaModule, huffmanModule, cabModule],
      package_dir={'uefi_support': 'uefi_support'},
      packages=['uefi_support'],
      package_data={'uefi_support': ['huff11.bin']}
      )
