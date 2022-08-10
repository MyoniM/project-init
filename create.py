import time
import sys
import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

from dotenv import load_dotenv

load_dotenv()

LOGIN_URL = "https://github.com/login"
CREATE_REPOSITORY_URL = "https://github.com/new"

def createRepository(projectName):
    # disable logging on terminal
    options = webdriver.ChromeOptions()
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    browser = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    try:
        # log the user in
        print("Logging in with the provided credentials")
        browser.get(LOGIN_URL)
        usernameInput = browser.find_element(By.XPATH, "//*[@id='login_field']")
        usernameInput.send_keys(os.getenv('GITHUB_USER_USERNAME'))
        passwordInput = browser.find_element(By.XPATH, "//*[@id='password']")
        passwordInput.send_keys(os.getenv('GITHUB_USER_PASSWORD'))
        submitBtn = browser.find_element(By.XPATH, "//*[@id='login']/div[4]/form/div/input[12]")
        submitBtn.click()

        browser.get(CREATE_REPOSITORY_URL)
        # get githubUsername
        githubUsername = browser.find_element(By.XPATH, "//*[@id='repository-owner']")
        githubUsername = githubUsername.get_attribute('innerHTML').split("\n")[2].strip()
        
        # create the repository with the provided project name 
        repoName = browser.find_element(By.XPATH, "//*[@id='repository_name']")
        repoName.send_keys(projectName)
        time.sleep(3)
        submitBtn = browser.find_element(By.XPATH, "//*[@id='new_repository']/div[5]/button")
        submitBtn.click()

        if browser.current_url == CREATE_REPOSITORY_URL:
            print("Failed to create repository. Maybe you have a repository with the same name?")
            browser.quit()
            return {'success': False}

        print("Done creating remote repository")
        browser.quit()
        return {'success': True, "githubUsername": githubUsername}

    except Exception: 
        print("Some error occurred. Maybe check your credentials?")
        browser.quit()
        return {'success': False}

def main():
    try:
        projectName = sys.argv[1]
        projectTemplate = sys.argv[2]
        TEMPLATES = {
            "cra"       : f"npx create-react-app {projectName}",
            "cra-t"     : f"npx create-react-app {projectName} --template typescript",
            "next"      : f"npx create-next-app@latest {projectName}",
            "next-t"    : f"npx create-next-app@latest {projectName} --ts",
            "flutter"   : f"flutter create {projectName}"  
        }
        
        # create the new project inside projects directory
        # navigate to the new directory
        print(f"Creating project directory inside {os.getenv('PDIR')}")
        _dir = os.getenv('PDIR')

        # create template project if specified inside arguments
        if projectTemplate in TEMPLATES:
            print(f"({projectTemplate}) template provided. Creating the template using {TEMPLATES[projectTemplate]} command")
            os.chdir(_dir)
            os.system(TEMPLATES[projectTemplate])
            os.chdir(_dir + '/' + projectName)
        else:
            print("No template provided. Creating only a directory")
            _dir += '/' + projectName
            os.makedirs(_dir)
            os.chdir(_dir)
            # add a readme file if project is initialized without a template
            os.system(f'echo #{projectName} >> README.md')
            print("Created a README.md inside directory")
        print("Done creating project directory")

        # currently inside the project directory
        # create remote repository
        print("Setting up remote git repository")
        response = createRepository(projectName)
        
        # continue only if the response was successful
        if response["success"] == False: return
        
        # create local repository and push changes
        print("Setting up local git repository")
        GIT_COMMANDS = [
            'git init',
            f'git remote add origin https://github.com/{response["githubUsername"]}/{projectName}.git',
            'git add .',
            'git commit -m "Initial commit"',
            'echo Done creating local repository. Committing and pushing to remote repository'
            # by default main is the first branch
            'git push -u origin main'
        ]
        # execute git commands
        for command in GIT_COMMANDS:
            os.system(command)
        print("Local repository in sync with remote repository")
        # done with project setup open vs code editor
        # assuming vs code is installed
        print("Done. Opening Vs Code")
        os.system("code .")
        print("Happy Hacking (☞ﾟヮﾟ)☞")

    except Exception as e:
        print("======ERRRRRRRRRRR====")
        print(e)

if __name__ == "__main__":
    main()
