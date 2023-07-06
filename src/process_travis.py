from PyTravisCI import TravisCI, defaults
import time, datetime


class ProcessTravisCIBuilds:
    def __init__(self, token):
        self.travis = TravisCI(access_token=token, access_point=defaults.access_points.PRIVATE)

    def create_build_request(self, repo_name, branch):
        '''
        :param repo_name: user_name/repo
        :param branch: branch_name
        :return: None
        '''
        repo = self.travis.get_repository(repo_name)
        repo.create_request(f"Build request created for {repo_name}, {branch} branch.", branch)

    def get_build_info(self, build_id):
        return self.travis.get_build(build_id).state

    def get_build_details(self, repo_link, latest_n):
        '''
        :param repo_link: user_name/repo
        :param latest_n: last n builds
        :return: dict (key, value) -> (build_id, {job_list : list of job ids, status : build status})
        '''
        build_dict = {}
        try:
            repository = self.travis.get_repository(repo_link)
            builds = repository.get_builds(params={"limit": latest_n})
            for build in builds:
                build_dict[build.id] = {"job_list": [job.id for job in build.jobs], "status": build.state}
            return build_dict
        except:
            return "Nothing found."

    def get_job_details(self, job_id):
        job = self.travis.get_job(job_id)
        if str(job.number)[-2:] == ".1":
            job_config_str = "Linux-Xenial_3.8_amd64"
        elif str(job.number)[-2:] == ".2":
            job_config_str = 'Linux-Xenial_3.6_amd64'
        elif str(job.number)[-2:] == ".3":
            job_config_str = 'Linux-Xenial_3.7_amd64'
        elif str(job.number)[-2:] == ".4":
            job_config_str = 'Linux-Bionic_3.7_amd64'
        elif str(job.number)[-2:] == ".5":
            job_config_str = 'Linux-Focal_3.7_amd64'
        elif str(job.number)[-2:] == ".6":
            job_config_str = 'Linux-Xenial_3.7_arm64'
        # elif str(job.number)[-2:] == ".7":
        #     job_config_str = 'Linux-Xenial_3.7_s390x'
        elif str(job.number)[-2:] == ".7":
            job_config_str = 'MacOS_3.7_amd64'
        elif str(job.number)[-2:] == ".8":
            job_config_str = 'Windows_3.7_amd64'
        else:
            raise ValueError("Invalid Configuration!")
        # print(job)
        processing_time = ((job.finished_at - job.started_at).total_seconds())
        return {"job_config": job_config_str, "status": job.state, "log": f"{job.get_log().content}",
                "processing_time": processing_time}

    def restart_job(self, job_id):
        job = self.travis.get_job(job_id)
        job.restart()

    def list_repos(self):
        repos = self.travis.get_repositories()
        repo_list = [repo.slug for repo in repos]
        return repo_list

    def __del__(self):
        pass
