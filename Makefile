

build: clean \
	copy-files \
	macos-build-m1 \
	macos-build-intel \
	linux-64-build linux-32-build \
	windows-64-build windows-32-build

.PHONY: build-prod
build-prod: clean \
	copy-files \
	linux-64-build linux-32-build \
	windows-64-build windows-32-build \
	macos-build-m1 macos-build-intel

.PHONY: linux-64-build
linux-64-build:
	GOOS=linux GOARCH=amd64 go build -o packaging/Photo-Album-Generator-linux-64 packaging/main.go
	mv packaging/Photo-Album-Generator-linux-64 packaging/build/

.PHONY: linux-32-build
linux-32-build:
	GOOS=linux GOARCH=386 go build -o packaging/Photo-Album-Generator-linux-386 packaging/main.go
	mv packaging/Photo-Album-Generator-linux-386 packaging/build/

.PHONY: windows-64-build
windows-64-build:
	GOOS=windows GOARCH=amd64 go build -o packaging/Photo-Album-Generator-win-64.exe packaging/main.go
	mv packaging/Photo-Album-Generator-win-64.exe packaging/build/

.PHONY: windows-32-build
windows-32-build:
	GOOS=windows GOARCH=386 go build -o packaging/Photo-Album-Generator-win-32.exe packaging/main.go
	mv packaging/Photo-Album-Generator-win-32.exe packaging/build/

.PHONY: macos-build-m1
macos-build-m1:
	mkdir -p packaging/Photo-Album-Generator-macos-arm64.app/Contents/MacOS
	cp packaging/Info.plist packaging/Photo-Album-Generator-macos-arm64.app/Contents/
	GOOS=darwin GOARCH=arm64 go build -o packaging/Photo-Album-Generator-macos-arm64.app/Contents/MacOS/Photo-Album-Generator packaging/main.go
	mv packaging/Photo-Album-Generator-macos-arm64.app packaging/build/

	GOOS=darwin GOARCH=arm64 go build -o packaging/Photo-Album-Generator-macos-arm64 packaging/main.go
	mv packaging/Photo-Album-Generator-macos-arm64 packaging/build/

	rm -f test_folder/Photo-Album-Generator-macos-arm64
	cp packaging/build/Photo-Album-Generator-macos-arm64 test_folder/


.PHONY: macos-build-intel
macos-build-intel:
	mkdir -p packaging/Photo-Album-Generator-intel.app/Contents/MacOS
	GOOS=darwin GOARCH=amd64 go build -o packaging/Photo-Album-Generator-intel.app/Contents/MacOS/Photo-Album-Generator packaging/main.go
	mv packaging/Photo-Album-Generator-intel.app packaging/build/

	GOOS=darwin GOARCH=amd64 go build -o packaging/Photo-Album-Generator-intel-amd64 packaging/main.go
	mv packaging/Photo-Album-Generator-intel-amd64 packaging/build/

.PHONY: clean
clean:
	rm -r packaging/build/Photo-Album-Generator* && echo || echo

.PHONY: copy-files
copy-files:
	go generate packaging/main.go

copy:
	# scp -i ~/.ssh/SEED-VM_key.pem get-docker.sh jigneshsatam@20.120.94.114:/home/jigneshsatam

	# scp -i ~/.ssh/SEED-VM_key.pem -r docker-compose.yml jigneshsatam@20.120.94.114:/home/jigneshsatam

	# scp -i ~/.ssh/SEED-VM_key.pem -r ../../Photo-Album-Generator/packaging/linux-docker.sh jigneshsatam@20.120.94.114:/home/jigneshsatam

	scp -i ~/.ssh/SEED-VM_key.pem -r packaging/build/Photo-Album-Generator-linux-64 jigneshsatam@20.120.94.114:/home/jigneshsatam

.PHONY: run
run: stop-clean
	docker compose up

run-deamon:
	docker compose up -d --scale backend=3
	open http://localhost:4200/


stop:
	docker compose down


stop-clean:
	docker compose down -v --rmi all
