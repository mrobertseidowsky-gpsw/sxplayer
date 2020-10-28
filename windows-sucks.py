#!/usr/bin/env python
#
# Python script to compile and install ffmpeg.
#
# part of ffcluster project.
# see full project at github.com/santazhang/ffcluster
#
# Author: Santa Zhang <santa1987@gmail.com>

import os
import urllib2
import traceback

# goto script folder
os.chdir(os.path.join(os.getcwd(), os.path.dirname(__file__)))

# path relative to this script file
# where will the dependency packages be downloaded
DOWNLOAD_DIR = "download"

# where to install ffcluster and all dependencies
PREFIX_DIR = "/opt/ffcluster"


def my_mkdir(path):
    if os.path.exists(path) == False:
        os.makedirs(path)

def my_remove(path):
    if os.path.exists(path):
        os.remove(path)

def my_exec(cmd):
    print "[cmd] %s" % cmd
    os.system(cmd)

def prepare_package(pkg_url):
    ret = True
    my_mkdir(DOWNLOAD_DIR)
    pkg_name = os.path.basename(urllib2.urlparse.urlparse(pkg_url).path)
    pkg_fpath = os.path.join(DOWNLOAD_DIR, pkg_name)
    tmp_fpath = os.path.join(DOWNLOAD_DIR, pkg_name + ".downloading")
    my_remove(tmp_fpath)
    if os.path.exists(pkg_fpath):
        print "%s already downloaded" % pkg_name
    else:
        f = open(tmp_fpath, "wb")
        try:
            print "downloading %s from %s" % (pkg_name, pkg_url)
            f.write(urllib2.urlopen(pkg_url).read())
            os.rename(tmp_fpath, pkg_fpath)
        except:
            traceback.print_exc()
            my_remove(tmp_fpath)
            exit(1)
        finally:
            f.close()
    if ret == True:
        if pkg_name.endswith(".tar.bz2"):
            if os.path.exists(os.path.join(DOWNLOAD_DIR, pkg_name[:-8])) == False:
                print "extracting %s" % pkg_name
                my_exec("cd '%s' ; tar xjf %s" % (DOWNLOAD_DIR, pkg_name))
        if pkg_name.endswith(".tar.gz"):
            if os.path.exists(os.path.join(DOWNLOAD_DIR, pkg_name[:-7])) == False:
                print "extracting %s" % pkg_name
                my_exec("cd '%s' ; tar xzf %s" % (DOWNLOAD_DIR, pkg_name))
    return ret

if os.path.exists(PREFIX_DIR) == False:
    my_exec("sudo mkdir -p '%s' ; sudo chmod 777 '%s'" % (PREFIX_DIR, PREFIX_DIR))


# # build yasm
# prepare_package("http://www.tortall.net/projects/yasm/releases/yasm-1.2.0.tar.gz")
# my_exec("""
#     export PATH=/bin:/usr/bin:%s/bin:$PATH
#     cd %s/yasm-1.2.0
#     ./configure --prefix=%s
#     make
#     make install
# """ % (PREFIX_DIR, DOWNLOAD_DIR, PREFIX_DIR))


# # build x264
# prepare_package("ftp://ftp.videolan.org/pub/x264/snapshots/x264-snapshot-20120302-2245-stable.tar.bz2")
# my_exec("""
#     export PATH=/bin:/usr/bin:%s/bin:$PATH
#     cd %s/x264-snapshot-20120302-2245-stable
#     ./configure --prefix=%s --enable-static --extra-cflags='-I%s/include' --extra-ldflags='-L%s/lib'
#     make
#     make install
# """ % (PREFIX_DIR, DOWNLOAD_DIR, PREFIX_DIR, PREFIX_DIR, PREFIX_DIR))


