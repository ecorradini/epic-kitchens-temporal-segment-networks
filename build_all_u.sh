#!/usr/bin/env bash
CAFFE_USE_MPI=${1:-OFF}
CAFFE_MPI_PREFIX=${MPI_PREFIX:-""}

# update the submodules: Caffe and Dense Flow
git submodule update --remote

# install Caffe dependencies
sudo apt-get -qq install libprotobuf-dev libleveldb-dev libsnappy-dev libhdf5-serial-dev protobuf-compiler libatlas-base-dev
sudo apt-get -qq install --no-install-recommends libboost1.55-all-dev
sudo apt-get -qq install libgflags-dev libgoogle-glog-dev liblmdb-dev

# install Dense_Flow dependencies
sudo apt-get -qq install libzip-dev

# install common dependencies: OpenCV
# adpated from OpenCV.sh
version="2.4.13"

echo "Building OpenCV" $version
[[ -d 3rd-party ]] || mkdir 3rd-party/
cd 3rd-party/

if [ ! -d "opencv-$version" ]; then
    echo "Installing OpenCV Dependenices"
    sudo apt-get -qq install libopencv-dev build-essential checkinstall cmake pkg-config yasm libjpeg-dev libjasper-dev libavcodec-dev libavformat-dev libswscale-dev libdc1394-22-dev libgstreamer0.10-dev libgstreamer-plugins-base0.10-dev libv4l-dev python-dev python-numpy libtbb-dev libqt4-dev libgtk2.0-dev libfaac-dev libmp3lame-dev libopencore-amrnb-dev libopencore-amrwb-dev libtheora-dev libvorbis-dev libxvidcore-dev x264 v4l-utils

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
sed -i -e '86i        string(REGEX MATCH "[0-9]+\\.[0-9]+\\.[0-9]+" CMAKE_GCC_REGEX_VERSION "${CMAKE_OPENCV_GCC_VERSION_FULL}")' ../cmake/OpenCVDetectCXXCompiler.cmake
sed -i -e '87i    endif()\' ../cmake/OpenCVDetectCXXCompiler.cmake

cmake -D CMAKE_BUILD_TYPE=RELEASE -D WITH_TBB=ON -D WITH_V4L=ON -DENABLE_PRECOMPILED_HEADERS=OFF ..

if make -j32 ; then
    cp lib/cv2.so ../../../
    echo "OpenCV" $version "built."
else
    echo "Failed to build OpenCV. Please check the logs above."
    exit 1
fi
