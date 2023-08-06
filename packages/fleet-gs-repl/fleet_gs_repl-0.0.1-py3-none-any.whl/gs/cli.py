#!/usr/bin/env python
import asyncio
import os
import random
import readline
import signal
import string

import click
from aioconsole import ainput
from blessings import Terminal
from hbmqtt.client import ClientException, MQTTClient
from hbmqtt.mqtt.constants import QOS_2
from yarl import URL

from gs.relay import GSRelay

t = Terminal()


@click.group()
def cli():
    pass


def random_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for x in range(size))


def create_task(af):
    """ asyncio.create_task in python 3.7 """
    return asyncio.ensure_future(af)


def _run(af):
    """ asyncio.run in python 3.7 """
    return asyncio.get_event_loop().run_until_complete(af)


client_id = random_generator()
default_pub = f'PROXY/CMD/{client_id}'
default_sub = f'PROXY/ANS/+'


async def sub_loop(topic, host, port, username, password):
    C = MQTTClient()
    url = str(URL.build(scheme='mqtt', host=host, port=port,
                        user=username, password=password))
    await C.connect(url)
    await C.subscribe([(topic, QOS_2)])
    click.echo("listening ...")
    while True:
        message = await C.deliver_message()
        packet = message.publish_packet
        print(t.dim(message.topic + " >> " + packet.payload.data.decode('UTF-8')))


async def send_loop(topic, host, port, username, password):
    C = MQTTClient()
    url = str(URL.build(scheme='mqtt', host=host, port=port,
                        user=username, password=password))
    await C.connect(url)
    while True:
        cmd = await ainput()
        cmd = cmd.strip()
        if cmd:
            await C.publish(topic, cmd.encode('UTF-8'), qos=QOS_2)
    await C.disconnect()


def _add_signal_handlers(loop):

    async def shutdown(signal, loop):
        print(signal.name)
        tasks = [t for t in asyncio.Task.all_tasks() if t is not
                 asyncio.Task.current_task()]
        [task.cancel() for task in tasks]
        await asyncio.wait(tasks)
        loop.stop()

    signals = (signal.SIGHUP, signal.SIGTERM, signal.SIGINT)
    for s in signals:
        loop.add_signal_handler(
            s, lambda s=s: create_task(shutdown(s, loop)))


@cli.command()
@click.option('--sub-topic', default=default_sub)
@click.option('--pub-topic', default=default_pub)
@click.option('--host', default=os.environ.get("GS_MQTT_HOST", "127.0.0.1"))
@click.option('--port', default=int(os.environ.get("GS_MQTT_PORT", 1883)))
@click.option('--username', default=os.environ.get("GS_MQTT_USER"))
@click.option('--password', default=os.environ.get("GS_MQTT_PASS"))
def repl(sub_topic, pub_topic, host, port, username, password):
    loop = asyncio.get_event_loop()

    create_task(
        sub_loop(sub_topic, host, port, username, password))
    create_task(
        send_loop(pub_topic, host, port, username, password))

    _add_signal_handlers(loop)

    loop.run_forever()


@cli.group()
def relay():
    pass


def print_relay_status(status):
    msgs, warnings = status
    if msgs:
        click.echo("\n".join(msgs))
    for warning in warnings:
        click.echo(
            click.style(warning, fg='black', bg='red'))
        

@relay.command()
@click.option('--relay-host', default=os.environ.get("GS_RELAY_HOST", "127.0.0.1"))
@click.option('--relay-port', default=int(os.environ.get("GS_RELAY_PORT", 8080)))
def status(relay_host, relay_port):
    relay = GSRelay(relay_host, relay_port)
    print_relay_status(relay.human_status())


@relay.command()
@click.option('--relay-host', default=os.environ.get("GS_RELAY_HOST", "127.0.0.1"))
@click.option('--relay-port', default=int(os.environ.get("GS_RELAY_PORT", 8080)))
def start(relay_host, relay_port):
    relay = GSRelay(relay_host, relay_port)
    print(relay.start())
    print_relay_status(relay.human_status())


@relay.command()
@click.option('--relay-host', default=os.environ.get("GS_RELAY_HOST", "127.0.0.1"))
@click.option('--relay-port', default=int(os.environ.get("GS_RELAY_PORT", 8080)))
def stop(relay_host, relay_port):
    relay = GSRelay(relay_host, relay_port)
    print(relay.stop())
    print_relay_status(relay.human_status())


@relay.command()
@click.option('--relay-host', default=os.environ.get("GS_RELAY_HOST", "127.0.0.1"))
@click.option('--relay-port', default=int(os.environ.get("GS_RELAY_PORT", 8080)))
def toggle_breaker(relay_host, relay_port):
    relay = GSRelay(relay_host, relay_port)
    print(relay.toggle_breaker())
    print_relay_status(relay.human_status())


@relay.command()
@click.option('--relay-host', default=os.environ.get("GS_RELAY_HOST", "127.0.0.1"))
@click.option('--relay-port', default=int(os.environ.get("GS_RELAY_PORT", 8080)))
def recover(relay_host, relay_port):
    relay = GSRelay(relay_host, relay_port)
    print(relay.toggle_breaker())
    print(relay.start())
    print_relay_status(relay.human_status())


@relay.command()
@click.option('--relay-host', default=os.environ.get("GS_RELAY_HOST", "127.0.0.1"))
@click.option('--relay-port', default=int(os.environ.get("GS_RELAY_PORT", 8080)))
@click.argument('command', type=click.Choice(['enable', 'disable']))
def limit_switches(relay_host, relay_port, command):
    relay = GSRelay(relay_host, relay_port)
    print({
        "enable": relay.enable_limit_switches,
        "disable": relay.disable_limit_switches
    }[command]())
    print_relay_status(relay.human_status())


def main():
    cli()


if __name__ == "__main__":
    main()
