import express from 'express';
import mqtt from'mqtt';

var options = {
    host:     process.env.MQTT_BROKER_HOST,
    port:     process.env.MQTT_BROKER_PORT,
    protocol: process.env.MQTT_BROKER_PROTOCOL,
    username: process.env.MQTT_BROKER_USERNAME,
    password: process.env.MQTT_BROKER_PASSWORD
}

//initialize the MQTT client
var client = mqtt.connect(options);

//setup the callbacks
client.on('connect', function () {
    console.log('Connected');
});

client.on('error', function (error) {
    console.log(error);
});

client.on('message', function (topic, message) {
    //Called each time a message is received
    console.log('Received message:', topic, message.toString());
});

// subscribe to topic 'testtopic/1'
client.subscribe('testtopic/1');

// publish message 'Hello' to topic 'testtopic/1'
// client.publish('testtopic/1', 'Hello');

var router = express.Router();

/* GET home page. */
router.get('/', function(req, res, next) {
  res.render('index', { title: 'Express' });
});

router.put("/start", (req, res,next) => {
  client.publish('testtopic/1', 'start');
})

router.put("/stop", (req, res,next) => {
  client.publish('testtopic/1', 'stop');
})

export default router;
