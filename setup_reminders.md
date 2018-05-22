Since this repository is being used by relatively fresh users of git, I thought it might be nice to post a few of the commands we use.

# Setting Up the Fork
* Make your fork of the repository on github
  - On your terminal (may need to go get git bash)
  - git clone [url of YOUR fork from github]
  - change into your cloned directory (cd name of the project)
  - git remote add upstream [url of the original repository on github]

# Syncing your fork
* git fetch upstream
* git checkout master
* git merge upstream/master

# Commit your new merges or any changes
* git commit -m "put your message here"
* git push
