# Photo-Album-Generator
Web application that takes your photos, allows for the creation of custom user tags. The administrator can then provide access to family members (users) to auto generate a digital photo album and a slide show of the best pictures based on the tags.

## Table of Contents
- [Installation](#Installation)
  * [Run](#Run)
    * [Build Docker](#Build-Docker)
  * [Verify Build](#Verify-Build)
    * [Hello Page](#Hello-Page)
  * [Terminate Docker](#Terminate-Docker)
    * [Stop Docker](#Stop-Docker)
    * [Stop Docker and Remove Volumes](#Stop-Docker-and-Remove-Volumes)
    * [Stop Docker and Remove all the images](#Stop-Docker-and-Remove-all-the-images)
- [Project Management](#Project-Management)
  * [Project Board](#Project-Board)

## User Installation Guide
[User Installation Guide](https://farishah.github.io/Photo-Album-Generator/Installation_Guide.pdf)

## Developer Installation Guide:
1. Clone the Main branch of this repository.
2. Next, install Docker on your local machine from here ==> [Docker](https://www.docker.com)
3. Make sure the Docker Application is open on your computer.
4. Open the cloned project onto your preferred choice of IDE (VS Code is recommended).
5. Now that your IDE contains the project, navigate to the IDE terminal and build the docker using the commands below.

## Run

### Build Docker
```
docker compose up -d --scale backend=3
```

## Verify Build

### Hello Page
In the browser visit http://localhost:4200

## Terminate Docker

### Stop Docker
```
docker compose down
```

### Stop Docker and Remove Volumes
```
docker compose down -v
```

### Stop Docker and Remove all the images
```
docker compose down -v --rmi all
```

## Project Management

### [Project Board](https://github.com/users/jigneshsatam/projects/1/views/1)
