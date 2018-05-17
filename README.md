# GenisysEvals
This is the capstone project I worked on at Weber State. Our team worked on the Evaluations section of the site, and I specifically worked on the My Reports / My Evals section of the site.

## Build Setup

### Source Code
Download Repo

### Docker
Download Docker

Restart Docker to enable HyperV (Windows Only)

### To Run
Open the repo in your favorite IDE (preferably WebStorm)

Navigate to the repo in the terminal or command line

#### Windows users may need to restart docker

Run `docker-compose build`

Run `docker-compose up`

Open `localhost` in your browser

### End of Day
Commit and push your branch to enable others to look at your branch

### Start of Day
Pull from master to get the latest code

### Useful Docker Tips
#### How to install an npm node module

`cd whatYouNamedTheRepoFolder/frontend`

`npm install --save <module-name>`

or if it is only for development

`npm install --save-dev <module-name>`

`cd ../`

`docker-compose build`


#### Useful commands to run python commands in the backend

`docker-compose run --rm backend python manage.py 'your command'`


### When docker is broken
`docker-compose down`

`docker system prune -a`

`docker ps`

`docker rm <any containers listed from ps>`

`docker volume ls`

`docker volume rm <any volume names>`

`docker-compose build`

`docker-compose up`


