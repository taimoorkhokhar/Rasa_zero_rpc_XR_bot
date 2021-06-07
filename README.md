# Rasa And XR Bot With Zero-RPC

Run the commnad to build the docker image:
```
docker build -t xr_bot .
```
Run the command to start docker container: 
```
docker run -d -p 8000:8000 xr_bot
```
Get response from the API by running this command:
```
docker exec <container id> node test-bot.js --id=1 --mesage="hello!"
```
