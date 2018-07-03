#!/usr/bin/env bash
sudo dnf -y install protobuf-devel leveldb-devel snappy-devel hdf5-devel protobuf-compiler atlas-devel
sudo dnf -y install boost-devel
sudo dnf -y install gflags-devel glog-devel lmdb-devel
sudo dnf -y install libzip-devel
sudo dnf -y install https://download1.rpmfusion.org/free/fedora/rpmfusion-free-release-$(rpm -E %fedora).noarch.rpm https://download1.rpmfusion.org/nonfree/fedora/rpmfusion-nonfree-release-$(rpm -E %fedora).noarch.rpm

# install common dependencies: OpenCV
# adpated from OpenCV.sh
version="2.4.13"

echo "Building OpenCV" $version
[[ -d 3rd-party ]] || mkdir 3rd-party/
cd 3rd-party/

if [ ! -d "opencv-$version" ]; then
    echo "Installing OpenCV Dependenices"
    sudo dnf -y install java-1.8.0-openjdk-devel opencv-devel cmake pkg-config yasm libjpeg-devel libjasper-devel ffmpeg-devel libdc1394-devel gstreamer-devel gstreamer-plugins-base-devel libv4l-devel python-devel python-numpy tbb-devel qt4-devel gtk2-devel faac-devel lame-devel opencore-amr-devel libtheora-devel libvorbis-devel xvidcore-devel x264 v4l-utils
	
    sudo dnf -y groupinstall "C Development Tools and Libraries"

    echo "Downloading OpenCV" $version
    wget -O OpenCV-$version.zip https://github.com/Itseez/opencv/archive/$version.zip

    echo "Extracting OpenCV" $version
    unzip OpenCV-$version.zip
fi

echo "Building OpenCV" $version
cd opencv-$version
[[ -d build ]] || mkdir build
cd build
sed -i -e '4iset(OPENCV_VCSVERSION "2.4.13")\' ../cmake/OpenCVPackaging.cmake 
sed -i -e '81i    #dumpversion prints only major version since gcc7' ../cmake/OpenCVDetectCXXCompiler.cmake
sed -i -e '82i    if((NOT CMAKE_GCC_REGEX_VERSION) AND (${CMAKE_OPENCV_GCC_VERSION_FULL} GREATER 6))' ../cmake/OpenCVDetectCXXCompiler.cmake
sed -i -e '83i        execute_process(COMMAND ${CMAKE_CXX_COMPILER} ${CMAKE_CXX_COMPILER_ARG1} -dumpfullversion' ../cmake/OpenCVDetectCXXCompiler.cmake
sed -i -e '84i                        OUTPUT_VARIABLE CMAKE_OPENCV_GCC_VERSION_FULL' ../cmake/OpenCVDetectCXXCompiler.cmake
sed -i -e '85i                        OUTPUT_STRIP_TRAILING_WHITESPACE)' ../cmake/OpenCVDetectCXXCompiler.cmake
sed -i -e '86i        string(REGEX MATCH \"[0-9]+\\\\.[0-9]+\\\\.[0-9]+" CMAKE_GCC_REGEX_VERSION "${CMAKE_OPENCV_GCC_VERSION_FULL}")' ../cmake/OpenCVDetectCXXCompiler.cmake
sed -i -e '87i    endif()\' ../cmake/OpenCVDetectCXXCompiler.cmake

cmake -D CMAKE_BUILD_TYPE=RELEASE -D WITH_TBB=ON -D WITH_V4L=ON -DENABLE_PRECOMPILED_HEADERS=OFF ..
if make -j32 ; then
    cp lib/cv2.so ../../../
    echo "OpenCV" $version "built."
else
    echo "Failed to build OpenCV. Please check the logs above."
    exit 1
fi
