//go:generate cp ../postgres-sql/create-tables.sql create-tables.sql

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
var macDocker string

//go:embed windows-docker.sh
var windowsDocker string

//go:embed create-tables.sql
var schema string

//go:embed docker-compose-dev.yml
var dockerCompse string

func main() {
	createSchema()
	switch runtime.GOOS {
	case "windows":
		defer shutdownDockerWindows()
		fmt.Println("Hello from Windows -", runtime.GOARCH)
		runBashCommand(windowsDocker)
		startDockerWindows()
	case "linux":
		defer shutdownDocker()
		fmt.Println("Hello from Linux -", runtime.GOARCH)
		fmt.Println("Installing docker if not present...")
		runBashCommand(linuxDocker)
		startDocker()
		// runBashCommand(linuxDocker)
	case "darwin":
		defer shutdownDocker()
		fmt.Println("Hello from Darwin(Mac) -", runtime.GOARCH)
		type output struct {
			out []byte
			err error
		}

		// ch := make(chan output)
		// go func() {
		// 	// cmd := exec.Command("sleep", "1")
		// 	// cmd := exec.Command("sleep", "5")
		// 	cmd := exec.Command(".", "/usr/bin/open -a Docker")
		// 	out, err := cmd.CombinedOutput()
		// 	ch <- output{out, err}
		// }()

		// x := <-ch
		// fmt.Printf("program done; out: %q\n", string(x.out))
		// if x.err != nil {
		// 	fmt.Printf("program errored: %s\n", x.err)
		// }

		runBashCommand(macDocker)
		startDocker()
	}

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

func startDockerWindows() {
	fmt.Println("Starting Application on Windows...")
	createDockerComposeYAML()
	runBashCommandWindows("docker compose up -d --scale backend=3")
	runBashCommandWindows("start http://localhost:4200")
}

func shutdownDocker() {
	stop := "docker compose down -v"
	runBashCommand(stop)
	runBashCommand("rm docker-compose.yml")
}

func shutdownDockerWindows() {
	stop := "docker compose down -v"
	runBashCommandWindows(stop)
	runBashCommandWindows("rm docker-compose.yml")
}

func createDockerComposeYAML() {
	err := os.WriteFile("docker-compose.yml", []byte(dockerCompse), 0644)
	if err != nil {
		fmt.Println("Error: ", err)
	}
}

func createSchema() {
	err := os.WriteFile("Photo-Generator-Pictures/create-tables.sql", []byte(schema), 0644)
	if err != nil {
		fmt.Println("Error: ", err)
	}
}

// func runBashCommandWindows() {
// 	// dockerCompse1 := "name: photo-album-generator\nversion: 3.9"
// 	// testFile, err := os.Create("docker-compose.yml")
// 	// if err != nil {
// 	// 	fmt.Println("Error: ", err)
// 	// }

// 	// d1 := []byte("hello\ngo\n")
// 	err := os.WriteFile("docker-compose.yml", []byte(dockerCompse), 0644)
// 	if err != nil {
// 		fmt.Println("Error: ", err)
// 	}

// 	// cmd := exec.Command("cmd", "/K", "echo "+dockerCompse1)

// 	// cmd.Stdout = testFile

// 	// // out, err := cmd.Output()

// 	// err = cmd.Start()
// 	// if err != nil {
// 	// 	fmt.Println("Error: ", err)
// 	// }

// 	// cmd.Wait()

// 	// fmt.Println("output: ", string(out))

// }

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

func runBashCommandWindows(comm string) {
	cmd := exec.Command("cmd", "/K", comm)
	out, err := cmd.Output()
	if err != nil {
		fmt.Println("Error: ", err)
	}
	fmt.Println("output: ", string(out))

	// cmd := exec.Command("bash")
	// // cmd.Stdin = strings.NewReader(command)
	// stdout, _ := cmd.StdoutPipe()
	// cmd.Start()
	// scanner := bufio.NewScanner(stdout)
	// // scanner.Split(bufio.ScanWords)
	// for scanner.Scan() {
	// 	m := scanner.Text()
	// 	fmt.Println(m)
	// }
	// cmd.Wait()
}
