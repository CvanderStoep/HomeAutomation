# Python file in Docker

[comment]: <> (builds an image from the dockerfile)
docker build -t "city_weather" .

docker run --rm -it city_weather
docker run --rm -it cvanderstoep/city_weather

docker tag city_weather cvanderstoep/city_weather


[comment]: <> (make the docker image)
docker build -t "nlm" .

[comment]: <> (run the docker image)
docker run -ti nlm

[comment]: <> (check docker images)
docker images

[comment]: <> (check all containers)
docker ps -a

[comment]: <> (map docker files to PC)
docker run -v "C:\Users\carlo\OneDrive\Documenten\16. Python\Dockertest":/usr/src/app nlm

[comment]: <> (compose and run using docker-compose)
docker compose up

[comment]: <> (use container in interactive mode)
docker compose run --rm nlm


[comment]: <> (be very carefull with below; this deletes all volume, images, containers, ...)
docker system prune

[comment]: <> (run with a volume attached, can be found in //wsl$/)
docker run -p 8086:8086 -v influxdb:/var/lib/influxdb influxdb:1.8

[comment]: <> (volume location: \\wsl$\)

docker compose run --service-ports grafana
docker compose run --service-ports influxDB

docker run -p 8086:8086 -v influxdb2:/var/lib/influxdb2 -v influxdb2.conf:/etc/influxdb2 influxdb:2.0
