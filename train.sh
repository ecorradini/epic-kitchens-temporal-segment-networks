#!/bin/sh
lib/caffe-action/build/tools/caffe train --solver=models/epic_kitchens_solver_1.prototxt >> output.txt 2>&1
lib/caffe-action/build/tools/caffe train --solver=models/epic_kitchens_solver_2.prototxt --snapshot=models/epic_kitchens_model_iter_61.solverstate >> output.txt 2>&1
lib/caffe-action/build/tools/caffe train --solver=models/epic_kitchens_solver_3.prototxt --snapshot=models/epic_kitchens_model_iter_123.solverstate >> output.txt 2>&1

