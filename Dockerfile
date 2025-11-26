# Use an official Python image as the base image
FROM python:3.12-slim

# Install Git
RUN apt-get update && apt-get install -y git


# Set the working directory in the container
WORKDIR /app

# Copy the project files to the working directory
COPY . /app

# Install required dependencies for building the package
RUN pip install --upgrade pip setuptools wheel setuptools_scm build

# Install runtime dependencies listed in pyproject.toml
RUN pip install .

# Build the package
RUN python -m build