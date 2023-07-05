#!/bin/bash

KERNEL_TOP_PATH="$( cd "$(dirname "$0")" ; pwd -P)"
OUTPUT="$KERNEL_TOP_PATH/out"
echo "$OUTPUT"

cd linux

make O=$OUTPUT modules_install
cp $OUTPUT/arch/arm64/boot/dts/broadcom/*.dtb /boot/
cp $OUTPUT/arch/arm64/boot/dts/overlays/*.dtb* /boot/overlays/
#cp $OUTPUT/arch/arm64/boot/dts/overlays/README /boot/overlays/
cp $OUTPUT/arch/arm64/boot/Image.gz /boot/kernel8.img
