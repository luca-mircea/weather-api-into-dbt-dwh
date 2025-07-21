FROM python:3.11-slim

# To make sure messages get printed
ENV PYTHONUNBUFFERED=1

# System deps for dbt & build
RUN apt-get update && apt-get install -y \
    build-essential \
    git \
    && rm -rf /var/lib/apt/lists/*

# Create and switch to a new (admin) user,
# needed to change permissions so we can write csv file
# directly in the docker container
RUN useradd -ms /bin/bash admin

# Set working directory
WORKDIR /app

# Copy requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the project
COPY . .

# change permissions now
RUN chown -R admin:admin /app
RUN chmod 755 .
USER admin

# Copy profiles explicitly so we can use it when we run the container
COPY dbt_weather/profiles /app/dbt_weather/profiles

# docker build . -t weather_dbt
# docker run weather_dbt python src --data_interval_start "2025-07-20T00:00:00" --data_interval_end "2025-07-21T00:00:00"
# docker run weather_dbt python src
# docker run weather_dbt bash -c "dbt seed --profiles-dir /app/dbt_weather/profiles && dbt run --profiles-dir /app/dbt_weather/profiles"
