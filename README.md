# PySpark Project on WSL & Docker

This project contains a sample PySpark application that can be run in two different development environments:
1.  Natively in a Windows Subsystem for Linux (WSL) environment.
2.  In a self-contained Docker container using VS Code Dev Containers.

## Prerequisites

- **For WSL**: Windows 11 with WSL enabled and an Ubuntu distribution installed.
- **For Docker**: Docker Desktop installed and running.
- **Editor**: Visual Studio Code.

---

## Setup Option 1: Native WSL Environment

### 1.1. One-Time System Setup

This script prepares your entire WSL system for PySpark development. Run it once in your Ubuntu terminal to install Java, Apache Spark, and other necessary tools.

```bash
#!/bin/bash
# Exit immediately if a command exits with a non-zero status.
set -e

# --- Install System Dependencies ---
echo "Updating package lists and installing dependencies..."
sudo apt update
sudo apt install -y default-jdk python3-pip python3-venv wget

# --- Download and Unpack Apache Spark ---
echo "Downloading and unpacking Spark..."
cd ~
wget [https://archive.apache.org/dist/spark/spark-3.5.1/spark-3.5.1-bin-hadoop3.tgz](https://archive.apache.org/dist/spark/spark-3.5.1/spark-3.5.1-bin-hadoop3.tgz)
tar -xzf spark-3.5.1-bin-hadoop3.tgz

# --- Configure Environment Variables ---
echo "Configuring environment variables in .bashrc..."
cat <<EOF >> ~/.bashrc

# Spark and Java Environment Variables
export SPARK_HOME=~/spark-3.5.1-bin-hadoop3
export JAVA_HOME=/usr/lib/jvm/java-21-openjdk-amd64
export PATH=\$SPARK_HOME/bin:\$PATH
export PATH=\$SPARK_HOME/sbin:\$PATH
EOF

# --- Clean Up ---
rm spark-3.5.1-bin-hadoop3.tgz

echo "✅ Spark environment successfully installed!"
echo "Please restart your WSL terminal or run 'source ~/.bashrc' to load the new environment."
```

### 1.2. Project-Specific Python Setup

1.  **Create a Python virtual environment**:
    ```bash
    python3 -m venv .venv
    ```

2.  **Activate the environment**:
    ```bash
    source .venv/bin/activate
    ```

3.  **Install required Python packages**:
    ```bash
    pip install pyspark debugpy
    ```

---

## Setup Option 2: Docker Environment

This method uses Docker to create a consistent, isolated development environment. All dependencies are managed inside the container.

### 2.1. Required Files

Ensure the following files exist in your project root.

**`docker-compose.yml`**:
```yaml
version: '3.8'
services:
  spark-app:
    image: jupyter/pyspark-notebook
    ports:
      - "5678:5678"
    volumes:
      - .:/app
    working_dir: /app
    command: tail -f /dev/null
```

**`.devcontainer/devcontainer.json`**:
```json
{
    "name": "PySpark Dev Environment",
    "dockerComposeFile": "../docker-compose.yml",
    "service": "spark-app",
    "workspaceFolder": "/app",
    "customizations": {
        "vscode": {
            "extensions": [
                "ms-python.python"
            ]
        }
    }
}
```

### 2.2. Launching the Environment

1.  Install the **Dev Containers** extension in VS Code.
2.  Open the project folder in VS Code.
3.  Open the Command Palette (`Ctrl+Shift+P`) and select **`Dev Containers: Reopen in Container`**.

VS Code will build the container and connect to it. No further installation is needed.

---

## Running the Application

### In the WSL Environment
Make sure your virtual environment is active (`source .venv/bin/activate`) and run:
```bash
spark-submit app.py
```

### In the Docker Environment
Open an integrated terminal in VS Code (it will be inside the container) and run:
```bash
spark-submit app.py
```

---

## Debugging the Application

The process is similar for both environments. Ensure your `debug-driver.sh` script is executable (`chmod +x debug-driver.sh`).

1.  In the **Run and Debug** view in VS Code, start the appropriate listener (`...WSL` or `...Spark Driver`).
2.  In the VS Code terminal (with the correct environment/container active), run the debug command:

    ```bash
    PYSPARK_DRIVER_PYTHON="./debug-driver.sh" spark-submit app.py
    ```