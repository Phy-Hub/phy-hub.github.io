# Use the base image specified in devcontainer.json
FROM ghcr.io/andsfonseca/miktex:latest

# Disable prompts during package installation
#ENV DEBIAN_FRONTEND=noninteractive

# Install any needed packages specified in requirements.txt
#RUN pip3 install --no-cache-dir -r .devcontainer/requirements.txt

# Install system dependencies
#RUN apt-get update && apt-get install -y \
#    python3 \
#    python3-pip \
#    perl
    #\
   # wget \
    #&& apt-get update \
   # && apt-get install -y \
  #  miktex \
 #   pdf2svg \
#    && apt-get clean

# Set the default shell to bash
SHELL ["/bin/bash", "-c"]

# Install pdf2svg Python package
#RUN pip3 install pdf2svg

# Verify installations
#RUN python3 --version && \
#    perl --version && \
 #   miktex --version && \
 #   pdf2svg --version
