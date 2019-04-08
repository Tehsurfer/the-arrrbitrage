#git_hub.py is used to update all github file for the git projec: 'hugo-contrarian'
import base64
from github import Github
from github import InputGitTreeElement
import config
import settings

Path = settings.PATH

class git_hub:
    def __init__(self):
        pass

    def update(self):
            user = config.gituser
            password = config.gitpassword 
            g = Github(user,password)
            repo = g.get_user().get_repo('hugo-contrarian')
            file_list = [
                Path / 'index.html',
                Path / 'margin_table.html',
                Path / 'margin_table_with_depth.html'
            ]

            file_names = [
                'site/layouts/index.html',
                'site/layouts/products/single.html',
                'site/layouts/values/single.html'
            ]

            commit_message = 'python update'
            master_ref = repo.get_git_ref('heads/master')
            master_sha = master_ref.object.sha
            base_tree = repo.get_git_tree(master_sha)
            element_list = list()
            for i, entry in enumerate(file_list):
                with open(entry) as input_file:
                    data = input_file.read()
                element = InputGitTreeElement(file_names[i], '100644', 'blob', data)
                element_list.append(element)
            tree = repo.create_git_tree(element_list, base_tree)
            parent = repo.get_git_commit(master_sha)
            commit = repo.create_git_commit(commit_message, tree, [parent])
            master_ref.edit(commit.sha)
