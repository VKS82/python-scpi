from scpi import SCPIDevice
import decimal


class KSPowerSupply(SCPIDevice):
    """
    Class that implements KeySight N6700 SCPI functions.
    Follows design pattern from: https://github.com/rambo/python-scpi
    KeySight SCPI commands defined in N6700 User manual (N6700-90902.pdf)
    """

    def __init__(self, protocol):
        super().__init__(protocol)

        self.channel_list = [1,2,3,4]

    async def measure_dc_current(self, channel):
        """
        Measure Channels current in Amps
        :param channel: channel to measure
        :return:response
        """
        resp = await self.ask('MEAS:CURR? (@{})'.format(channel))
        return decimal.Decimal(resp)

    async def measure_dc_voltage(self, channel):
        """
        Measure channel's voltage in volts
        :param channel: channel to measure
        :return: response
        """
        resp = await self.ask('MEAS:VOLT? (@{})'.format(channel))
        return decimal.Decimal(resp)

    async def measure_rms_current(self, channel):
        resp = await self.ask('MEAS:CURR:ACDC? (@{})'.format(channel))
        return decimal.Decimal(resp)

    async def enable_channel(self, channel):
        resp = await self.ask('OUTP ON, (@{})'.format(channel))
        return decimal.Decimal(resp)

    async def disable_channel(self, channel):
        resp = await self.ask('OUTP OFF, (@{})'.format(channel))
        return decimal.Decimal(resp)

    async def get_channel_state(self, channel):
        resp = await self.ask('OUTP? (@{})'.format(channel))
        return decimal.Decimal(resp)

    async def set_constant_current(self, channel):
        """
        Set a channel to operate in constant current mode
        :param channel: channel to configure
        :return:
        """
        resp = await self.ask('OUTP:PMOD CURR, (@{})'.format(channel))
        return decimal.Decimal(resp)

    async def set_constant_voltage(self, channel):
        """
        Set a channel to operate in constant voltage mode
        :param channel: channel to configure
        :return:
        """
        resp = await self.ask('OUTP:PMOD VOLT, (@{})'.format(channel))
        return decimal.Decimal(resp)

    async def set_current_range(self, max, channel):
        """
        :param max: Max Current in Amps
        :param channel: Channel to set max current on
        :return: response
        """
        resp = await self.ask('CURR:RANG {}, (@{})'.format(max,channel))
        return decimal.Decimal(resp)

    async def get_current_range(self, channel):
        resp = await self.ask('CURR:RANG: (@{})'.format(channel))
        return decimal.Decimal(resp)

    async def set_current(self, amps, channel):
        """
        Set current on a channel, must be within a channels allowable current range
        :param amps: current in amps to set
        :param channel: channel to configure
        :return: response
        """
        resp = await self.ask('CURR {}, (@{})'.format(amps, channel))
        return decimal.Decimal(resp)

    async def set_power_limit(self, power, channel):
        """
        Set power limit on a channel in watts
        :param power: power in watts
        :param channel: channel to configure
        :return: response
        """
        resp = await self.ask('POW:LIM {}, (@{})'.format(power, channel))
        return decimal.Decimal(resp)

    async def set_voltage(self, voltage, channel):
        """
        Set voltage on a channel
        :param voltage: voltage in volts
        :param channel: channel to configure
        :return: response
        """
        resp = await self.ask('VOLT {}, (@{})'.format(voltage, channel))
        return decimal.Decimal(resp)

    async def set_voltage_limit(self, max, channel):
        """
        Set Voltage limit on a channel
        :param max: voltage in volts
        :param channel: channel to configure
        :return: response
        """
        resp = await self.ask('VOLT:LIM {}, (@{})'.format(max, channel))
        return decimal.Decimal(resp)

    async def get_voltage_limit(self, channel):
        resp = await self.ask('VOLT:LIM? (@{})'.format(channel))
        return decimal.Decimal(resp)



def tcp(ip, port):
    """Quick helper to connect via TCP"""
    from scpi.transports.tcp import get as get_tcp
    from scpi import SCPIProtocol
    transport = get_tcp(ip, port)
    protocol = SCPIProtocol(transport)
    dev = KSPowerSupply(protocol)
    return dev
