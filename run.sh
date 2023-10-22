#!/bin/bash
python src/run_repo_in_ci_env.py Feature-Selection master 25 create_new
python src/run_repo_in_ci_env.py Feature-Selection master 25 append

# python src/run_repo_in_ci_env.py pymc-learn master 25 create_new
# python src/run_repo_in_ci_env.py pymc-learn master 25 append
