import click
import logging as log

from config import ROOT_DIR
import cli.util

from libflagship.mqttapi import AnkerMQTTBaseClient

servertable = {
    "eu": "make-mqtt-eu.ankermake.com",
    "us": "make-mqtt.ankermake.com",
}


def mqtt_open(config, printer_index, insecure):

    with config.open() as cfg:
        if printer_index >= len(cfg.printers):
            log.fatal(f"Printer number {printer_index} out of range, max printer number is {len(cfg.printers)-1} ")
            return
        printer = cfg.printers[printer_index]
        acct = cfg.account
        server = servertable[acct.region]
        env.log.info(f"Connecting printer {printer.p2p_duid} through {server}")
        client = AnkerMQTTBaseClient.login(
            printer.sn,
            acct.mqtt_username,
            acct.mqtt_password,
            printer.mqtt_key,
            ca_certs=ROOT_DIR / "ssl/ankermake-mqtt.crt",
            verify=not insecure,
        )
        client.connect(server)
        return client


def mqtt_command(client, msg):
    client.command(msg)

    reply = client.await_response(msg["commandType"])
    if reply:
        click.echo(cli.util.pretty_json(reply))
    else:
        log.error("No response from printer")
