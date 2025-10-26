#!/bin/bash

# Jenkins Installation and Setup Script

set -e

echo "========================================="
echo "  Jenkins Docker Setup Script"
echo "========================================="
echo ""

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "ERROR: Docker is not installed. Please install Docker first."
    echo "Visit: https://docs.docker.com/get-docker/"
    exit 1
fi

echo "✓ Docker is installed"

# Check if Jenkins container already exists
if docker ps -a | grep -q jenkins; then
    echo ""
    echo "WARNING: Jenkins container already exists."
    read -p "Do you want to remove the existing container and create a new one? (y/n) " -n 1 -r
    echo ""
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        echo "Stopping and removing existing Jenkins container..."
        docker stop jenkins 2>/dev/null || true
        docker rm jenkins 2>/dev/null || true
        docker volume rm jenkins_home 2>/dev/null || true
    else
        echo "Keeping existing container. Exiting."
        exit 0
    fi
fi

echo ""
echo "Starting Jenkins container..."
echo ""
docker run -d --name jenkins -p 8080:8080 -p 50000:50000 -v jenkins_home:/var/jenkins_home jenkins/jenkins:lts

echo ""
echo "✓ Jenkins container started successfully!"
echo ""
echo "Waiting for Jenkins to initialize..."
sleep 10

echo ""
echo "========================================="
echo "  Jenkins Setup Instructions"
echo "========================================="
echo ""
echo "1. Access Jenkins at: http://localhost:8080"
echo ""
echo "2. Get the initial admin password by running:"
echo "   docker exec -it jenkins cat /var/jenkins_home/secrets/initialAdminPassword"
echo ""
echo "3. Follow the on-screen instructions to complete setup"
echo ""
echo "4. Install the following plugins:"
echo "   - Git plugin"
echo "   - Pipeline"
echo "   - ShiningPanda Plugin"
echo "   - JUnit Plugin"
echo "   - HTML Publisher Plugin"
echo ""
echo "5. Configure GitHub credentials in Jenkins"
echo ""
echo "6. For detailed instructions, see: SETUP_JENKINS.md"
echo ""
echo "========================================="
echo ""
echo "Useful commands:"
echo "  - View Jenkins logs: docker logs -f jenkins"
echo "  - Stop Jenkins: docker stop jenkins"
echo "  - Start Jenkins: docker start jenkins"
echo "  - Restart Jenkins: docker restart jenkins"
echo "  - Remove Jenkins: docker stop jenkins && docker rm jenkins"
echo ""

# Try to get the initial admin password
echo "Attempting to retrieve initial admin password..."
sleep 5
PASSWORD=$(docker exec jenkins cat /var/jenkins_home/secrets/initialAdminPassword 2>/dev/null || echo "")
if [ -n "$PASSWORD" ]; then
    echo ""
    echo "Initial Admin Password: $PASSWORD"
    echo ""
fi

echo "Setup complete! Please follow the instructions above."

