import http from 'http';
import SocketIo from 'socket.io';
import amqp from 'amqplib/callback_api'
import fs from 'fs';
import JoinUser from './utils';


function handler(req, res) {
    res.setHeader('Access-Control-Allow-Origin', '*');
    fs.readFile(
        `${__dirname}/index.html`,
        (err, data) => {
            if (err) {
                res.writeHead(500);
                res.end('Error loading index.html');
            }
            res.writeHead(200);
            res.end(data);
        },
    );
}

const server = http.createServer(handler).listen(4000, '0.0.0.0');
const io = SocketIo.listen(server);
amqp.connect('amqp://admin:mypass@app_rabbit:5672', function(err, conn) {
    conn.createChannel(function(err, ch) {
        const channel = 'payload';
        const broadcast = 'broadcast';
        ch.assertQueue(channel, {durable: false});
        ch.assertQueue(broadcast, {durable: false});
        console.log("[*] Waiting for messages in %s. To exit press CTRL+C", channel);
        ch.consume(channel, function(msg) {
            console.log(" [%s] Received %s", channel, msg.content.toString());
            const message = JSON.parse(msg.content);
            io.to(message.room).emit(message.event, message.content);
        }, {noAck: true}
        );
        ch.consume(broadcast, function(msg) {
            console.log(" [%s] Received %s", broadcast, msg.content.toString());
            const message = JSON.parse(msg.content);
            // io.to(message.rooms[0]).emit(message.event, message.content);
            message.rooms.map(
                (room) => {
                    io.to(room).emit(message.event, message.content);
                })
        }, {noAck: true}
        );
    });
});


io.on('connection', (socket) => {
    const { token } = socket.handshake.query;
    console.log('User connected with token: ', token);
    JoinUser(token, socket, io);
    socket.on('test', (data) => {
        console.log(data);
    });
    socket.on('disconnect', () => {
        console.log('user disconnected');
    });
});

