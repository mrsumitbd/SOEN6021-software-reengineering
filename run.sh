#!/bin/bash
python src/run_repo_in_ci_env.py scikit-optimize 20 create_new
python src/run_repo_in_ci_env.py scikit-optimize 20 append
python src/run_repo_in_ci_env.py scikit-optimize 10 append
