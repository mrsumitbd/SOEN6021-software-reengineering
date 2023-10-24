import sys, re
import numpy as np
import pandas as pd
from utility import *
from process_travis import *


class RunRepoInCIEnv:
    def __init__(self, api_key):
        self.process_Travis = ProcessTravisCIBuilds(api_key)

    def build_n_times(self, n, repo, branch='master'):
        '''
        :param n: # of build requests to make
        :param repo: <slug>/<project_name>
        :param branch: default is master
        :return: a dictionary key -> buld_id, value -> dict{'job_list:[], 'status': build_state}
        '''
        for i in range(n):
            self.process_Travis.create_build_request(repo, branch)
            time.sleep(20)  # wait for 20 sec before sending the next build request

        time.sleep(
            60)  # wait for a minute because the build requests are not instantaneouly processed by the travis server

        return self.process_Travis.get_build_details(repo, n)

    def process_logs(self, build_list):
        '''
        :param build_list:
        :return:
        '''
        run = 0
        data_list = []
        for build_id, build_desc in build_list.items():

            run += 1
            status = build_desc['status']
            while status not in ['passed', 'errored', 'failed']:
                time.sleep(30)
                status = self.process_Travis.get_build_info(build_id)

            print(f"{build_id} completed with status {status}.")

            if status == 'passed':
                for job_id in build_list[build_id]['job_list']:
                    job_details = self.process_Travis.get_job_details(job_id)
                    try:
                        # score = job_details['log'].split("\nScore: ")[1].split("\n")[0]
                        score = re.findall(r"^Score:\s(\d+\.\d+)\s", job_details['log'], re.MULTILINE)[0]
                    except:
                        score = np.nan
                    data_list.append(list(np.append(job_details['job_config'].split('_'),
                                                    [int(run), round(float(score), 6),
                                                     job_details['processing_time']])))
            else:
                run -= 1

        return data_list

    def __del__(self):
        print("Done processing the project.")


if __name__ == '__main__':
    project_name = sys.argv[1]
    number_of_runs = sys.argv[3]
    print(f"Processing project: {project_name}. Running the project {number_of_runs} time(s).")

    run_obj = RunRepoInCIEnv("WMlSAymr_DTc5XHe5mCj4w")
    df = pd.DataFrame(
        run_obj.process_logs(run_obj.build_n_times(int(number_of_runs), f'notthatanonymous/{project_name}', branch=sys.argv[2])),
        columns=['OS', 'Python', 'Hardware', 'Run', 'Score', 'Processing_Time'])
    df["Project"] = [project_name] * df.shape[0]

    del run_obj

    if sys.argv[4] == 'create_new':
        write_df(df=df, file_name=f'{project_name}.csv')
    else:
        write_df(df=df, file_name=f'{project_name}.csv', overwrite_if_existing=False)
