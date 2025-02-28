ARG PYTHON_VERSION="3.11.11"
ARG PLATFORM_NAME="linux/amd64"
ARG POETRY_VERSION=1.6.1

FROM --platform=${PLATFORM_NAME} python:${PYTHON_VERSION}

# --- SYSTEM ARCHITECTURE
ARG TARGETPLATFORM
ARG TARGETARCH
ARG TARGETVARIANT

RUN printf "I'm building for TARGETPLATFORM=${TARGETPLATFORM}" \
    && printf ", TARGETARCH=${TARGETARCH}" \
    && printf ", TARGETVARIANT=${TARGETVARIANT} \n" \
    && printf "With uname -s : " && uname -s \
    && printf "and  uname -m : " && uname -mm

# --- Environment-variables
ENV APP_DIR="/app/"
ENV ROOT_DIR="/root/"
ENV PROJECT_DIR="/opt/ml"
ENV PROGRAM_DIR="/opt/program"
ENV HOME_DIR="/root/ml"
ENV LOCAL_DEV_DIR="assets"

# --- Project-specific environment variables
ENV LOG_LEVEL="DEBUG"
ENV ENV=${ENV}
ENV POETRY_VERSION=${POETRY_VERSION:-1.6.1}


# --- Docker Metadata
LABEL Maintainer="{{ cookiecutter.author_name }}"
ENV DEBIAN_FRONTEND=noninteractive

# ----------------------------- APP PORTS -------------------------------------

EXPOSE 80
EXPOSE 8000

# --------------------------- EXTRA PACKAGES ----------------------------------

# -- Necessary packages
RUN apt-get -y update && \
    apt-get upgrade -y && \
    apt-get clean && \
    # Packages
    apt-get install -y \
    curl \
    git

# -- Development packages
RUN apt-get -y update && \
    apt-get upgrade -y && \
    apt-get clean && \
    # Packages
    apt-get install -y \
    tree \
    tmux \
    direnv \
    bash-completion \
    zsh \
    htop \
    && \
    # Cleaning out
    rm -rf /var/lib/apt/lists/* && \
    apt-get clean && \
    # Install Zsh and OhZsh
    sh -c "$(curl -fsSL https://raw.github.com/ohmyzsh/ohmyzsh/master/tools/install.sh)" && \
    echo "source /etc/profile.d/bash_completion.sh" >> /root/.bashrc && \
    echo "source /etc/profile.d/bash_completion.sh" >> /root/.zshrc && \
    # Install direnv
    echo 'eval "$(direnv hook zsh)"' >> "${ROOT_DIR}/.zshrc" && \
    echo 'eval "$(direnv hook bash)"' >> "${ROOT_DIR}/.bash"

# ---------------------------- APP-SPECIFIC -----------------------------------

# Upgrading pip
RUN pip install --upgrade pip && pip install "poetry==${POETRY_VERSION}"

# Installing packages
WORKDIR ${APP_DIR}

COPY ./pyproject.toml ./poetry.lock* ${APP_DIR}

RUN poetry export -f requirements.txt --output requirements.txt --without-hashes
RUN pip install --no-cache-dir -r ${APP_DIR}/requirements.txt

# Copying the app directory
COPY . ${APP_DIR}

# -------------------------- PYTHON-SPECIFIC ----------------------------------

# Set some environment variables. PYTHONUNBUFFERED keeps Python from
# buffering our standard output stream, which means that logs can be
# delivered to the user quickly. PYTHONDONTWRITEBYTECODE keeps Python
# from writing the .pyc files which are unnecessary in this case. We also
# update PATH so that the train and serve programs are found when the
# container is invoked.

ENV PYTHONUNBUFFERED=TRUE
ENV PYTHONDONTWRITEBYTECODE=TRUE
ENV PATH="${PROGRAM_DIR}:${PATH}"
ENV PYTHONPATH="${PROGRAM_DIR}:${PYTHONPATH}"

WORKDIR ${APP_DIR}

CMD [ "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80" ]
