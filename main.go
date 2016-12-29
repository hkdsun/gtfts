package main

import(
  "net"
  "log"
  "errors"
  "os/exec"
  "fmt"
)

func volumeUp(incr uint32) error {
  // err := exec.Command("amixer", fmt.Sprintf("sset Master %d\\%-", incr)).Run()
  err := exec.Command("/usr/bin/amixer", "sset", "Master", "1%+").Run()
  if err != nil {
    log.Print("Error while running external cmd: ")
    log.Println(err)
  }
  return nil
}

func volumeDown(incr uint32) error {
  // err := exec.Command("amixer", fmt.Sprintf("sset Master %d\\%-", incr)).Run()
  err := exec.Command("/usr/bin/amixer", "sset", "Master", "1%-").Run()
  if err != nil {
    log.Print("Error while running external cmd: ")
    log.Println(err)
  }
  return nil
}

func runCmd(buf []byte) error {
  if buf[0] != 'V' && (buf[1] != '-' || buf[1] != '+') {
    return errors.New(fmt.Sprintf("Command not recognized: %s", buf))
  }

  if buf[1] == '+' {
    return volumeUp(2)
  } else {
    return volumeDown(2)
  }
}

func handleConn(conn *net.TCPConn) {
  conn.SetKeepAlive(true)

  for {
    buf := make([]byte, 2)

    len, err := conn.Read(buf)
    if err != nil {
      log.Println("Connection broken")
      log.Println(err)
      conn.Close()
      break
    }

    err = runCmd(buf)
    if err != nil {
      log.Println("Error processing command")
      log.Println(err)
      conn.Close()
      break
    }

    log.Printf("Received message[%d] %s", len, buf)
  }
}

func main() {
  log.Println("Listening on port 8098")

  tcpAdd, err := net.ResolveTCPAddr("tcp", "0.0.0.0:8098")
  if err != nil {
    log.Fatal(err)
  }

  ln, err := net.ListenTCP("tcp", tcpAdd)
  if err != nil {
    log.Fatal(err)
  }

  for {
    conn, err := ln.AcceptTCP()
    if err != nil {
      log.Fatal(nil)
    }

    go handleConn(conn)
  }
}
