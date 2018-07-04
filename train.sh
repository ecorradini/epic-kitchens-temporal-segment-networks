#!/bin/sh
lib/caffe-action/build/tools/caffe train --solver=models/tsn_bn_inception_rgb_solver.prototxt >> output.txt 2>&1

