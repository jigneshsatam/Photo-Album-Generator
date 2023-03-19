package main

import (
	"bufio"
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

//go:embed mac-docker.sh
var macDockerPart string

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
		runBashCommand(macDockerPart)
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

	runBashCommand("mkdir -p Photo-Generator-Pictures")

	compose := "echo '" + dockerCompse + "' > docker-compose.yml"
	// print(compose)
	runBashCommand(compose)

	// runBashCommand("echo " + dockerCompse + " > docker-compose.yml")
	runBashCommand("docker compose up -d --scale backend=3")

	runBashCommand("open http://localhost:4200")
}

func shutdownDocker() {
	stop := "docker compose down -v"
	runBashCommand(stop)
	runBashCommand("rm docker-compose.yml")
}

func runBashCommand(command string) {
	cmd := exec.Command("bash")
	cmd.Stdin = strings.NewReader(command)

	// stdout, err := c.StdoutPipe()
	// c.Stderr = c.Stdout
	// if err != nil {
	// 	fmt.Println(err)
	// }

	// if err = c.Start(); err != nil {
	// 	fmt.Println(err)
	// }

	// for {
	// 	t := make([]byte, 1024)
	// 	_, err := stdout.Read(t)
	// 	fmt.Print(string(t))
	// 	if err != nil {
	// 		fmt.Println(err)
	// 	}
	// 	time.Sleep(1 * time.Second)
	// }

	// ======== working start ========
	stdout, _ := cmd.StdoutPipe()
	cmd.Start()
	scanner := bufio.NewScanner(stdout)
	// scanner.Split(bufio.ScanWords)
	for scanner.Scan() {
		m := scanner.Text()
		fmt.Println(m)
	}
	cmd.Wait()
	// ======== working end ========

	// b, e := cmd.Output()
	// if e != nil {
	// 	fmt.Println(e)
	// }
	// fmt.Println(string(b))
}
