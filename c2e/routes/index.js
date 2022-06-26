import express from "express";
import mqtt from "mqtt";

var options = {
  host: process.env.MQTT_BROKER_HOST,
  port: process.env.MQTT_BROKER_PORT,
  protocol: process.env.MQTT_BROKER_PROTOCOL,
  username: process.env.MQTT_BROKER_USERNAME,
  password: process.env.MQTT_BROKER_PASSWORD,
};

//initialize the MQTT client
var client = mqtt.connect(options);

//setup the callbacks
client.on("connect", function () {
  console.log("Connected");
});

client.on("error", function (error) {
  console.log(error);
});

client.on("message", function (topic, message) {
  //Called each time a message is received
  console.log("Received message:", topic, message.toString());
});

// subscribe to topic 'testtopic/1'
client.subscribe("testtopic/1");

// publish message 'Hello' to topic 'testtopic/1'
// client.publish('testtopic/1', 'Hello');

function checkSignIn(req, res, next) {
  console.log(req.session);
  if (req.session.user) {
    next(); //If session exists, proceed to page
  } else {
    res.redirect("/login");
  }
}

var router = express.Router();

/* GET home page. */
router.get("/", checkSignIn, function (req, res, next) {
  res.render("index");
});

router.put("/stop", checkSignIn, (req, res, next) => {
  client.publish("testtopic/1", "stop");
  res.status(204).send();
});

router.put("/forward", checkSignIn, (req, res, next) => {
  client.publish("testtopic/1", "forward");
  res.status(204).send();
});

router.put("/backward", checkSignIn, (req, res, next) => {
  client.publish("testtopic/1", "backward");
  res.status(204).send();
});

export default router;
