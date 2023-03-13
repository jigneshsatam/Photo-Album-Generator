
# build: clean \
# 	macos-build-m1
# # macos-build-intel

build: clean \
	linux-64-build linux-32-build \
	windows-64-build windows-32-build \
	macos-build-m1 macos-build-intel

.PHONY: linux-64-build
linux-64-build:
	GOOS=linux GOARCH=amd64 go build -o Photo-Album-Generator-linux-64 main.go
	mv Photo-Album-Generator-linux-64 build/

.PHONY: linux-32-build
linux-32-build:
	GOOS=linux GOARCH=386 go build -o Photo-Album-Generator-linux-386 main.go
	mv Photo-Album-Generator-linux-386 build/

.PHONY: windows-64-build
windows-64-build:
	GOOS=windows GOARCH=amd64 go build -o Photo-Album-Generator-64.exe main.go
	mv Photo-Album-Generator-64.exe build/

.PHONY: windows-32-build
windows-32-build:
	GOOS=windows GOARCH=386 go build -o Photo-Album-Generator-32.exe main.go
	mv Photo-Album-Generator-32.exe build/

.PHONY: macos-build-m1
macos-build-m1:
	mkdir -p Photo-Album-Generator-macos-arm64.app/Contents/MacOS
	cp Info.plist Photo-Album-Generator-macos-arm64.app/Contents/
	GOOS=darwin GOARCH=arm64 go build -o Photo-Album-Generator-macos-arm64.app/Contents/MacOS/Photo-Album-Generator main.go
	mv Photo-Album-Generator-macos-arm64.app build/

	# mkdir -p helloworld.app/Contents/MacOS
	# go build -o helloworld.app/Contents/MacOS/helloworld main.go

	# GOOS=darwin GOARCH=arm64 go build -o Photo-Album-Generator-macos-arm64 main.go


.PHONY: macos-build-intel
macos-build-intel:
	mkdir -p Photo-Album-Generator-intel.app/Contents/MacOS
	GOOS=darwin GOARCH=amd64 go build -o Photo-Album-Generator-intel.app/Contents/MacOS/Photo-Album-Generator main.go
	mv Photo-Album-Generator-intel.app build/

.PHONY: clean
clean:
	rm -r build/Photo-Album-Generator* && echo || echo

copy:
	# scp -i ~/.ssh/SEED-VM_key.pem get-docker.sh jigneshsatam@20.120.94.114:/home/jigneshsatam

	# scp -i ~/.ssh/SEED-VM_key.pem -r docker-compose.yml jigneshsatam@20.120.94.114:/home/jigneshsatam

	# scp -i ~/.ssh/SEED-VM_key.pem -r ../../Photo-Album-Generator/packaging/linux-docker.sh jigneshsatam@20.120.94.114:/home/jigneshsatam

	scp -i ~/.ssh/SEED-VM_key.pem -r build/Photo-Album-Generator-linux-64 jigneshsatam@20.120.94.114:/home/jigneshsatam
