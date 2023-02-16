# Photo-Album-Generator
Web application that takes your photos, allows for the creation of custom user tags. The administrator can then provide access to family members (users) to auto generate a digital photo album and a slide show of the best pictures based on the tags.

## Installation
Install Docker for your local machine from here ==> [Docker](https://www.docker.com)

## Run

### Build Docker
`docker build -t photo-album-gen:latest .`

### Run Docker
`docker run -p 5000:5000 --rm photo-album-gen:latest`

## Verify
### Hello Page

In the browser visit `http://localhost:5000/hello`