# # build faac
# # also fix a compilation bug
# prepare_package("http://downloads.sourceforge.net/faac/faac-1.28.tar.gz")
# my_exec("""
#     export PATH=/bin:/usr/bin:%s/bin:$PATH
#     cd %s/faac-1.28
#     sed 's/^char\ \*strcasestr/\/\/char\ \*strcasestr/' common/mp4v2/mpeg4ip.h > common/mp4v2/mpeg4ip.h~
#     mv common/mp4v2/mpeg4ip.h~ common/mp4v2/mpeg4ip.h
#     ./configure --prefix=%s
#     make
#     make install
# """ % (PREFIX_DIR, DOWNLOAD_DIR, PREFIX_DIR))


# # build libmp3lame
# prepare_package("http://downloads.sourceforge.net/lame/lame-3.99.5.tar.gz")
# my_exec("""
#     export PATH=/bin:/usr/bin:%s/bin:$PATH
#     cd %s/lame-3.99.5
#     ./configure --prefix=%s
#     make
#     make install
# """ % (PREFIX_DIR, DOWNLOAD_DIR, PREFIX_DIR))


# # build libogg
# prepare_package("http://downloads.xiph.org/releases/ogg/libogg-1.3.0.tar.gz")
# my_exec("""
#     export PATH=/bin:/usr/bin:%s/bin:$PATH
#     cd %s/libogg-1.3.0
#     ./configure --prefix=%s
#     make
#     make install
# """ % (PREFIX_DIR, DOWNLOAD_DIR, PREFIX_DIR))


# # build libvorbis
# prepare_package("http://downloads.xiph.org/releases/vorbis/libvorbis-1.3.2.tar.bz2")
# my_exec("""
#     export PATH=/bin:/usr/bin:%s/bin:$PATH
#     cd %s/libvorbis-1.3.2
#     ./configure --prefix=%s --with-ogg=%s
#     make
#     make install
# """ % (PREFIX_DIR, DOWNLOAD_DIR, PREFIX_DIR, PREFIX_DIR))


# # build libtheora
# prepare_package("http://downloads.xiph.org/releases/theora/libtheora-1.1.1.tar.bz2")
# my_exec("""
#     export PATH=/bin:/usr/bin:%s/bin:$PATH
#     cd %s/libtheora-1.1.1
#     ./configure --prefix=%s --with-ogg=%s --with-vorbis=%s
#     make
#     make install
# """ % (PREFIX_DIR, DOWNLOAD_DIR, PREFIX_DIR, PREFIX_DIR, PREFIX_DIR))


# # build libvpx-v1.0.0.tar.bz2
# prepare_package("http://webm.googlecode.com/files/libvpx-v1.0.0.tar.bz2")
# my_exec("""
#     export PATH=/bin:/usr/bin:%s/bin:$PATH
#     cd %s/libvpx-v1.0.0
#     ./configure --prefix=%s
#     make
#     make install
# """ % (PREFIX_DIR, DOWNLOAD_DIR, PREFIX_DIR))


# # build libxvid
# prepare_package("http://downloads.xvid.org/downloads/xvidcore-1.3.2.tar.bz2")
# my_exec("""
#     export PATH=/bin:/usr/bin:%s/bin:$PATH
#     cd %s/xvidcore/build/generic
#     ./configure --prefix=%s
#     make
#     make install
# """ % (PREFIX_DIR, DOWNLOAD_DIR, PREFIX_DIR))


# # build ffmpeg
# prepare_package("http://ffmpeg.org/releases/ffmpeg-0.10.tar.bz2")
# my_exec("""
#     export PATH=/bin:/usr/bin:%s/bin:$PATH
#     cd %s/ffmpeg-0.10
#     ./configure \
#         --prefix=%s --enable-gpl --enable-nonfree \
#         --disable-ffserver \
#         --disable-shared --enable-static \
#         --extra-cflags='-static -I%s/include' \
#         --extra-ldflags='-L%s/lib' \
#         --enable-libx264 --enable-libfaac --enable-libmp3lame --enable-pthreads --enable-libvpx --enable-libxvid \
#         --enable-libvorbis --enable-libtheora
#     make
#     make install
# """ % (PREFIX_DIR, DOWNLOAD_DIR, PREFIX_DIR, PREFIX_DIR, PREFIX_DIR))