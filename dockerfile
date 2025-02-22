FROM mcr.microsoft.com/dotnet/sdk:9.0 AS dotnet-stage
FROM python:3.11

COPY --from=dotnet-stage /usr/share/dotnet /usr/share/dotnet
ENV PATH="${PATH}:/usr/share/dotnet"

RUN apt-get update && apt-get install -y \
    xvfb \
    dbus-x11 \
    x11-utils \
    libgtk-3-0 \
    libgbm-dev \
    libnotify-dev \
    libgconf-2-4 \
    libnss3 \
    libxss1 \
    libasound2 \
    fonts-liberation \
    libappindicator3-1 \
    libxrandr2 \
    lsb-release \
    wget \
    xdg-utils

WORKDIR /app


RUN pip3 install selenium pytest
COPY . . 

CMD ./run.sh



