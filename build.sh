docker buildx create --name photo-album-generator-builder --platform linux/amd64,linux/arm64,linux/arm/v7 --use

docker buildx build --platform linux/amd64,linux/arm64,linux/arm/v7 -t jigneshsatam/backend:latest --push backend/.

docker buildx build --platform linux/amd64,linux/arm64,linux/arm/v7 -t jigneshsatam/loadbalancer:latest --push loadbalancer/.

docker buildx build --platform linux/amd64,linux/arm64,linux/arm/v7 -t jigneshsatam/frontend:latest --push frontend/aespa/.
