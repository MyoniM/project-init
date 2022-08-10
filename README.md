### setup: 
```bash
git clone "https://github.com/MyoniM/project-init.git"
cd project-init
pip install -r requirements.txt

add "project-init" folder directory to system environment variables(PATH)

create .env file and add these fields
GITHUB_TOKEN="create personal token on github with repo_deployment, public_repo and read:user scope"
PDIR='the directory to store your projects'

```

### Usage:
```bash
Command to run the program

'create <project_name>'
'create <project_name> -t <template>'   - to add project templates
```
