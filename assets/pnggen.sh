#!/usr/bin/env bash

if [ $# -lt 4 ]; then
    echo Usage: $0 src dest width height >&2
    exit 1
fi

src="$1"
dest="$2"
width="$3"
height="$4"

cur_dir=$(pwd)

for f in $(ls ${src} | grep '.svg$'); do
    output="${dest}/${f%.*}-${width}x${height}.png"
    echo "Processing ${src} to ${output}"
    rsvg-convert -h ${height} -w ${width} "${src}/${f}" > "${output}"
    echo "Done."
done
