#!/usr/bin/env python3

import subprocess
import pytest
import os


class TestDockerContainer:
    """Test cases for the Docker container."""
    
    def test_docker_image_exists(self):
        """Test that the Docker image can be built and exists."""
        # Try to build the image
        result = subprocess.run(
            ["docker", "build", "-t", "test-gmnx", "."],
            capture_output=True,
            text=True,
            cwd=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        )
        assert result.returncode == 0, f"Failed to build image: {result.stderr}"
    
    def test_docker_container_runs_without_api_key(self):
        """Test that container fails gracefully without API key."""
        result = subprocess.run(
            ["docker", "run", "--rm", "test-gmnx"],
            capture_output=True,
            text=True
        )
        assert result.returncode == 1
        assert "GEMINI_API_KEY environment variable not set" in result.stdout
    
    def test_docker_container_runs_without_arguments(self):
        """Test that container shows usage without arguments."""
        result = subprocess.run(
            ["docker", "run", "--rm", "-e", "GEMINI_API_KEY=test-key", "test-gmnx"],
            capture_output=True,
            text=True
        )
        assert result.returncode == 0
        assert "Usage: ask" in result.stdout
    
    def test_docker_container_accepts_arguments(self):
        """Test that container accepts command line arguments."""
        result = subprocess.run(
            ["docker", "run", "--rm", "-e", "GEMINI_API_KEY=test-key", "test-gmnx", "test question"],
            capture_output=True,
            text=True,
            timeout=30  # Add timeout in case it hangs
        )
        # Should not crash, even if API call fails
        assert result.returncode in [0, 1]  # Either success or expected API failure
    
    def test_docker_image_size(self):
        """Test that the Docker image is reasonably sized."""
        result = subprocess.run(
            ["docker", "images", "test-gmnx", "--format", "{{.Size}}"],
            capture_output=True,
            text=True
        )
        assert result.returncode == 0
        size_str = result.stdout.strip()
        # Basic check that we got a size string (format like "123MB" or "1.2GB")
        assert "MB" in size_str or "GB" in size_str


if __name__ == "__main__":
    pytest.main([__file__])
