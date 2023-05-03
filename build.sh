# docker buildx rm photo-album-generator-builder

docker buildx create --name photo-album-generator-builder --platform linux/amd64,linux/arm64,linux/arm/v7 --use

docker buildx build --platform linux/amd64,linux/arm64,linux/arm/v7 -t jigneshsatam/backend:latest --push backend/.

docker buildx build --platform linux/amd64,linux/arm64,linux/arm/v7 -t jigneshsatam/loadbalancer:latest --push loadbalancer/.

docker buildx build --platform linux/amd64,linux/arm64,linux/arm/v7 -t jigneshsatam/frontend:latest --push frontend/.



# docker buildx create --name photo-album-generator-builder --platform linux/arm64,linux/amd64,linux/riscv64,linux/ppc64le,linux/s390x,linux/386,linux/arm/v7,linux/arm/v6 --use

# docker buildx build --platform linux/arm64,linux/amd64,linux/ppc64le,linux/s390x,linux/386,linux/arm/v7,linux/arm/v6 -t jigneshsatam/backend:latest --push backend/.

# docker buildx build --platform linux/arm64,linux/amd64,linux/ppc64le,linux/s390x,linux/386,linux/arm/v7,linux/arm/v6 -t jigneshsatam/loadbalancer:latest --push loadbalancer/.

# docker buildx build --platform linux/arm64,linux/amd64,linux/ppc64le,linux/s390x,linux/arm/v7,linux/arm/v6 -t jigneshsatam/frontend:latest --push frontend/aespa/.
