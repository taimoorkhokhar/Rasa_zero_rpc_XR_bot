# Rasa And XR Bot With Zero-RPC

Build the docker image:
```
docker build -t xr_bot .
```
Start docker container: 
```
docker run -d -p 8000:8000 xr_bot
```
Interect with bot:
+ id --- Rasa bot ID.
```
docker exec <container id> node test-bot.js --id=1 --mesage="hello!"
```
