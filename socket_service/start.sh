#!/bin/bash
while ! (timeout 3 bash -c "</dev/tcp/app_rabbit/5672") &> /dev/null;
do
    echo waiting for RabbitMQ to start...;
    sleep 3;
done;
npm i
npm run dev
