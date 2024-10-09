param(
    [switch]$useDocker = $false
)

# Step 1: Check if the script should run the Docker commands
if ($useDocker) {
    Write-Host "Running Docker commands..."

    # Build the Docker image
    docker build -t whiteduck .

    # Run the Docker container, remove it after execution, and map port 8000
    docker run --rm -p 8000:8000 whiteduck
}
else {

    $poetryPath = (Get-Command poetry -ErrorAction SilentlyContinue).Path
    if (-not $poetryPath) {
        Write-Host "Poetry is not installed. Poetry getting installed..."
        pip install poetry
    }
    else {
        Write-Host "Poetry is already installed."
    }

    # Step 4: Install project dependencies using Poetry
    Write-Host "Installing project dependencies using Poetry..."
    poetry lock
    poetry install --no-root

    # Step 5: Start the app
    Write-Host "Starting App..."
    poetry run shiny run .\app.py

    # Step 6: Keep the script open indefinitely
    Write-Host "Press Enter to exit the script..."
    Read-Host
}