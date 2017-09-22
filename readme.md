# Digit

#### On RPi in ~/Digit

**build image**
```bash
docker build -t digit:1.1 -f Dockerfile .
```

**run image**
```bash
docker run -d --device /dev/gpiomem digit:1.1 clock.py
docker run -d --device /dev/gpiomem --device /sys/bus/w1/devices/28-05170143ccff/w1_slave digit:1.1 ds18b20.py
docker run -d --device /dev/gpiomem digit:1.1 day.py
```

**build via docker-compose**
```bash
docker-compose -f docker-compose.yml build
```

**run via docker-compose**
```bash
docker-compose -f docker-compose.yml up -d
```
