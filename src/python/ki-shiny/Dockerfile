FROM mambaorg/micromamba:1.5.10

# root level commands
USER root
RUN mkdir /opt/whiteduck
RUN chmod -R 777 /opt/whiteduck
WORKDIR /opt/whiteduck
# build-essentials
RUN apt-get update && apt-get install -y \
    pkg-config \
    libcairo2-dev \
    libgirepository1.0-dev \
    build-essential \
    ffmpeg \
    libsm6 \
    libxext6 \
    && rm -rf /var/lib/apt/lists/*

# user level commands - we use micromamba as docker conda wrapper
# conda env export > environment.yml
# good example that pip is bad - if environment.yml is used, pip can't install all dependencies
# because of the order of the dependencies in the file
# PIP
# USER micromamba
# COPY environment.yml environment.yml
# RUN micromamba install -y -n base -f environment.yml && \
#     micromamba clean --all --yes
# ENV PATH="/opt/conda/envs/base/bin:$PATH"

# POETRY
# Add channels and install Python and pip
RUN micromamba create -y -p /opt/conda/envs/base -c conda-forge -c defaults python=3.10.12 pip && micromamba clean --all --yes
ENV PATH="/opt/conda/envs/base/bin:$PATH"

RUN pip install poetry
COPY pyproject.toml ./
RUN poetry config virtualenvs.create false && poetry install --no-root

USER micromamba
COPY . .
EXPOSE 8000

USER root

# IP address has to be 0.0.0.0 or it won't work
CMD ["shiny", "run", "-h", "0.0.0.0", "-p", "8000"]

