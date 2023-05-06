//go:generate cp ../postgres-sql/create-tables.sql create-tables.sql

package main

import (
	"bufio"
	_ "embed"
	"fmt"
	"io"
	"net/http"
	"os"
	"os/exec"
	"os/signal"
	"runtime"
	"strings"
	"syscall"
	"time"
)

//go:embed get-docker.sh
var script string

//go:embed linux-docker.sh
var linuxDocker string

//go:embed mac-docker.sh
var macDocker string

//go:embed windows-docker.bat
var windowsDocker string

//go:embed create-tables.sql
var schema string

//go:embed docker-compose-dev.yml
var dockerCompse string

// var stop = "docker compose down -v --rmi all"
var stop = "docker compose down"

func main() {
	createUtilsDir()
	createSchema()
	switch runtime.GOOS {
	case "windows":
		defer shutdownDockerWindows()
		fmt.Println("Hello from Windows -", runtime.GOARCH)
		// runBashCommand(windowsDocker)
		startDockerWindows()
		startApplicationWindows()
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
	time.Sleep(30 * time.Second)
	runBashCommand("open http://localhost:4200")
}

func startDockerWindows() {
	// downloadDocker := "curl.exe --output 'Docker Desktop Installer.exe' --url https://desktop.docker.com/win/main/amd64/Docker%20Desktop%20Installer.exe"
	// runBashCommandWindowsWithoutCMD(downloadDocker)
	// fmt.Println("Installing docker...")
	// installingDocker := `start /w \"\" \"Docker Desktop Installer.exe\" install`
	// runBashCommandWindowsWithoutCMD(installingDocker)
	// fmt.Println("Starting docker...")
	// stratDocker := "start /B \"\" \"C:\\Program Files\\Docker\\Docker\\Docker Desktop.exe\""
	// batFile := "windows-docker.bat"

	// ===== Working code ====
	// downloadDockerExe()
	// err = os.WriteFile("windows-docker.bat", []byte(windowsDocker), 0644)
	// if err != nil {
	// 	fmt.Println("Error: ", err)
	// }
	// runBashCommandWindows(`start /w windows-docker.bat`)
	// runBashCommandWindows("del windows-docker.bat")
	// ===== Working code ====

	// downloadDockerExe()
	// err := exec.Command("cmd", "/K", "start", "/w", "''", "'Docker Desktop Installer.exe' install").Run()
	// if err != nil {
	// 	fmt.Println("Error in *** Docker Installing *** ", err)
	// }

	// Check if Docker is installed
	fmt.Println("====== Docker on Windows ======")
	output, err := exec.Command("docker", "version").Output()
	if err != nil {
		if strings.Contains(err.Error(), "executable file not found") {
			cmd := exec.Command("cmd", "/K", "wsl --status")
			output10, err10 := cmd.CombinedOutput()
			if err10 != nil {
				fmt.Println("====== Updating WSL ======")
				output2, err2 := exec.Command("cmd", "/K", "wsl --install -d Ubuntu").Output()
				if err2 != nil {
					fmt.Println("Error in *** Updating WSL *** ")
					fmt.Println("Error:: ==> ", err.Error())
				}
				fmt.Println("Output:: ==> ", string(output2))
				fmt.Println("====== WSL Updated successfully ======")
			}
			fmt.Println("Output:: ==> ", string(output10))

			fmt.Println("====== Docker Installation Started ======")

			fmt.Println("Docker is not installed on this machine.")
			fmt.Println("====== Downloading Docker ======")
			downloadDockerExe()
			fmt.Println("====== Docker Download Completed ======")
			fmt.Println("====== Installing Docker ======")

			output, err = exec.Command("cmd.exe", "/K", "start /w Docker-Desktop-Installer.exe install").Output()
			if err != nil {
				fmt.Println("Error in *** Docker Installing *** ")
				fmt.Println("Error:: ==> ", err.Error())
			}
			fmt.Println("Output:: ==> ", string(output))
			fmt.Println("====== Docker Installation Completed ======")
		} else {
			fmt.Println("Docker is installed on this machine. Might not running.")
			fmt.Println("Check if Docker is installed Error")
			fmt.Println("Error in *** Docker Checking *** ")
			fmt.Println("Error:: ==> ", err.Error())
		}
	}

	output, err = exec.Command("docker", "ps").Output()
	if err != nil {
		fmt.Println("====== Starting Docker on Windows ======")

		err = os.WriteFile("windows-docker.bat", []byte(windowsDocker), 0644)
		if err != nil {
			fmt.Println("Error: ", err)
		}
		// cmd := exec.Command("cmd", "/c", "start /wait /b cmd /c windows-docker.bat")
		// cmd := exec.Command("cmd", "/K", "start /wait /b cmd /c windows-docker.bat")

		// cmd := exec.Command("cmd", "/K", "start /wait /b cmd /c windows-docker.bat")

		// fmt.Println("windowsDocker ==> ", windowsDocker)
		// cmd := exec.Command("cmd", "/K", windowsDocker)

		// cmd := exec.Command("cmd", "/K", `start /b C:\Program Files\Docker\Docker\Docker Desktop.exe`)
		ch := make(chan bool)
		go func(chan bool) {
			fmt.Println("In the goroutine.....")
			cmd := exec.Command("cmd", "/k", `C:\Program Files\Docker\Docker\Docker Desktop.exe`)
			op, err := cmd.CombinedOutput()
			if err != nil {
				fmt.Println("Goroutine Error:: ", err)
			}
			fmt.Println("Goroutine Output:: ", string(op))
			time.Sleep(20 * time.Second)
			ch <- true
		}(ch)

		for {
			fmt.Println("In the for loop...")
			output30, err30 := exec.Command("docker", "ps").Output()
			if err30 == nil {
				fmt.Println("For loop Output:: ", string(output30))
				break
			}
			fmt.Println("For loop Error:: ", err30)
			time.Sleep(2 * time.Second)
		}
		// <-ch
		// runBashCommandWindows(`start windows-docker.bat`)
		runBashCommandWindows("del windows-docker.bat")

		// // start := `start /B "" "C:\Program Files\Docker\Docker\Docker Desktop.exe`
		// // cmd := exec.Command("cmd", "/K", "start /B dockerd")
		// // cmd := exec.Command("cmd", "/c", "start", "/B", `""`, `"%ProgramFiles%\Docker\Docker\Docker Desktop.exe"`)
		// // cmd := exec.Command("cmd", "/c", "start", "/B", `""`, `"C:\Program Files\Docker\Docker\Docker Desktop.exe"`)
		// // cmd := exec.Command("C:\\Program Files\\Docker\\Docker\\Docker Desktop.exe")
		// // cmd := exec.Command("cmd", "/K", "start", "/B", "/wait", "C:\\Program Files\\Docker\\Docker\\Docker Desktop.exe")
		// // cmd := exec.Command("cmd", "/c", "start", "Docker Desktop")
		// cmd := exec.Command("cmd", "/K", "start", "\"\"", "/B", "C:\\Program Files\\Docker\\Docker\\Docker Desktop.exe")
		// err := cmd.Run()
		// output, err = cmd.CombinedOutput()
		// if err != nil {
		// 	fmt.Println("Error in *** Starting Docker *** ", err)
		// }
		// fmt.Println("Output:: ==> ", string(output))
		fmt.Println("====== Docker Started ======")
	} else {
		fmt.Println("Output:: ==> ", string(output))
		fmt.Println("====== Docker is Already Running ======")
	}
}

func startApplicationWindows() {
	fmt.Println("Starting Application on Windows...")
	createDockerComposeYAML()
	runBashCommandWindows("docker compose up -d --scale backend=3")
	time.Sleep(3 * time.Second)
	runBashCommandWindows("start http://localhost:4200")
}

func shutdownDocker() {
	runBashCommand(stop)
	runBashCommand("rm docker-compose.yml")
}

func shutdownDockerWindows() {
	runBashCommandWindows(stop)
	runBashCommandWindows("del docker-compose.yml")
}

func createDockerComposeYAML() {
	err := os.WriteFile("docker-compose.yml", []byte(dockerCompse), 0644)
	if err != nil {
		fmt.Println("Error: ", err)
	}
}

func createUtilsDir() {
	path := ".Photo-Generator-Pictures-utils"
	err := os.MkdirAll(path, os.ModePerm)
	if err != nil {
		fmt.Println(err)
	}
}

func createSchema() {
	err := os.WriteFile(".Photo-Generator-Pictures-utils/create-tables.sql", []byte(schema), 0644)
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

func runBashCommandWindowsWithoutCMD(comm string) {
	cmd := exec.Command(comm)
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

func downloadDockerExe() {
	out, err := os.Create("Docker-Desktop-Installer.exe")
	if err != nil {
		fmt.Println(err)
	}
	defer out.Close()

	resp, err := http.Get("https://desktop.docker.com/win/stable/Docker%20Desktop%20Installer.exe")
	// https://desktop.docker.com/win/main/amd64/Docker%20Desktop%20Installer.exe
	if err != nil {
		fmt.Println(err)
	}
	defer resp.Body.Close()

	_, err = io.Copy(out, resp.Body)
	if err != nil {
		fmt.Println(err)
	}
}
