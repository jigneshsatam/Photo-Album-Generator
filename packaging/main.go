package main

import (
	_ "embed"
	"fmt"
	"os"
	"os/exec"
	"os/signal"
	"runtime"
	"strings"
	"syscall"
)

//go:embed get-docker.sh
var script string

//go:embed linux-docker.sh
var linuxDocker string

// //go:embed linux-docker-part-2.sh
// var linuxDockerPart2 string

//go:embed docker-compose-dev.yml
var dockerCompse string

func main() {
	defer shutdownDocker()

	switch runtime.GOOS {
	case "windows":
		fmt.Println("Hello from Windows -", runtime.GOARCH)
	case "linux":
		fmt.Println("Hello from Linux -", runtime.GOARCH)
		fmt.Println("Installing docker if not present...")
		runBashCommand(linuxDocker)
		// runBashCommand(linuxDocker)
	case "darwin":
		fmt.Println("Hello from Darwin(Mac) -", runtime.GOARCH)
	}

	startDocker()

	done := make(chan os.Signal, 1)
	signal.Notify(done, syscall.SIGINT, syscall.SIGTERM)
	fmt.Println("Press ctrl+c to stop")
	<-done // Will block here until user hits ctrl+c

}

func startDocker() {
	fmt.Println("Starting Application...")

	runBashCommand("touch docker-compose.yml")
	compose := "echo '" + dockerCompse + "' > docker-compose.yml"
	// print(compose)
	runBashCommand(compose)

	// runBashCommand("echo " + dockerCompse + " > docker-compose.yml")
	runBashCommand("docker compose up -d --scale backend=3")

	runBashCommand("open http://localhost:8827")
}

func shutdownDocker() {
	stop := "docker compose down -v"
	runBashCommand(stop)
	runBashCommand("rm docker-compose.yml")
}

func runBashCommand(command string) {
	c := exec.Command("bash")
	c.Stdin = strings.NewReader(command)

	b, e := c.Output()
	if e != nil {
		fmt.Println(e)
	}
	fmt.Println(string(b))
}
