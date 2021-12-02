# -*- coding: utf-8 -*-
"""
...........
@desc:
@date:
@author:
@license:
@contact:

@para:
"""
import os
import hashlib
import subprocess
from .decorator import stages
from datetime import datetime
from git import Repo, NoSuchPathError, InvalidGitRepositoryError, GitCommandError, CheckoutError
from .display import Display

display = Display()


class BuildError(OSError):
    def __init__(self, message) -> None:
        Exception.__init__(self, message)

    def __str__(self) -> str:
        return Exception.__str__(self)


class Project(object):

    def __init__(self, name: str, remote_url: str, local_repo: str, desc: str = None):
        self.name = name
        self._remote_url = remote_url
        self.desc = desc

        try:
            self.repo = Repo(local_repo)
        except (NoSuchPathError, InvalidGitRepositoryError):
            self.repo = Repo.init(local_repo, mkdir=True)
            display.info(self.repo)
            origin = self.repo.create_remote('origin', remote_url)
            display.info(origin)
            origin.fetch()

    @stages('同步代码仓库')
    def sync(self, branch: str, reset: bool = False, remote: str = 'origin/master') -> [bool, Exception]:
        """同步代码仓库获取更新

        指定仓库分支，在拉取代码仓库前对仓库是否需要重置进行判断

        Args:
            branch: 指定代码分支
            reset:  Optional，如果需要重置仓库，默认值False
            remote: 未指定哈希值，默认选择origin/master分支回滚更新

        Returns:
            返回仓库同步结果，如果超时或需要登陆同步仓库失败，则
            返回False

        Raises:
            GitCommandError:
            CheckoutError:
        """
        if reset or self.repo.is_dirty():
            display.info('repo is dirty')
            output = self.repo.git.reset('--hard', remote)
            display.info(f'{output}')

        output = self.repo.git.checkout(branch)
        display.info(output)
        display.info(f'切换为{branch}分支')
        output = self.repo.git.pull()
        display.info(output)
        display.info('代码仓库更新成功')
        return False

    @stages('获取commit hash')
    def get_head(self) -> str:
        """获取最后一次代码提交的hash值"""
        head_hash = self.repo.head.object.hexsha
        display.info(f'commit hash: {head_hash}')
        return head_hash

    @stages('diff代码')
    def diff(self, previous_commit_hash: str = None) -> str:
        """代码比对"""
        if previous_commit_hash is None:
            previous_commit_hash = list(self.repo.iter_commits())[1].hexsha

        head_hash = self.repo.head.object.hexsha
        diffs = self.repo.git.diff(previous_commit_hash, head_hash)
        assert isinstance(diffs, str)
        display.info(f'Git_logs: \n {diffs}')
        return diffs

    @stages('changes')
    def change_logs(self):
        pass

    @stages('代码提交者信息')
    def old_get_committer_info(self) -> tuple[str, str, str, str]:
        """获取最近一次代码提交者的信息"""
        author = self.repo.head.reference.commit.author.name
        email = self.repo.head.reference.commit.author.email
        date = datetime.fromtimestamp(
            self.repo.head.reference.commit.committed_date)
        message = self.repo.head.reference.commit.message
        commit_info = (author, email, date.ctime(), message)

        return commit_info

    class Artifact(object):
        def __init__(self, name: str, path: str, version: str = None, **tag):
            self.name = name
            self.path = path
            self.version = version
            self.build_date = ''

        @stages('构建')
        def build(self, build_dir: str, commands: [str], rename: str = None, envs: list = None):
            """代码构建

            获得shell命令并到指定目录下运行，还可以同时指定构建的环境变量

            Args:
                build_dir: 代码构建的绝对路径
                commands: shell命令必须是一个List，例如：
                    npm install
                    npm run build
                    传入cmd中应该切割为[["npm", "install"], ["npm", "run" "build"]
                rename: 文件重命名
                envs: 一个环境变量List

            Returns:
                  build_process
            """
            if os.path.exists(build_dir):
                os.chdir(build_dir)
                self.build_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                build_process = subprocess.run(commands, env=envs, capture_output=True, shell=True)
                if build_process.returncode:
                    display.error(f'构建失败: \n{build_process.stderr.decode()}')
                else:
                    display.info('构建完成')
                if rename:
                    os.renames(self.name, rename)
            else:
                raise FileExistsError(f'{build_dir}路径不存在')

        @stages('压缩文件')
        def archive(self, compress_format: str) -> str:
            pass

        @stages('checksum')
        def checksum(self) -> dict:
            """checksum 校验和

            计算构建后artifact或打包后archive的MD5、SHA1、SHA512

            Args:
            file_path: 文件绝对路径
            """
            if os.path.exists(self.path):
                with open(self.path, 'rb') as file:
                    chunk = file.read()
                    md5 = hashlib.md5(chunk).hexdigest()
                    sha1 = hashlib.sha1(chunk).hexdigest()
                    sha512 = hashlib.sha512(chunk).hexdigest()
                    _sum = {'md5': md5, 'sha1': sha1, 'sha512': sha512}
                    return _sum

        @stages('容器化')
        def containerized(self, dockerfiles: list, build_dir: str, image_repo_url: str, namespace: str) -> None:
            """构建docker镜像

            推送容器到阿里云镜像仓库，镜像名：{仓库地址}/{namespace}/{项目}/{版本号}

            Args:
                dockerfiles: dockerfile 键值对 k:docker镜像名称， v：dockerfile绝对路径
                build_dir: 构建路径
                image_repo_url: 镜像仓库的域名地址
                namespace: 根据部署环境命名命名空间

            Returns:
                None
            """
            for df in dockerfiles:
                name = df.split(':')[0]
                path = df.split(':')[1]
                if not os.path.exists(path):
                    raise FileExistsError
                display.info(f'读取Dockerfile: {path}')
                image_tag = f'{image_repo_url}/{namespace}/{name}'
                display.info(f'docker tag: {image_tag}')
                if self.version is None:
                    image_tag += ':latest'
                else:
                    image_tag += f':{self.version}'

                docker_build_process = subprocess.run(f'docker build -f {path} -t {image_tag} {build_dir}',
                                                      capture_output=True, shell=True)
                if docker_build_process.returncode:
                    display.error(f'容器封装失败{docker_build_process.stderr}')
                else:
                    display.info('容器封装完成')

                docker_push_process = subprocess.run(f'docker push {image_tag}', capture_output=True, shell=True)
                if docker_push_process.returncode:
                    display.error(f'docker push failed :{docker_push_process.stderr}')
                else:
                    display.info(f'容器地址: {image_tag}')
                return None
