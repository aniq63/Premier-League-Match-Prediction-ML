# 🐳 Docker Guide for Beginners

Complete guide to Docker for the Premier League Match Prediction ML project - perfect for first-time Docker users!

---

## Table of Contents

1. [What is Docker?](#what-is-docker)
2. [Why Use Docker?](#why-use-docker)
3. [Installing Docker](#installing-docker)
4. [Understanding the Dockerfile](#understanding-the-dockerfile)
5. [Building the Docker Image](#building-the-docker-image)
6. [Running the Container](#running-the-container)
7. [Docker Hub Setup](#docker-hub-setup)
8. [Pushing to Docker Hub](#pushing-to-docker-hub)
9. [Pulling and Using Your Image](#pulling-and-using-your-image)
10. [Troubleshooting](#troubleshooting)

---

## What is Docker?

### Simple Explanation

Think of Docker like a **shipping container** for your application:

- 📦 **Container**: Packages your app + all dependencies together
- 🚢 **Portable**: Works the same everywhere (your PC, cloud, friend's PC)
- 🔒 **Isolated**: Runs in its own environment, doesn't mess with your system
- 🎯 **Consistent**: "It works on my machine" → "It works everywhere!"

### Key Concepts

| Term | What It Means | Analogy |
|------|---------------|---------|
| **Image** | Blueprint/template for your app | Recipe for a cake |
| **Container** | Running instance of an image | Actual cake made from recipe |
| **Dockerfile** | Instructions to build an image | Recipe instructions |
| **Docker Hub** | Online storage for images | Recipe sharing website |

---

## Why Use Docker?

### Benefits for Your ML Project

✅ **Consistency**: Same environment everywhere  
✅ **Easy Deployment**: One command to run anywhere  
✅ **No Dependency Hell**: All libraries packaged together  
✅ **Isolation**: Won't conflict with other projects  
✅ **Shareable**: Anyone can run your project instantly  
✅ **Professional**: Industry standard for deployment  

### Real-World Example

**Without Docker:**
```
You: "Clone my repo and install these 20 dependencies..."
Friend: "I get errors! My Python version is different!"
You: "Works on my machine 🤷"
```

**With Docker:**
```
You: "Run: docker run aniq63/epl-prediction"
Friend: "It works! 🎉"
```

---

## Installing Docker

### Windows

1. **Download Docker Desktop**
   - Go to [docker.com/products/docker-desktop](https://www.docker.com/products/docker-desktop)
   - Download for Windows
   - Run installer

2. **Enable WSL 2** (if prompted)
   - Follow Docker's instructions
   - Restart computer

3. **Verify Installation**
   ```bash
   docker --version
   docker run hello-world
   ```

### macOS

1. **Download Docker Desktop**
   - Go to [docker.com/products/docker-desktop](https://www.docker.com/products/docker-desktop)
   - Download for Mac (Intel or Apple Silicon)
   - Drag to Applications folder

2. **Start Docker Desktop**
   - Open from Applications
   - Wait for whale icon in menu bar

3. **Verify Installation**
   ```bash
   docker --version
   docker run hello-world
   ```

### Linux

```bash
# Ubuntu/Debian
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Add your user to docker group (no sudo needed)
sudo usermod -aG docker $USER
newgrp docker

# Verify
docker --version
docker run hello-world
```

---

## Understanding the Dockerfile

Let's break down our Dockerfile line by line!

### The Complete Dockerfile Structure

```dockerfile
# 1. BASE IMAGE - Starting point
FROM python:3.9-slim
```
**What it does**: Uses Python 3.9 as foundation  
**Why**: We need Python to run our FastAPI app

---

```dockerfile
# 2. METADATA - Documentation
LABEL maintainer="aniq63"
LABEL description="Premier League Match Prediction API"
```
**What it does**: Adds information about the image  
**Why**: Helps others know who made it and what it does

---

```dockerfile
# 3. ENVIRONMENT VARIABLES - Configuration
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV APP_HOME=/app
```
**What it does**: Sets up Python environment  
**Why**: 
- `PYTHONUNBUFFERED=1`: See logs immediately
- `PYTHONDONTWRITEBYTECODE=1`: Don't create .pyc files
- `APP_HOME=/app`: Our app lives in /app folder

---

```dockerfile
# 4. SYSTEM DEPENDENCIES - Install tools
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*
```
**What it does**: Installs system-level tools  
**Why**: 
- `build-essential`: Needed to compile some Python packages
- `curl`: For health checks
- `rm -rf /var/lib/apt/lists/*`: Clean up to save space

---

```dockerfile
# 5. WORKING DIRECTORY - Set location
WORKDIR $APP_HOME
```
**What it does**: Creates `/app` folder and moves there  
**Why**: All our code will live here

---

```dockerfile
# 6. COPY REQUIREMENTS - Get dependencies list
COPY requirements.txt .
```
**What it does**: Copies requirements.txt into container  
**Why**: We copy this FIRST for Docker layer caching (faster rebuilds)

---

```dockerfile
# 7. INSTALL PYTHON PACKAGES
RUN pip install --no-cache-dir --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt
```
**What it does**: Installs all Python dependencies  
**Why**: Our app needs FastAPI, scikit-learn, etc.

---

```dockerfile
# 8. COPY APPLICATION CODE
COPY . .
```
**What it does**: Copies all project files into container  
**Why**: We need the actual code to run!

---

```dockerfile
# 9. INSTALL PACKAGE
RUN pip install --no-cache-dir -e .
```
**What it does**: Installs our `src` package  
**Why**: Makes imports work (`from src.components import ...`)

---

```dockerfile
# 10. CREATE DIRECTORIES
RUN mkdir -p logs artifact saved_models
```
**What it does**: Creates folders the app needs  
**Why**: App writes logs and saves models here

---

```dockerfile
# 11. SECURITY - Non-root user
RUN useradd -m -u 1000 appuser && \
    chown -R appuser:appuser $APP_HOME
USER appuser
```
**What it does**: Creates and switches to non-root user  
**Why**: Security best practice (don't run as root)

---

```dockerfile
# 12. EXPOSE PORT - Document port
EXPOSE 8000
```
**What it does**: Documents that app uses port 8000  
**Why**: Tells users which port to map

---

```dockerfile
# 13. HEALTH CHECK - Monitor health
HEALTHCHECK --interval=30s --timeout=10s --start-period=30s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1
```
**What it does**: Checks if app is running every 30 seconds  
**Why**: Docker can restart if unhealthy

---

```dockerfile
# 14. STARTUP COMMAND - Run the app
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "1"]
```
**What it does**: Starts the FastAPI server  
**Why**: This is what runs when container starts

---

## Building the Docker Image

### Step 1: Navigate to Project Directory

```bash
cd e:\Premier-League-Match-Prediction-ML
```

### Step 2: Build the Image

```bash
docker build -t epl-prediction:latest .
```

**Breaking it down:**
- `docker build`: Command to build an image
- `-t epl-prediction:latest`: Tag (name) the image
  - `epl-prediction`: Image name
  - `latest`: Version tag
- `.`: Use Dockerfile in current directory

### Step 3: Watch the Build Process

You'll see output like:
```
[+] Building 45.2s (15/15) FINISHED
 => [1/10] FROM python:3.9-slim
 => [2/10] RUN apt-get update && apt-get install...
 => [3/10] WORKDIR /app
 => [4/10] COPY requirements.txt .
 => [5/10] RUN pip install --upgrade pip
 => [6/10] RUN pip install -r requirements.txt
 => [7/10] COPY . .
 => [8/10] RUN pip install -e .
 => [9/10] RUN mkdir -p logs artifact saved_models
 => [10/10] RUN useradd -m -u 1000 appuser...
 => exporting to image
 => => naming to docker.io/library/epl-prediction:latest
```

### Step 4: Verify Image was Created

```bash
docker images
```

You should see:
```
REPOSITORY        TAG       IMAGE ID       CREATED          SIZE
epl-prediction    latest    abc123def456   2 minutes ago    1.2GB
```

---

## Running the Container

### Basic Run Command

```bash
docker run -p 8000:8000 epl-prediction:latest
```

**Breaking it down:**
- `docker run`: Start a container
- `-p 8000:8000`: Map ports (host:container)
  - First 8000: Your computer's port
  - Second 8000: Container's port
- `epl-prediction:latest`: Image to run

### Run in Background (Detached Mode)

```bash
docker run -d -p 8000:8000 --name epl-api epl-prediction:latest
```

**New flags:**
- `-d`: Detached mode (runs in background)
- `--name epl-api`: Give container a name

### Run with Environment Variables

```bash
docker run -d -p 8000:8000 \
  -e MONGODB_URL="mongodb://localhost:27017" \
  --name epl-api \
  epl-prediction:latest
```

**New flag:**
- `-e`: Set environment variable

### Run with Volume (Persist Data)

```bash
docker run -d -p 8000:8000 \
  -v $(pwd)/saved_models:/app/saved_models \
  --name epl-api \
  epl-prediction:latest
```

**New flag:**
- `-v`: Mount volume (share folder between host and container)

### Access the Application

Once running, visit:
- **Web UI**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health

### Useful Container Commands

```bash
# List running containers
docker ps

# List all containers (including stopped)
docker ps -a

# View container logs
docker logs epl-api

# Follow logs in real-time
docker logs -f epl-api

# Stop container
docker stop epl-api

# Start stopped container
docker start epl-api

# Remove container
docker rm epl-api

# Remove container forcefully
docker rm -f epl-api
```

---

## Docker Hub Setup

Docker Hub is like GitHub but for Docker images!

### Step 1: Create Docker Hub Account

1. Go to [hub.docker.com](https://hub.docker.com/)
2. Click "Sign Up"
3. Fill in details:
   - Username (e.g., `aniq63`)
   - Email
   - Password
4. Verify email

### Step 2: Login from Terminal

```bash
docker login
```

Enter your Docker Hub username and password.

You should see:
```
Login Succeeded
```

### Step 3: Create Repository (Optional)

1. Go to [hub.docker.com](https://hub.docker.com/)
2. Click "Create Repository"
3. Fill in:
   - **Name**: `epl-prediction`
   - **Description**: "Premier League Match Prediction ML API"
   - **Visibility**: Public (free) or Private (paid)
4. Click "Create"

---

## Pushing to Docker Hub

### Step 1: Tag Your Image

Docker Hub images need format: `username/repository:tag`

```bash
docker tag epl-prediction:latest aniq63/epl-prediction:latest
```

**Breaking it down:**
- `docker tag`: Create a new tag for existing image
- `epl-prediction:latest`: Your local image
- `aniq63/epl-prediction:latest`: New name for Docker Hub
  - `aniq63`: Your Docker Hub username
  - `epl-prediction`: Repository name
  - `latest`: Version tag

### Step 2: Push to Docker Hub

```bash
docker push aniq63/epl-prediction:latest
```

You'll see upload progress:
```
The push refers to repository [docker.io/aniq63/epl-prediction]
abc123: Pushed
def456: Pushed
...
latest: digest: sha256:abc123... size: 1234
```

### Step 3: Verify on Docker Hub

1. Go to [hub.docker.com](https://hub.docker.com/)
2. Click on your repository
3. You should see your image!

### Push Multiple Tags

```bash
# Tag with version number
docker tag epl-prediction:latest aniq63/epl-prediction:v1.0.0
docker push aniq63/epl-prediction:v1.0.0

# Tag with date
docker tag epl-prediction:latest aniq63/epl-prediction:2025-01-15
docker push aniq63/epl-prediction:2025-01-15
```

---

## Pulling and Using Your Image

Now anyone can use your image!

### Pull Your Image

```bash
docker pull aniq63/epl-prediction:latest
```

### Run Your Image from Docker Hub

```bash
docker run -d -p 8000:8000 aniq63/epl-prediction:latest
```

### Share with Others

Tell others to run:
```bash
docker run -p 8000:8000 aniq63/epl-prediction:latest
```

That's it! No installation, no dependencies, just works! 🎉

---

## Troubleshooting

### Issue 1: "docker: command not found"

**Problem**: Docker not installed or not in PATH

**Solution**:
```bash
# Verify Docker is installed
docker --version

# If not, install Docker Desktop
# Windows/Mac: Download from docker.com
# Linux: curl -fsSL https://get.docker.com -o get-docker.sh && sudo sh get-docker.sh
```

---

### Issue 2: "permission denied" (Linux)

**Problem**: User not in docker group

**Solution**:
```bash
sudo usermod -aG docker $USER
newgrp docker
```

---

### Issue 3: Build fails with "No space left on device"

**Problem**: Docker ran out of disk space

**Solution**:
```bash
# Clean up unused images and containers
docker system prune -a

# Remove specific images
docker rmi <image-id>
```

---

### Issue 4: Port already in use

**Problem**: Port 8000 is already being used

**Solution**:
```bash
# Use different port
docker run -p 8001:8000 epl-prediction:latest

# Or stop the process using port 8000
# Windows
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# Linux/Mac
lsof -ti:8000 | xargs kill -9
```

---

### Issue 5: Container exits immediately

**Problem**: Application crashes on startup

**Solution**:
```bash
# Check logs
docker logs <container-name>

# Run interactively to debug
docker run -it epl-prediction:latest /bin/bash
```

---

### Issue 6: Can't connect to MongoDB

**Problem**: Container can't reach MongoDB on host

**Solution**:
```bash
# Use host.docker.internal instead of localhost
docker run -p 8000:8000 \
  -e MONGODB_URL="mongodb://host.docker.internal:27017" \
  epl-prediction:latest
```

---

### Issue 7: Image too large

**Problem**: Image is several GB

**Solution**:
```bash
# Use multi-stage builds (advanced)
# Or use .dockerignore to exclude files
# Check what's taking space
docker history epl-prediction:latest
```

---

## Docker Commands Cheat Sheet

### Images

```bash
# List images
docker images

# Remove image
docker rmi <image-name>

# Remove all unused images
docker image prune -a

# Inspect image
docker inspect <image-name>
```

### Containers

```bash
# List running containers
docker ps

# List all containers
docker ps -a

# Stop container
docker stop <container-name>

# Start container
docker start <container-name>

# Restart container
docker restart <container-name>

# Remove container
docker rm <container-name>

# Remove all stopped containers
docker container prune
```

### Logs and Debugging

```bash
# View logs
docker logs <container-name>

# Follow logs
docker logs -f <container-name>

# Execute command in running container
docker exec -it <container-name> /bin/bash

# Inspect container
docker inspect <container-name>
```

### Cleanup

```bash
# Remove everything unused
docker system prune -a

# Remove all stopped containers
docker container prune

# Remove all unused images
docker image prune -a

# Remove all unused volumes
docker volume prune
```

---

## Best Practices

### 1. Use .dockerignore

Always exclude unnecessary files:
```
venv/
*.pyc
.git/
logs/
```

### 2. Multi-stage Builds (Advanced)

For smaller images:
```dockerfile
FROM python:3.9 AS builder
# Build dependencies

FROM python:3.9-slim
# Copy only what's needed
```

### 3. Layer Caching

Order Dockerfile commands from least to most frequently changed:
```dockerfile
COPY requirements.txt .  # Changes rarely
RUN pip install -r requirements.txt
COPY . .  # Changes often
```

### 4. Security

- Don't run as root
- Don't include secrets in image
- Use official base images
- Keep images updated

### 5. Tagging

Use meaningful tags:
```bash
docker tag myapp:latest myapp:v1.0.0
docker tag myapp:latest myapp:2025-01-15
```

---

## Next Steps

1. ✅ Build your image
2. ✅ Test locally
3. ✅ Push to Docker Hub
4. 🚀 Deploy to cloud:
   - AWS ECS
   - Google Cloud Run
   - Azure Container Instances
   - Heroku
   - DigitalOcean

---

## Additional Resources

- **Official Docker Docs**: [docs.docker.com](https://docs.docker.com/)
- **Docker Hub**: [hub.docker.com](https://hub.docker.com/)
- **Docker Cheat Sheet**: [dockerlabs.collabnix.com](https://dockerlabs.collabnix.com/docker/cheatsheet/)

---

**Happy Dockerizing! 🐳**
