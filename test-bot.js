const argv = require('minimist')(process.argv.slice(2));
const zerorpc = require("zerorpc");

clientOptions = {
    timeout: 120,
    heartbeatInterval: 1200000
}
const client = new zerorpc.Client(clientOptions);

client.connect("tcp://127.0.0.1:4242");

bot_id = argv.id
message = argv.message

client.invoke("get_bot_response", bot_id, message, function(error, res, more) {
    console.log("Bot Response => ", res);
});