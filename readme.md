## Digit

**on RPi in ~/Digit**

build image
```bash
docker build -t digit:1.0 -f Dockerfile .
```

run image
```bash
docker run -d --device /dev/gpiomem digit:1.0 clock.py
docker run -d --device /dev/gpiomem digit:1.0 temperature.py
docker run -d --device /dev/gpiomem digit:1.0 day.py
```

build via docker-compose
```bash
docker-compose -f docker-compose.yml build
```

run via docker-compose
```bash
docker-compose -f docker-compose.yml up -d