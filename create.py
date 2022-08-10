import sys
import os
from termcolor import cprint
from github import Github
from dotenv import load_dotenv

load_dotenv()
os.system('color')

def main():
    try:
        projectName = sys.argv[1]
        projectTemplate = sys.argv[2]

        # using an access token
        g = Github(os.getenv("GITHUB_TOKEN"))
        user = g.get_user()
        
        TEMPLATES = {
            "cra"       : f"npx create-react-app {projectName}",
            "cra-t"     : f"npx create-react-app {projectName} --template typescript",
            "next"      : f"npx create-next-app@latest {projectName}",
            "next-t"    : f"npx create-next-app@latest {projectName} --ts",
            "flutter"   : f"flutter create {projectName}"  
        }
        
        # create the new project inside projects directory
        # navigate to the new directory
        cprint(f"Creating project directory inside {os.getenv('PDIR')}", 'blue')
        _dir = os.getenv('PDIR')

        # create template project if specified inside arguments
        if projectTemplate in TEMPLATES:
            cprint(f"({projectTemplate}) template provided. Creating the template using {TEMPLATES[projectTemplate]} command", 'blue')
            os.chdir(_dir)
            os.system(TEMPLATES[projectTemplate])
            os.chdir(_dir + '/' + projectName)
        else:
            cprint("No template provided. Creating only a directory", 'blue')
            _dir += '/' + projectName
            os.makedirs(_dir)
            os.chdir(_dir)
            # add a readme file if project is initialized without a template
            os.system(f'echo #{projectName} >> README.md')
            cprint("Created a README.md inside directory", 'green')
        cprint("Done creating project directory", 'green')

        # currently inside the project directory
        # create remote repository
        cprint("Setting up remote repository", 'blue')
        user.create_repo(projectName)
        cprint("Done setting up remote repository", 'green')

        # create local repository and push changes
        cprint("Setting up local git repository", 'blue')
        GIT_COMMANDS = [
            'git init',
            f'git remote add origin https://github.com/{user.login}/{projectName}.git',
            'git add .',
            'git commit -m "Initial commit"',
            'git push origin main'
        ]
        # execute git commands
        for command in GIT_COMMANDS:
            os.system(command)
        cprint("Local repository in sync with remote repository", 'green')
        # done with project setup open vs code editor
        # assuming vs code is installed
        cprint("Done. Opening Vs Code", 'green')
        os.system("code .")
        cprint("Enjoy? :-P", 'white', 'on_blue')

    except Exception as e:
        print(e)
        cprint("Oops, something just broke", 'red')

if __name__ == "__main__":
    main()
