import json
import socket
import time
import logging

logger = logging.getLogger("gs.relay")


HOLD_BUTTON_S = 2
BUTTON_MAP = {
    "stop_button": "relay1",
    "breaker_toggle": "relay2",
    "start_button": "relay3",
    "limit_switch_disable": "relay4"
}
RELAY_MAP = {v: k for k, v in BUTTON_MAP.items()}


class GSRelay(object):
    buffer_size = 1024

    def __init__(self, host, port):
        self.host = host
        self.port = port
        logger.info(f"relay host: {host}")
        logger.info(f"relay port: {port}")
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((self.host, self.port))

    def _send(self, data=None, raw=None):
        if raw:
            encoded = raw
        else:
            encoded = json.dumps(data, separators=(',', ':')).encode()
        logger.debug("sending message: {msg}".format(msg=str(encoded)))
        self.socket.send(encoded)
        data = self.socket.recv(self.buffer_size)
        logger.debug("received message: {msg}".format(msg=str(data)))
        data = data.strip(b'\x00')  # null terminated response
        return json.loads(data.decode())

    def _press_button(self, relay):
        data_on = self._send({relay: "on"})
        time.sleep(HOLD_BUTTON_S)
        data_off = self._send({relay: "off"})
        return [data_on, data_off]

    def start(self):
        """ This function physically presses the start button
            in the cabinet (5 in diagram)
        """
        return self._press_button(BUTTON_MAP["start_button"])

    def stop(self):
        """ This function physically presses the stop
            button in the cabinet (4 in diagram)
        """
        return self._press_button(BUTTON_MAP["stop_button"])

    def toggle_breaker(self):
        """ This function physically toggles the breaker
            in the cabinet. (2 in diagram)

            The breaker must be pressed after stop, in order for
            the start button to work.
        """
        return self._press_button(BUTTON_MAP["breaker_toggle"])

    def disable_limit_switches(self):
        switch = BUTTON_MAP["limit_switch_disable"]
        return self._send({switch: "on"})

    def enable_limit_switches(self):
        switch = BUTTON_MAP["limit_switch_disable"]
        return self._send({switch: "off"})

    def status(self):
        return self._send({"get":"relayStatus"})

    def named_status(self):
        status = self.status()
        return {RELAY_MAP.get(k, k): v for k, v in status.items()}

    def human_status(self):
        status = self.named_status()
        msgs = ["\t".join([k, v]) for k, v in status.items()]
        warnings = []
        if status["limit_switch_disable"] == "on":
            warnings += ["Warning! Limit Switch is Disabled!"]
        return msgs, warnings
