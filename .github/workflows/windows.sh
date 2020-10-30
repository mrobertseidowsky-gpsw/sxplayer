#!/bin/bash

set -e

if [[ -z "${FFRUST_VC_PATH}" ]]; then
    if [[ -n "${FFRUST_RECURSING}" ]]; then
        echo "Something went terribly wrong with our MVSC/msys2 magic"
        exit 1
    fi

    ###############################################################
    # Detect Visual Studio installation, the galaxy brain way
    ###############################################################
    VARSALL_2017_PATH='C:\Program Files (x86)\Microsoft Visual Studio\2017\Community\VC\Auxiliary\Build\vcvarsall.bat'
    VARSALL_2015_PATH='C:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\vcvarsall.bat'

    # Look for various places MSVC could hide
    for edition in 2017 2015; do
        echo "Looking for MVSC ${edition}..."
        name="VARSALL_${edition}_PATH"
        file="${!name}"
        if [[ -f "${file}" ]]; then
            echo "✓ Found MSVC ${edition}"
            VARSALL_PATH=${file}
            break
        fi
    done

    # Translate our 'build architecture' to something the MSVC toolchain understands
    case "${CI_ARCH}" in
        x86_64) VARSALL_ARCH="amd64" ;;
        i686)   VARSALL_ARCH="x86" ;;
        *)      echo "Unknown arch: ${CI_ARCH}"; exit 1
    esac    

    ###############################################################
    # Set up PATH so we can call Visual Studio command-line tools
    ###############################################################

    # Make a temporary batch file that calls varsall.bat, and writes path
    # to another temporary file.
    (
cat <<EOF
    call "${VARSALL_PATH}" ${VARSALL_ARCH}
    set FFRUST_VC_PATH=%PATH%
    %BASH_PATH% -lc '%SCRIPT_PATH%'
    exit /b %ERRORLEVEL%
EOF
    ) > .generate_vc_path.bat 

    export BASH_PATH=$(cygpath -w $(which bash.exe))
    export SCRIPT_PATH="${PWD}/release/windows.sh"
    export FFRUST_RECURSING=1

    # gotta double up '/C' so that automatic mingw path translation
    # does not kick in
    cmd.exe //C .generate_vc_path.bat
    exit 0
fi

###############################################################
# Prerequisites
###############################################################
if [[ -z $CI_ARCH ]]; then
    echo "Missing argument: CI_ARCH"
    exit 1
fi
for cmd in wget patch make nasm; do
    if hash ${cmd} 2>/dev/null; then
        echo "✓ Found ${cmd}"
    else
        echo "Missing command: ${cmd}"
        exit 1
    fi
done

# cygpath translates between windows-style and unix-style paths
# '-p' translates a semi-colon-separated list to a colon-separate list
export PATH=${PATH}:$(cygpath -p -u "${FFRUST_VC_PATH}")
set -x
# Safety check
cl

###############################################################
# Config
###############################################################
FFMPEG_VERSION="4.1.3"

echo "Building for ${CI_ARCH}"

###############################################################
# Set up rest of build environment
###############################################################

# Make sources directory
rm -rf sources/
mkdir -p sources/

# Make prefix
export FFRUST_PREFIX=${PWD}/artifacts/${CI_ARCH}/prefix
mkdir -p ${FFRUST_PREFIX}

pushd sources

###############################################################
# Build x264
###############################################################

wget -O - http://ftp.videolan.org/pub/x264/snapshots/last_x264.tar.bz2 | tar xjf -
pushd x264-snapshot-*/

FEATURE_X264_OPTS="\
    --disable-cli --disable-interlaced \
    --enable-static --enable-pic --enable-strip \
    --bit-depth=8 --chroma-format=420"

# sic.: that host works for both i686 and x86_64
CC=cl ./configure --host=x86_64-w64-mingw32 --prefix=${FFRUST_PREFIX} ${FEATURE_X264_OPTS}
make -j
make install

popd # x264-snapshot

###############################################################
# Build FFMPEG
###############################################################

wget -O - https://ffmpeg.org/releases/ffmpeg-${FFMPEG_VERSION}.tar.bz2 | tar xjf -
pushd ffmpeg-${FFMPEG_VERSION}/

patch -p1 < ../../create-lib-libraries.patch

FEATURE_FFMPEG_OPTS="--disable-all --disable-network --enable-w32threads \
    --enable-gpl --enable-libx264 \
    --enable-avformat --enable-avcodec --enable-swscale --enable-swresample \
    --enable-muxer=mp4 --enable-demuxer=mov \
    --enable-decoder=h264 --enable-encoder=libx264 \
    --enable-decoder=aac --enable-encoder=aac \
    --enable-protocol=file \
    --disable-shared --enable-static \
    --enable-pic \
    --extra-cflags=//I --extra-cflags=${FFRUST_PREFIX}/include \
    --extra-ldflags=//LIBPATH:$(cygpath -w ${FFRUST_PREFIX}/lib)"

case "${CI_ARCH}" in
    x86_64) PLATFORM_FFMPEG_OPTS="--target-os=win64 --arch=x86_64" ;;
    i686)   PLATFORM_FFMPEG_OPTS="--target-os=win32 --arch=x86" ;;
    *)      echo "Unknown arch: ${CI_ARCH}"; exit 1
esac    

./configure --toolchain=msvc --prefix=${FFRUST_PREFIX} ${PLATFORM_FFMPEG_OPTS} ${FEATURE_FFMPEG_OPTS}
make -j
make install

popd # ffmpeg

popd # sources
