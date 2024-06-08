# Use the latest Python base image
FROM python:latest

# Install cron, supervisord, and sudo
RUN apt-get update && apt-get install -y --no-install-recommends cron supervisor sudo

# Clean up APT when done
RUN apt-get clean && rm -rf /var/lib/apt/lists/*

# Declare UID and GID as arguments
ARG UID=1001
ARG GID=1000

# Set user and group name, and use previous UID and GID as environment variables
ENV UNAME=appuser
ENV GNAME=appgroup
ENV UID=${UID}
ENV GID=${GID}

# Create a new group with a specific GID
RUN groupadd -g ${GID} ${GNAME}

# Create a new user with specified UID, GID, and password
RUN useradd --create-home --uid ${UID} --gid ${GID} --shell /bin/bash --password $(echo "password" | openssl passwd -1 -stdin) ${UNAME}

# Add the new user to the sudo group
RUN adduser ${UNAME} sudo

# Configure sudoers to allow user to execute sudo commands without a password
RUN echo "${UNAME} ALL=(ALL) NOPASSWD: ALL" > /etc/sudoers.d/${UNAME}
RUN chmod 0440 /etc/sudoers.d/${UNAME}

# Set the working directory
WORKDIR /home/${UNAME}/app

# Copy host folder contents to the working directory and change ownership
COPY --chown=${UNAME}:${GNAME} ./app /home/${UNAME}/app

# Change ownership of the working directory
RUN chown -R ${UNAME}:${GNAME} /home/${UNAME}/app

# Switch to the user '${UNAME}' for subsequent commands and switch to the working directory
USER ${UNAME}

# Use echo to append a newline to the crontab file
RUN echo "" >> /home/${UNAME}/app/misc/crontab

# Set permissions for the crontab file
RUN chmod 0644 /home/${UNAME}/app/misc/crontab

# Apply the crontab file
RUN crontab /home/${UNAME}/app/misc/crontab

# Create a Python virtual environment and install dependencies from requirements.txt
RUN python -m venv venv && \
    . venv/bin/activate && \
    pip install -r /home/${UNAME}/app/misc/requirements.txt

# Keep the Python virtual environment active by default when running commands in the container
ENV PATH="/home/${UNAME}/app/venv/bin:$PATH"

# Make the scripts executable
RUN chmod +x /home/${UNAME}/app/bin/init.sh \
    && chmod +x /home/${UNAME}/app/bin/entrypoint.sh \
    && chmod +x /home/${UNAME}/app/bin/compute_prediction.sh

# Run the initialization script
RUN /home/${UNAME}/app/bin/init.sh

# Set supervisord as ENTRYPOINT to launch everything
ENTRYPOINT ["/usr/bin/supervisord", "-n", "-c", "/home/appuser/app/misc/supervisord.conf"]