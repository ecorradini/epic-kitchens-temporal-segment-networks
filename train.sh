#!/bin/sh
lib/caffe-action/build/tools/caffe train --solver=models/epic_kitchens_solver_1.prototxt >> output.txt 2>&1

