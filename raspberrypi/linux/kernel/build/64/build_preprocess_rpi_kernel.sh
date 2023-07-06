#!/bin/bash

echo "configure build output path"

KERNEL_TOP_PATH="$( cd "$(dirname "$0")"; pwd -P )"
OUTPUT="$KERNEL_TOP_PATH/out"
echo "$OUTPUT"

KERNEL=kernel8
BUILD_LOG="$KERNEL_TOP_PATH/rpi_build_log.txt"

PREPROCESS_FILE=$1
echo "build preprocessed file: $PREPROCESS_FILE"

echo "move kernel source"
cd linux

echo "make defconfig"
make O=$OUTPUT bcm2711_defconfig

echo "kernel build"
make $PREPROCESS_FILE O=$OUTPUT Image.gz modules dtbs -j4 2>&1 | tee $BUILD_LOG
