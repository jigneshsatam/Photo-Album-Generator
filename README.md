# Photo-Album-Generator
Web application that takes your photos, allows for the creation of custom user tags. The administrator can then provide access to family members (users) to auto generate a digital photo album and a slide show of the best pictures based on the tags.

## Installation
Install Docker for your local machine from here ==> [Docker](https://www.docker.com)

## Run

### Build Docker
```
docker compose up --scale backend=3 -d
```

## Verify Build
### Hello Page

In the browser visit http://localhost:5000/hello

## Terminate Docker
### Stop Docker
```
docker compose down
```

### Stop Docker and Remove Volumnes
```
docker compose down -v
```

### Stop Docker and Remove all the images
```
docker compose down -v --rmi all
```
