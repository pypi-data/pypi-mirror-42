# Generated from 'v1_8_1.xml' on 2019-02-12 07:24:21.065046

from typing import Tuple

from toptica.lasersdk.client import AccessLevel
from toptica.lasersdk.client import Client

from toptica.lasersdk.client import DecofBoolean
from toptica.lasersdk.client import DecofInteger
from toptica.lasersdk.client import DecofReal
from toptica.lasersdk.client import DecofString
from toptica.lasersdk.client import DecofBinary

from toptica.lasersdk.client import MutableDecofBoolean
from toptica.lasersdk.client import MutableDecofInteger
from toptica.lasersdk.client import MutableDecofReal
from toptica.lasersdk.client import MutableDecofString
from toptica.lasersdk.client import MutableDecofBinary

from toptica.lasersdk.client import Connection
from toptica.lasersdk.client import NetworkConnection
from toptica.lasersdk.client import SerialConnection

from toptica.lasersdk.client import DecofError
from toptica.lasersdk.client import DeviceNotFoundError


class BuildInformation:
    def __init__(self, client: Client, name: str) -> None:
        self.__client = client
        self.__name = name
        self._c_compiler_version = DecofString(client, name + ':c-compiler-version')
        self._build_number = DecofInteger(client, name + ':build-number')
        self._cxx_compiler_id = DecofString(client, name + ':cxx-compiler-id')
        self._build_tag = DecofString(client, name + ':build-tag')
        self._job_name = DecofString(client, name + ':job-name')
        self._c_compiler_id = DecofString(client, name + ':c-compiler-id')
        self._build_node_name = DecofString(client, name + ':build-node-name')
        self._build_id = DecofString(client, name + ':build-id')
        self._build_url = DecofString(client, name + ':build-url')
        self._cxx_compiler_version = DecofString(client, name + ':cxx-compiler-version')

    @property
    def c_compiler_version(self) -> 'DecofString':
        return self._c_compiler_version

    @property
    def build_number(self) -> 'DecofInteger':
        return self._build_number

    @property
    def cxx_compiler_id(self) -> 'DecofString':
        return self._cxx_compiler_id

    @property
    def build_tag(self) -> 'DecofString':
        return self._build_tag

    @property
    def job_name(self) -> 'DecofString':
        return self._job_name

    @property
    def c_compiler_id(self) -> 'DecofString':
        return self._c_compiler_id

    @property
    def build_node_name(self) -> 'DecofString':
        return self._build_node_name

    @property
    def build_id(self) -> 'DecofString':
        return self._build_id

    @property
    def build_url(self) -> 'DecofString':
        return self._build_url

    @property
    def cxx_compiler_version(self) -> 'DecofString':
        return self._cxx_compiler_version


class CcBoard:
    def __init__(self, client: Client, name: str) -> None:
        self.__client = client
        self.__name = name
        self._board_temp = DecofReal(client, name + ':board-temp')
        self._channel2 = CurrDrv2(client, name + ':channel2')
        self._channel1 = CurrDrv2(client, name + ':channel1')
        self._status = DecofInteger(client, name + ':status')
        self._serial_number = DecofString(client, name + ':serial-number')
        self._variant = DecofString(client, name + ':variant')
        self._revision = DecofString(client, name + ':revision')
        self._slot = DecofString(client, name + ':slot')
        self._fpga_fw_ver = DecofInteger(client, name + ':fpga-fw-ver')
        self._parallel_mode = DecofBoolean(client, name + ':parallel-mode')
        self._status_txt = DecofString(client, name + ':status-txt')

    @property
    def board_temp(self) -> 'DecofReal':
        return self._board_temp

    @property
    def channel2(self) -> 'CurrDrv2':
        return self._channel2

    @property
    def channel1(self) -> 'CurrDrv2':
        return self._channel1

    @property
    def status(self) -> 'DecofInteger':
        return self._status

    @property
    def serial_number(self) -> 'DecofString':
        return self._serial_number

    @property
    def variant(self) -> 'DecofString':
        return self._variant

    @property
    def revision(self) -> 'DecofString':
        return self._revision

    @property
    def slot(self) -> 'DecofString':
        return self._slot

    @property
    def fpga_fw_ver(self) -> 'DecofInteger':
        return self._fpga_fw_ver

    @property
    def parallel_mode(self) -> 'DecofBoolean':
        return self._parallel_mode

    @property
    def status_txt(self) -> 'DecofString':
        return self._status_txt


class CurrDrv2:
    def __init__(self, client: Client, name: str) -> None:
        self.__client = client
        self.__name = name
        self._snubber = MutableDecofBoolean(client, name + ':snubber')
        self._feedforward_enabled = MutableDecofBoolean(client, name + ':feedforward-enabled')
        self._current_set_dithering = MutableDecofBoolean(client, name + ':current-set-dithering')
        self._emission = DecofBoolean(client, name + ':emission')
        self._aux = DecofReal(client, name + ':aux')
        self._feedforward_factor = MutableDecofReal(client, name + ':feedforward-factor')
        self._current_act = DecofReal(client, name + ':current-act')
        self._external_input = ExtInput3(client, name + ':external-input')
        self._pd = DecofReal(client, name + ':pd')
        self._output_filter = OutputFilter3(client, name + ':output-filter')
        self._positive_polarity = MutableDecofBoolean(client, name + ':positive-polarity')
        self._current_offset = MutableDecofReal(client, name + ':current-offset')
        self._current_set = MutableDecofReal(client, name + ':current-set')
        self._enabled = MutableDecofBoolean(client, name + ':enabled')
        self._status_txt = DecofString(client, name + ':status-txt')
        self._current_clip = MutableDecofReal(client, name + ':current-clip')
        self._status = DecofInteger(client, name + ':status')
        self._variant = DecofString(client, name + ':variant')
        self._feedforward_master = MutableDecofInteger(client, name + ':feedforward-master')
        self._voltage_act = DecofReal(client, name + ':voltage-act')
        self._forced_off = MutableDecofBoolean(client, name + ':forced-off')
        self._voltage_clip = MutableDecofReal(client, name + ':voltage-clip')
        self._current_clip_limit = DecofReal(client, name + ':current-clip-limit')
        self._path = DecofString(client, name + ':path')

    @property
    def snubber(self) -> 'MutableDecofBoolean':
        return self._snubber

    @property
    def feedforward_enabled(self) -> 'MutableDecofBoolean':
        return self._feedforward_enabled

    @property
    def current_set_dithering(self) -> 'MutableDecofBoolean':
        return self._current_set_dithering

    @property
    def emission(self) -> 'DecofBoolean':
        return self._emission

    @property
    def aux(self) -> 'DecofReal':
        return self._aux

    @property
    def feedforward_factor(self) -> 'MutableDecofReal':
        return self._feedforward_factor

    @property
    def current_act(self) -> 'DecofReal':
        return self._current_act

    @property
    def external_input(self) -> 'ExtInput3':
        return self._external_input

    @property
    def pd(self) -> 'DecofReal':
        return self._pd

    @property
    def output_filter(self) -> 'OutputFilter3':
        return self._output_filter

    @property
    def positive_polarity(self) -> 'MutableDecofBoolean':
        return self._positive_polarity

    @property
    def current_offset(self) -> 'MutableDecofReal':
        return self._current_offset

    @property
    def current_set(self) -> 'MutableDecofReal':
        return self._current_set

    @property
    def enabled(self) -> 'MutableDecofBoolean':
        return self._enabled

    @property
    def status_txt(self) -> 'DecofString':
        return self._status_txt

    @property
    def current_clip(self) -> 'MutableDecofReal':
        return self._current_clip

    @property
    def status(self) -> 'DecofInteger':
        return self._status

    @property
    def variant(self) -> 'DecofString':
        return self._variant

    @property
    def feedforward_master(self) -> 'MutableDecofInteger':
        return self._feedforward_master

    @property
    def voltage_act(self) -> 'DecofReal':
        return self._voltage_act

    @property
    def forced_off(self) -> 'MutableDecofBoolean':
        return self._forced_off

    @property
    def voltage_clip(self) -> 'MutableDecofReal':
        return self._voltage_clip

    @property
    def current_clip_limit(self) -> 'DecofReal':
        return self._current_clip_limit

    @property
    def path(self) -> 'DecofString':
        return self._path


class ExtInput3:
    def __init__(self, client: Client, name: str) -> None:
        self.__client = client
        self.__name = name
        self._signal = MutableDecofInteger(client, name + ':signal')
        self._enabled = MutableDecofBoolean(client, name + ':enabled')
        self._factor = MutableDecofReal(client, name + ':factor')

    @property
    def signal(self) -> 'MutableDecofInteger':
        return self._signal

    @property
    def enabled(self) -> 'MutableDecofBoolean':
        return self._enabled

    @property
    def factor(self) -> 'MutableDecofReal':
        return self._factor


class OutputFilter3:
    def __init__(self, client: Client, name: str) -> None:
        self.__client = client
        self.__name = name
        self._slew_rate_enabled = MutableDecofBoolean(client, name + ':slew-rate-enabled')
        self._slew_rate = MutableDecofReal(client, name + ':slew-rate')
        self._slew_rate_limited = DecofBoolean(client, name + ':slew-rate-limited')

    @property
    def slew_rate_enabled(self) -> 'MutableDecofBoolean':
        return self._slew_rate_enabled

    @property
    def slew_rate(self) -> 'MutableDecofReal':
        return self._slew_rate

    @property
    def slew_rate_limited(self) -> 'DecofBoolean':
        return self._slew_rate_limited


class Cc5000Board:
    def __init__(self, client: Client, name: str) -> None:
        self.__client = client
        self.__name = name
        self._regulator_temp = DecofReal(client, name + ':regulator-temp')
        self._channel1 = Cc5000Drv(client, name + ':channel1')
        self._board_temp = DecofReal(client, name + ':board-temp')
        self._power_15v = MutableDecofBoolean(client, name + ':power-15v')
        self._status = DecofInteger(client, name + ':status')
        self._serial_number = DecofString(client, name + ':serial-number')
        self._variant = DecofString(client, name + ':variant')
        self._inverter_temp = DecofReal(client, name + ':inverter-temp')
        self._revision = DecofString(client, name + ':revision')
        self._slot = DecofString(client, name + ':slot')
        self._fpga_fw_ver = DecofInteger(client, name + ':fpga-fw-ver')
        self._regulator_temp_fuse = DecofReal(client, name + ':regulator-temp-fuse')
        self._parallel_mode = DecofBoolean(client, name + ':parallel-mode')
        self._inverter_temp_fuse = DecofReal(client, name + ':inverter-temp-fuse')
        self._status_txt = DecofString(client, name + ':status-txt')

    @property
    def regulator_temp(self) -> 'DecofReal':
        return self._regulator_temp

    @property
    def channel1(self) -> 'Cc5000Drv':
        return self._channel1

    @property
    def board_temp(self) -> 'DecofReal':
        return self._board_temp

    @property
    def power_15v(self) -> 'MutableDecofBoolean':
        return self._power_15v

    @property
    def status(self) -> 'DecofInteger':
        return self._status

    @property
    def serial_number(self) -> 'DecofString':
        return self._serial_number

    @property
    def variant(self) -> 'DecofString':
        return self._variant

    @property
    def inverter_temp(self) -> 'DecofReal':
        return self._inverter_temp

    @property
    def revision(self) -> 'DecofString':
        return self._revision

    @property
    def slot(self) -> 'DecofString':
        return self._slot

    @property
    def fpga_fw_ver(self) -> 'DecofInteger':
        return self._fpga_fw_ver

    @property
    def regulator_temp_fuse(self) -> 'DecofReal':
        return self._regulator_temp_fuse

    @property
    def parallel_mode(self) -> 'DecofBoolean':
        return self._parallel_mode

    @property
    def inverter_temp_fuse(self) -> 'DecofReal':
        return self._inverter_temp_fuse

    @property
    def status_txt(self) -> 'DecofString':
        return self._status_txt


class Cc5000Drv:
    def __init__(self, client: Client, name: str) -> None:
        self.__client = client
        self.__name = name
        self._feedforward_enabled = MutableDecofBoolean(client, name + ':feedforward-enabled')
        self._voltage_out = DecofReal(client, name + ':voltage-out')
        self._emission = DecofBoolean(client, name + ':emission')
        self._aux = DecofReal(client, name + ':aux')
        self._feedforward_master = MutableDecofInteger(client, name + ':feedforward-master')
        self._feedforward_factor = MutableDecofReal(client, name + ':feedforward-factor')
        self._current_act = DecofReal(client, name + ':current-act')
        self._variant = DecofString(client, name + ':variant')
        self._current_offset = MutableDecofReal(client, name + ':current-offset')
        self._current_set = MutableDecofReal(client, name + ':current-set')
        self._enabled = MutableDecofBoolean(client, name + ':enabled')
        self._status_txt = DecofString(client, name + ':status-txt')
        self._current_clip = MutableDecofReal(client, name + ':current-clip')
        self._status = DecofInteger(client, name + ':status')
        self._output_filter = OutputFilter2(client, name + ':output-filter')
        self._voltage_act = DecofReal(client, name + ':voltage-act')
        self._forced_off = MutableDecofBoolean(client, name + ':forced-off')
        self._voltage_clip = MutableDecofReal(client, name + ':voltage-clip')
        self._current_clip_limit = DecofReal(client, name + ':current-clip-limit')
        self._path = DecofString(client, name + ':path')

    @property
    def feedforward_enabled(self) -> 'MutableDecofBoolean':
        return self._feedforward_enabled

    @property
    def voltage_out(self) -> 'DecofReal':
        return self._voltage_out

    @property
    def emission(self) -> 'DecofBoolean':
        return self._emission

    @property
    def aux(self) -> 'DecofReal':
        return self._aux

    @property
    def feedforward_master(self) -> 'MutableDecofInteger':
        return self._feedforward_master

    @property
    def feedforward_factor(self) -> 'MutableDecofReal':
        return self._feedforward_factor

    @property
    def current_act(self) -> 'DecofReal':
        return self._current_act

    @property
    def variant(self) -> 'DecofString':
        return self._variant

    @property
    def current_offset(self) -> 'MutableDecofReal':
        return self._current_offset

    @property
    def current_set(self) -> 'MutableDecofReal':
        return self._current_set

    @property
    def enabled(self) -> 'MutableDecofBoolean':
        return self._enabled

    @property
    def status_txt(self) -> 'DecofString':
        return self._status_txt

    @property
    def current_clip(self) -> 'MutableDecofReal':
        return self._current_clip

    @property
    def status(self) -> 'DecofInteger':
        return self._status

    @property
    def output_filter(self) -> 'OutputFilter2':
        return self._output_filter

    @property
    def voltage_act(self) -> 'DecofReal':
        return self._voltage_act

    @property
    def forced_off(self) -> 'MutableDecofBoolean':
        return self._forced_off

    @property
    def voltage_clip(self) -> 'MutableDecofReal':
        return self._voltage_clip

    @property
    def current_clip_limit(self) -> 'DecofReal':
        return self._current_clip_limit

    @property
    def path(self) -> 'DecofString':
        return self._path


class OutputFilter2:
    def __init__(self, client: Client, name: str) -> None:
        self.__client = client
        self.__name = name
        self._slew_rate_enabled = MutableDecofBoolean(client, name + ':slew-rate-enabled')
        self._slew_rate = MutableDecofReal(client, name + ':slew-rate')
        self._slew_rate_limited = DecofBoolean(client, name + ':slew-rate-limited')

    @property
    def slew_rate_enabled(self) -> 'MutableDecofBoolean':
        return self._slew_rate_enabled

    @property
    def slew_rate(self) -> 'MutableDecofReal':
        return self._slew_rate

    @property
    def slew_rate_limited(self) -> 'DecofBoolean':
        return self._slew_rate_limited


class Laser:
    def __init__(self, client: Client, name: str) -> None:
        self.__client = client
        self.__name = name
        self._product_name = DecofString(client, name + ':product-name')
        self._dl = LaserHead(client, name + ':dl')
        self._nlo = Nlo(client, name + ':nlo')
        self._emission = DecofBoolean(client, name + ':emission')
        self._dpss = Dpss2(client, name + ':dpss')
        self._pd_ext = PdExt(client, name + ':pd-ext')
        self._scan = ScanGenerator(client, name + ':scan')
        self._uv = UvShg(client, name + ':uv')
        self._recorder = Recorder(client, name + ':recorder')
        self._health = DecofInteger(client, name + ':health')
        self._power_stabilization = PwrStab(client, name + ':power-stabilization')
        self._config = LaserConfig(client, name + ':config')
        self._ctl = CtlT(client, name + ':ctl')
        self._type_ = DecofString(client, name + ':type')
        self._amp = LaserAmp(client, name + ':amp')
        self._wide_scan = WideScan(client, name + ':wide-scan')
        self._scope = ScopeT(client, name + ':scope')
        self._health_txt = DecofString(client, name + ':health-txt')

    @property
    def product_name(self) -> 'DecofString':
        return self._product_name

    @property
    def dl(self) -> 'LaserHead':
        return self._dl

    @property
    def nlo(self) -> 'Nlo':
        return self._nlo

    @property
    def emission(self) -> 'DecofBoolean':
        return self._emission

    @property
    def dpss(self) -> 'Dpss2':
        return self._dpss

    @property
    def pd_ext(self) -> 'PdExt':
        return self._pd_ext

    @property
    def scan(self) -> 'ScanGenerator':
        return self._scan

    @property
    def uv(self) -> 'UvShg':
        return self._uv

    @property
    def recorder(self) -> 'Recorder':
        return self._recorder

    @property
    def health(self) -> 'DecofInteger':
        return self._health

    @property
    def power_stabilization(self) -> 'PwrStab':
        return self._power_stabilization

    @property
    def config(self) -> 'LaserConfig':
        return self._config

    @property
    def ctl(self) -> 'CtlT':
        return self._ctl

    @property
    def type_(self) -> 'DecofString':
        return self._type_

    @property
    def amp(self) -> 'LaserAmp':
        return self._amp

    @property
    def wide_scan(self) -> 'WideScan':
        return self._wide_scan

    @property
    def scope(self) -> 'ScopeT':
        return self._scope

    @property
    def health_txt(self) -> 'DecofString':
        return self._health_txt

    def load_head(self) -> None:
        self.__client.exec(self.__name + ':load-head', input_stream=None, output_type=None, return_type=None)

    def load(self) -> None:
        self.__client.exec(self.__name + ':load', input_stream=None, output_type=None, return_type=None)

    def save(self) -> None:
        self.__client.exec(self.__name + ':save', input_stream=None, output_type=None, return_type=None)


class LaserHead:
    def __init__(self, client: Client, name: str) -> None:
        self.__client = client
        self.__name = name
        self._model = DecofString(client, name + ':model')
        self._factory_settings = LhFactory(client, name + ':factory-settings')
        self._serial_number = DecofString(client, name + ':serial-number')
        self._legacy = DecofBoolean(client, name + ':legacy')
        self._cc = CurrDrv1(client, name + ':cc')
        self._pc = PiezoDrv2(client, name + ':pc')
        self._lock = Lock(client, name + ':lock')
        self._ontime_txt = DecofString(client, name + ':ontime-txt')
        self._pressure_compensation = PressureCompensation(client, name + ':pressure-compensation')
        self._pd = PdCal(client, name + ':pd')
        self._type_ = DecofString(client, name + ':type')
        self._ontime = DecofInteger(client, name + ':ontime')
        self._tc = TcChannel2(client, name + ':tc')
        self._version = DecofString(client, name + ':version')

    @property
    def model(self) -> 'DecofString':
        return self._model

    @property
    def factory_settings(self) -> 'LhFactory':
        return self._factory_settings

    @property
    def serial_number(self) -> 'DecofString':
        return self._serial_number

    @property
    def legacy(self) -> 'DecofBoolean':
        return self._legacy

    @property
    def cc(self) -> 'CurrDrv1':
        return self._cc

    @property
    def pc(self) -> 'PiezoDrv2':
        return self._pc

    @property
    def lock(self) -> 'Lock':
        return self._lock

    @property
    def ontime_txt(self) -> 'DecofString':
        return self._ontime_txt

    @property
    def pressure_compensation(self) -> 'PressureCompensation':
        return self._pressure_compensation

    @property
    def pd(self) -> 'PdCal':
        return self._pd

    @property
    def type_(self) -> 'DecofString':
        return self._type_

    @property
    def ontime(self) -> 'DecofInteger':
        return self._ontime

    @property
    def tc(self) -> 'TcChannel2':
        return self._tc

    @property
    def version(self) -> 'DecofString':
        return self._version

    def restore(self) -> None:
        self.__client.exec(self.__name + ':restore', input_stream=None, output_type=None, return_type=None)

    def store(self) -> None:
        self.__client.exec(self.__name + ':store', input_stream=None, output_type=None, return_type=None)


class LhFactory:
    def __init__(self, client: Client, name: str) -> None:
        self.__client = client
        self.__name = name
        self._last_modified = DecofString(client, name + ':last-modified')
        self._threshold_current = MutableDecofReal(client, name + ':threshold-current')
        self._pd = PdCalFactorySettings(client, name + ':pd')
        self._cc = LhFactoryCc(client, name + ':cc')
        self._pc = PcFactorySettings(client, name + ':pc')
        self._modified = DecofBoolean(client, name + ':modified')
        self._power = MutableDecofReal(client, name + ':power')
        self._tc = TcFactorySettings(client, name + ':tc')
        self._wavelength = MutableDecofReal(client, name + ':wavelength')

    @property
    def last_modified(self) -> 'DecofString':
        return self._last_modified

    @property
    def threshold_current(self) -> 'MutableDecofReal':
        return self._threshold_current

    @property
    def pd(self) -> 'PdCalFactorySettings':
        return self._pd

    @property
    def cc(self) -> 'LhFactoryCc':
        return self._cc

    @property
    def pc(self) -> 'PcFactorySettings':
        return self._pc

    @property
    def modified(self) -> 'DecofBoolean':
        return self._modified

    @property
    def power(self) -> 'MutableDecofReal':
        return self._power

    @property
    def tc(self) -> 'TcFactorySettings':
        return self._tc

    @property
    def wavelength(self) -> 'MutableDecofReal':
        return self._wavelength

    def apply(self) -> None:
        self.__client.exec(self.__name + ':apply', input_stream=None, output_type=None, return_type=None)

    def retrieve_now(self) -> None:
        self.__client.exec(self.__name + ':retrieve-now', input_stream=None, output_type=None, return_type=None)


class PdCalFactorySettings:
    def __init__(self, client: Client, name: str) -> None:
        self.__client = client
        self.__name = name
        self._cal_offset = MutableDecofReal(client, name + ':cal-offset')
        self._cal_factor = MutableDecofReal(client, name + ':cal-factor')

    @property
    def cal_offset(self) -> 'MutableDecofReal':
        return self._cal_offset

    @property
    def cal_factor(self) -> 'MutableDecofReal':
        return self._cal_factor


class LhFactoryCc:
    def __init__(self, client: Client, name: str) -> None:
        self.__client = client
        self.__name = name
        self._current_clip = MutableDecofReal(client, name + ':current-clip')
        self._current_clip_last_modified = DecofString(client, name + ':current-clip-last-modified')
        self._positive_polarity = MutableDecofBoolean(client, name + ':positive-polarity')
        self._voltage_clip = MutableDecofReal(client, name + ':voltage-clip')
        self._snubber = MutableDecofBoolean(client, name + ':snubber')
        self._current_set = MutableDecofReal(client, name + ':current-set')
        self._feedforward_factor = MutableDecofReal(client, name + ':feedforward-factor')
        self._current_clip_modified = DecofBoolean(client, name + ':current-clip-modified')

    @property
    def current_clip(self) -> 'MutableDecofReal':
        return self._current_clip

    @property
    def current_clip_last_modified(self) -> 'DecofString':
        return self._current_clip_last_modified

    @property
    def positive_polarity(self) -> 'MutableDecofBoolean':
        return self._positive_polarity

    @property
    def voltage_clip(self) -> 'MutableDecofReal':
        return self._voltage_clip

    @property
    def snubber(self) -> 'MutableDecofBoolean':
        return self._snubber

    @property
    def current_set(self) -> 'MutableDecofReal':
        return self._current_set

    @property
    def feedforward_factor(self) -> 'MutableDecofReal':
        return self._feedforward_factor

    @property
    def current_clip_modified(self) -> 'DecofBoolean':
        return self._current_clip_modified


class PcFactorySettings:
    def __init__(self, client: Client, name: str) -> None:
        self.__client = client
        self.__name = name
        self._scan_offset = MutableDecofReal(client, name + ':scan-offset')
        self._feedforward_enabled = MutableDecofBoolean(client, name + ':feedforward-enabled')
        self._slew_rate = MutableDecofReal(client, name + ':slew-rate')
        self._scan_amplitude = MutableDecofReal(client, name + ':scan-amplitude')
        self._pressure_compensation_factor = MutableDecofReal(client, name + ':pressure-compensation-factor')
        self._capacitance = MutableDecofReal(client, name + ':capacitance')
        self._voltage_max = MutableDecofReal(client, name + ':voltage-max')
        self._voltage_min = MutableDecofReal(client, name + ':voltage-min')
        self._feedforward_factor = MutableDecofReal(client, name + ':feedforward-factor')
        self._slew_rate_enabled = MutableDecofBoolean(client, name + ':slew-rate-enabled')

    @property
    def scan_offset(self) -> 'MutableDecofReal':
        return self._scan_offset

    @property
    def feedforward_enabled(self) -> 'MutableDecofBoolean':
        return self._feedforward_enabled

    @property
    def slew_rate(self) -> 'MutableDecofReal':
        return self._slew_rate

    @property
    def scan_amplitude(self) -> 'MutableDecofReal':
        return self._scan_amplitude

    @property
    def pressure_compensation_factor(self) -> 'MutableDecofReal':
        return self._pressure_compensation_factor

    @property
    def capacitance(self) -> 'MutableDecofReal':
        return self._capacitance

    @property
    def voltage_max(self) -> 'MutableDecofReal':
        return self._voltage_max

    @property
    def voltage_min(self) -> 'MutableDecofReal':
        return self._voltage_min

    @property
    def feedforward_factor(self) -> 'MutableDecofReal':
        return self._feedforward_factor

    @property
    def slew_rate_enabled(self) -> 'MutableDecofBoolean':
        return self._slew_rate_enabled


class TcFactorySettings:
    def __init__(self, client: Client, name: str) -> None:
        self.__client = client
        self.__name = name
        self._ok_tolerance = MutableDecofReal(client, name + ':ok-tolerance')
        self._temp_min = MutableDecofReal(client, name + ':temp-min')
        self._temp_roc_enabled = MutableDecofBoolean(client, name + ':temp-roc-enabled')
        self._i_gain = MutableDecofReal(client, name + ':i-gain')
        self._p_gain = MutableDecofReal(client, name + ':p-gain')
        self._ntc_series_resistance = MutableDecofReal(client, name + ':ntc-series-resistance')
        self._d_gain = MutableDecofReal(client, name + ':d-gain')
        self._ntc_parallel_resistance = MutableDecofReal(client, name + ':ntc-parallel-resistance')
        self._temp_set = MutableDecofReal(client, name + ':temp-set')
        self._current_min = MutableDecofReal(client, name + ':current-min')
        self._ok_time = MutableDecofReal(client, name + ':ok-time')
        self._temp_max = MutableDecofReal(client, name + ':temp-max')
        self._power_source = MutableDecofInteger(client, name + ':power-source')
        self._current_max = MutableDecofReal(client, name + ':current-max')
        self._temp_roc_limit = MutableDecofReal(client, name + ':temp-roc-limit')
        self._c_gain = MutableDecofReal(client, name + ':c-gain')
        self._timeout = MutableDecofInteger(client, name + ':timeout')

    @property
    def ok_tolerance(self) -> 'MutableDecofReal':
        return self._ok_tolerance

    @property
    def temp_min(self) -> 'MutableDecofReal':
        return self._temp_min

    @property
    def temp_roc_enabled(self) -> 'MutableDecofBoolean':
        return self._temp_roc_enabled

    @property
    def i_gain(self) -> 'MutableDecofReal':
        return self._i_gain

    @property
    def p_gain(self) -> 'MutableDecofReal':
        return self._p_gain

    @property
    def ntc_series_resistance(self) -> 'MutableDecofReal':
        return self._ntc_series_resistance

    @property
    def d_gain(self) -> 'MutableDecofReal':
        return self._d_gain

    @property
    def ntc_parallel_resistance(self) -> 'MutableDecofReal':
        return self._ntc_parallel_resistance

    @property
    def temp_set(self) -> 'MutableDecofReal':
        return self._temp_set

    @property
    def current_min(self) -> 'MutableDecofReal':
        return self._current_min

    @property
    def ok_time(self) -> 'MutableDecofReal':
        return self._ok_time

    @property
    def temp_max(self) -> 'MutableDecofReal':
        return self._temp_max

    @property
    def power_source(self) -> 'MutableDecofInteger':
        return self._power_source

    @property
    def current_max(self) -> 'MutableDecofReal':
        return self._current_max

    @property
    def temp_roc_limit(self) -> 'MutableDecofReal':
        return self._temp_roc_limit

    @property
    def c_gain(self) -> 'MutableDecofReal':
        return self._c_gain

    @property
    def timeout(self) -> 'MutableDecofInteger':
        return self._timeout


class CurrDrv1:
    def __init__(self, client: Client, name: str) -> None:
        self.__client = client
        self.__name = name
        self._snubber = MutableDecofBoolean(client, name + ':snubber')
        self._feedforward_enabled = MutableDecofBoolean(client, name + ':feedforward-enabled')
        self._current_set_dithering = MutableDecofBoolean(client, name + ':current-set-dithering')
        self._emission = DecofBoolean(client, name + ':emission')
        self._aux = DecofReal(client, name + ':aux')
        self._feedforward_factor = MutableDecofReal(client, name + ':feedforward-factor')
        self._current_act = DecofReal(client, name + ':current-act')
        self._external_input = ExtInput2(client, name + ':external-input')
        self._pd = DecofReal(client, name + ':pd')
        self._output_filter = OutputFilter2(client, name + ':output-filter')
        self._positive_polarity = MutableDecofBoolean(client, name + ':positive-polarity')
        self._current_offset = MutableDecofReal(client, name + ':current-offset')
        self._current_set = MutableDecofReal(client, name + ':current-set')
        self._enabled = MutableDecofBoolean(client, name + ':enabled')
        self._status_txt = DecofString(client, name + ':status-txt')
        self._current_clip = MutableDecofReal(client, name + ':current-clip')
        self._status = DecofInteger(client, name + ':status')
        self._variant = DecofString(client, name + ':variant')
        self._feedforward_master = MutableDecofInteger(client, name + ':feedforward-master')
        self._voltage_act = DecofReal(client, name + ':voltage-act')
        self._forced_off = MutableDecofBoolean(client, name + ':forced-off')
        self._voltage_clip = MutableDecofReal(client, name + ':voltage-clip')
        self._current_clip_limit = DecofReal(client, name + ':current-clip-limit')
        self._path = DecofString(client, name + ':path')

    @property
    def snubber(self) -> 'MutableDecofBoolean':
        return self._snubber

    @property
    def feedforward_enabled(self) -> 'MutableDecofBoolean':
        return self._feedforward_enabled

    @property
    def current_set_dithering(self) -> 'MutableDecofBoolean':
        return self._current_set_dithering

    @property
    def emission(self) -> 'DecofBoolean':
        return self._emission

    @property
    def aux(self) -> 'DecofReal':
        return self._aux

    @property
    def feedforward_factor(self) -> 'MutableDecofReal':
        return self._feedforward_factor

    @property
    def current_act(self) -> 'DecofReal':
        return self._current_act

    @property
    def external_input(self) -> 'ExtInput2':
        return self._external_input

    @property
    def pd(self) -> 'DecofReal':
        return self._pd

    @property
    def output_filter(self) -> 'OutputFilter2':
        return self._output_filter

    @property
    def positive_polarity(self) -> 'MutableDecofBoolean':
        return self._positive_polarity

    @property
    def current_offset(self) -> 'MutableDecofReal':
        return self._current_offset

    @property
    def current_set(self) -> 'MutableDecofReal':
        return self._current_set

    @property
    def enabled(self) -> 'MutableDecofBoolean':
        return self._enabled

    @property
    def status_txt(self) -> 'DecofString':
        return self._status_txt

    @property
    def current_clip(self) -> 'MutableDecofReal':
        return self._current_clip

    @property
    def status(self) -> 'DecofInteger':
        return self._status

    @property
    def variant(self) -> 'DecofString':
        return self._variant

    @property
    def feedforward_master(self) -> 'MutableDecofInteger':
        return self._feedforward_master

    @property
    def voltage_act(self) -> 'DecofReal':
        return self._voltage_act

    @property
    def forced_off(self) -> 'MutableDecofBoolean':
        return self._forced_off

    @property
    def voltage_clip(self) -> 'MutableDecofReal':
        return self._voltage_clip

    @property
    def current_clip_limit(self) -> 'DecofReal':
        return self._current_clip_limit

    @property
    def path(self) -> 'DecofString':
        return self._path


class ExtInput2:
    def __init__(self, client: Client, name: str) -> None:
        self.__client = client
        self.__name = name
        self._signal = MutableDecofInteger(client, name + ':signal')
        self._enabled = MutableDecofBoolean(client, name + ':enabled')
        self._factor = MutableDecofReal(client, name + ':factor')

    @property
    def signal(self) -> 'MutableDecofInteger':
        return self._signal

    @property
    def enabled(self) -> 'MutableDecofBoolean':
        return self._enabled

    @property
    def factor(self) -> 'MutableDecofReal':
        return self._factor


class PiezoDrv2:
    def __init__(self, client: Client, name: str) -> None:
        self.__client = client
        self.__name = name
        self._status = DecofInteger(client, name + ':status')
        self._feedforward_master = MutableDecofInteger(client, name + ':feedforward-master')
        self._feedforward_factor = MutableDecofReal(client, name + ':feedforward-factor')
        self._external_input = ExtInput2(client, name + ':external-input')
        self._voltage_min = MutableDecofReal(client, name + ':voltage-min')
        self._status_txt = DecofString(client, name + ':status-txt')
        self._feedforward_enabled = MutableDecofBoolean(client, name + ':feedforward-enabled')
        self._voltage_set_dithering = MutableDecofBoolean(client, name + ':voltage-set-dithering')
        self._voltage_max = MutableDecofReal(client, name + ':voltage-max')
        self._enabled = MutableDecofBoolean(client, name + ':enabled')
        self._voltage_set = MutableDecofReal(client, name + ':voltage-set')
        self._output_filter = OutputFilter2(client, name + ':output-filter')
        self._heatsink_temp = DecofReal(client, name + ':heatsink-temp')
        self._voltage_act = DecofReal(client, name + ':voltage-act')
        self._path = DecofString(client, name + ':path')

    @property
    def status(self) -> 'DecofInteger':
        return self._status

    @property
    def feedforward_master(self) -> 'MutableDecofInteger':
        return self._feedforward_master

    @property
    def feedforward_factor(self) -> 'MutableDecofReal':
        return self._feedforward_factor

    @property
    def external_input(self) -> 'ExtInput2':
        return self._external_input

    @property
    def voltage_min(self) -> 'MutableDecofReal':
        return self._voltage_min

    @property
    def status_txt(self) -> 'DecofString':
        return self._status_txt

    @property
    def feedforward_enabled(self) -> 'MutableDecofBoolean':
        return self._feedforward_enabled

    @property
    def voltage_set_dithering(self) -> 'MutableDecofBoolean':
        return self._voltage_set_dithering

    @property
    def voltage_max(self) -> 'MutableDecofReal':
        return self._voltage_max

    @property
    def enabled(self) -> 'MutableDecofBoolean':
        return self._enabled

    @property
    def voltage_set(self) -> 'MutableDecofReal':
        return self._voltage_set

    @property
    def output_filter(self) -> 'OutputFilter2':
        return self._output_filter

    @property
    def heatsink_temp(self) -> 'DecofReal':
        return self._heatsink_temp

    @property
    def voltage_act(self) -> 'DecofReal':
        return self._voltage_act

    @property
    def path(self) -> 'DecofString':
        return self._path


class Lock:
    def __init__(self, client: Client, name: str) -> None:
        self.__client = client
        self.__name = name
        self._pid_selection = MutableDecofInteger(client, name + ':pid-selection')
        self._pid1 = Pid(client, name + ':pid1')
        self._relock = AlRelock(client, name + ':relock')
        self._hold = MutableDecofBoolean(client, name + ':hold')
        self._lock_enabled = MutableDecofBoolean(client, name + ':lock-enabled')
        self._lockpoint = AlLockpoint(client, name + ':lockpoint')
        self._state_txt = DecofString(client, name + ':state-txt')
        self._candidate_filter = AlCandidateFilter(client, name + ':candidate-filter')
        self._reset = AlReset(client, name + ':reset')
        self._locking_delay = MutableDecofInteger(client, name + ':locking-delay')
        self._lock_without_lockpoint = MutableDecofBoolean(client, name + ':lock-without-lockpoint')
        self._candidates = DecofBinary(client, name + ':candidates')
        self._window = AlWindow(client, name + ':window')
        self._setpoint = MutableDecofReal(client, name + ':setpoint')
        self._state = DecofInteger(client, name + ':state')
        self._type_ = MutableDecofInteger(client, name + ':type')
        self._background_trace = DecofBinary(client, name + ':background-trace')
        self._lock_tracking = Coordinate(client, name + ':lock-tracking')
        self._lockin = Lockin(client, name + ':lockin')
        self._spectrum_input_channel = MutableDecofInteger(client, name + ':spectrum-input-channel')
        self._pid2 = Pid(client, name + ':pid2')

    @property
    def pid_selection(self) -> 'MutableDecofInteger':
        return self._pid_selection

    @property
    def pid1(self) -> 'Pid':
        return self._pid1

    @property
    def relock(self) -> 'AlRelock':
        return self._relock

    @property
    def hold(self) -> 'MutableDecofBoolean':
        return self._hold

    @property
    def lock_enabled(self) -> 'MutableDecofBoolean':
        return self._lock_enabled

    @property
    def lockpoint(self) -> 'AlLockpoint':
        return self._lockpoint

    @property
    def state_txt(self) -> 'DecofString':
        return self._state_txt

    @property
    def candidate_filter(self) -> 'AlCandidateFilter':
        return self._candidate_filter

    @property
    def reset(self) -> 'AlReset':
        return self._reset

    @property
    def locking_delay(self) -> 'MutableDecofInteger':
        return self._locking_delay

    @property
    def lock_without_lockpoint(self) -> 'MutableDecofBoolean':
        return self._lock_without_lockpoint

    @property
    def candidates(self) -> 'DecofBinary':
        return self._candidates

    @property
    def window(self) -> 'AlWindow':
        return self._window

    @property
    def setpoint(self) -> 'MutableDecofReal':
        return self._setpoint

    @property
    def state(self) -> 'DecofInteger':
        return self._state

    @property
    def type_(self) -> 'MutableDecofInteger':
        return self._type_

    @property
    def background_trace(self) -> 'DecofBinary':
        return self._background_trace

    @property
    def lock_tracking(self) -> 'Coordinate':
        return self._lock_tracking

    @property
    def lockin(self) -> 'Lockin':
        return self._lockin

    @property
    def spectrum_input_channel(self) -> 'MutableDecofInteger':
        return self._spectrum_input_channel

    @property
    def pid2(self) -> 'Pid':
        return self._pid2

    def open(self) -> None:
        self.__client.exec(self.__name + ':open', input_stream=None, output_type=None, return_type=None)

    def find_candidates(self) -> None:
        self.__client.exec(self.__name + ':find-candidates', input_stream=None, output_type=None, return_type=None)

    def show_candidates(self) -> Tuple[str, int]:
        return self.__client.exec(self.__name + ':show-candidates', input_stream=None, output_type=str, return_type=int)

    def select_lockpoint(self, x: float, y: float, type_: int) -> None:
        assert isinstance(x, float), "expected type 'float' for parameter 'x', got '{}'".format(type(x))
        assert isinstance(y, float), "expected type 'float' for parameter 'y', got '{}'".format(type(y))
        assert isinstance(type_, int), "expected type 'int' for parameter 'type_', got '{}'".format(type(type_))
        self.__client.exec(self.__name + ':select-lockpoint', x, y, type_, input_stream=None, output_type=None, return_type=None)

    def close(self) -> None:
        self.__client.exec(self.__name + ':close', input_stream=None, output_type=None, return_type=None)


class Pid:
    def __init__(self, client: Client, name: str) -> None:
        self.__client = client
        self.__name = name
        self._hold_output_on_unlock = MutableDecofBoolean(client, name + ':hold-output-on-unlock')
        self._gain = Gain(client, name + ':gain')
        self._output_channel = MutableDecofInteger(client, name + ':output-channel')
        self._hold = MutableDecofBoolean(client, name + ':hold')
        self._sign = MutableDecofBoolean(client, name + ':sign')
        self._hold_state = DecofBoolean(client, name + ':hold-state')
        self._outputlimit = Outputlimit(client, name + ':outputlimit')
        self._regulating_state = DecofBoolean(client, name + ':regulating-state')
        self._setpoint = MutableDecofReal(client, name + ':setpoint')
        self._lock_state = DecofBoolean(client, name + ':lock-state')
        self._slope = MutableDecofBoolean(client, name + ':slope')
        self._enabled = MutableDecofBoolean(client, name + ':enabled')
        self._input_channel = MutableDecofInteger(client, name + ':input-channel')

    @property
    def hold_output_on_unlock(self) -> 'MutableDecofBoolean':
        return self._hold_output_on_unlock

    @property
    def gain(self) -> 'Gain':
        return self._gain

    @property
    def output_channel(self) -> 'MutableDecofInteger':
        return self._output_channel

    @property
    def hold(self) -> 'MutableDecofBoolean':
        return self._hold

    @property
    def sign(self) -> 'MutableDecofBoolean':
        return self._sign

    @property
    def hold_state(self) -> 'DecofBoolean':
        return self._hold_state

    @property
    def outputlimit(self) -> 'Outputlimit':
        return self._outputlimit

    @property
    def regulating_state(self) -> 'DecofBoolean':
        return self._regulating_state

    @property
    def setpoint(self) -> 'MutableDecofReal':
        return self._setpoint

    @property
    def lock_state(self) -> 'DecofBoolean':
        return self._lock_state

    @property
    def slope(self) -> 'MutableDecofBoolean':
        return self._slope

    @property
    def enabled(self) -> 'MutableDecofBoolean':
        return self._enabled

    @property
    def input_channel(self) -> 'MutableDecofInteger':
        return self._input_channel


class Gain:
    def __init__(self, client: Client, name: str) -> None:
        self.__client = client
        self.__name = name
        self._all = MutableDecofReal(client, name + ':all')
        self._d = MutableDecofReal(client, name + ':d')
        self._i = MutableDecofReal(client, name + ':i')
        self._i_cutoff_enabled = MutableDecofBoolean(client, name + ':i-cutoff-enabled')
        self._p = MutableDecofReal(client, name + ':p')
        self._fc_ip = DecofReal(client, name + ':fc-ip')
        self._i_cutoff = MutableDecofReal(client, name + ':i-cutoff')
        self._fc_pd = DecofReal(client, name + ':fc-pd')

    @property
    def all(self) -> 'MutableDecofReal':
        return self._all

    @property
    def d(self) -> 'MutableDecofReal':
        return self._d

    @property
    def i(self) -> 'MutableDecofReal':
        return self._i

    @property
    def i_cutoff_enabled(self) -> 'MutableDecofBoolean':
        return self._i_cutoff_enabled

    @property
    def p(self) -> 'MutableDecofReal':
        return self._p

    @property
    def fc_ip(self) -> 'DecofReal':
        return self._fc_ip

    @property
    def i_cutoff(self) -> 'MutableDecofReal':
        return self._i_cutoff

    @property
    def fc_pd(self) -> 'DecofReal':
        return self._fc_pd


class Outputlimit:
    def __init__(self, client: Client, name: str) -> None:
        self.__client = client
        self.__name = name
        self._max = MutableDecofReal(client, name + ':max')
        self._enabled = MutableDecofBoolean(client, name + ':enabled')

    @property
    def max(self) -> 'MutableDecofReal':
        return self._max

    @property
    def enabled(self) -> 'MutableDecofBoolean':
        return self._enabled


class AlRelock:
    def __init__(self, client: Client, name: str) -> None:
        self.__client = client
        self.__name = name
        self._frequency = MutableDecofReal(client, name + ':frequency')
        self._output_channel = MutableDecofInteger(client, name + ':output-channel')
        self._enabled = MutableDecofBoolean(client, name + ':enabled')
        self._delay = MutableDecofReal(client, name + ':delay')
        self._amplitude = MutableDecofReal(client, name + ':amplitude')

    @property
    def frequency(self) -> 'MutableDecofReal':
        return self._frequency

    @property
    def output_channel(self) -> 'MutableDecofInteger':
        return self._output_channel

    @property
    def enabled(self) -> 'MutableDecofBoolean':
        return self._enabled

    @property
    def delay(self) -> 'MutableDecofReal':
        return self._delay

    @property
    def amplitude(self) -> 'MutableDecofReal':
        return self._amplitude


class AlLockpoint:
    def __init__(self, client: Client, name: str) -> None:
        self.__client = client
        self.__name = name
        self._type_ = DecofString(client, name + ':type')
        self._position = Coordinate(client, name + ':position')

    @property
    def type_(self) -> 'DecofString':
        return self._type_

    @property
    def position(self) -> 'Coordinate':
        return self._position


class Coordinate:
    def __init__(self, client: Client, name: str) -> None:
        self.__client = client
        self.__name = name

    def get(self) -> Tuple[float, float]:
        return self.__client.get(self.__name)

    def set(self, y: float, x: float) -> None:
        assert isinstance(y, float), "expected type 'float' for 'y', got '{}'".format(type(y))
        assert isinstance(x, float), "expected type 'float' for 'x', got '{}'".format(type(x))
        self.__client.set(self.__name, y, x)


class AlCandidateFilter:
    def __init__(self, client: Client, name: str) -> None:
        self.__client = client
        self.__name = name
        self._positive_edge = MutableDecofBoolean(client, name + ':positive-edge')
        self._edge_min_distance = MutableDecofInteger(client, name + ':edge-min-distance')
        self._top = MutableDecofBoolean(client, name + ':top')
        self._edge_level = MutableDecofReal(client, name + ':edge-level')
        self._bottom = MutableDecofBoolean(client, name + ':bottom')
        self._negative_edge = MutableDecofBoolean(client, name + ':negative-edge')
        self._peak_noise_tolerance = MutableDecofReal(client, name + ':peak-noise-tolerance')

    @property
    def positive_edge(self) -> 'MutableDecofBoolean':
        return self._positive_edge

    @property
    def edge_min_distance(self) -> 'MutableDecofInteger':
        return self._edge_min_distance

    @property
    def top(self) -> 'MutableDecofBoolean':
        return self._top

    @property
    def edge_level(self) -> 'MutableDecofReal':
        return self._edge_level

    @property
    def bottom(self) -> 'MutableDecofBoolean':
        return self._bottom

    @property
    def negative_edge(self) -> 'MutableDecofBoolean':
        return self._negative_edge

    @property
    def peak_noise_tolerance(self) -> 'MutableDecofReal':
        return self._peak_noise_tolerance


class AlReset:
    def __init__(self, client: Client, name: str) -> None:
        self.__client = client
        self.__name = name
        self._enabled = MutableDecofBoolean(client, name + ':enabled')

    @property
    def enabled(self) -> 'MutableDecofBoolean':
        return self._enabled


class AlWindow:
    def __init__(self, client: Client, name: str) -> None:
        self.__client = client
        self.__name = name
        self._level_high = MutableDecofReal(client, name + ':level-high')
        self._input_channel = MutableDecofInteger(client, name + ':input-channel')
        self._enabled = MutableDecofBoolean(client, name + ':enabled')
        self._level_hysteresis = MutableDecofReal(client, name + ':level-hysteresis')
        self._level_low = MutableDecofReal(client, name + ':level-low')

    @property
    def level_high(self) -> 'MutableDecofReal':
        return self._level_high

    @property
    def input_channel(self) -> 'MutableDecofInteger':
        return self._input_channel

    @property
    def enabled(self) -> 'MutableDecofBoolean':
        return self._enabled

    @property
    def level_hysteresis(self) -> 'MutableDecofReal':
        return self._level_hysteresis

    @property
    def level_low(self) -> 'MutableDecofReal':
        return self._level_low


class Lockin:
    def __init__(self, client: Client, name: str) -> None:
        self.__client = client
        self.__name = name
        self._lock_level = MutableDecofReal(client, name + ':lock-level')
        self._frequency = MutableDecofReal(client, name + ':frequency')
        self._amplitude = MutableDecofReal(client, name + ':amplitude')
        self._modulation_enabled = MutableDecofBoolean(client, name + ':modulation-enabled')
        self._modulation_output_channel = MutableDecofInteger(client, name + ':modulation-output-channel')
        self._auto_lir = AutoLir(client, name + ':auto-lir')
        self._input_channel = MutableDecofInteger(client, name + ':input-channel')
        self._phase_shift = MutableDecofReal(client, name + ':phase-shift')

    @property
    def lock_level(self) -> 'MutableDecofReal':
        return self._lock_level

    @property
    def frequency(self) -> 'MutableDecofReal':
        return self._frequency

    @property
    def amplitude(self) -> 'MutableDecofReal':
        return self._amplitude

    @property
    def modulation_enabled(self) -> 'MutableDecofBoolean':
        return self._modulation_enabled

    @property
    def modulation_output_channel(self) -> 'MutableDecofInteger':
        return self._modulation_output_channel

    @property
    def auto_lir(self) -> 'AutoLir':
        return self._auto_lir

    @property
    def input_channel(self) -> 'MutableDecofInteger':
        return self._input_channel

    @property
    def phase_shift(self) -> 'MutableDecofReal':
        return self._phase_shift


class AutoLir:
    def __init__(self, client: Client, name: str) -> None:
        self.__client = client
        self.__name = name
        self._progress = DecofInteger(client, name + ':progress')

    @property
    def progress(self) -> 'DecofInteger':
        return self._progress

    def auto_lir(self) -> None:
        self.__client.exec(self.__name + ':auto-lir', input_stream=None, output_type=None, return_type=None)


class PressureCompensation:
    def __init__(self, client: Client, name: str) -> None:
        self.__client = client
        self.__name = name
        self._air_pressure = DecofReal(client, name + ':air-pressure')
        self._compensation_voltage = DecofReal(client, name + ':compensation-voltage')
        self._enabled = MutableDecofBoolean(client, name + ':enabled')
        self._factor = MutableDecofReal(client, name + ':factor')
        self._offset = DecofReal(client, name + ':offset')

    @property
    def air_pressure(self) -> 'DecofReal':
        return self._air_pressure

    @property
    def compensation_voltage(self) -> 'DecofReal':
        return self._compensation_voltage

    @property
    def enabled(self) -> 'MutableDecofBoolean':
        return self._enabled

    @property
    def factor(self) -> 'MutableDecofReal':
        return self._factor

    @property
    def offset(self) -> 'DecofReal':
        return self._offset


class PdCal:
    def __init__(self, client: Client, name: str) -> None:
        self.__client = client
        self.__name = name
        self._photodiode = DecofReal(client, name + ':photodiode')
        self._power = DecofReal(client, name + ':power')
        self._cal_offset = MutableDecofReal(client, name + ':cal-offset')
        self._cal_factor = MutableDecofReal(client, name + ':cal-factor')

    @property
    def photodiode(self) -> 'DecofReal':
        return self._photodiode

    @property
    def power(self) -> 'DecofReal':
        return self._power

    @property
    def cal_offset(self) -> 'MutableDecofReal':
        return self._cal_offset

    @property
    def cal_factor(self) -> 'MutableDecofReal':
        return self._cal_factor


class TcChannel2:
    def __init__(self, client: Client, name: str) -> None:
        self.__client = client
        self.__name = name
        self._status = DecofInteger(client, name + ':status')
        self._ntc_series_resistance = DecofReal(client, name + ':ntc-series-resistance')
        self._resistance = DecofReal(client, name + ':resistance')
        self._temp_set_max = MutableDecofReal(client, name + ':temp-set-max')
        self._temp_set = MutableDecofReal(client, name + ':temp-set')
        self._current_act = DecofReal(client, name + ':current-act')
        self._external_input = ExtInput2(client, name + ':external-input')
        self._t_loop = TcChannelTLoop2(client, name + ':t-loop')
        self._ready = DecofBoolean(client, name + ':ready')
        self._drv_voltage = DecofReal(client, name + ':drv-voltage')
        self._c_loop = TcChannelCLoop2(client, name + ':c-loop')
        self._current_set = DecofReal(client, name + ':current-set')
        self._enabled = MutableDecofBoolean(client, name + ':enabled')
        self._status_txt = DecofString(client, name + ':status-txt')
        self._limits = TcChannelCheck2(client, name + ':limits')
        self._temp_roc_enabled = MutableDecofBoolean(client, name + ':temp-roc-enabled')
        self._temp_set_min = MutableDecofReal(client, name + ':temp-set-min')
        self._power_source = DecofInteger(client, name + ':power-source')
        self._ntc_parallel_resistance = DecofReal(client, name + ':ntc-parallel-resistance')
        self._temp_act = DecofReal(client, name + ':temp-act')
        self._temp_reset = MutableDecofBoolean(client, name + ':temp-reset')
        self._fault = DecofBoolean(client, name + ':fault')
        self._voltage_act = DecofReal(client, name + ':voltage-act')
        self._current_set_min = MutableDecofReal(client, name + ':current-set-min')
        self._temp_roc_limit = MutableDecofReal(client, name + ':temp-roc-limit')
        self._current_set_max = MutableDecofReal(client, name + ':current-set-max')
        self._path = DecofString(client, name + ':path')

    @property
    def status(self) -> 'DecofInteger':
        return self._status

    @property
    def ntc_series_resistance(self) -> 'DecofReal':
        return self._ntc_series_resistance

    @property
    def resistance(self) -> 'DecofReal':
        return self._resistance

    @property
    def temp_set_max(self) -> 'MutableDecofReal':
        return self._temp_set_max

    @property
    def temp_set(self) -> 'MutableDecofReal':
        return self._temp_set

    @property
    def current_act(self) -> 'DecofReal':
        return self._current_act

    @property
    def external_input(self) -> 'ExtInput2':
        return self._external_input

    @property
    def t_loop(self) -> 'TcChannelTLoop2':
        return self._t_loop

    @property
    def ready(self) -> 'DecofBoolean':
        return self._ready

    @property
    def drv_voltage(self) -> 'DecofReal':
        return self._drv_voltage

    @property
    def c_loop(self) -> 'TcChannelCLoop2':
        return self._c_loop

    @property
    def current_set(self) -> 'DecofReal':
        return self._current_set

    @property
    def enabled(self) -> 'MutableDecofBoolean':
        return self._enabled

    @property
    def status_txt(self) -> 'DecofString':
        return self._status_txt

    @property
    def limits(self) -> 'TcChannelCheck2':
        return self._limits

    @property
    def temp_roc_enabled(self) -> 'MutableDecofBoolean':
        return self._temp_roc_enabled

    @property
    def temp_set_min(self) -> 'MutableDecofReal':
        return self._temp_set_min

    @property
    def power_source(self) -> 'DecofInteger':
        return self._power_source

    @property
    def ntc_parallel_resistance(self) -> 'DecofReal':
        return self._ntc_parallel_resistance

    @property
    def temp_act(self) -> 'DecofReal':
        return self._temp_act

    @property
    def temp_reset(self) -> 'MutableDecofBoolean':
        return self._temp_reset

    @property
    def fault(self) -> 'DecofBoolean':
        return self._fault

    @property
    def voltage_act(self) -> 'DecofReal':
        return self._voltage_act

    @property
    def current_set_min(self) -> 'MutableDecofReal':
        return self._current_set_min

    @property
    def temp_roc_limit(self) -> 'MutableDecofReal':
        return self._temp_roc_limit

    @property
    def current_set_max(self) -> 'MutableDecofReal':
        return self._current_set_max

    @property
    def path(self) -> 'DecofString':
        return self._path

    def check_peltier(self) -> float:
        return self.__client.exec(self.__name + ':check-peltier', input_stream=None, output_type=None, return_type=float)


class TcChannelTLoop2:
    def __init__(self, client: Client, name: str) -> None:
        self.__client = client
        self.__name = name
        self._on = MutableDecofBoolean(client, name + ':on')
        self._ok_time = MutableDecofReal(client, name + ':ok-time')
        self._i_gain = MutableDecofReal(client, name + ':i-gain')
        self._ok_tolerance = MutableDecofReal(client, name + ':ok-tolerance')
        self._p_gain = MutableDecofReal(client, name + ':p-gain')
        self._d_gain = MutableDecofReal(client, name + ':d-gain')

    @property
    def on(self) -> 'MutableDecofBoolean':
        return self._on

    @property
    def ok_time(self) -> 'MutableDecofReal':
        return self._ok_time

    @property
    def i_gain(self) -> 'MutableDecofReal':
        return self._i_gain

    @property
    def ok_tolerance(self) -> 'MutableDecofReal':
        return self._ok_tolerance

    @property
    def p_gain(self) -> 'MutableDecofReal':
        return self._p_gain

    @property
    def d_gain(self) -> 'MutableDecofReal':
        return self._d_gain


class TcChannelCLoop2:
    def __init__(self, client: Client, name: str) -> None:
        self.__client = client
        self.__name = name
        self._on = MutableDecofBoolean(client, name + ':on')
        self._i_gain = MutableDecofReal(client, name + ':i-gain')

    @property
    def on(self) -> 'MutableDecofBoolean':
        return self._on

    @property
    def i_gain(self) -> 'MutableDecofReal':
        return self._i_gain


class TcChannelCheck2:
    def __init__(self, client: Client, name: str) -> None:
        self.__client = client
        self.__name = name
        self._timed_out = DecofBoolean(client, name + ':timed-out')
        self._temp_min = MutableDecofReal(client, name + ':temp-min')
        self._temp_max = MutableDecofReal(client, name + ':temp-max')
        self._timeout = MutableDecofInteger(client, name + ':timeout')
        self._out_of_range = DecofBoolean(client, name + ':out-of-range')

    @property
    def timed_out(self) -> 'DecofBoolean':
        return self._timed_out

    @property
    def temp_min(self) -> 'MutableDecofReal':
        return self._temp_min

    @property
    def temp_max(self) -> 'MutableDecofReal':
        return self._temp_max

    @property
    def timeout(self) -> 'MutableDecofInteger':
        return self._timeout

    @property
    def out_of_range(self) -> 'DecofBoolean':
        return self._out_of_range


class Nlo:
    def __init__(self, client: Client, name: str) -> None:
        self.__client = client
        self.__name = name
        self._fhg = Fhg(client, name + ':fhg')
        self._shg = Shg(client, name + ':shg')
        self._pd = NloPhotoDiodes(client, name + ':pd')
        self._servo = NloLaserHeadServos(client, name + ':servo')
        self._power_optimization = NloLaserHeadPowerOptimization(client, name + ':power-optimization')
        self._ssw_ver = DecofString(client, name + ':ssw-ver')

    @property
    def fhg(self) -> 'Fhg':
        return self._fhg

    @property
    def shg(self) -> 'Shg':
        return self._shg

    @property
    def pd(self) -> 'NloPhotoDiodes':
        return self._pd

    @property
    def servo(self) -> 'NloLaserHeadServos':
        return self._servo

    @property
    def power_optimization(self) -> 'NloLaserHeadPowerOptimization':
        return self._power_optimization

    @property
    def ssw_ver(self) -> 'DecofString':
        return self._ssw_ver


class Fhg:
    def __init__(self, client: Client, name: str) -> None:
        self.__client = client
        self.__name = name
        self._scan = NloLaserHeadSiggen2(client, name + ':scan')
        self._factory_settings = FhgFactorySettings(client, name + ':factory-settings')
        self._pc = PiezoDrv2(client, name + ':pc')
        self._lock = NloLaserHeadLockFhg(client, name + ':lock')
        self._scope = NloLaserHeadScopeT2(client, name + ':scope')
        self._tc = TcChannel2(client, name + ':tc')

    @property
    def scan(self) -> 'NloLaserHeadSiggen2':
        return self._scan

    @property
    def factory_settings(self) -> 'FhgFactorySettings':
        return self._factory_settings

    @property
    def pc(self) -> 'PiezoDrv2':
        return self._pc

    @property
    def lock(self) -> 'NloLaserHeadLockFhg':
        return self._lock

    @property
    def scope(self) -> 'NloLaserHeadScopeT2':
        return self._scope

    @property
    def tc(self) -> 'TcChannel2':
        return self._tc

    def restore(self) -> None:
        self.__client.exec(self.__name + ':restore', input_stream=None, output_type=None, return_type=None)

    def store(self) -> None:
        self.__client.exec(self.__name + ':store', input_stream=None, output_type=None, return_type=None)


class NloLaserHeadSiggen2:
    def __init__(self, client: Client, name: str) -> None:
        self.__client = client
        self.__name = name
        self._frequency = MutableDecofReal(client, name + ':frequency')
        self._offset = MutableDecofReal(client, name + ':offset')
        self._amplitude = MutableDecofReal(client, name + ':amplitude')
        self._enabled = MutableDecofBoolean(client, name + ':enabled')

    @property
    def frequency(self) -> 'MutableDecofReal':
        return self._frequency

    @property
    def offset(self) -> 'MutableDecofReal':
        return self._offset

    @property
    def amplitude(self) -> 'MutableDecofReal':
        return self._amplitude

    @property
    def enabled(self) -> 'MutableDecofBoolean':
        return self._enabled


class FhgFactorySettings:
    def __init__(self, client: Client, name: str) -> None:
        self.__client = client
        self.__name = name
        self._pd = NloLaserHeadFhgPhotodiodesFactorySettings(client, name + ':pd')
        self._pc = NloLaserHeadPcFactorySettings(client, name + ':pc')
        self._modified = DecofBoolean(client, name + ':modified')
        self._lock = NloLaserHeadLockFactorySettings(client, name + ':lock')
        self._tc = NloLaserHeadTcFactorySettings(client, name + ':tc')

    @property
    def pd(self) -> 'NloLaserHeadFhgPhotodiodesFactorySettings':
        return self._pd

    @property
    def pc(self) -> 'NloLaserHeadPcFactorySettings':
        return self._pc

    @property
    def modified(self) -> 'DecofBoolean':
        return self._modified

    @property
    def lock(self) -> 'NloLaserHeadLockFactorySettings':
        return self._lock

    @property
    def tc(self) -> 'NloLaserHeadTcFactorySettings':
        return self._tc

    def apply(self) -> None:
        self.__client.exec(self.__name + ':apply', input_stream=None, output_type=None, return_type=None)

    def retrieve_now(self) -> None:
        self.__client.exec(self.__name + ':retrieve-now', input_stream=None, output_type=None, return_type=None)


class NloLaserHeadFhgPhotodiodesFactorySettings:
    def __init__(self, client: Client, name: str) -> None:
        self.__client = client
        self.__name = name
        self._fhg = NloLaserHeadPdFactorySettings1(client, name + ':fhg')
        self._pdh_rf = NloLaserHeadPdPdhFactorySettings(client, name + ':pdh-rf')
        self._pdh_dc = NloLaserHeadPdDigilockFactorySettings(client, name + ':pdh-dc')
        self._int = NloLaserHeadPdDigilockFactorySettings(client, name + ':int')

    @property
    def fhg(self) -> 'NloLaserHeadPdFactorySettings1':
        return self._fhg

    @property
    def pdh_rf(self) -> 'NloLaserHeadPdPdhFactorySettings':
        return self._pdh_rf

    @property
    def pdh_dc(self) -> 'NloLaserHeadPdDigilockFactorySettings':
        return self._pdh_dc

    @property
    def int(self) -> 'NloLaserHeadPdDigilockFactorySettings':
        return self._int


class NloLaserHeadPdFactorySettings1:
    def __init__(self, client: Client, name: str) -> None:
        self.__client = client
        self.__name = name
        self._cal_offset = MutableDecofReal(client, name + ':cal-offset')
        self._cal_factor = MutableDecofReal(client, name + ':cal-factor')

    @property
    def cal_offset(self) -> 'MutableDecofReal':
        return self._cal_offset

    @property
    def cal_factor(self) -> 'MutableDecofReal':
        return self._cal_factor


class NloLaserHeadPdPdhFactorySettings:
    def __init__(self, client: Client, name: str) -> None:
        self.__client = client
        self.__name = name
        self._gain = MutableDecofReal(client, name + ':gain')

    @property
    def gain(self) -> 'MutableDecofReal':
        return self._gain


class NloLaserHeadPdDigilockFactorySettings:
    def __init__(self, client: Client, name: str) -> None:
        self.__client = client
        self.__name = name
        self._cal_offset = MutableDecofReal(client, name + ':cal-offset')

    @property
    def cal_offset(self) -> 'MutableDecofReal':
        return self._cal_offset


class NloLaserHeadPcFactorySettings:
    def __init__(self, client: Client, name: str) -> None:
        self.__client = client
        self.__name = name
        self._scan_offset = MutableDecofReal(client, name + ':scan-offset')
        self._feedforward_enabled = MutableDecofBoolean(client, name + ':feedforward-enabled')
        self._scan_amplitude = MutableDecofReal(client, name + ':scan-amplitude')
        self._capacitance = MutableDecofReal(client, name + ':capacitance')
        self._voltage_max = MutableDecofReal(client, name + ':voltage-max')
        self._scan_frequency = MutableDecofReal(client, name + ':scan-frequency')
        self._voltage_min = MutableDecofReal(client, name + ':voltage-min')
        self._feedforward_factor = MutableDecofReal(client, name + ':feedforward-factor')

    @property
    def scan_offset(self) -> 'MutableDecofReal':
        return self._scan_offset

    @property
    def feedforward_enabled(self) -> 'MutableDecofBoolean':
        return self._feedforward_enabled

    @property
    def scan_amplitude(self) -> 'MutableDecofReal':
        return self._scan_amplitude

    @property
    def capacitance(self) -> 'MutableDecofReal':
        return self._capacitance

    @property
    def voltage_max(self) -> 'MutableDecofReal':
        return self._voltage_max

    @property
    def scan_frequency(self) -> 'MutableDecofReal':
        return self._scan_frequency

    @property
    def voltage_min(self) -> 'MutableDecofReal':
        return self._voltage_min

    @property
    def feedforward_factor(self) -> 'MutableDecofReal':
        return self._feedforward_factor


class NloLaserHeadLockFactorySettings:
    def __init__(self, client: Client, name: str) -> None:
        self.__client = client
        self.__name = name
        self._pid_selection = MutableDecofInteger(client, name + ':pid-selection')
        self._analog_p_gain = MutableDecofReal(client, name + ':analog-p-gain')
        self._pid1_gain = NloLaserHeadPidGainFactorySettings(client, name + ':pid1-gain')
        self._relock = NloLaserHeadRelockFactorySettings(client, name + ':relock')
        self._local_oscillator = NloLaserHeadLocalOscillatorFactorySettings(client, name + ':local-oscillator')
        self._pid2_gain = NloLaserHeadPidGainFactorySettings(client, name + ':pid2-gain')
        self._setpoint = MutableDecofReal(client, name + ':setpoint')
        self._window = NloLaserHeadLockWindowFactorySettings(client, name + ':window')

    @property
    def pid_selection(self) -> 'MutableDecofInteger':
        return self._pid_selection

    @property
    def analog_p_gain(self) -> 'MutableDecofReal':
        return self._analog_p_gain

    @property
    def pid1_gain(self) -> 'NloLaserHeadPidGainFactorySettings':
        return self._pid1_gain

    @property
    def relock(self) -> 'NloLaserHeadRelockFactorySettings':
        return self._relock

    @property
    def local_oscillator(self) -> 'NloLaserHeadLocalOscillatorFactorySettings':
        return self._local_oscillator

    @property
    def pid2_gain(self) -> 'NloLaserHeadPidGainFactorySettings':
        return self._pid2_gain

    @property
    def setpoint(self) -> 'MutableDecofReal':
        return self._setpoint

    @property
    def window(self) -> 'NloLaserHeadLockWindowFactorySettings':
        return self._window


class NloLaserHeadPidGainFactorySettings:
    def __init__(self, client: Client, name: str) -> None:
        self.__client = client
        self.__name = name
        self._all = MutableDecofReal(client, name + ':all')
        self._d = MutableDecofReal(client, name + ':d')
        self._i = MutableDecofReal(client, name + ':i')
        self._i_cutoff_enabled = MutableDecofBoolean(client, name + ':i-cutoff-enabled')
        self._p = MutableDecofReal(client, name + ':p')
        self._i_cutoff = MutableDecofReal(client, name + ':i-cutoff')

    @property
    def all(self) -> 'MutableDecofReal':
        return self._all

    @property
    def d(self) -> 'MutableDecofReal':
        return self._d

    @property
    def i(self) -> 'MutableDecofReal':
        return self._i

    @property
    def i_cutoff_enabled(self) -> 'MutableDecofBoolean':
        return self._i_cutoff_enabled

    @property
    def p(self) -> 'MutableDecofReal':
        return self._p

    @property
    def i_cutoff(self) -> 'MutableDecofReal':
        return self._i_cutoff


class NloLaserHeadRelockFactorySettings:
    def __init__(self, client: Client, name: str) -> None:
        self.__client = client
        self.__name = name
        self._frequency = MutableDecofReal(client, name + ':frequency')
        self._enabled = MutableDecofBoolean(client, name + ':enabled')
        self._delay = MutableDecofReal(client, name + ':delay')
        self._amplitude = MutableDecofReal(client, name + ':amplitude')

    @property
    def frequency(self) -> 'MutableDecofReal':
        return self._frequency

    @property
    def enabled(self) -> 'MutableDecofBoolean':
        return self._enabled

    @property
    def delay(self) -> 'MutableDecofReal':
        return self._delay

    @property
    def amplitude(self) -> 'MutableDecofReal':
        return self._amplitude


class NloLaserHeadLocalOscillatorFactorySettings:
    def __init__(self, client: Client, name: str) -> None:
        self.__client = client
        self.__name = name
        self._coupled_modulation = MutableDecofBoolean(client, name + ':coupled-modulation')
        self._phase_shift_shg = MutableDecofReal(client, name + ':phase-shift-shg')
        self._attenuation_fhg_raw = MutableDecofInteger(client, name + ':attenuation-fhg-raw')
        self._enabled = MutableDecofBoolean(client, name + ':enabled')
        self._phase_shift_fhg = MutableDecofReal(client, name + ':phase-shift-fhg')
        self._use_fast_oscillator = MutableDecofBoolean(client, name + ':use-fast-oscillator')
        self._attenuation_shg_raw = MutableDecofInteger(client, name + ':attenuation-shg-raw')

    @property
    def coupled_modulation(self) -> 'MutableDecofBoolean':
        return self._coupled_modulation

    @property
    def phase_shift_shg(self) -> 'MutableDecofReal':
        return self._phase_shift_shg

    @property
    def attenuation_fhg_raw(self) -> 'MutableDecofInteger':
        return self._attenuation_fhg_raw

    @property
    def enabled(self) -> 'MutableDecofBoolean':
        return self._enabled

    @property
    def phase_shift_fhg(self) -> 'MutableDecofReal':
        return self._phase_shift_fhg

    @property
    def use_fast_oscillator(self) -> 'MutableDecofBoolean':
        return self._use_fast_oscillator

    @property
    def attenuation_shg_raw(self) -> 'MutableDecofInteger':
        return self._attenuation_shg_raw


class NloLaserHeadLockWindowFactorySettings:
    def __init__(self, client: Client, name: str) -> None:
        self.__client = client
        self.__name = name
        self._threshold = MutableDecofReal(client, name + ':threshold')
        self._input_channel = MutableDecofInteger(client, name + ':input-channel')
        self._level_hysteresis = MutableDecofReal(client, name + ':level-hysteresis')

    @property
    def threshold(self) -> 'MutableDecofReal':
        return self._threshold

    @property
    def input_channel(self) -> 'MutableDecofInteger':
        return self._input_channel

    @property
    def level_hysteresis(self) -> 'MutableDecofReal':
        return self._level_hysteresis


class NloLaserHeadTcFactorySettings:
    def __init__(self, client: Client, name: str) -> None:
        self.__client = client
        self.__name = name
        self._ok_tolerance = MutableDecofReal(client, name + ':ok-tolerance')
        self._temp_min = MutableDecofReal(client, name + ':temp-min')
        self._temp_roc_enabled = MutableDecofBoolean(client, name + ':temp-roc-enabled')
        self._i_gain = MutableDecofReal(client, name + ':i-gain')
        self._temp_roc_limit = MutableDecofReal(client, name + ':temp-roc-limit')
        self._p_gain = MutableDecofReal(client, name + ':p-gain')
        self._ntc_series_resistance = MutableDecofReal(client, name + ':ntc-series-resistance')
        self._d_gain = MutableDecofReal(client, name + ':d-gain')
        self._temp_set = MutableDecofReal(client, name + ':temp-set')
        self._current_min = MutableDecofReal(client, name + ':current-min')
        self._ok_time = MutableDecofReal(client, name + ':ok-time')
        self._temp_max = MutableDecofReal(client, name + ':temp-max')
        self._power_source = MutableDecofInteger(client, name + ':power-source')
        self._current_max = MutableDecofReal(client, name + ':current-max')
        self._c_gain = MutableDecofReal(client, name + ':c-gain')
        self._timeout = MutableDecofInteger(client, name + ':timeout')

    @property
    def ok_tolerance(self) -> 'MutableDecofReal':
        return self._ok_tolerance

    @property
    def temp_min(self) -> 'MutableDecofReal':
        return self._temp_min

    @property
    def temp_roc_enabled(self) -> 'MutableDecofBoolean':
        return self._temp_roc_enabled

    @property
    def i_gain(self) -> 'MutableDecofReal':
        return self._i_gain

    @property
    def temp_roc_limit(self) -> 'MutableDecofReal':
        return self._temp_roc_limit

    @property
    def p_gain(self) -> 'MutableDecofReal':
        return self._p_gain

    @property
    def ntc_series_resistance(self) -> 'MutableDecofReal':
        return self._ntc_series_resistance

    @property
    def d_gain(self) -> 'MutableDecofReal':
        return self._d_gain

    @property
    def temp_set(self) -> 'MutableDecofReal':
        return self._temp_set

    @property
    def current_min(self) -> 'MutableDecofReal':
        return self._current_min

    @property
    def ok_time(self) -> 'MutableDecofReal':
        return self._ok_time

    @property
    def temp_max(self) -> 'MutableDecofReal':
        return self._temp_max

    @property
    def power_source(self) -> 'MutableDecofInteger':
        return self._power_source

    @property
    def current_max(self) -> 'MutableDecofReal':
        return self._current_max

    @property
    def c_gain(self) -> 'MutableDecofReal':
        return self._c_gain

    @property
    def timeout(self) -> 'MutableDecofInteger':
        return self._timeout


class NloLaserHeadLockFhg:
    def __init__(self, client: Client, name: str) -> None:
        self.__client = client
        self.__name = name
        self._pid_selection = MutableDecofInteger(client, name + ':pid-selection')
        self._pid1 = NloLaserHeadPid2(client, name + ':pid1')
        self._relock = NloLaserHeadRelock2(client, name + ':relock')
        self._state_txt = DecofString(client, name + ':state-txt')
        self._cavity_fast_pzt_voltage = MutableDecofReal(client, name + ':cavity-fast-pzt-voltage')
        self._state = DecofInteger(client, name + ':state')
        self._window = NloLaserHeadWindow2(client, name + ':window')
        self._setpoint = MutableDecofReal(client, name + ':setpoint')
        self._local_oscillator = NloLaserHeadLocalOscillatorFhg(client, name + ':local-oscillator')
        self._background_trace = DecofBinary(client, name + ':background-trace')
        self._cavity_slow_pzt_voltage = MutableDecofReal(client, name + ':cavity-slow-pzt-voltage')
        self._lock_enabled = MutableDecofBoolean(client, name + ':lock-enabled')
        self._pid2 = NloLaserHeadPid2(client, name + ':pid2')

    @property
    def pid_selection(self) -> 'MutableDecofInteger':
        return self._pid_selection

    @property
    def pid1(self) -> 'NloLaserHeadPid2':
        return self._pid1

    @property
    def relock(self) -> 'NloLaserHeadRelock2':
        return self._relock

    @property
    def state_txt(self) -> 'DecofString':
        return self._state_txt

    @property
    def cavity_fast_pzt_voltage(self) -> 'MutableDecofReal':
        return self._cavity_fast_pzt_voltage

    @property
    def state(self) -> 'DecofInteger':
        return self._state

    @property
    def window(self) -> 'NloLaserHeadWindow2':
        return self._window

    @property
    def setpoint(self) -> 'MutableDecofReal':
        return self._setpoint

    @property
    def local_oscillator(self) -> 'NloLaserHeadLocalOscillatorFhg':
        return self._local_oscillator

    @property
    def background_trace(self) -> 'DecofBinary':
        return self._background_trace

    @property
    def cavity_slow_pzt_voltage(self) -> 'MutableDecofReal':
        return self._cavity_slow_pzt_voltage

    @property
    def lock_enabled(self) -> 'MutableDecofBoolean':
        return self._lock_enabled

    @property
    def pid2(self) -> 'NloLaserHeadPid2':
        return self._pid2


class NloLaserHeadPid2:
    def __init__(self, client: Client, name: str) -> None:
        self.__client = client
        self.__name = name
        self._gain = NloLaserHeadGain2(client, name + ':gain')

    @property
    def gain(self) -> 'NloLaserHeadGain2':
        return self._gain


class NloLaserHeadGain2:
    def __init__(self, client: Client, name: str) -> None:
        self.__client = client
        self.__name = name
        self._all = MutableDecofReal(client, name + ':all')
        self._d = MutableDecofReal(client, name + ':d')
        self._i_cutoff_enabled = MutableDecofBoolean(client, name + ':i-cutoff-enabled')
        self._p = MutableDecofReal(client, name + ':p')
        self._i_cutoff = MutableDecofReal(client, name + ':i-cutoff')
        self._i = MutableDecofReal(client, name + ':i')

    @property
    def all(self) -> 'MutableDecofReal':
        return self._all

    @property
    def d(self) -> 'MutableDecofReal':
        return self._d

    @property
    def i_cutoff_enabled(self) -> 'MutableDecofBoolean':
        return self._i_cutoff_enabled

    @property
    def p(self) -> 'MutableDecofReal':
        return self._p

    @property
    def i_cutoff(self) -> 'MutableDecofReal':
        return self._i_cutoff

    @property
    def i(self) -> 'MutableDecofReal':
        return self._i


class NloLaserHeadRelock2:
    def __init__(self, client: Client, name: str) -> None:
        self.__client = client
        self.__name = name
        self._frequency = MutableDecofReal(client, name + ':frequency')
        self._delay = MutableDecofReal(client, name + ':delay')
        self._amplitude = MutableDecofReal(client, name + ':amplitude')
        self._enabled = MutableDecofBoolean(client, name + ':enabled')

    @property
    def frequency(self) -> 'MutableDecofReal':
        return self._frequency

    @property
    def delay(self) -> 'MutableDecofReal':
        return self._delay

    @property
    def amplitude(self) -> 'MutableDecofReal':
        return self._amplitude

    @property
    def enabled(self) -> 'MutableDecofBoolean':
        return self._enabled


class NloLaserHeadWindow2:
    def __init__(self, client: Client, name: str) -> None:
        self.__client = client
        self.__name = name
        self._input_channel = MutableDecofInteger(client, name + ':input-channel')
        self._calibration = NloLaserHeadWindowCalibration2(client, name + ':calibration')
        self._threshold = MutableDecofReal(client, name + ':threshold')
        self._level_hysteresis = MutableDecofReal(client, name + ':level-hysteresis')

    @property
    def input_channel(self) -> 'MutableDecofInteger':
        return self._input_channel

    @property
    def calibration(self) -> 'NloLaserHeadWindowCalibration2':
        return self._calibration

    @property
    def threshold(self) -> 'MutableDecofReal':
        return self._threshold

    @property
    def level_hysteresis(self) -> 'MutableDecofReal':
        return self._level_hysteresis


class NloLaserHeadWindowCalibration2:
    def __init__(self, client: Client, name: str) -> None:
        self.__client = client
        self.__name = name


class NloLaserHeadLocalOscillatorFhg:
    def __init__(self, client: Client, name: str) -> None:
        self.__client = client
        self.__name = name
        self._coupled_modulation = MutableDecofBoolean(client, name + ':coupled-modulation')
        self._amplitude = MutableDecofReal(client, name + ':amplitude')
        self._enabled = MutableDecofBoolean(client, name + ':enabled')
        self._use_fast_oscillator = MutableDecofBoolean(client, name + ':use-fast-oscillator')
        self._phase_shift = MutableDecofReal(client, name + ':phase-shift')
        self._attenuation_raw = MutableDecofInteger(client, name + ':attenuation-raw')

    @property
    def coupled_modulation(self) -> 'MutableDecofBoolean':
        return self._coupled_modulation

    @property
    def amplitude(self) -> 'MutableDecofReal':
        return self._amplitude

    @property
    def enabled(self) -> 'MutableDecofBoolean':
        return self._enabled

    @property
    def use_fast_oscillator(self) -> 'MutableDecofBoolean':
        return self._use_fast_oscillator

    @property
    def phase_shift(self) -> 'MutableDecofReal':
        return self._phase_shift

    @property
    def attenuation_raw(self) -> 'MutableDecofInteger':
        return self._attenuation_raw

    def auto_pdh(self) -> None:
        self.__client.exec(self.__name + ':auto-pdh', input_stream=None, output_type=None, return_type=None)


class NloLaserHeadScopeT2:
    def __init__(self, client: Client, name: str) -> None:
        self.__client = client
        self.__name = name
        self._timescale = MutableDecofReal(client, name + ':timescale')
        self._data = DecofBinary(client, name + ':data')
        self._channel2 = NloLaserHeadScopeChannelT2(client, name + ':channel2')
        self._channel1 = NloLaserHeadScopeChannelT2(client, name + ':channel1')
        self._channelx = NloLaserHeadScopeXAxisT2(client, name + ':channelx')
        self._update_rate = MutableDecofInteger(client, name + ':update-rate')
        self._variant = MutableDecofInteger(client, name + ':variant')

    @property
    def timescale(self) -> 'MutableDecofReal':
        return self._timescale

    @property
    def data(self) -> 'DecofBinary':
        return self._data

    @property
    def channel2(self) -> 'NloLaserHeadScopeChannelT2':
        return self._channel2

    @property
    def channel1(self) -> 'NloLaserHeadScopeChannelT2':
        return self._channel1

    @property
    def channelx(self) -> 'NloLaserHeadScopeXAxisT2':
        return self._channelx

    @property
    def update_rate(self) -> 'MutableDecofInteger':
        return self._update_rate

    @property
    def variant(self) -> 'MutableDecofInteger':
        return self._variant


class NloLaserHeadScopeChannelT2:
    def __init__(self, client: Client, name: str) -> None:
        self.__client = client
        self.__name = name
        self._unit = DecofString(client, name + ':unit')
        self._signal = MutableDecofInteger(client, name + ':signal')
        self._name = DecofString(client, name + ':name')
        self._enabled = MutableDecofBoolean(client, name + ':enabled')

    @property
    def unit(self) -> 'DecofString':
        return self._unit

    @property
    def signal(self) -> 'MutableDecofInteger':
        return self._signal

    @property
    def name(self) -> 'DecofString':
        return self._name

    @property
    def enabled(self) -> 'MutableDecofBoolean':
        return self._enabled


class NloLaserHeadScopeXAxisT2:
    def __init__(self, client: Client, name: str) -> None:
        self.__client = client
        self.__name = name
        self._unit = DecofString(client, name + ':unit')
        self._name = DecofString(client, name + ':name')
        self._spectrum_range = MutableDecofReal(client, name + ':spectrum-range')
        self._spectrum_omit_dc = MutableDecofBoolean(client, name + ':spectrum-omit-dc')
        self._scope_timescale = MutableDecofReal(client, name + ':scope-timescale')
        self._xy_signal = MutableDecofInteger(client, name + ':xy-signal')

    @property
    def unit(self) -> 'DecofString':
        return self._unit

    @property
    def name(self) -> 'DecofString':
        return self._name

    @property
    def spectrum_range(self) -> 'MutableDecofReal':
        return self._spectrum_range

    @property
    def spectrum_omit_dc(self) -> 'MutableDecofBoolean':
        return self._spectrum_omit_dc

    @property
    def scope_timescale(self) -> 'MutableDecofReal':
        return self._scope_timescale

    @property
    def xy_signal(self) -> 'MutableDecofInteger':
        return self._xy_signal


class Shg:
    def __init__(self, client: Client, name: str) -> None:
        self.__client = client
        self.__name = name
        self._scan = NloLaserHeadSiggen2(client, name + ':scan')
        self._factory_settings = ShgFactorySettings(client, name + ':factory-settings')
        self._pc = PiezoDrv2(client, name + ':pc')
        self._lock = NloLaserHeadLockShg2(client, name + ':lock')
        self._scope = NloLaserHeadScopeT2(client, name + ':scope')
        self._tc = TcChannel2(client, name + ':tc')

    @property
    def scan(self) -> 'NloLaserHeadSiggen2':
        return self._scan

    @property
    def factory_settings(self) -> 'ShgFactorySettings':
        return self._factory_settings

    @property
    def pc(self) -> 'PiezoDrv2':
        return self._pc

    @property
    def lock(self) -> 'NloLaserHeadLockShg2':
        return self._lock

    @property
    def scope(self) -> 'NloLaserHeadScopeT2':
        return self._scope

    @property
    def tc(self) -> 'TcChannel2':
        return self._tc

    def restore(self) -> None:
        self.__client.exec(self.__name + ':restore', input_stream=None, output_type=None, return_type=None)

    def store(self) -> None:
        self.__client.exec(self.__name + ':store', input_stream=None, output_type=None, return_type=None)


class ShgFactorySettings:
    def __init__(self, client: Client, name: str) -> None:
        self.__client = client
        self.__name = name
        self._pd = NloLaserHeadShgPhotodiodesFactorySettings(client, name + ':pd')
        self._pc = NloLaserHeadPcFactorySettings(client, name + ':pc')
        self._modified = DecofBoolean(client, name + ':modified')
        self._lock = NloLaserHeadLockFactorySettings(client, name + ':lock')
        self._tc = NloLaserHeadTcFactorySettings(client, name + ':tc')

    @property
    def pd(self) -> 'NloLaserHeadShgPhotodiodesFactorySettings':
        return self._pd

    @property
    def pc(self) -> 'NloLaserHeadPcFactorySettings':
        return self._pc

    @property
    def modified(self) -> 'DecofBoolean':
        return self._modified

    @property
    def lock(self) -> 'NloLaserHeadLockFactorySettings':
        return self._lock

    @property
    def tc(self) -> 'NloLaserHeadTcFactorySettings':
        return self._tc

    def apply(self) -> None:
        self.__client.exec(self.__name + ':apply', input_stream=None, output_type=None, return_type=None)

    def retrieve_now(self) -> None:
        self.__client.exec(self.__name + ':retrieve-now', input_stream=None, output_type=None, return_type=None)


class NloLaserHeadShgPhotodiodesFactorySettings:
    def __init__(self, client: Client, name: str) -> None:
        self.__client = client
        self.__name = name
        self._shg_input = NloLaserHeadPdFactorySettings2(client, name + ':shg-input')
        self._fiber = NloLaserHeadPdFactorySettings1(client, name + ':fiber')
        self._shg = NloLaserHeadPdFactorySettings1(client, name + ':shg')
        self._pdh_dc = NloLaserHeadPdDigilockFactorySettings(client, name + ':pdh-dc')
        self._pdh_rf = NloLaserHeadPdPdhFactorySettings(client, name + ':pdh-rf')
        self._int = NloLaserHeadPdDigilockFactorySettings(client, name + ':int')

    @property
    def shg_input(self) -> 'NloLaserHeadPdFactorySettings2':
        return self._shg_input

    @property
    def fiber(self) -> 'NloLaserHeadPdFactorySettings1':
        return self._fiber

    @property
    def shg(self) -> 'NloLaserHeadPdFactorySettings1':
        return self._shg

    @property
    def pdh_dc(self) -> 'NloLaserHeadPdDigilockFactorySettings':
        return self._pdh_dc

    @property
    def pdh_rf(self) -> 'NloLaserHeadPdPdhFactorySettings':
        return self._pdh_rf

    @property
    def int(self) -> 'NloLaserHeadPdDigilockFactorySettings':
        return self._int


class NloLaserHeadPdFactorySettings2:
    def __init__(self, client: Client, name: str) -> None:
        self.__client = client
        self.__name = name
        self._cal_offset = MutableDecofReal(client, name + ':cal-offset')
        self._cal_factor = MutableDecofReal(client, name + ':cal-factor')

    @property
    def cal_offset(self) -> 'MutableDecofReal':
        return self._cal_offset

    @property
    def cal_factor(self) -> 'MutableDecofReal':
        return self._cal_factor


class NloLaserHeadLockShg2:
    def __init__(self, client: Client, name: str) -> None:
        self.__client = client
        self.__name = name
        self._pid_selection = MutableDecofInteger(client, name + ':pid-selection')
        self._pid1 = NloLaserHeadPid2(client, name + ':pid1')
        self._relock = NloLaserHeadRelock2(client, name + ':relock')
        self._state_txt = DecofString(client, name + ':state-txt')
        self._cavity_fast_pzt_voltage = MutableDecofReal(client, name + ':cavity-fast-pzt-voltage')
        self._state = DecofInteger(client, name + ':state')
        self._analog_dl_gain = NloLaserHeadMinifalc2(client, name + ':analog-dl-gain')
        self._window = NloLaserHeadWindow2(client, name + ':window')
        self._setpoint = MutableDecofReal(client, name + ':setpoint')
        self._local_oscillator = NloLaserHeadLocalOscillatorShg2(client, name + ':local-oscillator')
        self._background_trace = DecofBinary(client, name + ':background-trace')
        self._cavity_slow_pzt_voltage = MutableDecofReal(client, name + ':cavity-slow-pzt-voltage')
        self._lock_enabled = MutableDecofBoolean(client, name + ':lock-enabled')
        self._pid2 = NloLaserHeadPid2(client, name + ':pid2')

    @property
    def pid_selection(self) -> 'MutableDecofInteger':
        return self._pid_selection

    @property
    def pid1(self) -> 'NloLaserHeadPid2':
        return self._pid1

    @property
    def relock(self) -> 'NloLaserHeadRelock2':
        return self._relock

    @property
    def state_txt(self) -> 'DecofString':
        return self._state_txt

    @property
    def cavity_fast_pzt_voltage(self) -> 'MutableDecofReal':
        return self._cavity_fast_pzt_voltage

    @property
    def state(self) -> 'DecofInteger':
        return self._state

    @property
    def analog_dl_gain(self) -> 'NloLaserHeadMinifalc2':
        return self._analog_dl_gain

    @property
    def window(self) -> 'NloLaserHeadWindow2':
        return self._window

    @property
    def setpoint(self) -> 'MutableDecofReal':
        return self._setpoint

    @property
    def local_oscillator(self) -> 'NloLaserHeadLocalOscillatorShg2':
        return self._local_oscillator

    @property
    def background_trace(self) -> 'DecofBinary':
        return self._background_trace

    @property
    def cavity_slow_pzt_voltage(self) -> 'MutableDecofReal':
        return self._cavity_slow_pzt_voltage

    @property
    def lock_enabled(self) -> 'MutableDecofBoolean':
        return self._lock_enabled

    @property
    def pid2(self) -> 'NloLaserHeadPid2':
        return self._pid2


class NloLaserHeadMinifalc2:
    def __init__(self, client: Client, name: str) -> None:
        self.__client = client
        self.__name = name
        self._p_gain = MutableDecofReal(client, name + ':p-gain')

    @property
    def p_gain(self) -> 'MutableDecofReal':
        return self._p_gain


class NloLaserHeadLocalOscillatorShg2:
    def __init__(self, client: Client, name: str) -> None:
        self.__client = client
        self.__name = name
        self._coupled_modulation = MutableDecofBoolean(client, name + ':coupled-modulation')
        self._amplitude = MutableDecofReal(client, name + ':amplitude')
        self._use_external_oscillator = MutableDecofBoolean(client, name + ':use-external-oscillator')
        self._enabled = MutableDecofBoolean(client, name + ':enabled')
        self._use_fast_oscillator = MutableDecofBoolean(client, name + ':use-fast-oscillator')
        self._phase_shift = MutableDecofReal(client, name + ':phase-shift')
        self._attenuation_raw = MutableDecofInteger(client, name + ':attenuation-raw')

    @property
    def coupled_modulation(self) -> 'MutableDecofBoolean':
        return self._coupled_modulation

    @property
    def amplitude(self) -> 'MutableDecofReal':
        return self._amplitude

    @property
    def use_external_oscillator(self) -> 'MutableDecofBoolean':
        return self._use_external_oscillator

    @property
    def enabled(self) -> 'MutableDecofBoolean':
        return self._enabled

    @property
    def use_fast_oscillator(self) -> 'MutableDecofBoolean':
        return self._use_fast_oscillator

    @property
    def phase_shift(self) -> 'MutableDecofReal':
        return self._phase_shift

    @property
    def attenuation_raw(self) -> 'MutableDecofInteger':
        return self._attenuation_raw

    def auto_pdh(self) -> None:
        self.__client.exec(self.__name + ':auto-pdh', input_stream=None, output_type=None, return_type=None)


class NloPhotoDiodes:
    def __init__(self, client: Client, name: str) -> None:
        self.__client = client
        self.__name = name
        self._fhg = NloLaserHeadNloPhotodiode2(client, name + ':fhg')
        self._shg_input = PdCal(client, name + ':shg-input')
        self._dl = NloLaserHeadNloPhotodiode2(client, name + ':dl')
        self._shg = NloLaserHeadNloPhotodiode2(client, name + ':shg')
        self._shg_pdh_dc = NloLaserHeadNloDigilockPhotodiode2(client, name + ':shg-pdh-dc')
        self._shg_pdh_rf = NloLaserHeadNloPdhPhotodiode2(client, name + ':shg-pdh-rf')
        self._fhg_int = NloLaserHeadNloDigilockPhotodiode2(client, name + ':fhg-int')
        self._fhg_pdh_rf = NloLaserHeadNloPdhPhotodiode2(client, name + ':fhg-pdh-rf')
        self._fiber = NloLaserHeadNloPhotodiode2(client, name + ':fiber')
        self._fhg_pdh_dc = NloLaserHeadNloDigilockPhotodiode2(client, name + ':fhg-pdh-dc')
        self._amp = NloLaserHeadNloPhotodiode2(client, name + ':amp')
        self._shg_int = NloLaserHeadNloDigilockPhotodiode2(client, name + ':shg-int')

    @property
    def fhg(self) -> 'NloLaserHeadNloPhotodiode2':
        return self._fhg

    @property
    def shg_input(self) -> 'PdCal':
        return self._shg_input

    @property
    def dl(self) -> 'NloLaserHeadNloPhotodiode2':
        return self._dl

    @property
    def shg(self) -> 'NloLaserHeadNloPhotodiode2':
        return self._shg

    @property
    def shg_pdh_dc(self) -> 'NloLaserHeadNloDigilockPhotodiode2':
        return self._shg_pdh_dc

    @property
    def shg_pdh_rf(self) -> 'NloLaserHeadNloPdhPhotodiode2':
        return self._shg_pdh_rf

    @property
    def fhg_int(self) -> 'NloLaserHeadNloDigilockPhotodiode2':
        return self._fhg_int

    @property
    def fhg_pdh_rf(self) -> 'NloLaserHeadNloPdhPhotodiode2':
        return self._fhg_pdh_rf

    @property
    def fiber(self) -> 'NloLaserHeadNloPhotodiode2':
        return self._fiber

    @property
    def fhg_pdh_dc(self) -> 'NloLaserHeadNloDigilockPhotodiode2':
        return self._fhg_pdh_dc

    @property
    def amp(self) -> 'NloLaserHeadNloPhotodiode2':
        return self._amp

    @property
    def shg_int(self) -> 'NloLaserHeadNloDigilockPhotodiode2':
        return self._shg_int


class NloLaserHeadNloPhotodiode2:
    def __init__(self, client: Client, name: str) -> None:
        self.__client = client
        self.__name = name
        self._cal_factor = MutableDecofReal(client, name + ':cal-factor')
        self._photodiode = DecofReal(client, name + ':photodiode')
        self._power = DecofReal(client, name + ':power')
        self._cal_offset = MutableDecofReal(client, name + ':cal-offset')

    @property
    def cal_factor(self) -> 'MutableDecofReal':
        return self._cal_factor

    @property
    def photodiode(self) -> 'DecofReal':
        return self._photodiode

    @property
    def power(self) -> 'DecofReal':
        return self._power

    @property
    def cal_offset(self) -> 'MutableDecofReal':
        return self._cal_offset


class NloLaserHeadNloDigilockPhotodiode2:
    def __init__(self, client: Client, name: str) -> None:
        self.__client = client
        self.__name = name
        self._photodiode = DecofReal(client, name + ':photodiode')
        self._cal_offset = MutableDecofReal(client, name + ':cal-offset')

    @property
    def photodiode(self) -> 'DecofReal':
        return self._photodiode

    @property
    def cal_offset(self) -> 'MutableDecofReal':
        return self._cal_offset


class NloLaserHeadNloPdhPhotodiode2:
    def __init__(self, client: Client, name: str) -> None:
        self.__client = client
        self.__name = name
        self._photodiode = DecofReal(client, name + ':photodiode')
        self._gain = MutableDecofReal(client, name + ':gain')

    @property
    def photodiode(self) -> 'DecofReal':
        return self._photodiode

    @property
    def gain(self) -> 'MutableDecofReal':
        return self._gain


class NloLaserHeadServos:
    def __init__(self, client: Client, name: str) -> None:
        self.__client = client
        self.__name = name
        self._fhg2_vert = NloLaserHeadServoPwm2(client, name + ':fhg2-vert')
        self._ta2_hor = NloLaserHeadServoPwm2(client, name + ':ta2-hor')
        self._ta1_vert = NloLaserHeadServoPwm2(client, name + ':ta1-vert')
        self._ta1_hor = NloLaserHeadServoPwm2(client, name + ':ta1-hor')
        self._shg2_vert = NloLaserHeadServoPwm2(client, name + ':shg2-vert')
        self._fhg1_hor = NloLaserHeadServoPwm2(client, name + ':fhg1-hor')
        self._fiber1_hor = NloLaserHeadServoPwm2(client, name + ':fiber1-hor')
        self._fhg2_hor = NloLaserHeadServoPwm2(client, name + ':fhg2-hor')
        self._uv_cryst = NloLaserHeadServoPwm2(client, name + ':uv-cryst')
        self._fiber2_hor = NloLaserHeadServoPwm2(client, name + ':fiber2-hor')
        self._shg2_hor = NloLaserHeadServoPwm2(client, name + ':shg2-hor')
        self._fiber2_vert = NloLaserHeadServoPwm2(client, name + ':fiber2-vert')
        self._fhg1_vert = NloLaserHeadServoPwm2(client, name + ':fhg1-vert')
        self._ta2_vert = NloLaserHeadServoPwm2(client, name + ':ta2-vert')
        self._uv_outcpl = NloLaserHeadServoPwm2(client, name + ':uv-outcpl')
        self._fiber1_vert = NloLaserHeadServoPwm2(client, name + ':fiber1-vert')
        self._shg1_vert = NloLaserHeadServoPwm2(client, name + ':shg1-vert')
        self._shg1_hor = NloLaserHeadServoPwm2(client, name + ':shg1-hor')

    @property
    def fhg2_vert(self) -> 'NloLaserHeadServoPwm2':
        return self._fhg2_vert

    @property
    def ta2_hor(self) -> 'NloLaserHeadServoPwm2':
        return self._ta2_hor

    @property
    def ta1_vert(self) -> 'NloLaserHeadServoPwm2':
        return self._ta1_vert

    @property
    def ta1_hor(self) -> 'NloLaserHeadServoPwm2':
        return self._ta1_hor

    @property
    def shg2_vert(self) -> 'NloLaserHeadServoPwm2':
        return self._shg2_vert

    @property
    def fhg1_hor(self) -> 'NloLaserHeadServoPwm2':
        return self._fhg1_hor

    @property
    def fiber1_hor(self) -> 'NloLaserHeadServoPwm2':
        return self._fiber1_hor

    @property
    def fhg2_hor(self) -> 'NloLaserHeadServoPwm2':
        return self._fhg2_hor

    @property
    def uv_cryst(self) -> 'NloLaserHeadServoPwm2':
        return self._uv_cryst

    @property
    def fiber2_hor(self) -> 'NloLaserHeadServoPwm2':
        return self._fiber2_hor

    @property
    def shg2_hor(self) -> 'NloLaserHeadServoPwm2':
        return self._shg2_hor

    @property
    def fiber2_vert(self) -> 'NloLaserHeadServoPwm2':
        return self._fiber2_vert

    @property
    def fhg1_vert(self) -> 'NloLaserHeadServoPwm2':
        return self._fhg1_vert

    @property
    def ta2_vert(self) -> 'NloLaserHeadServoPwm2':
        return self._ta2_vert

    @property
    def uv_outcpl(self) -> 'NloLaserHeadServoPwm2':
        return self._uv_outcpl

    @property
    def fiber1_vert(self) -> 'NloLaserHeadServoPwm2':
        return self._fiber1_vert

    @property
    def shg1_vert(self) -> 'NloLaserHeadServoPwm2':
        return self._shg1_vert

    @property
    def shg1_hor(self) -> 'NloLaserHeadServoPwm2':
        return self._shg1_hor

    def center_fiber_servos(self) -> None:
        self.__client.exec(self.__name + ':center-fiber-servos', input_stream=None, output_type=None, return_type=None)

    def center_shg_servos(self) -> None:
        self.__client.exec(self.__name + ':center-shg-servos', input_stream=None, output_type=None, return_type=None)

    def center_all_servos(self) -> None:
        self.__client.exec(self.__name + ':center-all-servos', input_stream=None, output_type=None, return_type=None)

    def center_ta_servos(self) -> None:
        self.__client.exec(self.__name + ':center-ta-servos', input_stream=None, output_type=None, return_type=None)

    def center_fhg_servos(self) -> None:
        self.__client.exec(self.__name + ':center-fhg-servos', input_stream=None, output_type=None, return_type=None)


class NloLaserHeadServoPwm2:
    def __init__(self, client: Client, name: str) -> None:
        self.__client = client
        self.__name = name
        self._value = MutableDecofInteger(client, name + ':value')
        self._enabled = MutableDecofBoolean(client, name + ':enabled')
        self._display_name = DecofString(client, name + ':display-name')

    @property
    def value(self) -> 'MutableDecofInteger':
        return self._value

    @property
    def enabled(self) -> 'MutableDecofBoolean':
        return self._enabled

    @property
    def display_name(self) -> 'DecofString':
        return self._display_name

    def center_servo(self) -> None:
        self.__client.exec(self.__name + ':center-servo', input_stream=None, output_type=None, return_type=None)


class NloLaserHeadPowerOptimization:
    def __init__(self, client: Client, name: str) -> None:
        self.__client = client
        self.__name = name
        self._progress_data_shg = DecofBinary(client, name + ':progress-data-shg')
        self._stage2 = NloLaserHeadStage2(client, name + ':stage2')
        self._ongoing = DecofBoolean(client, name + ':ongoing')
        self._abort = MutableDecofBoolean(client, name + ':abort')
        self._status = DecofInteger(client, name + ':status')
        self._stage5 = NloLaserHeadStage2(client, name + ':stage5')
        self._shg_advanced = MutableDecofBoolean(client, name + ':shg-advanced')
        self._progress_data_fiber = DecofBinary(client, name + ':progress-data-fiber')
        self._progress_data_amp = DecofBinary(client, name + ':progress-data-amp')
        self._stage1 = NloLaserHeadStage2(client, name + ':stage1')
        self._progress = DecofInteger(client, name + ':progress')
        self._status_string = DecofString(client, name + ':status-string')
        self._stage3 = NloLaserHeadStage2(client, name + ':stage3')
        self._stage4 = NloLaserHeadStage2(client, name + ':stage4')
        self._progress_data_fhg = DecofBinary(client, name + ':progress-data-fhg')

    @property
    def progress_data_shg(self) -> 'DecofBinary':
        return self._progress_data_shg

    @property
    def stage2(self) -> 'NloLaserHeadStage2':
        return self._stage2

    @property
    def ongoing(self) -> 'DecofBoolean':
        return self._ongoing

    @property
    def abort(self) -> 'MutableDecofBoolean':
        return self._abort

    @property
    def status(self) -> 'DecofInteger':
        return self._status

    @property
    def stage5(self) -> 'NloLaserHeadStage2':
        return self._stage5

    @property
    def shg_advanced(self) -> 'MutableDecofBoolean':
        return self._shg_advanced

    @property
    def progress_data_fiber(self) -> 'DecofBinary':
        return self._progress_data_fiber

    @property
    def progress_data_amp(self) -> 'DecofBinary':
        return self._progress_data_amp

    @property
    def stage1(self) -> 'NloLaserHeadStage2':
        return self._stage1

    @property
    def progress(self) -> 'DecofInteger':
        return self._progress

    @property
    def status_string(self) -> 'DecofString':
        return self._status_string

    @property
    def stage3(self) -> 'NloLaserHeadStage2':
        return self._stage3

    @property
    def stage4(self) -> 'NloLaserHeadStage2':
        return self._stage4

    @property
    def progress_data_fhg(self) -> 'DecofBinary':
        return self._progress_data_fhg

    def start_optimization_fiber(self) -> int:
        return self.__client.exec(self.__name + ':start-optimization-fiber', input_stream=None, output_type=None, return_type=int)

    def start_optimization_fhg(self) -> int:
        return self.__client.exec(self.__name + ':start-optimization-fhg', input_stream=None, output_type=None, return_type=int)

    def start_optimization_amp(self) -> int:
        return self.__client.exec(self.__name + ':start-optimization-amp', input_stream=None, output_type=None, return_type=int)

    def start_optimization_all(self) -> int:
        return self.__client.exec(self.__name + ':start-optimization-all', input_stream=None, output_type=None, return_type=int)

    def start_optimization_shg(self) -> int:
        return self.__client.exec(self.__name + ':start-optimization-shg', input_stream=None, output_type=None, return_type=int)


class NloLaserHeadStage2:
    def __init__(self, client: Client, name: str) -> None:
        self.__client = client
        self.__name = name
        self._optimization_in_progress = DecofBoolean(client, name + ':optimization-in-progress')
        self._input = NloLaserHeadOptInput2(client, name + ':input')
        self._progress = DecofInteger(client, name + ':progress')
        self._autosave_actuator_values = MutableDecofBoolean(client, name + ':autosave-actuator-values')
        self._regress_tolerance = MutableDecofInteger(client, name + ':regress-tolerance')
        self._restore_on_abort = MutableDecofBoolean(client, name + ':restore-on-abort')
        self._restore_on_regress = MutableDecofBoolean(client, name + ':restore-on-regress')

    @property
    def optimization_in_progress(self) -> 'DecofBoolean':
        return self._optimization_in_progress

    @property
    def input(self) -> 'NloLaserHeadOptInput2':
        return self._input

    @property
    def progress(self) -> 'DecofInteger':
        return self._progress

    @property
    def autosave_actuator_values(self) -> 'MutableDecofBoolean':
        return self._autosave_actuator_values

    @property
    def regress_tolerance(self) -> 'MutableDecofInteger':
        return self._regress_tolerance

    @property
    def restore_on_abort(self) -> 'MutableDecofBoolean':
        return self._restore_on_abort

    @property
    def restore_on_regress(self) -> 'MutableDecofBoolean':
        return self._restore_on_regress

    def start_optimization(self) -> int:
        return self.__client.exec(self.__name + ':start-optimization', input_stream=None, output_type=None, return_type=int)


class NloLaserHeadOptInput2:
    def __init__(self, client: Client, name: str) -> None:
        self.__client = client
        self.__name = name
        self._value_calibrated = DecofReal(client, name + ':value-calibrated')

    @property
    def value_calibrated(self) -> 'DecofReal':
        return self._value_calibrated


class Dpss2:
    def __init__(self, client: Client, name: str) -> None:
        self.__client = client
        self.__name = name
        self._tc_status_txt = DecofString(client, name + ':tc-status-txt')
        self._tc_status = DecofInteger(client, name + ':tc-status')
        self._power_act = DecofReal(client, name + ':power-act')
        self._status = DecofInteger(client, name + ':status')
        self._power_max = DecofReal(client, name + ':power-max')
        self._error_txt = DecofString(client, name + ':error-txt')
        self._power_margin = DecofReal(client, name + ':power-margin')
        self._operation_time = DecofReal(client, name + ':operation-time')
        self._current_act = DecofReal(client, name + ':current-act')
        self._power_set = MutableDecofReal(client, name + ':power-set')
        self._error_code = DecofInteger(client, name + ':error-code')
        self._current_max = DecofReal(client, name + ':current-max')
        self._enabled = MutableDecofBoolean(client, name + ':enabled')
        self._status_txt = DecofString(client, name + ':status-txt')

    @property
    def tc_status_txt(self) -> 'DecofString':
        return self._tc_status_txt

    @property
    def tc_status(self) -> 'DecofInteger':
        return self._tc_status

    @property
    def power_act(self) -> 'DecofReal':
        return self._power_act

    @property
    def status(self) -> 'DecofInteger':
        return self._status

    @property
    def power_max(self) -> 'DecofReal':
        return self._power_max

    @property
    def error_txt(self) -> 'DecofString':
        return self._error_txt

    @property
    def power_margin(self) -> 'DecofReal':
        return self._power_margin

    @property
    def operation_time(self) -> 'DecofReal':
        return self._operation_time

    @property
    def current_act(self) -> 'DecofReal':
        return self._current_act

    @property
    def power_set(self) -> 'MutableDecofReal':
        return self._power_set

    @property
    def error_code(self) -> 'DecofInteger':
        return self._error_code

    @property
    def current_max(self) -> 'DecofReal':
        return self._current_max

    @property
    def enabled(self) -> 'MutableDecofBoolean':
        return self._enabled

    @property
    def status_txt(self) -> 'DecofString':
        return self._status_txt


class PdExt:
    def __init__(self, client: Client, name: str) -> None:
        self.__client = client
        self.__name = name
        self._photodiode = DecofReal(client, name + ':photodiode')
        self._input_channel = MutableDecofInteger(client, name + ':input-channel')
        self._power = DecofReal(client, name + ':power')
        self._cal_offset = MutableDecofReal(client, name + ':cal-offset')
        self._cal_factor = MutableDecofReal(client, name + ':cal-factor')

    @property
    def photodiode(self) -> 'DecofReal':
        return self._photodiode

    @property
    def input_channel(self) -> 'MutableDecofInteger':
        return self._input_channel

    @property
    def power(self) -> 'DecofReal':
        return self._power

    @property
    def cal_offset(self) -> 'MutableDecofReal':
        return self._cal_offset

    @property
    def cal_factor(self) -> 'MutableDecofReal':
        return self._cal_factor


class ScanGenerator:
    def __init__(self, client: Client, name: str) -> None:
        self.__client = client
        self.__name = name
        self._start = MutableDecofReal(client, name + ':start')
        self._frequency = MutableDecofReal(client, name + ':frequency')
        self._signal_type = MutableDecofInteger(client, name + ':signal-type')
        self._offset = MutableDecofReal(client, name + ':offset')
        self._amplitude = MutableDecofReal(client, name + ':amplitude')
        self._hold = MutableDecofBoolean(client, name + ':hold')
        self._unit = DecofString(client, name + ':unit')
        self._output_channel = MutableDecofInteger(client, name + ':output-channel')
        self._enabled = MutableDecofBoolean(client, name + ':enabled')
        self._phase_shift = MutableDecofReal(client, name + ':phase-shift')
        self._end = MutableDecofReal(client, name + ':end')

    @property
    def start(self) -> 'MutableDecofReal':
        return self._start

    @property
    def frequency(self) -> 'MutableDecofReal':
        return self._frequency

    @property
    def signal_type(self) -> 'MutableDecofInteger':
        return self._signal_type

    @property
    def offset(self) -> 'MutableDecofReal':
        return self._offset

    @property
    def amplitude(self) -> 'MutableDecofReal':
        return self._amplitude

    @property
    def hold(self) -> 'MutableDecofBoolean':
        return self._hold

    @property
    def unit(self) -> 'DecofString':
        return self._unit

    @property
    def output_channel(self) -> 'MutableDecofInteger':
        return self._output_channel

    @property
    def enabled(self) -> 'MutableDecofBoolean':
        return self._enabled

    @property
    def phase_shift(self) -> 'MutableDecofReal':
        return self._phase_shift

    @property
    def end(self) -> 'MutableDecofReal':
        return self._end


class UvShg:
    def __init__(self, client: Client, name: str) -> None:
        self.__client = client
        self.__name = name
        self._specs_fulfilled = DecofBoolean(client, name + ':specs-fulfilled')
        self._factory_settings = UvFactorySettings(client, name + ':factory-settings')
        self._status = DecofInteger(client, name + ':status')
        self._hwp_transmittance = DecofReal(client, name + ':hwp-transmittance')
        self._eom = UvEom(client, name + ':eom')
        self._lock = NloLaserHeadLockShg1(client, name + ':lock')
        self._cavity = UvCavity(client, name + ':cavity')
        self._crystal = UvCrystal(client, name + ':crystal')
        self._pump = Dpss1(client, name + ':pump')
        self._status_txt = DecofString(client, name + ':status-txt')
        self._ssw_ver = DecofString(client, name + ':ssw-ver')
        self._error = DecofInteger(client, name + ':error')
        self._status_parameters = UvStatusParameters(client, name + ':status-parameters')
        self._error_txt = DecofString(client, name + ':error-txt')
        self._servo = NloLaserHeadUvServos(client, name + ':servo')
        self._power_optimization = UvShgPowerOptimization(client, name + ':power-optimization')
        self._power_margin = DecofReal(client, name + ':power-margin')
        self._operation_time = DecofReal(client, name + ':operation-time')
        self._pd = NloLaserHeadUvPhotoDiodes(client, name + ':pd')
        self._scan = NloLaserHeadSiggen1(client, name + ':scan')
        self._power_stabilization = UvShgPowerStabilization(client, name + ':power-stabilization')
        self._remaining_optics_spots = DecofInteger(client, name + ':remaining-optics-spots')
        self._scope = NloLaserHeadScopeT1(client, name + ':scope')
        self._baseplate_temperature = DecofReal(client, name + ':baseplate-temperature')

    @property
    def specs_fulfilled(self) -> 'DecofBoolean':
        return self._specs_fulfilled

    @property
    def factory_settings(self) -> 'UvFactorySettings':
        return self._factory_settings

    @property
    def status(self) -> 'DecofInteger':
        return self._status

    @property
    def hwp_transmittance(self) -> 'DecofReal':
        return self._hwp_transmittance

    @property
    def eom(self) -> 'UvEom':
        return self._eom

    @property
    def lock(self) -> 'NloLaserHeadLockShg1':
        return self._lock

    @property
    def cavity(self) -> 'UvCavity':
        return self._cavity

    @property
    def crystal(self) -> 'UvCrystal':
        return self._crystal

    @property
    def pump(self) -> 'Dpss1':
        return self._pump

    @property
    def status_txt(self) -> 'DecofString':
        return self._status_txt

    @property
    def ssw_ver(self) -> 'DecofString':
        return self._ssw_ver

    @property
    def error(self) -> 'DecofInteger':
        return self._error

    @property
    def status_parameters(self) -> 'UvStatusParameters':
        return self._status_parameters

    @property
    def error_txt(self) -> 'DecofString':
        return self._error_txt

    @property
    def servo(self) -> 'NloLaserHeadUvServos':
        return self._servo

    @property
    def power_optimization(self) -> 'UvShgPowerOptimization':
        return self._power_optimization

    @property
    def power_margin(self) -> 'DecofReal':
        return self._power_margin

    @property
    def operation_time(self) -> 'DecofReal':
        return self._operation_time

    @property
    def pd(self) -> 'NloLaserHeadUvPhotoDiodes':
        return self._pd

    @property
    def scan(self) -> 'NloLaserHeadSiggen1':
        return self._scan

    @property
    def power_stabilization(self) -> 'UvShgPowerStabilization':
        return self._power_stabilization

    @property
    def remaining_optics_spots(self) -> 'DecofInteger':
        return self._remaining_optics_spots

    @property
    def scope(self) -> 'NloLaserHeadScopeT1':
        return self._scope

    @property
    def baseplate_temperature(self) -> 'DecofReal':
        return self._baseplate_temperature

    def clear_errors(self) -> None:
        self.__client.exec(self.__name + ':clear-errors', input_stream=None, output_type=None, return_type=None)

    def restore(self) -> None:
        self.__client.exec(self.__name + ':restore', input_stream=None, output_type=None, return_type=None)

    def store(self) -> None:
        self.__client.exec(self.__name + ':store', input_stream=None, output_type=None, return_type=None)

    def perform_optics_shift(self) -> None:
        self.__client.exec(self.__name + ':perform-optics-shift', input_stream=None, output_type=None, return_type=None)

    def perform_optimization(self) -> None:
        self.__client.exec(self.__name + ':perform-optimization', input_stream=None, output_type=None, return_type=None)


class UvFactorySettings:
    def __init__(self, client: Client, name: str) -> None:
        self.__client = client
        self.__name = name
        self._crystal_tc = NloLaserHeadTcFactorySettings(client, name + ':crystal-tc')
        self._modified = DecofBoolean(client, name + ':modified')
        self._eom_tc = NloLaserHeadTcFactorySettings(client, name + ':eom-tc')
        self._pd = NloLaserHeadUvPhotodiodesFactorySettings(client, name + ':pd')
        self._pc = NloLaserHeadPcFactorySettings(client, name + ':pc')
        self._cavity_tc = NloLaserHeadTcFactorySettings(client, name + ':cavity-tc')
        self._lock = NloLaserHeadLockFactorySettings(client, name + ':lock')

    @property
    def crystal_tc(self) -> 'NloLaserHeadTcFactorySettings':
        return self._crystal_tc

    @property
    def modified(self) -> 'DecofBoolean':
        return self._modified

    @property
    def eom_tc(self) -> 'NloLaserHeadTcFactorySettings':
        return self._eom_tc

    @property
    def pd(self) -> 'NloLaserHeadUvPhotodiodesFactorySettings':
        return self._pd

    @property
    def pc(self) -> 'NloLaserHeadPcFactorySettings':
        return self._pc

    @property
    def cavity_tc(self) -> 'NloLaserHeadTcFactorySettings':
        return self._cavity_tc

    @property
    def lock(self) -> 'NloLaserHeadLockFactorySettings':
        return self._lock

    def apply(self) -> None:
        self.__client.exec(self.__name + ':apply', input_stream=None, output_type=None, return_type=None)

    def retrieve_now(self) -> None:
        self.__client.exec(self.__name + ':retrieve-now', input_stream=None, output_type=None, return_type=None)


class NloLaserHeadUvPhotodiodesFactorySettings:
    def __init__(self, client: Client, name: str) -> None:
        self.__client = client
        self.__name = name
        self._pdh_rf = NloLaserHeadPdPdhFactorySettings(client, name + ':pdh-rf')
        self._shg = NloLaserHeadPdFactorySettings1(client, name + ':shg')
        self._pdh_dc = NloLaserHeadPdDigilockFactorySettings(client, name + ':pdh-dc')

    @property
    def pdh_rf(self) -> 'NloLaserHeadPdPdhFactorySettings':
        return self._pdh_rf

    @property
    def shg(self) -> 'NloLaserHeadPdFactorySettings1':
        return self._shg

    @property
    def pdh_dc(self) -> 'NloLaserHeadPdDigilockFactorySettings':
        return self._pdh_dc


class UvEom:
    def __init__(self, client: Client, name: str) -> None:
        self.__client = client
        self.__name = name
        self._tc = TcChannel1(client, name + ':tc')

    @property
    def tc(self) -> 'TcChannel1':
        return self._tc


class TcChannel1:
    def __init__(self, client: Client, name: str) -> None:
        self.__client = client
        self.__name = name
        self._status = DecofInteger(client, name + ':status')
        self._ntc_series_resistance = DecofReal(client, name + ':ntc-series-resistance')
        self._resistance = DecofReal(client, name + ':resistance')
        self._temp_set_max = DecofReal(client, name + ':temp-set-max')
        self._temp_set = DecofReal(client, name + ':temp-set')
        self._current_act = DecofReal(client, name + ':current-act')
        self._external_input = ExtInput1(client, name + ':external-input')
        self._t_loop = TcChannelTLoop1(client, name + ':t-loop')
        self._ready = DecofBoolean(client, name + ':ready')
        self._drv_voltage = DecofReal(client, name + ':drv-voltage')
        self._c_loop = TcChannelCLoop1(client, name + ':c-loop')
        self._current_set = DecofReal(client, name + ':current-set')
        self._enabled = DecofBoolean(client, name + ':enabled')
        self._status_txt = DecofString(client, name + ':status-txt')
        self._limits = TcChannelCheck1(client, name + ':limits')
        self._temp_roc_enabled = DecofBoolean(client, name + ':temp-roc-enabled')
        self._temp_set_min = DecofReal(client, name + ':temp-set-min')
        self._power_source = DecofInteger(client, name + ':power-source')
        self._ntc_parallel_resistance = DecofReal(client, name + ':ntc-parallel-resistance')
        self._temp_act = DecofReal(client, name + ':temp-act')
        self._temp_reset = DecofBoolean(client, name + ':temp-reset')
        self._fault = DecofBoolean(client, name + ':fault')
        self._voltage_act = DecofReal(client, name + ':voltage-act')
        self._current_set_min = DecofReal(client, name + ':current-set-min')
        self._temp_roc_limit = DecofReal(client, name + ':temp-roc-limit')
        self._current_set_max = DecofReal(client, name + ':current-set-max')
        self._path = DecofString(client, name + ':path')

    @property
    def status(self) -> 'DecofInteger':
        return self._status

    @property
    def ntc_series_resistance(self) -> 'DecofReal':
        return self._ntc_series_resistance

    @property
    def resistance(self) -> 'DecofReal':
        return self._resistance

    @property
    def temp_set_max(self) -> 'DecofReal':
        return self._temp_set_max

    @property
    def temp_set(self) -> 'DecofReal':
        return self._temp_set

    @property
    def current_act(self) -> 'DecofReal':
        return self._current_act

    @property
    def external_input(self) -> 'ExtInput1':
        return self._external_input

    @property
    def t_loop(self) -> 'TcChannelTLoop1':
        return self._t_loop

    @property
    def ready(self) -> 'DecofBoolean':
        return self._ready

    @property
    def drv_voltage(self) -> 'DecofReal':
        return self._drv_voltage

    @property
    def c_loop(self) -> 'TcChannelCLoop1':
        return self._c_loop

    @property
    def current_set(self) -> 'DecofReal':
        return self._current_set

    @property
    def enabled(self) -> 'DecofBoolean':
        return self._enabled

    @property
    def status_txt(self) -> 'DecofString':
        return self._status_txt

    @property
    def limits(self) -> 'TcChannelCheck1':
        return self._limits

    @property
    def temp_roc_enabled(self) -> 'DecofBoolean':
        return self._temp_roc_enabled

    @property
    def temp_set_min(self) -> 'DecofReal':
        return self._temp_set_min

    @property
    def power_source(self) -> 'DecofInteger':
        return self._power_source

    @property
    def ntc_parallel_resistance(self) -> 'DecofReal':
        return self._ntc_parallel_resistance

    @property
    def temp_act(self) -> 'DecofReal':
        return self._temp_act

    @property
    def temp_reset(self) -> 'DecofBoolean':
        return self._temp_reset

    @property
    def fault(self) -> 'DecofBoolean':
        return self._fault

    @property
    def voltage_act(self) -> 'DecofReal':
        return self._voltage_act

    @property
    def current_set_min(self) -> 'DecofReal':
        return self._current_set_min

    @property
    def temp_roc_limit(self) -> 'DecofReal':
        return self._temp_roc_limit

    @property
    def current_set_max(self) -> 'DecofReal':
        return self._current_set_max

    @property
    def path(self) -> 'DecofString':
        return self._path


class ExtInput1:
    def __init__(self, client: Client, name: str) -> None:
        self.__client = client
        self.__name = name
        self._signal = DecofInteger(client, name + ':signal')
        self._enabled = DecofBoolean(client, name + ':enabled')
        self._factor = DecofReal(client, name + ':factor')

    @property
    def signal(self) -> 'DecofInteger':
        return self._signal

    @property
    def enabled(self) -> 'DecofBoolean':
        return self._enabled

    @property
    def factor(self) -> 'DecofReal':
        return self._factor


class TcChannelTLoop1:
    def __init__(self, client: Client, name: str) -> None:
        self.__client = client
        self.__name = name
        self._on = DecofBoolean(client, name + ':on')
        self._ok_time = DecofReal(client, name + ':ok-time')
        self._i_gain = DecofReal(client, name + ':i-gain')
        self._ok_tolerance = DecofReal(client, name + ':ok-tolerance')
        self._p_gain = DecofReal(client, name + ':p-gain')
        self._d_gain = DecofReal(client, name + ':d-gain')

    @property
    def on(self) -> 'DecofBoolean':
        return self._on

    @property
    def ok_time(self) -> 'DecofReal':
        return self._ok_time

    @property
    def i_gain(self) -> 'DecofReal':
        return self._i_gain

    @property
    def ok_tolerance(self) -> 'DecofReal':
        return self._ok_tolerance

    @property
    def p_gain(self) -> 'DecofReal':
        return self._p_gain

    @property
    def d_gain(self) -> 'DecofReal':
        return self._d_gain


class TcChannelCLoop1:
    def __init__(self, client: Client, name: str) -> None:
        self.__client = client
        self.__name = name
        self._on = DecofBoolean(client, name + ':on')
        self._i_gain = DecofReal(client, name + ':i-gain')

    @property
    def on(self) -> 'DecofBoolean':
        return self._on

    @property
    def i_gain(self) -> 'DecofReal':
        return self._i_gain


class TcChannelCheck1:
    def __init__(self, client: Client, name: str) -> None:
        self.__client = client
        self.__name = name
        self._timed_out = DecofBoolean(client, name + ':timed-out')
        self._temp_min = DecofReal(client, name + ':temp-min')
        self._temp_max = DecofReal(client, name + ':temp-max')
        self._timeout = DecofInteger(client, name + ':timeout')
        self._out_of_range = DecofBoolean(client, name + ':out-of-range')

    @property
    def timed_out(self) -> 'DecofBoolean':
        return self._timed_out

    @property
    def temp_min(self) -> 'DecofReal':
        return self._temp_min

    @property
    def temp_max(self) -> 'DecofReal':
        return self._temp_max

    @property
    def timeout(self) -> 'DecofInteger':
        return self._timeout

    @property
    def out_of_range(self) -> 'DecofBoolean':
        return self._out_of_range


class NloLaserHeadLockShg1:
    def __init__(self, client: Client, name: str) -> None:
        self.__client = client
        self.__name = name
        self._pid_selection = DecofInteger(client, name + ':pid-selection')
        self._pid1 = NloLaserHeadPid1(client, name + ':pid1')
        self._relock = NloLaserHeadRelock1(client, name + ':relock')
        self._state_txt = DecofString(client, name + ':state-txt')
        self._cavity_fast_pzt_voltage = DecofReal(client, name + ':cavity-fast-pzt-voltage')
        self._state = DecofInteger(client, name + ':state')
        self._analog_dl_gain = NloLaserHeadMinifalc1(client, name + ':analog-dl-gain')
        self._window = NloLaserHeadWindow1(client, name + ':window')
        self._setpoint = DecofReal(client, name + ':setpoint')
        self._local_oscillator = NloLaserHeadLocalOscillatorShg1(client, name + ':local-oscillator')
        self._background_trace = DecofBinary(client, name + ':background-trace')
        self._cavity_slow_pzt_voltage = DecofReal(client, name + ':cavity-slow-pzt-voltage')
        self._lock_enabled = DecofBoolean(client, name + ':lock-enabled')
        self._pid2 = NloLaserHeadPid1(client, name + ':pid2')

    @property
    def pid_selection(self) -> 'DecofInteger':
        return self._pid_selection

    @property
    def pid1(self) -> 'NloLaserHeadPid1':
        return self._pid1

    @property
    def relock(self) -> 'NloLaserHeadRelock1':
        return self._relock

    @property
    def state_txt(self) -> 'DecofString':
        return self._state_txt

    @property
    def cavity_fast_pzt_voltage(self) -> 'DecofReal':
        return self._cavity_fast_pzt_voltage

    @property
    def state(self) -> 'DecofInteger':
        return self._state

    @property
    def analog_dl_gain(self) -> 'NloLaserHeadMinifalc1':
        return self._analog_dl_gain

    @property
    def window(self) -> 'NloLaserHeadWindow1':
        return self._window

    @property
    def setpoint(self) -> 'DecofReal':
        return self._setpoint

    @property
    def local_oscillator(self) -> 'NloLaserHeadLocalOscillatorShg1':
        return self._local_oscillator

    @property
    def background_trace(self) -> 'DecofBinary':
        return self._background_trace

    @property
    def cavity_slow_pzt_voltage(self) -> 'DecofReal':
        return self._cavity_slow_pzt_voltage

    @property
    def lock_enabled(self) -> 'DecofBoolean':
        return self._lock_enabled

    @property
    def pid2(self) -> 'NloLaserHeadPid1':
        return self._pid2


class NloLaserHeadPid1:
    def __init__(self, client: Client, name: str) -> None:
        self.__client = client
        self.__name = name
        self._gain = NloLaserHeadGain1(client, name + ':gain')

    @property
    def gain(self) -> 'NloLaserHeadGain1':
        return self._gain


class NloLaserHeadGain1:
    def __init__(self, client: Client, name: str) -> None:
        self.__client = client
        self.__name = name
        self._all = DecofReal(client, name + ':all')
        self._d = DecofReal(client, name + ':d')
        self._i_cutoff_enabled = DecofBoolean(client, name + ':i-cutoff-enabled')
        self._p = DecofReal(client, name + ':p')
        self._i_cutoff = DecofReal(client, name + ':i-cutoff')
        self._i = DecofReal(client, name + ':i')

    @property
    def all(self) -> 'DecofReal':
        return self._all

    @property
    def d(self) -> 'DecofReal':
        return self._d

    @property
    def i_cutoff_enabled(self) -> 'DecofBoolean':
        return self._i_cutoff_enabled

    @property
    def p(self) -> 'DecofReal':
        return self._p

    @property
    def i_cutoff(self) -> 'DecofReal':
        return self._i_cutoff

    @property
    def i(self) -> 'DecofReal':
        return self._i


class NloLaserHeadRelock1:
    def __init__(self, client: Client, name: str) -> None:
        self.__client = client
        self.__name = name
        self._frequency = DecofReal(client, name + ':frequency')
        self._delay = DecofReal(client, name + ':delay')
        self._amplitude = DecofReal(client, name + ':amplitude')
        self._enabled = DecofBoolean(client, name + ':enabled')

    @property
    def frequency(self) -> 'DecofReal':
        return self._frequency

    @property
    def delay(self) -> 'DecofReal':
        return self._delay

    @property
    def amplitude(self) -> 'DecofReal':
        return self._amplitude

    @property
    def enabled(self) -> 'DecofBoolean':
        return self._enabled


class NloLaserHeadMinifalc1:
    def __init__(self, client: Client, name: str) -> None:
        self.__client = client
        self.__name = name
        self._p_gain = DecofReal(client, name + ':p-gain')

    @property
    def p_gain(self) -> 'DecofReal':
        return self._p_gain


class NloLaserHeadWindow1:
    def __init__(self, client: Client, name: str) -> None:
        self.__client = client
        self.__name = name
        self._input_channel = DecofInteger(client, name + ':input-channel')
        self._calibration = NloLaserHeadWindowCalibration1(client, name + ':calibration')
        self._threshold = DecofReal(client, name + ':threshold')
        self._level_hysteresis = DecofReal(client, name + ':level-hysteresis')

    @property
    def input_channel(self) -> 'DecofInteger':
        return self._input_channel

    @property
    def calibration(self) -> 'NloLaserHeadWindowCalibration1':
        return self._calibration

    @property
    def threshold(self) -> 'DecofReal':
        return self._threshold

    @property
    def level_hysteresis(self) -> 'DecofReal':
        return self._level_hysteresis


class NloLaserHeadWindowCalibration1:
    def __init__(self, client: Client, name: str) -> None:
        self.__client = client
        self.__name = name


class NloLaserHeadLocalOscillatorShg1:
    def __init__(self, client: Client, name: str) -> None:
        self.__client = client
        self.__name = name
        self._coupled_modulation = DecofBoolean(client, name + ':coupled-modulation')
        self._amplitude = DecofReal(client, name + ':amplitude')
        self._use_external_oscillator = DecofBoolean(client, name + ':use-external-oscillator')
        self._enabled = DecofBoolean(client, name + ':enabled')
        self._use_fast_oscillator = DecofBoolean(client, name + ':use-fast-oscillator')
        self._phase_shift = DecofReal(client, name + ':phase-shift')
        self._attenuation_raw = DecofInteger(client, name + ':attenuation-raw')

    @property
    def coupled_modulation(self) -> 'DecofBoolean':
        return self._coupled_modulation

    @property
    def amplitude(self) -> 'DecofReal':
        return self._amplitude

    @property
    def use_external_oscillator(self) -> 'DecofBoolean':
        return self._use_external_oscillator

    @property
    def enabled(self) -> 'DecofBoolean':
        return self._enabled

    @property
    def use_fast_oscillator(self) -> 'DecofBoolean':
        return self._use_fast_oscillator

    @property
    def phase_shift(self) -> 'DecofReal':
        return self._phase_shift

    @property
    def attenuation_raw(self) -> 'DecofInteger':
        return self._attenuation_raw


class UvCavity:
    def __init__(self, client: Client, name: str) -> None:
        self.__client = client
        self.__name = name
        self._pc = PiezoDrv1(client, name + ':pc')
        self._tc = TcChannel1(client, name + ':tc')

    @property
    def pc(self) -> 'PiezoDrv1':
        return self._pc

    @property
    def tc(self) -> 'TcChannel1':
        return self._tc


class PiezoDrv1:
    def __init__(self, client: Client, name: str) -> None:
        self.__client = client
        self.__name = name
        self._status = DecofInteger(client, name + ':status')
        self._feedforward_master = DecofInteger(client, name + ':feedforward-master')
        self._feedforward_factor = DecofReal(client, name + ':feedforward-factor')
        self._external_input = ExtInput1(client, name + ':external-input')
        self._voltage_min = DecofReal(client, name + ':voltage-min')
        self._status_txt = DecofString(client, name + ':status-txt')
        self._feedforward_enabled = DecofBoolean(client, name + ':feedforward-enabled')
        self._voltage_set_dithering = DecofBoolean(client, name + ':voltage-set-dithering')
        self._voltage_max = DecofReal(client, name + ':voltage-max')
        self._enabled = DecofBoolean(client, name + ':enabled')
        self._voltage_set = DecofReal(client, name + ':voltage-set')
        self._output_filter = OutputFilter1(client, name + ':output-filter')
        self._heatsink_temp = DecofReal(client, name + ':heatsink-temp')
        self._voltage_act = DecofReal(client, name + ':voltage-act')
        self._path = DecofString(client, name + ':path')

    @property
    def status(self) -> 'DecofInteger':
        return self._status

    @property
    def feedforward_master(self) -> 'DecofInteger':
        return self._feedforward_master

    @property
    def feedforward_factor(self) -> 'DecofReal':
        return self._feedforward_factor

    @property
    def external_input(self) -> 'ExtInput1':
        return self._external_input

    @property
    def voltage_min(self) -> 'DecofReal':
        return self._voltage_min

    @property
    def status_txt(self) -> 'DecofString':
        return self._status_txt

    @property
    def feedforward_enabled(self) -> 'DecofBoolean':
        return self._feedforward_enabled

    @property
    def voltage_set_dithering(self) -> 'DecofBoolean':
        return self._voltage_set_dithering

    @property
    def voltage_max(self) -> 'DecofReal':
        return self._voltage_max

    @property
    def enabled(self) -> 'DecofBoolean':
        return self._enabled

    @property
    def voltage_set(self) -> 'DecofReal':
        return self._voltage_set

    @property
    def output_filter(self) -> 'OutputFilter1':
        return self._output_filter

    @property
    def heatsink_temp(self) -> 'DecofReal':
        return self._heatsink_temp

    @property
    def voltage_act(self) -> 'DecofReal':
        return self._voltage_act

    @property
    def path(self) -> 'DecofString':
        return self._path


class OutputFilter1:
    def __init__(self, client: Client, name: str) -> None:
        self.__client = client
        self.__name = name
        self._slew_rate_enabled = DecofBoolean(client, name + ':slew-rate-enabled')
        self._slew_rate = DecofReal(client, name + ':slew-rate')
        self._slew_rate_limited = DecofBoolean(client, name + ':slew-rate-limited')

    @property
    def slew_rate_enabled(self) -> 'DecofBoolean':
        return self._slew_rate_enabled

    @property
    def slew_rate(self) -> 'DecofReal':
        return self._slew_rate

    @property
    def slew_rate_limited(self) -> 'DecofBoolean':
        return self._slew_rate_limited


class UvCrystal:
    def __init__(self, client: Client, name: str) -> None:
        self.__client = client
        self.__name = name
        self._optics_shifters = NloLaserHeadUvCrystalSpots(client, name + ':optics-shifters')
        self._tc = TcChannel1(client, name + ':tc')

    @property
    def optics_shifters(self) -> 'NloLaserHeadUvCrystalSpots':
        return self._optics_shifters

    @property
    def tc(self) -> 'TcChannel1':
        return self._tc


class NloLaserHeadUvCrystalSpots:
    def __init__(self, client: Client, name: str) -> None:
        self.__client = client
        self.__name = name
        self._current_spot = DecofInteger(client, name + ':current-spot')
        self._remaining_spots = DecofInteger(client, name + ':remaining-spots')

    @property
    def current_spot(self) -> 'DecofInteger':
        return self._current_spot

    @property
    def remaining_spots(self) -> 'DecofInteger':
        return self._remaining_spots


class Dpss1:
    def __init__(self, client: Client, name: str) -> None:
        self.__client = client
        self.__name = name
        self._tc_status_txt = DecofString(client, name + ':tc-status-txt')
        self._tc_status = DecofInteger(client, name + ':tc-status')
        self._power_act = DecofReal(client, name + ':power-act')
        self._status = DecofInteger(client, name + ':status')
        self._power_max = DecofReal(client, name + ':power-max')
        self._error_txt = DecofString(client, name + ':error-txt')
        self._power_margin = DecofReal(client, name + ':power-margin')
        self._operation_time = DecofReal(client, name + ':operation-time')
        self._current_act = DecofReal(client, name + ':current-act')
        self._power_set = DecofReal(client, name + ':power-set')
        self._error_code = DecofInteger(client, name + ':error-code')
        self._current_max = DecofReal(client, name + ':current-max')
        self._enabled = DecofBoolean(client, name + ':enabled')
        self._status_txt = DecofString(client, name + ':status-txt')

    @property
    def tc_status_txt(self) -> 'DecofString':
        return self._tc_status_txt

    @property
    def tc_status(self) -> 'DecofInteger':
        return self._tc_status

    @property
    def power_act(self) -> 'DecofReal':
        return self._power_act

    @property
    def status(self) -> 'DecofInteger':
        return self._status

    @property
    def power_max(self) -> 'DecofReal':
        return self._power_max

    @property
    def error_txt(self) -> 'DecofString':
        return self._error_txt

    @property
    def power_margin(self) -> 'DecofReal':
        return self._power_margin

    @property
    def operation_time(self) -> 'DecofReal':
        return self._operation_time

    @property
    def current_act(self) -> 'DecofReal':
        return self._current_act

    @property
    def power_set(self) -> 'DecofReal':
        return self._power_set

    @property
    def error_code(self) -> 'DecofInteger':
        return self._error_code

    @property
    def current_max(self) -> 'DecofReal':
        return self._current_max

    @property
    def enabled(self) -> 'DecofBoolean':
        return self._enabled

    @property
    def status_txt(self) -> 'DecofString':
        return self._status_txt


class UvStatusParameters:
    def __init__(self, client: Client, name: str) -> None:
        self.__client = client
        self.__name = name
        self._baseplate_temperature_limit = DecofReal(client, name + ':baseplate-temperature-limit')
        self._cavity_lock_settle_time = DecofInteger(client, name + ':cavity-lock-settle-time')
        self._settle_down_delay = DecofInteger(client, name + ':settle-down-delay')
        self._temperature_settle_time = DecofInteger(client, name + ':temperature-settle-time')
        self._cavity_scan_duration = DecofInteger(client, name + ':cavity-scan-duration')
        self._degradation_detection_measurement_interval = DecofInteger(client, name + ':degradation-detection-measurement-interval')
        self._operational_pump_power = DecofReal(client, name + ':operational-pump-power')
        self._degradation_detection_slope_threshold = DecofReal(client, name + ':degradation-detection-slope-threshold')
        self._power_output_relative_error_max = DecofReal(client, name + ':power-output-relative-error-max')
        self._power_margin_threshold = DecofReal(client, name + ':power-margin-threshold')
        self._cavity_lock_tolerance_factor = DecofInteger(client, name + ':cavity-lock-tolerance-factor')
        self._power_output_relative_deviation_max = DecofReal(client, name + ':power-output-relative-deviation-max')
        self._power_stabilization_strategy = DecofInteger(client, name + ':power-stabilization-strategy')
        self._pump_lock_settle_time = DecofInteger(client, name + ':pump-lock-settle-time')
        self._power_lock_settle_time = DecofInteger(client, name + ':power-lock-settle-time')
        self._power_stabilization_level_low_factor = DecofReal(client, name + ':power-stabilization-level-low-factor')
        self._power_margin_tolerance_time = DecofInteger(client, name + ':power-margin-tolerance-time')
        self._degradation_detection_number_of_measurements = DecofInteger(client, name + ':degradation-detection-number-of-measurements')

    @property
    def baseplate_temperature_limit(self) -> 'DecofReal':
        return self._baseplate_temperature_limit

    @property
    def cavity_lock_settle_time(self) -> 'DecofInteger':
        return self._cavity_lock_settle_time

    @property
    def settle_down_delay(self) -> 'DecofInteger':
        return self._settle_down_delay

    @property
    def temperature_settle_time(self) -> 'DecofInteger':
        return self._temperature_settle_time

    @property
    def cavity_scan_duration(self) -> 'DecofInteger':
        return self._cavity_scan_duration

    @property
    def degradation_detection_measurement_interval(self) -> 'DecofInteger':
        return self._degradation_detection_measurement_interval

    @property
    def operational_pump_power(self) -> 'DecofReal':
        return self._operational_pump_power

    @property
    def degradation_detection_slope_threshold(self) -> 'DecofReal':
        return self._degradation_detection_slope_threshold

    @property
    def power_output_relative_error_max(self) -> 'DecofReal':
        return self._power_output_relative_error_max

    @property
    def power_margin_threshold(self) -> 'DecofReal':
        return self._power_margin_threshold

    @property
    def cavity_lock_tolerance_factor(self) -> 'DecofInteger':
        return self._cavity_lock_tolerance_factor

    @property
    def power_output_relative_deviation_max(self) -> 'DecofReal':
        return self._power_output_relative_deviation_max

    @property
    def power_stabilization_strategy(self) -> 'DecofInteger':
        return self._power_stabilization_strategy

    @property
    def pump_lock_settle_time(self) -> 'DecofInteger':
        return self._pump_lock_settle_time

    @property
    def power_lock_settle_time(self) -> 'DecofInteger':
        return self._power_lock_settle_time

    @property
    def power_stabilization_level_low_factor(self) -> 'DecofReal':
        return self._power_stabilization_level_low_factor

    @property
    def power_margin_tolerance_time(self) -> 'DecofInteger':
        return self._power_margin_tolerance_time

    @property
    def degradation_detection_number_of_measurements(self) -> 'DecofInteger':
        return self._degradation_detection_number_of_measurements


class NloLaserHeadUvServos:
    def __init__(self, client: Client, name: str) -> None:
        self.__client = client
        self.__name = name
        self._hwp = NloLaserHeadServoPwm1(client, name + ':hwp')
        self._comp_hor = NloLaserHeadServoPwm1(client, name + ':comp-hor')
        self._cryst = NloLaserHeadServoPwm1(client, name + ':cryst')
        self._outcpl = NloLaserHeadServoPwm1(client, name + ':outcpl')
        self._shg2_vert = NloLaserHeadServoPwm1(client, name + ':shg2-vert')
        self._shg2_hor = NloLaserHeadServoPwm1(client, name + ':shg2-hor')
        self._shg1_vert = NloLaserHeadServoPwm1(client, name + ':shg1-vert')
        self._lens = NloLaserHeadServoPwm1(client, name + ':lens')
        self._comp_vert = NloLaserHeadServoPwm1(client, name + ':comp-vert')
        self._shg1_hor = NloLaserHeadServoPwm1(client, name + ':shg1-hor')

    @property
    def hwp(self) -> 'NloLaserHeadServoPwm1':
        return self._hwp

    @property
    def comp_hor(self) -> 'NloLaserHeadServoPwm1':
        return self._comp_hor

    @property
    def cryst(self) -> 'NloLaserHeadServoPwm1':
        return self._cryst

    @property
    def outcpl(self) -> 'NloLaserHeadServoPwm1':
        return self._outcpl

    @property
    def shg2_vert(self) -> 'NloLaserHeadServoPwm1':
        return self._shg2_vert

    @property
    def shg2_hor(self) -> 'NloLaserHeadServoPwm1':
        return self._shg2_hor

    @property
    def shg1_vert(self) -> 'NloLaserHeadServoPwm1':
        return self._shg1_vert

    @property
    def lens(self) -> 'NloLaserHeadServoPwm1':
        return self._lens

    @property
    def comp_vert(self) -> 'NloLaserHeadServoPwm1':
        return self._comp_vert

    @property
    def shg1_hor(self) -> 'NloLaserHeadServoPwm1':
        return self._shg1_hor


class NloLaserHeadServoPwm1:
    def __init__(self, client: Client, name: str) -> None:
        self.__client = client
        self.__name = name
        self._value = DecofInteger(client, name + ':value')
        self._enabled = DecofBoolean(client, name + ':enabled')
        self._display_name = DecofString(client, name + ':display-name')

    @property
    def value(self) -> 'DecofInteger':
        return self._value

    @property
    def enabled(self) -> 'DecofBoolean':
        return self._enabled

    @property
    def display_name(self) -> 'DecofString':
        return self._display_name


class UvShgPowerOptimization:
    def __init__(self, client: Client, name: str) -> None:
        self.__client = client
        self.__name = name
        self._progress_data = DecofBinary(client, name + ':progress-data')
        self._cavity = NloLaserHeadStage1(client, name + ':cavity')
        self._ongoing = DecofBoolean(client, name + ':ongoing')
        self._abort = DecofBoolean(client, name + ':abort')
        self._status = DecofInteger(client, name + ':status')
        self._status_string = DecofString(client, name + ':status-string')

    @property
    def progress_data(self) -> 'DecofBinary':
        return self._progress_data

    @property
    def cavity(self) -> 'NloLaserHeadStage1':
        return self._cavity

    @property
    def ongoing(self) -> 'DecofBoolean':
        return self._ongoing

    @property
    def abort(self) -> 'DecofBoolean':
        return self._abort

    @property
    def status(self) -> 'DecofInteger':
        return self._status

    @property
    def status_string(self) -> 'DecofString':
        return self._status_string


class NloLaserHeadStage1:
    def __init__(self, client: Client, name: str) -> None:
        self.__client = client
        self.__name = name
        self._optimization_in_progress = DecofBoolean(client, name + ':optimization-in-progress')
        self._input = NloLaserHeadOptInput1(client, name + ':input')
        self._progress = DecofInteger(client, name + ':progress')
        self._autosave_actuator_values = DecofBoolean(client, name + ':autosave-actuator-values')
        self._regress_tolerance = DecofInteger(client, name + ':regress-tolerance')
        self._restore_on_abort = DecofBoolean(client, name + ':restore-on-abort')
        self._restore_on_regress = DecofBoolean(client, name + ':restore-on-regress')

    @property
    def optimization_in_progress(self) -> 'DecofBoolean':
        return self._optimization_in_progress

    @property
    def input(self) -> 'NloLaserHeadOptInput1':
        return self._input

    @property
    def progress(self) -> 'DecofInteger':
        return self._progress

    @property
    def autosave_actuator_values(self) -> 'DecofBoolean':
        return self._autosave_actuator_values

    @property
    def regress_tolerance(self) -> 'DecofInteger':
        return self._regress_tolerance

    @property
    def restore_on_abort(self) -> 'DecofBoolean':
        return self._restore_on_abort

    @property
    def restore_on_regress(self) -> 'DecofBoolean':
        return self._restore_on_regress


class NloLaserHeadOptInput1:
    def __init__(self, client: Client, name: str) -> None:
        self.__client = client
        self.__name = name
        self._value_calibrated = DecofReal(client, name + ':value-calibrated')

    @property
    def value_calibrated(self) -> 'DecofReal':
        return self._value_calibrated


class NloLaserHeadUvPhotoDiodes:
    def __init__(self, client: Client, name: str) -> None:
        self.__client = client
        self.__name = name
        self._pdh_rf = NloLaserHeadNloPdhPhotodiode1(client, name + ':pdh-rf')
        self._shg = NloLaserHeadNloPhotodiode1(client, name + ':shg')
        self._pdh_dc = NloLaserHeadNloDigilockPhotodiode1(client, name + ':pdh-dc')

    @property
    def pdh_rf(self) -> 'NloLaserHeadNloPdhPhotodiode1':
        return self._pdh_rf

    @property
    def shg(self) -> 'NloLaserHeadNloPhotodiode1':
        return self._shg

    @property
    def pdh_dc(self) -> 'NloLaserHeadNloDigilockPhotodiode1':
        return self._pdh_dc


class NloLaserHeadNloPdhPhotodiode1:
    def __init__(self, client: Client, name: str) -> None:
        self.__client = client
        self.__name = name
        self._photodiode = DecofReal(client, name + ':photodiode')
        self._gain = DecofReal(client, name + ':gain')

    @property
    def photodiode(self) -> 'DecofReal':
        return self._photodiode

    @property
    def gain(self) -> 'DecofReal':
        return self._gain


class NloLaserHeadNloPhotodiode1:
    def __init__(self, client: Client, name: str) -> None:
        self.__client = client
        self.__name = name
        self._cal_factor = DecofReal(client, name + ':cal-factor')
        self._photodiode = DecofReal(client, name + ':photodiode')
        self._power = DecofReal(client, name + ':power')
        self._cal_offset = DecofReal(client, name + ':cal-offset')

    @property
    def cal_factor(self) -> 'DecofReal':
        return self._cal_factor

    @property
    def photodiode(self) -> 'DecofReal':
        return self._photodiode

    @property
    def power(self) -> 'DecofReal':
        return self._power

    @property
    def cal_offset(self) -> 'DecofReal':
        return self._cal_offset


class NloLaserHeadNloDigilockPhotodiode1:
    def __init__(self, client: Client, name: str) -> None:
        self.__client = client
        self.__name = name
        self._photodiode = DecofReal(client, name + ':photodiode')
        self._cal_offset = DecofReal(client, name + ':cal-offset')

    @property
    def photodiode(self) -> 'DecofReal':
        return self._photodiode

    @property
    def cal_offset(self) -> 'DecofReal':
        return self._cal_offset


class NloLaserHeadSiggen1:
    def __init__(self, client: Client, name: str) -> None:
        self.__client = client
        self.__name = name
        self._frequency = DecofReal(client, name + ':frequency')
        self._offset = DecofReal(client, name + ':offset')
        self._amplitude = DecofReal(client, name + ':amplitude')
        self._enabled = DecofBoolean(client, name + ':enabled')

    @property
    def frequency(self) -> 'DecofReal':
        return self._frequency

    @property
    def offset(self) -> 'DecofReal':
        return self._offset

    @property
    def amplitude(self) -> 'DecofReal':
        return self._amplitude

    @property
    def enabled(self) -> 'DecofBoolean':
        return self._enabled


class UvShgPowerStabilization:
    def __init__(self, client: Client, name: str) -> None:
        self.__client = client
        self.__name = name
        self._update_strategy = DecofInteger(client, name + ':update-strategy')
        self._gain = PwrStabGain1(client, name + ':gain')
        self._power_min = DecofReal(client, name + ':power-min')
        self._power_set = DecofReal(client, name + ':power-set')
        self._power_max = DecofReal(client, name + ':power-max')
        self._state = DecofInteger(client, name + ':state')
        self._enabled = DecofBoolean(client, name + ':enabled')
        self._power_act = DecofReal(client, name + ':power-act')

    @property
    def update_strategy(self) -> 'DecofInteger':
        return self._update_strategy

    @property
    def gain(self) -> 'PwrStabGain1':
        return self._gain

    @property
    def power_min(self) -> 'DecofReal':
        return self._power_min

    @property
    def power_set(self) -> 'DecofReal':
        return self._power_set

    @property
    def power_max(self) -> 'DecofReal':
        return self._power_max

    @property
    def state(self) -> 'DecofInteger':
        return self._state

    @property
    def enabled(self) -> 'DecofBoolean':
        return self._enabled

    @property
    def power_act(self) -> 'DecofReal':
        return self._power_act


class PwrStabGain1:
    def __init__(self, client: Client, name: str) -> None:
        self.__client = client
        self.__name = name
        self._all = DecofReal(client, name + ':all')
        self._d = DecofReal(client, name + ':d')
        self._i = DecofReal(client, name + ':i')
        self._p = DecofReal(client, name + ':p')

    @property
    def all(self) -> 'DecofReal':
        return self._all

    @property
    def d(self) -> 'DecofReal':
        return self._d

    @property
    def i(self) -> 'DecofReal':
        return self._i

    @property
    def p(self) -> 'DecofReal':
        return self._p


class NloLaserHeadScopeT1:
    def __init__(self, client: Client, name: str) -> None:
        self.__client = client
        self.__name = name
        self._timescale = DecofReal(client, name + ':timescale')
        self._data = DecofBinary(client, name + ':data')
        self._channel2 = NloLaserHeadScopeChannelT1(client, name + ':channel2')
        self._channel1 = NloLaserHeadScopeChannelT1(client, name + ':channel1')
        self._channelx = NloLaserHeadScopeXAxisT1(client, name + ':channelx')
        self._update_rate = DecofInteger(client, name + ':update-rate')
        self._variant = DecofInteger(client, name + ':variant')

    @property
    def timescale(self) -> 'DecofReal':
        return self._timescale

    @property
    def data(self) -> 'DecofBinary':
        return self._data

    @property
    def channel2(self) -> 'NloLaserHeadScopeChannelT1':
        return self._channel2

    @property
    def channel1(self) -> 'NloLaserHeadScopeChannelT1':
        return self._channel1

    @property
    def channelx(self) -> 'NloLaserHeadScopeXAxisT1':
        return self._channelx

    @property
    def update_rate(self) -> 'DecofInteger':
        return self._update_rate

    @property
    def variant(self) -> 'DecofInteger':
        return self._variant


class NloLaserHeadScopeChannelT1:
    def __init__(self, client: Client, name: str) -> None:
        self.__client = client
        self.__name = name
        self._unit = DecofString(client, name + ':unit')
        self._signal = DecofInteger(client, name + ':signal')
        self._name = DecofString(client, name + ':name')
        self._enabled = DecofBoolean(client, name + ':enabled')

    @property
    def unit(self) -> 'DecofString':
        return self._unit

    @property
    def signal(self) -> 'DecofInteger':
        return self._signal

    @property
    def name(self) -> 'DecofString':
        return self._name

    @property
    def enabled(self) -> 'DecofBoolean':
        return self._enabled


class NloLaserHeadScopeXAxisT1:
    def __init__(self, client: Client, name: str) -> None:
        self.__client = client
        self.__name = name
        self._unit = DecofString(client, name + ':unit')
        self._name = DecofString(client, name + ':name')
        self._spectrum_range = DecofReal(client, name + ':spectrum-range')
        self._spectrum_omit_dc = DecofBoolean(client, name + ':spectrum-omit-dc')
        self._scope_timescale = DecofReal(client, name + ':scope-timescale')
        self._xy_signal = DecofInteger(client, name + ':xy-signal')

    @property
    def unit(self) -> 'DecofString':
        return self._unit

    @property
    def name(self) -> 'DecofString':
        return self._name

    @property
    def spectrum_range(self) -> 'DecofReal':
        return self._spectrum_range

    @property
    def spectrum_omit_dc(self) -> 'DecofBoolean':
        return self._spectrum_omit_dc

    @property
    def scope_timescale(self) -> 'DecofReal':
        return self._scope_timescale

    @property
    def xy_signal(self) -> 'DecofInteger':
        return self._xy_signal


class Recorder:
    def __init__(self, client: Client, name: str) -> None:
        self.__client = client
        self.__name = name
        self._recording_time = MutableDecofReal(client, name + ':recording-time')
        self._data = RecorderData(client, name + ':data')
        self._sampling_interval = DecofReal(client, name + ':sampling-interval')
        self._state = DecofInteger(client, name + ':state')
        self._state_txt = DecofString(client, name + ':state-txt')
        self._sample_count_set = MutableDecofInteger(client, name + ':sample-count-set')
        self._signals = RecorderInputs(client, name + ':signals')
        self._sample_count = DecofInteger(client, name + ':sample-count')

    @property
    def recording_time(self) -> 'MutableDecofReal':
        return self._recording_time

    @property
    def data(self) -> 'RecorderData':
        return self._data

    @property
    def sampling_interval(self) -> 'DecofReal':
        return self._sampling_interval

    @property
    def state(self) -> 'DecofInteger':
        return self._state

    @property
    def state_txt(self) -> 'DecofString':
        return self._state_txt

    @property
    def sample_count_set(self) -> 'MutableDecofInteger':
        return self._sample_count_set

    @property
    def signals(self) -> 'RecorderInputs':
        return self._signals

    @property
    def sample_count(self) -> 'DecofInteger':
        return self._sample_count


class RecorderData:
    def __init__(self, client: Client, name: str) -> None:
        self.__client = client
        self.__name = name
        self._zoom_amplitude = MutableDecofReal(client, name + ':zoom-amplitude')
        self._recorded_sample_count = DecofInteger(client, name + ':recorded-sample-count')
        self._channel2 = RecorderChannel(client, name + ':channel2')
        self._channel1 = RecorderChannel(client, name + ':channel1')
        self._channelx = RecorderChannel(client, name + ':channelx')
        self._zoom_offset = MutableDecofReal(client, name + ':zoom-offset')
        self._zoom_data = DecofBinary(client, name + ':zoom-data')
        self._last_valid_sample = DecofInteger(client, name + ':last-valid-sample')

    @property
    def zoom_amplitude(self) -> 'MutableDecofReal':
        return self._zoom_amplitude

    @property
    def recorded_sample_count(self) -> 'DecofInteger':
        return self._recorded_sample_count

    @property
    def channel2(self) -> 'RecorderChannel':
        return self._channel2

    @property
    def channel1(self) -> 'RecorderChannel':
        return self._channel1

    @property
    def channelx(self) -> 'RecorderChannel':
        return self._channelx

    @property
    def zoom_offset(self) -> 'MutableDecofReal':
        return self._zoom_offset

    @property
    def zoom_data(self) -> 'DecofBinary':
        return self._zoom_data

    @property
    def last_valid_sample(self) -> 'DecofInteger':
        return self._last_valid_sample

    def get_data(self, start_index: int, count: int) -> bytes:
        assert isinstance(start_index, int), "expected type 'int' for parameter 'start_index', got '{}'".format(type(start_index))
        assert isinstance(count, int), "expected type 'int' for parameter 'count', got '{}'".format(type(count))
        return self.__client.exec(self.__name + ':get-data', start_index, count, input_stream=None, output_type=None, return_type=bytes)

    def show_data(self, start_index: int, count: int) -> None:
        assert isinstance(start_index, int), "expected type 'int' for parameter 'start_index', got '{}'".format(type(start_index))
        assert isinstance(count, int), "expected type 'int' for parameter 'count', got '{}'".format(type(count))
        self.__client.exec(self.__name + ':show-data', start_index, count, input_stream=None, output_type=None, return_type=None)

    def zoom_out(self) -> None:
        self.__client.exec(self.__name + ':zoom-out', input_stream=None, output_type=None, return_type=None)


class RecorderChannel:
    def __init__(self, client: Client, name: str) -> None:
        self.__client = client
        self.__name = name
        self._unit = DecofString(client, name + ':unit')
        self._signal = DecofInteger(client, name + ':signal')
        self._name = DecofString(client, name + ':name')

    @property
    def unit(self) -> 'DecofString':
        return self._unit

    @property
    def signal(self) -> 'DecofInteger':
        return self._signal

    @property
    def name(self) -> 'DecofString':
        return self._name


class RecorderInputs:
    def __init__(self, client: Client, name: str) -> None:
        self.__client = client
        self.__name = name
        self._channelx = MutableDecofInteger(client, name + ':channelx')
        self._channel2 = MutableDecofInteger(client, name + ':channel2')
        self._channel1 = MutableDecofInteger(client, name + ':channel1')

    @property
    def channelx(self) -> 'MutableDecofInteger':
        return self._channelx

    @property
    def channel2(self) -> 'MutableDecofInteger':
        return self._channel2

    @property
    def channel1(self) -> 'MutableDecofInteger':
        return self._channel1


class PwrStab:
    def __init__(self, client: Client, name: str) -> None:
        self.__client = client
        self.__name = name
        self._hold_output_on_unlock = MutableDecofBoolean(client, name + ':hold-output-on-unlock')
        self._gain = PwrStabGain2(client, name + ':gain')
        self._input_channel_value_act = DecofReal(client, name + ':input-channel-value-act')
        self._feedforward_enabled = MutableDecofBoolean(client, name + ':feedforward-enabled')
        self._sign = MutableDecofBoolean(client, name + ':sign')
        self._output_channel = DecofInteger(client, name + ':output-channel')
        self._feedforward_factor = MutableDecofReal(client, name + ':feedforward-factor')
        self._window = PwrStabWindow(client, name + ':window')
        self._setpoint = MutableDecofReal(client, name + ':setpoint')
        self._state = DecofInteger(client, name + ':state')
        self._enabled = MutableDecofBoolean(client, name + ':enabled')
        self._input_channel = MutableDecofInteger(client, name + ':input-channel')

    @property
    def hold_output_on_unlock(self) -> 'MutableDecofBoolean':
        return self._hold_output_on_unlock

    @property
    def gain(self) -> 'PwrStabGain2':
        return self._gain

    @property
    def input_channel_value_act(self) -> 'DecofReal':
        return self._input_channel_value_act

    @property
    def feedforward_enabled(self) -> 'MutableDecofBoolean':
        return self._feedforward_enabled

    @property
    def sign(self) -> 'MutableDecofBoolean':
        return self._sign

    @property
    def output_channel(self) -> 'DecofInteger':
        return self._output_channel

    @property
    def feedforward_factor(self) -> 'MutableDecofReal':
        return self._feedforward_factor

    @property
    def window(self) -> 'PwrStabWindow':
        return self._window

    @property
    def setpoint(self) -> 'MutableDecofReal':
        return self._setpoint

    @property
    def state(self) -> 'DecofInteger':
        return self._state

    @property
    def enabled(self) -> 'MutableDecofBoolean':
        return self._enabled

    @property
    def input_channel(self) -> 'MutableDecofInteger':
        return self._input_channel


class PwrStabGain2:
    def __init__(self, client: Client, name: str) -> None:
        self.__client = client
        self.__name = name
        self._all = MutableDecofReal(client, name + ':all')
        self._d = MutableDecofReal(client, name + ':d')
        self._i = MutableDecofReal(client, name + ':i')
        self._p = MutableDecofReal(client, name + ':p')

    @property
    def all(self) -> 'MutableDecofReal':
        return self._all

    @property
    def d(self) -> 'MutableDecofReal':
        return self._d

    @property
    def i(self) -> 'MutableDecofReal':
        return self._i

    @property
    def p(self) -> 'MutableDecofReal':
        return self._p


class PwrStabWindow:
    def __init__(self, client: Client, name: str) -> None:
        self.__client = client
        self.__name = name
        self._enabled = MutableDecofBoolean(client, name + ':enabled')
        self._level_hysteresis = MutableDecofReal(client, name + ':level-hysteresis')
        self._level_low = MutableDecofReal(client, name + ':level-low')

    @property
    def enabled(self) -> 'MutableDecofBoolean':
        return self._enabled

    @property
    def level_hysteresis(self) -> 'MutableDecofReal':
        return self._level_hysteresis

    @property
    def level_low(self) -> 'MutableDecofReal':
        return self._level_low


class LaserConfig:
    def __init__(self, client: Client, name: str) -> None:
        self.__client = client
        self.__name = name
        self._product_name = DecofString(client, name + ':product-name')
        self._caption = MutableDecofString(client, name + ':caption')
        self._date = DecofString(client, name + ':date')
        self._pristine = DecofBoolean(client, name + ':pristine')
        self._source = DecofString(client, name + ':source')

    @property
    def product_name(self) -> 'DecofString':
        return self._product_name

    @property
    def caption(self) -> 'MutableDecofString':
        return self._caption

    @property
    def date(self) -> 'DecofString':
        return self._date

    @property
    def pristine(self) -> 'DecofBoolean':
        return self._pristine

    @property
    def source(self) -> 'DecofString':
        return self._source

    def list(self) -> str:
        return self.__client.exec(self.__name + ':list', input_stream=None, output_type=None, return_type=str)

    def load(self, source: str) -> None:
        assert isinstance(source, str), "expected type 'str' for parameter 'source', got '{}'".format(type(source))
        self.__client.exec(self.__name + ':load', source, input_stream=None, output_type=None, return_type=None)

    def show(self) -> str:
        return self.__client.exec(self.__name + ':show', input_stream=None, output_type=str, return_type=None)

    def import_(self, stream_input: bytes) -> None:
        assert isinstance(stream_input, bytes), "expected type 'bytes' for parameter 'stream_input', got '{}'".format(type(stream_input))
        self.__client.exec(self.__name + ':import', input_stream=stream_input, output_type=None, return_type=None)

    def apply(self) -> bool:
        return self.__client.exec(self.__name + ':apply', input_stream=None, output_type=None, return_type=bool)

    def retrieve(self) -> None:
        self.__client.exec(self.__name + ':retrieve', input_stream=None, output_type=None, return_type=None)

    def save(self, destination: str) -> None:
        assert isinstance(destination, str), "expected type 'str' for parameter 'destination', got '{}'".format(type(destination))
        self.__client.exec(self.__name + ':save', destination, input_stream=None, output_type=None, return_type=None)

    def export(self) -> bytes:
        return self.__client.exec(self.__name + ':export', input_stream=None, output_type=bytes, return_type=None)


class CtlT:
    def __init__(self, client: Client, name: str) -> None:
        self.__client = client
        self.__name = name
        self._tuning_current_min = DecofReal(client, name + ':tuning-current-min')
        self._factory_settings = CtlFactory(client, name + ':factory-settings')
        self._wavelength_min = DecofReal(client, name + ':wavelength-min')
        self._state_txt = DecofString(client, name + ':state-txt')
        self._motor = CtlMotor(client, name + ':motor')
        self._wavelength_max = DecofReal(client, name + ':wavelength-max')
        self._head_temperature = DecofReal(client, name + ':head-temperature')
        self._power = CtlPower(client, name + ':power')
        self._fpga_fw_ver = DecofInteger(client, name + ':fpga-fw-ver')
        self._scan = CtlScanT(client, name + ':scan')
        self._mode_control = CtlModeControl(client, name + ':mode-control')
        self._wavelength_set = MutableDecofReal(client, name + ':wavelength-set')
        self._optimization = CtlOptimizationT(client, name + ':optimization')
        self._state = DecofInteger(client, name + ':state')
        self._wavelength_act = DecofReal(client, name + ':wavelength-act')
        self._remote_control = CtlRemoteControl(client, name + ':remote-control')
        self._tuning_power_min = DecofReal(client, name + ':tuning-power-min')

    @property
    def tuning_current_min(self) -> 'DecofReal':
        return self._tuning_current_min

    @property
    def factory_settings(self) -> 'CtlFactory':
        return self._factory_settings

    @property
    def wavelength_min(self) -> 'DecofReal':
        return self._wavelength_min

    @property
    def state_txt(self) -> 'DecofString':
        return self._state_txt

    @property
    def motor(self) -> 'CtlMotor':
        return self._motor

    @property
    def wavelength_max(self) -> 'DecofReal':
        return self._wavelength_max

    @property
    def head_temperature(self) -> 'DecofReal':
        return self._head_temperature

    @property
    def power(self) -> 'CtlPower':
        return self._power

    @property
    def fpga_fw_ver(self) -> 'DecofInteger':
        return self._fpga_fw_ver

    @property
    def scan(self) -> 'CtlScanT':
        return self._scan

    @property
    def mode_control(self) -> 'CtlModeControl':
        return self._mode_control

    @property
    def wavelength_set(self) -> 'MutableDecofReal':
        return self._wavelength_set

    @property
    def optimization(self) -> 'CtlOptimizationT':
        return self._optimization

    @property
    def state(self) -> 'DecofInteger':
        return self._state

    @property
    def wavelength_act(self) -> 'DecofReal':
        return self._wavelength_act

    @property
    def remote_control(self) -> 'CtlRemoteControl':
        return self._remote_control

    @property
    def tuning_power_min(self) -> 'DecofReal':
        return self._tuning_power_min


class CtlFactory:
    def __init__(self, client: Client, name: str) -> None:
        self.__client = client
        self.__name = name
        self._tuning_current_min = DecofReal(client, name + ':tuning-current-min')
        self._wavelength_min = DecofReal(client, name + ':wavelength-min')
        self._wavelength_max = DecofReal(client, name + ':wavelength-max')
        self._tuning_power_min = DecofReal(client, name + ':tuning-power-min')

    @property
    def tuning_current_min(self) -> 'DecofReal':
        return self._tuning_current_min

    @property
    def wavelength_min(self) -> 'DecofReal':
        return self._wavelength_min

    @property
    def wavelength_max(self) -> 'DecofReal':
        return self._wavelength_max

    @property
    def tuning_power_min(self) -> 'DecofReal':
        return self._tuning_power_min

    def apply(self) -> None:
        self.__client.exec(self.__name + ':apply', input_stream=None, output_type=None, return_type=None)


class CtlMotor:
    def __init__(self, client: Client, name: str) -> None:
        self.__client = client
        self.__name = name
        self._power_save_disabled = MutableDecofBoolean(client, name + ':power-save-disabled')
        self._position_hysteresis_fullstep = MutableDecofInteger(client, name + ':position-hysteresis-fullstep')
        self._position_accuracy_fullstep = MutableDecofInteger(client, name + ':position-accuracy-fullstep')
        self._position_accuracy_microstep = MutableDecofInteger(client, name + ':position-accuracy-microstep')
        self._position_hysteresis_microstep = MutableDecofInteger(client, name + ':position-hysteresis-microstep')

    @property
    def power_save_disabled(self) -> 'MutableDecofBoolean':
        return self._power_save_disabled

    @property
    def position_hysteresis_fullstep(self) -> 'MutableDecofInteger':
        return self._position_hysteresis_fullstep

    @property
    def position_accuracy_fullstep(self) -> 'MutableDecofInteger':
        return self._position_accuracy_fullstep

    @property
    def position_accuracy_microstep(self) -> 'MutableDecofInteger':
        return self._position_accuracy_microstep

    @property
    def position_hysteresis_microstep(self) -> 'MutableDecofInteger':
        return self._position_hysteresis_microstep


class CtlPower:
    def __init__(self, client: Client, name: str) -> None:
        self.__client = client
        self.__name = name
        self._power_act = DecofReal(client, name + ':power-act')

    @property
    def power_act(self) -> 'DecofReal':
        return self._power_act


class CtlScanT:
    def __init__(self, client: Client, name: str) -> None:
        self.__client = client
        self.__name = name
        self._remaining_time = DecofInteger(client, name + ':remaining-time')
        self._continuous_mode = MutableDecofBoolean(client, name + ':continuous-mode')
        self._progress = DecofInteger(client, name + ':progress')
        self._wavelength_begin = MutableDecofReal(client, name + ':wavelength-begin')
        self._microsteps = MutableDecofBoolean(client, name + ':microsteps')
        self._speed_max = DecofReal(client, name + ':speed-max')
        self._speed_min = DecofReal(client, name + ':speed-min')
        self._shape = MutableDecofInteger(client, name + ':shape')
        self._trigger = CtlTriggerT(client, name + ':trigger')
        self._wavelength_end = MutableDecofReal(client, name + ':wavelength-end')
        self._speed = MutableDecofReal(client, name + ':speed')

    @property
    def remaining_time(self) -> 'DecofInteger':
        return self._remaining_time

    @property
    def continuous_mode(self) -> 'MutableDecofBoolean':
        return self._continuous_mode

    @property
    def progress(self) -> 'DecofInteger':
        return self._progress

    @property
    def wavelength_begin(self) -> 'MutableDecofReal':
        return self._wavelength_begin

    @property
    def microsteps(self) -> 'MutableDecofBoolean':
        return self._microsteps

    @property
    def speed_max(self) -> 'DecofReal':
        return self._speed_max

    @property
    def speed_min(self) -> 'DecofReal':
        return self._speed_min

    @property
    def shape(self) -> 'MutableDecofInteger':
        return self._shape

    @property
    def trigger(self) -> 'CtlTriggerT':
        return self._trigger

    @property
    def wavelength_end(self) -> 'MutableDecofReal':
        return self._wavelength_end

    @property
    def speed(self) -> 'MutableDecofReal':
        return self._speed

    def start(self) -> None:
        self.__client.exec(self.__name + ':start', input_stream=None, output_type=None, return_type=None)

    def continue_(self) -> None:
        self.__client.exec(self.__name + ':continue', input_stream=None, output_type=None, return_type=None)

    def pause(self) -> None:
        self.__client.exec(self.__name + ':pause', input_stream=None, output_type=None, return_type=None)

    def stop(self) -> None:
        self.__client.exec(self.__name + ':stop', input_stream=None, output_type=None, return_type=None)


class CtlTriggerT:
    def __init__(self, client: Client, name: str) -> None:
        self.__client = client
        self.__name = name
        self._output_threshold = MutableDecofReal(client, name + ':output-threshold')
        self._input_channel = MutableDecofInteger(client, name + ':input-channel')
        self._output_enabled = MutableDecofBoolean(client, name + ':output-enabled')
        self._input_enabled = MutableDecofBoolean(client, name + ':input-enabled')

    @property
    def output_threshold(self) -> 'MutableDecofReal':
        return self._output_threshold

    @property
    def input_channel(self) -> 'MutableDecofInteger':
        return self._input_channel

    @property
    def output_enabled(self) -> 'MutableDecofBoolean':
        return self._output_enabled

    @property
    def input_enabled(self) -> 'MutableDecofBoolean':
        return self._input_enabled


class CtlModeControl:
    def __init__(self, client: Client, name: str) -> None:
        self.__client = client
        self.__name = name
        self._loop_enabled = MutableDecofBoolean(client, name + ':loop-enabled')

    @property
    def loop_enabled(self) -> 'MutableDecofBoolean':
        return self._loop_enabled


class CtlOptimizationT:
    def __init__(self, client: Client, name: str) -> None:
        self.__client = client
        self.__name = name
        self._progress = DecofInteger(client, name + ':progress')

    @property
    def progress(self) -> 'DecofInteger':
        return self._progress

    def smile(self) -> None:
        self.__client.exec(self.__name + ':smile', input_stream=None, output_type=None, return_type=None)

    def abort(self) -> None:
        self.__client.exec(self.__name + ':abort', input_stream=None, output_type=None, return_type=None)

    def flow(self) -> None:
        self.__client.exec(self.__name + ':flow', input_stream=None, output_type=None, return_type=None)


class CtlRemoteControl:
    def __init__(self, client: Client, name: str) -> None:
        self.__client = client
        self.__name = name
        self._signal = MutableDecofInteger(client, name + ':signal')
        self._enabled = MutableDecofBoolean(client, name + ':enabled')
        self._factor = MutableDecofReal(client, name + ':factor')
        self._speed = MutableDecofReal(client, name + ':speed')

    @property
    def signal(self) -> 'MutableDecofInteger':
        return self._signal

    @property
    def enabled(self) -> 'MutableDecofBoolean':
        return self._enabled

    @property
    def factor(self) -> 'MutableDecofReal':
        return self._factor

    @property
    def speed(self) -> 'MutableDecofReal':
        return self._speed


class LaserAmp:
    def __init__(self, client: Client, name: str) -> None:
        self.__client = client
        self.__name = name
        self._factory_settings = AmpFactory(client, name + ':factory-settings')
        self._serial_number = DecofString(client, name + ':serial-number')
        self._pd = AmpPd(client, name + ':pd')
        self._cc = Cc5000Drv(client, name + ':cc')
        self._ontime_txt = DecofString(client, name + ':ontime-txt')
        self._legacy = DecofBoolean(client, name + ':legacy')
        self._output_limits = AmpPower(client, name + ':output-limits')
        self._version = DecofString(client, name + ':version')
        self._type_ = DecofString(client, name + ':type')
        self._seedonly_check = AmpSeedonlyCheck(client, name + ':seedonly-check')
        self._ontime = DecofInteger(client, name + ':ontime')
        self._tc = TcChannel2(client, name + ':tc')
        self._seed_limits = AmpPower(client, name + ':seed-limits')

    @property
    def factory_settings(self) -> 'AmpFactory':
        return self._factory_settings

    @property
    def serial_number(self) -> 'DecofString':
        return self._serial_number

    @property
    def pd(self) -> 'AmpPd':
        return self._pd

    @property
    def cc(self) -> 'Cc5000Drv':
        return self._cc

    @property
    def ontime_txt(self) -> 'DecofString':
        return self._ontime_txt

    @property
    def legacy(self) -> 'DecofBoolean':
        return self._legacy

    @property
    def output_limits(self) -> 'AmpPower':
        return self._output_limits

    @property
    def version(self) -> 'DecofString':
        return self._version

    @property
    def type_(self) -> 'DecofString':
        return self._type_

    @property
    def seedonly_check(self) -> 'AmpSeedonlyCheck':
        return self._seedonly_check

    @property
    def ontime(self) -> 'DecofInteger':
        return self._ontime

    @property
    def tc(self) -> 'TcChannel2':
        return self._tc

    @property
    def seed_limits(self) -> 'AmpPower':
        return self._seed_limits

    def restore(self) -> None:
        self.__client.exec(self.__name + ':restore', input_stream=None, output_type=None, return_type=None)

    def store(self) -> None:
        self.__client.exec(self.__name + ':store', input_stream=None, output_type=None, return_type=None)


class AmpFactory:
    def __init__(self, client: Client, name: str) -> None:
        self.__client = client
        self.__name = name
        self._last_modified = DecofString(client, name + ':last-modified')
        self._output_limits = AmpFactoryPower(client, name + ':output-limits')
        self._modified = DecofBoolean(client, name + ':modified')
        self._pd = AmpPdFactorySettings(client, name + ':pd')
        self._cc = AmpFactoryCc(client, name + ':cc')
        self._seedonly_check = AmpFactorySeedonly(client, name + ':seedonly-check')
        self._seed_limits = AmpFactoryPower(client, name + ':seed-limits')
        self._power = MutableDecofReal(client, name + ':power')
        self._tc = TcFactorySettings(client, name + ':tc')
        self._wavelength = MutableDecofReal(client, name + ':wavelength')

    @property
    def last_modified(self) -> 'DecofString':
        return self._last_modified

    @property
    def output_limits(self) -> 'AmpFactoryPower':
        return self._output_limits

    @property
    def modified(self) -> 'DecofBoolean':
        return self._modified

    @property
    def pd(self) -> 'AmpPdFactorySettings':
        return self._pd

    @property
    def cc(self) -> 'AmpFactoryCc':
        return self._cc

    @property
    def seedonly_check(self) -> 'AmpFactorySeedonly':
        return self._seedonly_check

    @property
    def seed_limits(self) -> 'AmpFactoryPower':
        return self._seed_limits

    @property
    def power(self) -> 'MutableDecofReal':
        return self._power

    @property
    def tc(self) -> 'TcFactorySettings':
        return self._tc

    @property
    def wavelength(self) -> 'MutableDecofReal':
        return self._wavelength

    def apply(self) -> None:
        self.__client.exec(self.__name + ':apply', input_stream=None, output_type=None, return_type=None)

    def retrieve_now(self) -> None:
        self.__client.exec(self.__name + ':retrieve-now', input_stream=None, output_type=None, return_type=None)


class AmpFactoryPower:
    def __init__(self, client: Client, name: str) -> None:
        self.__client = client
        self.__name = name
        self._power_min = MutableDecofReal(client, name + ':power-min')
        self._power_max = MutableDecofReal(client, name + ':power-max')
        self._power_max_warning_delay = MutableDecofReal(client, name + ':power-max-warning-delay')
        self._power_max_shutdown_delay = MutableDecofReal(client, name + ':power-max-shutdown-delay')
        self._power_min_warning_delay = MutableDecofReal(client, name + ':power-min-warning-delay')
        self._power_min_shutdown_delay = MutableDecofReal(client, name + ':power-min-shutdown-delay')

    @property
    def power_min(self) -> 'MutableDecofReal':
        return self._power_min

    @property
    def power_max(self) -> 'MutableDecofReal':
        return self._power_max

    @property
    def power_max_warning_delay(self) -> 'MutableDecofReal':
        return self._power_max_warning_delay

    @property
    def power_max_shutdown_delay(self) -> 'MutableDecofReal':
        return self._power_max_shutdown_delay

    @property
    def power_min_warning_delay(self) -> 'MutableDecofReal':
        return self._power_min_warning_delay

    @property
    def power_min_shutdown_delay(self) -> 'MutableDecofReal':
        return self._power_min_shutdown_delay


class AmpPdFactorySettings:
    def __init__(self, client: Client, name: str) -> None:
        self.__client = client
        self.__name = name
        self._amp = PdCalFactorySettings(client, name + ':amp')
        self._seed = PdCalFactorySettings(client, name + ':seed')

    @property
    def amp(self) -> 'PdCalFactorySettings':
        return self._amp

    @property
    def seed(self) -> 'PdCalFactorySettings':
        return self._seed


class AmpFactoryCc:
    def __init__(self, client: Client, name: str) -> None:
        self.__client = client
        self.__name = name
        self._current_clip = MutableDecofReal(client, name + ':current-clip')
        self._current_clip_last_modified = DecofString(client, name + ':current-clip-last-modified')
        self._voltage_clip = MutableDecofReal(client, name + ':voltage-clip')
        self._current_set = MutableDecofReal(client, name + ':current-set')
        self._feedforward_factor = MutableDecofReal(client, name + ':feedforward-factor')
        self._current_clip_modified = DecofBoolean(client, name + ':current-clip-modified')

    @property
    def current_clip(self) -> 'MutableDecofReal':
        return self._current_clip

    @property
    def current_clip_last_modified(self) -> 'DecofString':
        return self._current_clip_last_modified

    @property
    def voltage_clip(self) -> 'MutableDecofReal':
        return self._voltage_clip

    @property
    def current_set(self) -> 'MutableDecofReal':
        return self._current_set

    @property
    def feedforward_factor(self) -> 'MutableDecofReal':
        return self._feedforward_factor

    @property
    def current_clip_modified(self) -> 'DecofBoolean':
        return self._current_clip_modified


class AmpFactorySeedonly:
    def __init__(self, client: Client, name: str) -> None:
        self.__client = client
        self.__name = name
        self._warning_delay = MutableDecofReal(client, name + ':warning-delay')
        self._shutdown_delay = MutableDecofReal(client, name + ':shutdown-delay')

    @property
    def warning_delay(self) -> 'MutableDecofReal':
        return self._warning_delay

    @property
    def shutdown_delay(self) -> 'MutableDecofReal':
        return self._shutdown_delay


class AmpPd:
    def __init__(self, client: Client, name: str) -> None:
        self.__client = client
        self.__name = name
        self._amp = PdCal(client, name + ':amp')
        self._seed = PdCal(client, name + ':seed')

    @property
    def amp(self) -> 'PdCal':
        return self._amp

    @property
    def seed(self) -> 'PdCal':
        return self._seed


class AmpPower:
    def __init__(self, client: Client, name: str) -> None:
        self.__client = client
        self.__name = name
        self._power_min = MutableDecofReal(client, name + ':power-min')
        self._status = DecofInteger(client, name + ':status')
        self._power_max = MutableDecofReal(client, name + ':power-max')
        self._power_max_warning_delay = MutableDecofReal(client, name + ':power-max-warning-delay')
        self._power_max_shutdown_delay = MutableDecofReal(client, name + ':power-max-shutdown-delay')
        self._power_min_warning_delay = MutableDecofReal(client, name + ':power-min-warning-delay')
        self._power = DecofReal(client, name + ':power')
        self._power_min_shutdown_delay = MutableDecofReal(client, name + ':power-min-shutdown-delay')
        self._status_txt = DecofString(client, name + ':status-txt')

    @property
    def power_min(self) -> 'MutableDecofReal':
        return self._power_min

    @property
    def status(self) -> 'DecofInteger':
        return self._status

    @property
    def power_max(self) -> 'MutableDecofReal':
        return self._power_max

    @property
    def power_max_warning_delay(self) -> 'MutableDecofReal':
        return self._power_max_warning_delay

    @property
    def power_max_shutdown_delay(self) -> 'MutableDecofReal':
        return self._power_max_shutdown_delay

    @property
    def power_min_warning_delay(self) -> 'MutableDecofReal':
        return self._power_min_warning_delay

    @property
    def power(self) -> 'DecofReal':
        return self._power

    @property
    def power_min_shutdown_delay(self) -> 'MutableDecofReal':
        return self._power_min_shutdown_delay

    @property
    def status_txt(self) -> 'DecofString':
        return self._status_txt


class AmpSeedonlyCheck:
    def __init__(self, client: Client, name: str) -> None:
        self.__client = client
        self.__name = name
        self._seed = DecofBoolean(client, name + ':seed')
        self._status = DecofInteger(client, name + ':status')
        self._shutdown_delay = MutableDecofReal(client, name + ':shutdown-delay')
        self._warning_delay = MutableDecofReal(client, name + ':warning-delay')
        self._pump = DecofBoolean(client, name + ':pump')
        self._status_txt = DecofString(client, name + ':status-txt')

    @property
    def seed(self) -> 'DecofBoolean':
        return self._seed

    @property
    def status(self) -> 'DecofInteger':
        return self._status

    @property
    def shutdown_delay(self) -> 'MutableDecofReal':
        return self._shutdown_delay

    @property
    def warning_delay(self) -> 'MutableDecofReal':
        return self._warning_delay

    @property
    def pump(self) -> 'DecofBoolean':
        return self._pump

    @property
    def status_txt(self) -> 'DecofString':
        return self._status_txt


class WideScan:
    def __init__(self, client: Client, name: str) -> None:
        self.__client = client
        self.__name = name
        self._scan_end = MutableDecofReal(client, name + ':scan-end')
        self._scan_begin = MutableDecofReal(client, name + ':scan-begin')
        self._duration = MutableDecofReal(client, name + ':duration')
        self._progress = DecofInteger(client, name + ':progress')
        self._offset = MutableDecofReal(client, name + ':offset')
        self._amplitude = MutableDecofReal(client, name + ':amplitude')
        self._state = DecofInteger(client, name + ':state')
        self._state_txt = DecofString(client, name + ':state-txt')
        self._output_channel = MutableDecofInteger(client, name + ':output-channel')
        self._remaining_time = DecofInteger(client, name + ':remaining-time')
        self._speed = MutableDecofReal(client, name + ':speed')

    @property
    def scan_end(self) -> 'MutableDecofReal':
        return self._scan_end

    @property
    def scan_begin(self) -> 'MutableDecofReal':
        return self._scan_begin

    @property
    def duration(self) -> 'MutableDecofReal':
        return self._duration

    @property
    def progress(self) -> 'DecofInteger':
        return self._progress

    @property
    def offset(self) -> 'MutableDecofReal':
        return self._offset

    @property
    def amplitude(self) -> 'MutableDecofReal':
        return self._amplitude

    @property
    def state(self) -> 'DecofInteger':
        return self._state

    @property
    def state_txt(self) -> 'DecofString':
        return self._state_txt

    @property
    def output_channel(self) -> 'MutableDecofInteger':
        return self._output_channel

    @property
    def remaining_time(self) -> 'DecofInteger':
        return self._remaining_time

    @property
    def speed(self) -> 'MutableDecofReal':
        return self._speed

    def start(self) -> None:
        self.__client.exec(self.__name + ':start', input_stream=None, output_type=None, return_type=None)

    def stop(self) -> None:
        self.__client.exec(self.__name + ':stop', input_stream=None, output_type=None, return_type=None)


class ScopeT:
    def __init__(self, client: Client, name: str) -> None:
        self.__client = client
        self.__name = name
        self._timescale = MutableDecofReal(client, name + ':timescale')
        self._data = DecofBinary(client, name + ':data')
        self._channel2 = ScopeChannelT(client, name + ':channel2')
        self._channel1 = ScopeChannelT(client, name + ':channel1')
        self._channelx = ScopeXAxisT(client, name + ':channelx')
        self._update_rate = MutableDecofInteger(client, name + ':update-rate')
        self._variant = MutableDecofInteger(client, name + ':variant')

    @property
    def timescale(self) -> 'MutableDecofReal':
        return self._timescale

    @property
    def data(self) -> 'DecofBinary':
        return self._data

    @property
    def channel2(self) -> 'ScopeChannelT':
        return self._channel2

    @property
    def channel1(self) -> 'ScopeChannelT':
        return self._channel1

    @property
    def channelx(self) -> 'ScopeXAxisT':
        return self._channelx

    @property
    def update_rate(self) -> 'MutableDecofInteger':
        return self._update_rate

    @property
    def variant(self) -> 'MutableDecofInteger':
        return self._variant


class ScopeChannelT:
    def __init__(self, client: Client, name: str) -> None:
        self.__client = client
        self.__name = name
        self._unit = DecofString(client, name + ':unit')
        self._signal = MutableDecofInteger(client, name + ':signal')
        self._name = DecofString(client, name + ':name')
        self._enabled = MutableDecofBoolean(client, name + ':enabled')

    @property
    def unit(self) -> 'DecofString':
        return self._unit

    @property
    def signal(self) -> 'MutableDecofInteger':
        return self._signal

    @property
    def name(self) -> 'DecofString':
        return self._name

    @property
    def enabled(self) -> 'MutableDecofBoolean':
        return self._enabled


class ScopeXAxisT:
    def __init__(self, client: Client, name: str) -> None:
        self.__client = client
        self.__name = name
        self._name = DecofString(client, name + ':name')
        self._spectrum_range = MutableDecofReal(client, name + ':spectrum-range')
        self._unit = DecofString(client, name + ':unit')
        self._spectrum_omit_dc = MutableDecofBoolean(client, name + ':spectrum-omit-dc')
        self._scope_timescale = MutableDecofReal(client, name + ':scope-timescale')
        self._xy_signal = MutableDecofInteger(client, name + ':xy-signal')

    @property
    def name(self) -> 'DecofString':
        return self._name

    @property
    def spectrum_range(self) -> 'MutableDecofReal':
        return self._spectrum_range

    @property
    def unit(self) -> 'DecofString':
        return self._unit

    @property
    def spectrum_omit_dc(self) -> 'MutableDecofBoolean':
        return self._spectrum_omit_dc

    @property
    def scope_timescale(self) -> 'MutableDecofReal':
        return self._scope_timescale

    @property
    def xy_signal(self) -> 'MutableDecofInteger':
        return self._xy_signal


class McBoard:
    def __init__(self, client: Client, name: str) -> None:
        self.__client = client
        self.__name = name
        self._revision = DecofString(client, name + ':revision')
        self._air_pressure = DecofReal(client, name + ':air-pressure')
        self._board_temp = DecofReal(client, name + ':board-temp')
        self._serial_number = DecofString(client, name + ':serial-number')
        self._relative_humidity = DecofReal(client, name + ':relative-humidity')
        self._fpga_fw_ver = DecofString(client, name + ':fpga-fw-ver')

    @property
    def revision(self) -> 'DecofString':
        return self._revision

    @property
    def air_pressure(self) -> 'DecofReal':
        return self._air_pressure

    @property
    def board_temp(self) -> 'DecofReal':
        return self._board_temp

    @property
    def serial_number(self) -> 'DecofString':
        return self._serial_number

    @property
    def relative_humidity(self) -> 'DecofReal':
        return self._relative_humidity

    @property
    def fpga_fw_ver(self) -> 'DecofString':
        return self._fpga_fw_ver


class UvShgLaser:
    def __init__(self, client: Client, name: str) -> None:
        self.__client = client
        self.__name = name
        self._error = DecofInteger(client, name + ':error')
        self._specs_fulfilled = DecofBoolean(client, name + ':specs-fulfilled')
        self._power_act = DecofReal(client, name + ':power-act')
        self._status = DecofInteger(client, name + ':status')
        self._operation_time_pump = DecofReal(client, name + ':operation-time-pump')
        self._pump_power_margin = DecofReal(client, name + ':pump-power-margin')
        self._error_txt = DecofString(client, name + ':error-txt')
        self._emission = DecofBoolean(client, name + ':emission')
        self._operation_time_uv = DecofReal(client, name + ':operation-time-uv')
        self._idle_mode = MutableDecofBoolean(client, name + ':idle-mode')
        self._power_set = MutableDecofReal(client, name + ':power-set')
        self._remaining_optics_spots = DecofInteger(client, name + ':remaining-optics-spots')
        self._laser_on = MutableDecofBoolean(client, name + ':laser-on')
        self._status_txt = DecofString(client, name + ':status-txt')
        self._baseplate_temperature = DecofReal(client, name + ':baseplate-temperature')

    @property
    def error(self) -> 'DecofInteger':
        return self._error

    @property
    def specs_fulfilled(self) -> 'DecofBoolean':
        return self._specs_fulfilled

    @property
    def power_act(self) -> 'DecofReal':
        return self._power_act

    @property
    def status(self) -> 'DecofInteger':
        return self._status

    @property
    def operation_time_pump(self) -> 'DecofReal':
        return self._operation_time_pump

    @property
    def pump_power_margin(self) -> 'DecofReal':
        return self._pump_power_margin

    @property
    def error_txt(self) -> 'DecofString':
        return self._error_txt

    @property
    def emission(self) -> 'DecofBoolean':
        return self._emission

    @property
    def operation_time_uv(self) -> 'DecofReal':
        return self._operation_time_uv

    @property
    def idle_mode(self) -> 'MutableDecofBoolean':
        return self._idle_mode

    @property
    def power_set(self) -> 'MutableDecofReal':
        return self._power_set

    @property
    def remaining_optics_spots(self) -> 'DecofInteger':
        return self._remaining_optics_spots

    @property
    def laser_on(self) -> 'MutableDecofBoolean':
        return self._laser_on

    @property
    def status_txt(self) -> 'DecofString':
        return self._status_txt

    @property
    def baseplate_temperature(self) -> 'DecofReal':
        return self._baseplate_temperature

    def clear_errors(self) -> None:
        self.__client.exec(self.__name + ':clear-errors', input_stream=None, output_type=None, return_type=None)

    def perform_optics_shift(self) -> None:
        self.__client.exec(self.__name + ':perform-optics-shift', input_stream=None, output_type=None, return_type=None)

    def perform_optimization(self) -> None:
        self.__client.exec(self.__name + ':perform-optimization', input_stream=None, output_type=None, return_type=None)


class LaserCommon:
    def __init__(self, client: Client, name: str) -> None:
        self.__client = client
        self.__name = name
        self._scan = ScanSynchronization(client, name + ':scan')

    @property
    def scan(self) -> 'ScanSynchronization':
        return self._scan

    def retrieve_all(self) -> None:
        self.__client.exec(self.__name + ':retrieve-all', input_stream=None, output_type=None, return_type=None)

    def load_all(self) -> None:
        self.__client.exec(self.__name + ':load-all', input_stream=None, output_type=None, return_type=None)

    def apply_all(self) -> None:
        self.__client.exec(self.__name + ':apply-all', input_stream=None, output_type=None, return_type=None)

    def restore_all(self) -> None:
        self.__client.exec(self.__name + ':restore-all', input_stream=None, output_type=None, return_type=None)

    def save_all(self) -> None:
        self.__client.exec(self.__name + ':save-all', input_stream=None, output_type=None, return_type=None)

    def store_all(self) -> None:
        self.__client.exec(self.__name + ':store-all', input_stream=None, output_type=None, return_type=None)


class ScanSynchronization:
    def __init__(self, client: Client, name: str) -> None:
        self.__client = client
        self.__name = name
        self._sync_laser1 = MutableDecofBoolean(client, name + ':sync-laser1')
        self._sync_laser2 = MutableDecofBoolean(client, name + ':sync-laser2')
        self._frequency = MutableDecofReal(client, name + ':frequency')

    @property
    def sync_laser1(self) -> 'MutableDecofBoolean':
        return self._sync_laser1

    @property
    def sync_laser2(self) -> 'MutableDecofBoolean':
        return self._sync_laser2

    @property
    def frequency(self) -> 'MutableDecofReal':
        return self._frequency

    def load(self) -> None:
        self.__client.exec(self.__name + ':load', input_stream=None, output_type=None, return_type=None)

    def save(self) -> None:
        self.__client.exec(self.__name + ':save', input_stream=None, output_type=None, return_type=None)

    def sync(self) -> None:
        self.__client.exec(self.__name + ':sync', input_stream=None, output_type=None, return_type=None)


class Buzzer:
    def __init__(self, client: Client, name: str) -> None:
        self.__client = client
        self.__name = name
        self._welcome = MutableDecofString(client, name + ':welcome')

    @property
    def welcome(self) -> 'MutableDecofString':
        return self._welcome

    def play_welcome(self) -> None:
        self.__client.exec(self.__name + ':play-welcome', input_stream=None, output_type=None, return_type=None)

    def play(self, melody: str) -> None:
        assert isinstance(melody, str), "expected type 'str' for parameter 'melody', got '{}'".format(type(melody))
        self.__client.exec(self.__name + ':play', melody, input_stream=None, output_type=None, return_type=None)


class PowerSupply:
    def __init__(self, client: Client, name: str) -> None:
        self.__client = client
        self.__name = name
        self._voltage_3V3 = DecofReal(client, name + ':voltage-3V3')
        self._heatsink_temp = DecofReal(client, name + ':heatsink-temp')
        self._current_5V = DecofReal(client, name + ':current-5V')
        self._board_temp = DecofReal(client, name + ':board-temp')
        self._voltage_15V = DecofReal(client, name + ':voltage-15V')
        self._status = DecofInteger(client, name + ':status')
        self._current_15V = DecofReal(client, name + ':current-15V')
        self._serial_number = DecofString(client, name + ':serial-number')
        self._revision = DecofString(client, name + ':revision')
        self._voltage_5V = DecofReal(client, name + ':voltage-5V')
        self._type_ = DecofString(client, name + ':type')
        self._current_15Vn = DecofReal(client, name + ':current-15Vn')
        self._status_txt = DecofString(client, name + ':status-txt')
        self._voltage_15Vn = DecofReal(client, name + ':voltage-15Vn')
        self._load = DecofReal(client, name + ':load')

    @property
    def voltage_3V3(self) -> 'DecofReal':
        return self._voltage_3V3

    @property
    def heatsink_temp(self) -> 'DecofReal':
        return self._heatsink_temp

    @property
    def current_5V(self) -> 'DecofReal':
        return self._current_5V

    @property
    def board_temp(self) -> 'DecofReal':
        return self._board_temp

    @property
    def voltage_15V(self) -> 'DecofReal':
        return self._voltage_15V

    @property
    def status(self) -> 'DecofInteger':
        return self._status

    @property
    def current_15V(self) -> 'DecofReal':
        return self._current_15V

    @property
    def serial_number(self) -> 'DecofString':
        return self._serial_number

    @property
    def revision(self) -> 'DecofString':
        return self._revision

    @property
    def voltage_5V(self) -> 'DecofReal':
        return self._voltage_5V

    @property
    def type_(self) -> 'DecofString':
        return self._type_

    @property
    def current_15Vn(self) -> 'DecofReal':
        return self._current_15Vn

    @property
    def status_txt(self) -> 'DecofString':
        return self._status_txt

    @property
    def voltage_15Vn(self) -> 'DecofReal':
        return self._voltage_15Vn

    @property
    def load(self) -> 'DecofReal':
        return self._load


class Display:
    def __init__(self, client: Client, name: str) -> None:
        self.__client = client
        self.__name = name
        self._state = DecofInteger(client, name + ':state')
        self._auto_dark = MutableDecofBoolean(client, name + ':auto-dark')
        self._brightness = MutableDecofReal(client, name + ':brightness')
        self._idle_timeout = MutableDecofInteger(client, name + ':idle-timeout')

    @property
    def state(self) -> 'DecofInteger':
        return self._state

    @property
    def auto_dark(self) -> 'MutableDecofBoolean':
        return self._auto_dark

    @property
    def brightness(self) -> 'MutableDecofReal':
        return self._brightness

    @property
    def idle_timeout(self) -> 'MutableDecofInteger':
        return self._idle_timeout

    def load(self) -> None:
        self.__client.exec(self.__name + ':load', input_stream=None, output_type=None, return_type=None)

    def save(self) -> None:
        self.__client.exec(self.__name + ':save', input_stream=None, output_type=None, return_type=None)

    def update_state(self, active: bool) -> None:
        assert isinstance(active, bool), "expected type 'bool' for parameter 'active', got '{}'".format(type(active))
        self.__client.exec(self.__name + ':update-state', active, input_stream=None, output_type=None, return_type=None)


class TcBoard:
    def __init__(self, client: Client, name: str) -> None:
        self.__client = client
        self.__name = name
        self._revision = DecofString(client, name + ':revision')
        self._slot = DecofString(client, name + ':slot')
        self._channel2 = TcChannel2(client, name + ':channel2')
        self._channel1 = TcChannel2(client, name + ':channel1')
        self._serial_number = DecofString(client, name + ':serial-number')
        self._board_temp = DecofReal(client, name + ':board-temp')
        self._fpga_fw_ver = DecofString(client, name + ':fpga-fw-ver')

    @property
    def revision(self) -> 'DecofString':
        return self._revision

    @property
    def slot(self) -> 'DecofString':
        return self._slot

    @property
    def channel2(self) -> 'TcChannel2':
        return self._channel2

    @property
    def channel1(self) -> 'TcChannel2':
        return self._channel1

    @property
    def serial_number(self) -> 'DecofString':
        return self._serial_number

    @property
    def board_temp(self) -> 'DecofReal':
        return self._board_temp

    @property
    def fpga_fw_ver(self) -> 'DecofString':
        return self._fpga_fw_ver


class PcBoard:
    def __init__(self, client: Client, name: str) -> None:
        self.__client = client
        self.__name = name
        self._revision = DecofString(client, name + ':revision')
        self._channel1 = PiezoDrv3(client, name + ':channel1')
        self._channel_count = DecofInteger(client, name + ':channel-count')
        self._channel2 = PiezoDrv3(client, name + ':channel2')
        self._fpga_fw_ver = DecofInteger(client, name + ':fpga-fw-ver')
        self._status = DecofInteger(client, name + ':status')
        self._slot = DecofString(client, name + ':slot')
        self._serial_number = DecofString(client, name + ':serial-number')
        self._status_txt = DecofString(client, name + ':status-txt')
        self._variant = DecofString(client, name + ':variant')

    @property
    def revision(self) -> 'DecofString':
        return self._revision

    @property
    def channel1(self) -> 'PiezoDrv3':
        return self._channel1

    @property
    def channel_count(self) -> 'DecofInteger':
        return self._channel_count

    @property
    def channel2(self) -> 'PiezoDrv3':
        return self._channel2

    @property
    def fpga_fw_ver(self) -> 'DecofInteger':
        return self._fpga_fw_ver

    @property
    def status(self) -> 'DecofInteger':
        return self._status

    @property
    def slot(self) -> 'DecofString':
        return self._slot

    @property
    def serial_number(self) -> 'DecofString':
        return self._serial_number

    @property
    def status_txt(self) -> 'DecofString':
        return self._status_txt

    @property
    def variant(self) -> 'DecofString':
        return self._variant


class PiezoDrv3:
    def __init__(self, client: Client, name: str) -> None:
        self.__client = client
        self.__name = name
        self._status = DecofInteger(client, name + ':status')
        self._feedforward_master = MutableDecofInteger(client, name + ':feedforward-master')
        self._feedforward_factor = MutableDecofReal(client, name + ':feedforward-factor')
        self._external_input = ExtInput3(client, name + ':external-input')
        self._voltage_min = MutableDecofReal(client, name + ':voltage-min')
        self._status_txt = DecofString(client, name + ':status-txt')
        self._feedforward_enabled = MutableDecofBoolean(client, name + ':feedforward-enabled')
        self._voltage_set_dithering = MutableDecofBoolean(client, name + ':voltage-set-dithering')
        self._voltage_max = MutableDecofReal(client, name + ':voltage-max')
        self._enabled = MutableDecofBoolean(client, name + ':enabled')
        self._voltage_set = MutableDecofReal(client, name + ':voltage-set')
        self._output_filter = OutputFilter3(client, name + ':output-filter')
        self._heatsink_temp = DecofReal(client, name + ':heatsink-temp')
        self._voltage_act = DecofReal(client, name + ':voltage-act')
        self._path = DecofString(client, name + ':path')

    @property
    def status(self) -> 'DecofInteger':
        return self._status

    @property
    def feedforward_master(self) -> 'MutableDecofInteger':
        return self._feedforward_master

    @property
    def feedforward_factor(self) -> 'MutableDecofReal':
        return self._feedforward_factor

    @property
    def external_input(self) -> 'ExtInput3':
        return self._external_input

    @property
    def voltage_min(self) -> 'MutableDecofReal':
        return self._voltage_min

    @property
    def status_txt(self) -> 'DecofString':
        return self._status_txt

    @property
    def feedforward_enabled(self) -> 'MutableDecofBoolean':
        return self._feedforward_enabled

    @property
    def voltage_set_dithering(self) -> 'MutableDecofBoolean':
        return self._voltage_set_dithering

    @property
    def voltage_max(self) -> 'MutableDecofReal':
        return self._voltage_max

    @property
    def enabled(self) -> 'MutableDecofBoolean':
        return self._enabled

    @property
    def voltage_set(self) -> 'MutableDecofReal':
        return self._voltage_set

    @property
    def output_filter(self) -> 'OutputFilter3':
        return self._output_filter

    @property
    def heatsink_temp(self) -> 'DecofReal':
        return self._heatsink_temp

    @property
    def voltage_act(self) -> 'DecofReal':
        return self._voltage_act

    @property
    def path(self) -> 'DecofString':
        return self._path


class Standby:
    def __init__(self, client: Client, name: str) -> None:
        self.__client = client
        self.__name = name
        self._laser1 = StandbyLaser(client, name + ':laser1')
        self._laser2 = StandbyLaser2(client, name + ':laser2')
        self._state = DecofInteger(client, name + ':state')
        self._enabled = MutableDecofBoolean(client, name + ':enabled')

    @property
    def laser1(self) -> 'StandbyLaser':
        return self._laser1

    @property
    def laser2(self) -> 'StandbyLaser2':
        return self._laser2

    @property
    def state(self) -> 'DecofInteger':
        return self._state

    @property
    def enabled(self) -> 'MutableDecofBoolean':
        return self._enabled


class StandbyLaser:
    def __init__(self, client: Client, name: str) -> None:
        self.__client = client
        self.__name = name
        self._ctl = StandbyCtl(client, name + ':ctl')
        self._amp = StandbyAmp(client, name + ':amp')
        self._dl = StandbyDl(client, name + ':dl')
        self._nlo = StandbyShg(client, name + ':nlo')

    @property
    def ctl(self) -> 'StandbyCtl':
        return self._ctl

    @property
    def amp(self) -> 'StandbyAmp':
        return self._amp

    @property
    def dl(self) -> 'StandbyDl':
        return self._dl

    @property
    def nlo(self) -> 'StandbyShg':
        return self._nlo


class StandbyCtl:
    def __init__(self, client: Client, name: str) -> None:
        self.__client = client
        self.__name = name
        self._disable = MutableDecofBoolean(client, name + ':disable')

    @property
    def disable(self) -> 'MutableDecofBoolean':
        return self._disable


class StandbyAmp:
    def __init__(self, client: Client, name: str) -> None:
        self.__client = client
        self.__name = name
        self._disable_cc = MutableDecofBoolean(client, name + ':disable-cc')
        self._disable_tc = MutableDecofBoolean(client, name + ':disable-tc')

    @property
    def disable_cc(self) -> 'MutableDecofBoolean':
        return self._disable_cc

    @property
    def disable_tc(self) -> 'MutableDecofBoolean':
        return self._disable_tc


class StandbyDl:
    def __init__(self, client: Client, name: str) -> None:
        self.__client = client
        self.__name = name
        self._disable_pc = MutableDecofBoolean(client, name + ':disable-pc')
        self._disable_cc = MutableDecofBoolean(client, name + ':disable-cc')
        self._disable_tc = MutableDecofBoolean(client, name + ':disable-tc')

    @property
    def disable_pc(self) -> 'MutableDecofBoolean':
        return self._disable_pc

    @property
    def disable_cc(self) -> 'MutableDecofBoolean':
        return self._disable_cc

    @property
    def disable_tc(self) -> 'MutableDecofBoolean':
        return self._disable_tc


class StandbyShg:
    def __init__(self, client: Client, name: str) -> None:
        self.__client = client
        self.__name = name
        self._disable_pc = MutableDecofBoolean(client, name + ':disable-pc')
        self._disable_cavity_lock = MutableDecofBoolean(client, name + ':disable-cavity-lock')
        self._disable_servo_subsystem = MutableDecofBoolean(client, name + ':disable-servo-subsystem')
        self._disable_tc = MutableDecofBoolean(client, name + ':disable-tc')
        self._disable_power_stabilization = MutableDecofBoolean(client, name + ':disable-power-stabilization')

    @property
    def disable_pc(self) -> 'MutableDecofBoolean':
        return self._disable_pc

    @property
    def disable_cavity_lock(self) -> 'MutableDecofBoolean':
        return self._disable_cavity_lock

    @property
    def disable_servo_subsystem(self) -> 'MutableDecofBoolean':
        return self._disable_servo_subsystem

    @property
    def disable_tc(self) -> 'MutableDecofBoolean':
        return self._disable_tc

    @property
    def disable_power_stabilization(self) -> 'MutableDecofBoolean':
        return self._disable_power_stabilization


class StandbyLaser2:
    def __init__(self, client: Client, name: str) -> None:
        self.__client = client
        self.__name = name
        self._dl = StandbyDl(client, name + ':dl')

    @property
    def dl(self) -> 'StandbyDl':
        return self._dl


class PdhBoard:
    def __init__(self, client: Client, name: str) -> None:
        self.__client = client
        self.__name = name
        self._board_temp = DecofReal(client, name + ':board-temp')
        self._channel2 = PdhChannel(client, name + ':channel2')
        self._status = DecofInteger(client, name + ':status')
        self._channel1 = PdhChannel(client, name + ':channel1')
        self._serial_number = DecofString(client, name + ':serial-number')
        self._fpga_fw_ver = DecofInteger(client, name + ':fpga-fw-ver')
        self._revision = DecofString(client, name + ':revision')
        self._slot = DecofString(client, name + ':slot')
        self._status_txt = DecofString(client, name + ':status-txt')

    @property
    def board_temp(self) -> 'DecofReal':
        return self._board_temp

    @property
    def channel2(self) -> 'PdhChannel':
        return self._channel2

    @property
    def status(self) -> 'DecofInteger':
        return self._status

    @property
    def channel1(self) -> 'PdhChannel':
        return self._channel1

    @property
    def serial_number(self) -> 'DecofString':
        return self._serial_number

    @property
    def fpga_fw_ver(self) -> 'DecofInteger':
        return self._fpga_fw_ver

    @property
    def revision(self) -> 'DecofString':
        return self._revision

    @property
    def slot(self) -> 'DecofString':
        return self._slot

    @property
    def status_txt(self) -> 'DecofString':
        return self._status_txt

    def load(self) -> None:
        self.__client.exec(self.__name + ':load', input_stream=None, output_type=None, return_type=None)

    def save(self) -> None:
        self.__client.exec(self.__name + ':save', input_stream=None, output_type=None, return_type=None)


class PdhChannel:
    def __init__(self, client: Client, name: str) -> None:
        self.__client = client
        self.__name = name
        self._modulation_amplitude_dbm = MutableDecofReal(client, name + ':modulation-amplitude-dbm')
        self._lo_output_enabled = MutableDecofBoolean(client, name + ':lo-output-enabled')
        self._input_level_max = MutableDecofInteger(client, name + ':input-level-max')
        self._use_fast_oscillator = MutableDecofBoolean(client, name + ':use-fast-oscillator')
        self._lo_output_amplitude_dbm = MutableDecofReal(client, name + ':lo-output-amplitude-dbm')
        self._modulation_enabled = MutableDecofBoolean(client, name + ':modulation-enabled')
        self._phase_shift = MutableDecofReal(client, name + ':phase-shift')
        self._lock_level = MutableDecofReal(client, name + ':lock-level')
        self._modulation_amplitude_vpp = DecofReal(client, name + ':modulation-amplitude-vpp')
        self._lo_output_amplitude_vpp = DecofReal(client, name + ':lo-output-amplitude-vpp')

    @property
    def modulation_amplitude_dbm(self) -> 'MutableDecofReal':
        return self._modulation_amplitude_dbm

    @property
    def lo_output_enabled(self) -> 'MutableDecofBoolean':
        return self._lo_output_enabled

    @property
    def input_level_max(self) -> 'MutableDecofInteger':
        return self._input_level_max

    @property
    def use_fast_oscillator(self) -> 'MutableDecofBoolean':
        return self._use_fast_oscillator

    @property
    def lo_output_amplitude_dbm(self) -> 'MutableDecofReal':
        return self._lo_output_amplitude_dbm

    @property
    def modulation_enabled(self) -> 'MutableDecofBoolean':
        return self._modulation_enabled

    @property
    def phase_shift(self) -> 'MutableDecofReal':
        return self._phase_shift

    @property
    def lock_level(self) -> 'MutableDecofReal':
        return self._lock_level

    @property
    def modulation_amplitude_vpp(self) -> 'DecofReal':
        return self._modulation_amplitude_vpp

    @property
    def lo_output_amplitude_vpp(self) -> 'DecofReal':
        return self._lo_output_amplitude_vpp


class IoBoard:
    def __init__(self, client: Client, name: str) -> None:
        self.__client = client
        self.__name = name
        self._digital_in0 = IoDigitalInput(client, name + ':digital-in0')
        self._serial_number = DecofString(client, name + ':serial-number')
        self._digital_in3 = IoDigitalInput(client, name + ':digital-in3')
        self._digital_out0 = IoDigitalOutput(client, name + ':digital-out0')
        self._fast_3 = IoInputChannel(client, name + ':fast-3')
        self._fast_4 = IoInputChannel(client, name + ':fast-4')
        self._digital_in2 = IoDigitalInput(client, name + ':digital-in2')
        self._fpga_fw_ver = DecofInteger(client, name + ':fpga-fw-ver')
        self._fine_2 = IoInputChannel(client, name + ':fine-2')
        self._revision = DecofString(client, name + ':revision')
        self._digital_in1 = IoDigitalInput(client, name + ':digital-in1')
        self._digital_out1 = IoDigitalOutput(client, name + ':digital-out1')
        self._digital_out2 = IoDigitalOutput(client, name + ':digital-out2')
        self._out_b = IoOutputChannel(client, name + ':out-b')
        self._fine_1 = IoInputChannel(client, name + ':fine-1')
        self._out_a = IoOutputChannel(client, name + ':out-a')
        self._digital_out3 = IoDigitalOutput(client, name + ':digital-out3')

    @property
    def digital_in0(self) -> 'IoDigitalInput':
        return self._digital_in0

    @property
    def serial_number(self) -> 'DecofString':
        return self._serial_number

    @property
    def digital_in3(self) -> 'IoDigitalInput':
        return self._digital_in3

    @property
    def digital_out0(self) -> 'IoDigitalOutput':
        return self._digital_out0

    @property
    def fast_3(self) -> 'IoInputChannel':
        return self._fast_3

    @property
    def fast_4(self) -> 'IoInputChannel':
        return self._fast_4

    @property
    def digital_in2(self) -> 'IoDigitalInput':
        return self._digital_in2

    @property
    def fpga_fw_ver(self) -> 'DecofInteger':
        return self._fpga_fw_ver

    @property
    def fine_2(self) -> 'IoInputChannel':
        return self._fine_2

    @property
    def revision(self) -> 'DecofString':
        return self._revision

    @property
    def digital_in1(self) -> 'IoDigitalInput':
        return self._digital_in1

    @property
    def digital_out1(self) -> 'IoDigitalOutput':
        return self._digital_out1

    @property
    def digital_out2(self) -> 'IoDigitalOutput':
        return self._digital_out2

    @property
    def out_b(self) -> 'IoOutputChannel':
        return self._out_b

    @property
    def fine_1(self) -> 'IoInputChannel':
        return self._fine_1

    @property
    def out_a(self) -> 'IoOutputChannel':
        return self._out_a

    @property
    def digital_out3(self) -> 'IoDigitalOutput':
        return self._digital_out3

    def load(self) -> None:
        self.__client.exec(self.__name + ':load', input_stream=None, output_type=None, return_type=None)

    def save(self) -> None:
        self.__client.exec(self.__name + ':save', input_stream=None, output_type=None, return_type=None)


class IoDigitalInput:
    def __init__(self, client: Client, name: str) -> None:
        self.__client = client
        self.__name = name
        self._value_act = DecofBoolean(client, name + ':value-act')

    @property
    def value_act(self) -> 'DecofBoolean':
        return self._value_act


class IoDigitalOutput:
    def __init__(self, client: Client, name: str) -> None:
        self.__client = client
        self.__name = name
        self._value_act = DecofBoolean(client, name + ':value-act')
        self._mode = MutableDecofInteger(client, name + ':mode')
        self._value_set = MutableDecofBoolean(client, name + ':value-set')
        self._invert = MutableDecofBoolean(client, name + ':invert')

    @property
    def value_act(self) -> 'DecofBoolean':
        return self._value_act

    @property
    def mode(self) -> 'MutableDecofInteger':
        return self._mode

    @property
    def value_set(self) -> 'MutableDecofBoolean':
        return self._value_set

    @property
    def invert(self) -> 'MutableDecofBoolean':
        return self._invert


class IoInputChannel:
    def __init__(self, client: Client, name: str) -> None:
        self.__client = client
        self.__name = name
        self._value_act = DecofReal(client, name + ':value-act')

    @property
    def value_act(self) -> 'DecofReal':
        return self._value_act


class IoOutputChannel:
    def __init__(self, client: Client, name: str) -> None:
        self.__client = client
        self.__name = name
        self._feedforward_enabled = MutableDecofBoolean(client, name + ':feedforward-enabled')
        self._voltage_max = MutableDecofReal(client, name + ':voltage-max')
        self._feedforward_factor = MutableDecofReal(client, name + ':feedforward-factor')
        self._feedforward_master = MutableDecofInteger(client, name + ':feedforward-master')
        self._output_filter = OutputFilter2(client, name + ':output-filter')
        self._voltage_offset = MutableDecofReal(client, name + ':voltage-offset')
        self._external_input = ExtInput2(client, name + ':external-input')
        self._linked_laser = MutableDecofInteger(client, name + ':linked-laser')
        self._voltage_set = MutableDecofReal(client, name + ':voltage-set')
        self._voltage_min = MutableDecofReal(client, name + ':voltage-min')

    @property
    def feedforward_enabled(self) -> 'MutableDecofBoolean':
        return self._feedforward_enabled

    @property
    def voltage_max(self) -> 'MutableDecofReal':
        return self._voltage_max

    @property
    def feedforward_factor(self) -> 'MutableDecofReal':
        return self._feedforward_factor

    @property
    def feedforward_master(self) -> 'MutableDecofInteger':
        return self._feedforward_master

    @property
    def output_filter(self) -> 'OutputFilter2':
        return self._output_filter

    @property
    def voltage_offset(self) -> 'MutableDecofReal':
        return self._voltage_offset

    @property
    def external_input(self) -> 'ExtInput2':
        return self._external_input

    @property
    def linked_laser(self) -> 'MutableDecofInteger':
        return self._linked_laser

    @property
    def voltage_set(self) -> 'MutableDecofReal':
        return self._voltage_set

    @property
    def voltage_min(self) -> 'MutableDecofReal':
        return self._voltage_min


class FwUpdate:
    def __init__(self, client: Client, name: str) -> None:
        self.__client = client
        self.__name = name

    def show_log(self) -> str:
        return self.__client.exec(self.__name + ':show-log', input_stream=None, output_type=str, return_type=None)

    def show_history(self) -> str:
        return self.__client.exec(self.__name + ':show-history', input_stream=None, output_type=str, return_type=None)

    def upload(self, stream_input: bytes, filename: str) -> None:
        assert isinstance(stream_input, bytes), "expected type 'bytes' for parameter 'stream_input', got '{}'".format(type(stream_input))
        assert isinstance(filename, str), "expected type 'str' for parameter 'filename', got '{}'".format(type(filename))
        self.__client.exec(self.__name + ':upload', filename, input_stream=stream_input, output_type=None, return_type=None)


class SystemMessages:
    def __init__(self, client: Client, name: str) -> None:
        self.__client = client
        self.__name = name
        self._latest_message = DecofString(client, name + ':latest-message')
        self._count = DecofInteger(client, name + ':count')
        self._count_new = DecofInteger(client, name + ':count-new')

    @property
    def latest_message(self) -> 'DecofString':
        return self._latest_message

    @property
    def count(self) -> 'DecofInteger':
        return self._count

    @property
    def count_new(self) -> 'DecofInteger':
        return self._count_new

    def show_all(self) -> str:
        return self.__client.exec(self.__name + ':show-all', input_stream=None, output_type=str, return_type=None)

    def show_log(self) -> str:
        return self.__client.exec(self.__name + ':show-log', input_stream=None, output_type=str, return_type=None)

    def mark_as_read(self, ID: int) -> None:
        assert isinstance(ID, int), "expected type 'int' for parameter 'ID', got '{}'".format(type(ID))
        self.__client.exec(self.__name + ':mark-as-read', ID, input_stream=None, output_type=None, return_type=None)

    def show_persistent(self) -> str:
        return self.__client.exec(self.__name + ':show-persistent', input_stream=None, output_type=str, return_type=None)

    def show_new(self) -> str:
        return self.__client.exec(self.__name + ':show-new', input_stream=None, output_type=str, return_type=None)


class ServiceReport:
    def __init__(self, client: Client, name: str) -> None:
        self.__client = client
        self.__name = name
        self._ready = DecofBoolean(client, name + ':ready')

    @property
    def ready(self) -> 'DecofBoolean':
        return self._ready

    def print(self) -> bytes:
        return self.__client.exec(self.__name + ':print', input_stream=None, output_type=bytes, return_type=None)

    def service_report(self) -> bytes:
        return self.__client.exec(self.__name + ':service-report', input_stream=None, output_type=bytes, return_type=None)

    def request(self) -> None:
        self.__client.exec(self.__name + ':request', input_stream=None, output_type=None, return_type=None)


class Licenses:
    def __init__(self, client: Client, name: str) -> None:
        self.__client = client
        self.__name = name
        self._installed_keys = DecofInteger(client, name + ':installed-keys')
        self._options = LicenseOptions(client, name + ':options')

    @property
    def installed_keys(self) -> 'DecofInteger':
        return self._installed_keys

    @property
    def options(self) -> 'LicenseOptions':
        return self._options

    def get_key(self, key_number: int) -> str:
        assert isinstance(key_number, int), "expected type 'int' for parameter 'key_number', got '{}'".format(type(key_number))
        return self.__client.exec(self.__name + ':get-key', key_number, input_stream=None, output_type=None, return_type=str)

    def install(self, licensekey: str) -> bool:
        assert isinstance(licensekey, str), "expected type 'str' for parameter 'licensekey', got '{}'".format(type(licensekey))
        return self.__client.exec(self.__name + ':install', licensekey, input_stream=None, output_type=None, return_type=bool)


class LicenseOptions:
    def __init__(self, client: Client, name: str) -> None:
        self.__client = client
        self.__name = name
        self._lock = LicenseOption(client, name + ':lock')
        self._quad_laser_operation = LicenseOption(client, name + ':quad-laser-operation')
        self._dual_laser_operation = LicenseOption(client, name + ':dual-laser-operation')

    @property
    def lock(self) -> 'LicenseOption':
        return self._lock

    @property
    def quad_laser_operation(self) -> 'LicenseOption':
        return self._quad_laser_operation

    @property
    def dual_laser_operation(self) -> 'LicenseOption':
        return self._dual_laser_operation


class LicenseOption:
    def __init__(self, client: Client, name: str) -> None:
        self.__client = client
        self.__name = name
        self._enabled = DecofBoolean(client, name + ':enabled')
        self._valid_until = DecofString(client, name + ':valid-until')
        self._licensee = DecofString(client, name + ':licensee')

    @property
    def enabled(self) -> 'DecofBoolean':
        return self._enabled

    @property
    def valid_until(self) -> 'DecofString':
        return self._valid_until

    @property
    def licensee(self) -> 'DecofString':
        return self._licensee


class Ipconfig:
    def __init__(self, client: Client, name: str) -> None:
        self.__client = client
        self.__name = name
        self._mac_addr = DecofString(client, name + ':mac-addr')
        self._dhcp = DecofBoolean(client, name + ':dhcp')
        self._cmd_port = DecofInteger(client, name + ':cmd-port')
        self._ip_addr = DecofString(client, name + ':ip-addr')
        self._mon_port = DecofInteger(client, name + ':mon-port')
        self._net_mask = DecofString(client, name + ':net-mask')

    @property
    def mac_addr(self) -> 'DecofString':
        return self._mac_addr

    @property
    def dhcp(self) -> 'DecofBoolean':
        return self._dhcp

    @property
    def cmd_port(self) -> 'DecofInteger':
        return self._cmd_port

    @property
    def ip_addr(self) -> 'DecofString':
        return self._ip_addr

    @property
    def mon_port(self) -> 'DecofInteger':
        return self._mon_port

    @property
    def net_mask(self) -> 'DecofString':
        return self._net_mask

    def set_dhcp(self) -> None:
        self.__client.exec(self.__name + ':set-dhcp', input_stream=None, output_type=None, return_type=None)

    def set_ip(self, ip_addr: str, net_mask: str) -> None:
        assert isinstance(ip_addr, str), "expected type 'str' for parameter 'ip_addr', got '{}'".format(type(ip_addr))
        assert isinstance(net_mask, str), "expected type 'str' for parameter 'net_mask', got '{}'".format(type(net_mask))
        self.__client.exec(self.__name + ':set-ip', ip_addr, net_mask, input_stream=None, output_type=None, return_type=None)

    def apply(self) -> None:
        self.__client.exec(self.__name + ':apply', input_stream=None, output_type=None, return_type=None)


class DLCpro:
    def __init__(self, connection: Connection) -> None:
        self.__client = Client(connection)
        self._uptime = DecofInteger(self.__client, 'uptime')
        self._ssw_svn_revision = DecofString(self.__client, 'ssw-svn-revision')
        self._decof_svn_revision = DecofString(self.__client, 'decof-svn-revision')
        self._echo = MutableDecofBoolean(self.__client, 'echo')
        self._serial_number = DecofString(self.__client, 'serial-number')
        self._svn_revision = DecofString(self.__client, 'svn-revision')
        self._decof_ver = DecofString(self.__client, 'decof-ver')
        self._uptime_txt = DecofString(self.__client, 'uptime-txt')
        self._system_type = DecofString(self.__client, 'system-type')
        self._system_model = DecofString(self.__client, 'system-model')
        self._ssw_ver = DecofString(self.__client, 'ssw-ver')
        self._system_label = MutableDecofString(self.__client, 'system-label')
        self._fw_ver = DecofString(self.__client, 'fw-ver')
        self._build_information = BuildInformation(self.__client, 'build-information')
        self._cc2 = CcBoard(self.__client, 'cc2')
        self._emission_button_enabled = MutableDecofBoolean(self.__client, 'emission-button-enabled')
        self._ampcc2 = Cc5000Board(self.__client, 'ampcc2')
        self._ampcc1 = Cc5000Board(self.__client, 'ampcc1')
        self._laser1 = Laser(self.__client, 'laser1')
        self._emission = DecofBoolean(self.__client, 'emission')
        self._system_health = DecofInteger(self.__client, 'system-health')
        self._mc = McBoard(self.__client, 'mc')
        self._cc1 = CcBoard(self.__client, 'cc1')
        self._uv = UvShgLaser(self.__client, 'uv')
        self._laser_common = LaserCommon(self.__client, 'laser-common')
        self._buzzer = Buzzer(self.__client, 'buzzer')
        self._power_supply = PowerSupply(self.__client, 'power-supply')
        self._display = Display(self.__client, 'display')
        self._tc1 = TcBoard(self.__client, 'tc1')
        self._frontkey_locked = DecofBoolean(self.__client, 'frontkey-locked')
        self._system_health_txt = DecofString(self.__client, 'system-health-txt')
        self._pc2 = PcBoard(self.__client, 'pc2')
        self._standby = Standby(self.__client, 'standby')
        self._pc3 = PcBoard(self.__client, 'pc3')
        self._interlock_open = DecofBoolean(self.__client, 'interlock-open')
        self._pc1 = PcBoard(self.__client, 'pc1')
        self._laser2 = Laser(self.__client, 'laser2')
        self._tc2 = TcBoard(self.__client, 'tc2')
        self._pdh1 = PdhBoard(self.__client, 'pdh1')
        self._io = IoBoard(self.__client, 'io')
        self._fw_update = FwUpdate(self.__client, 'fw-update')
        self._time = MutableDecofString(self.__client, 'time')
        self._system_messages = SystemMessages(self.__client, 'system-messages')
        self._system_service_report = ServiceReport(self.__client, 'system-service-report')
        self._tan = DecofInteger(self.__client, 'tan')
        self._licenses = Licenses(self.__client, 'licenses')
        self._ul = MutableDecofInteger(self.__client, 'ul')
        self._net_conf = Ipconfig(self.__client, 'net-conf')

    def __enter__(self):
        self.open()
        return self

    def __exit__(self, *args):
        self.close()

    def open(self) -> None:
        self.__client.open()

    def close(self) -> None:
        self.__client.close()

    def run(self) -> None:
        self.__client.run()

    def stop(self) -> None:
        self.__client.stop()

    def poll(self) -> None:
        self.__client.poll()

    @property
    def uptime(self) -> 'DecofInteger':
        return self._uptime

    @property
    def ssw_svn_revision(self) -> 'DecofString':
        return self._ssw_svn_revision

    @property
    def decof_svn_revision(self) -> 'DecofString':
        return self._decof_svn_revision

    @property
    def echo(self) -> 'MutableDecofBoolean':
        return self._echo

    @property
    def serial_number(self) -> 'DecofString':
        return self._serial_number

    @property
    def svn_revision(self) -> 'DecofString':
        return self._svn_revision

    @property
    def decof_ver(self) -> 'DecofString':
        return self._decof_ver

    @property
    def uptime_txt(self) -> 'DecofString':
        return self._uptime_txt

    @property
    def system_type(self) -> 'DecofString':
        return self._system_type

    @property
    def system_model(self) -> 'DecofString':
        return self._system_model

    @property
    def ssw_ver(self) -> 'DecofString':
        return self._ssw_ver

    @property
    def system_label(self) -> 'MutableDecofString':
        return self._system_label

    @property
    def fw_ver(self) -> 'DecofString':
        return self._fw_ver

    @property
    def build_information(self) -> 'BuildInformation':
        return self._build_information

    @property
    def cc2(self) -> 'CcBoard':
        return self._cc2

    @property
    def emission_button_enabled(self) -> 'MutableDecofBoolean':
        return self._emission_button_enabled

    @property
    def ampcc2(self) -> 'Cc5000Board':
        return self._ampcc2

    @property
    def ampcc1(self) -> 'Cc5000Board':
        return self._ampcc1

    @property
    def laser1(self) -> 'Laser':
        return self._laser1

    @property
    def emission(self) -> 'DecofBoolean':
        return self._emission

    @property
    def system_health(self) -> 'DecofInteger':
        return self._system_health

    @property
    def mc(self) -> 'McBoard':
        return self._mc

    @property
    def cc1(self) -> 'CcBoard':
        return self._cc1

    @property
    def uv(self) -> 'UvShgLaser':
        return self._uv

    @property
    def laser_common(self) -> 'LaserCommon':
        return self._laser_common

    @property
    def buzzer(self) -> 'Buzzer':
        return self._buzzer

    @property
    def power_supply(self) -> 'PowerSupply':
        return self._power_supply

    @property
    def display(self) -> 'Display':
        return self._display

    @property
    def tc1(self) -> 'TcBoard':
        return self._tc1

    @property
    def frontkey_locked(self) -> 'DecofBoolean':
        return self._frontkey_locked

    @property
    def system_health_txt(self) -> 'DecofString':
        return self._system_health_txt

    @property
    def pc2(self) -> 'PcBoard':
        return self._pc2

    @property
    def standby(self) -> 'Standby':
        return self._standby

    @property
    def pc3(self) -> 'PcBoard':
        return self._pc3

    @property
    def interlock_open(self) -> 'DecofBoolean':
        return self._interlock_open

    @property
    def pc1(self) -> 'PcBoard':
        return self._pc1

    @property
    def laser2(self) -> 'Laser':
        return self._laser2

    @property
    def tc2(self) -> 'TcBoard':
        return self._tc2

    @property
    def pdh1(self) -> 'PdhBoard':
        return self._pdh1

    @property
    def io(self) -> 'IoBoard':
        return self._io

    @property
    def fw_update(self) -> 'FwUpdate':
        return self._fw_update

    @property
    def time(self) -> 'MutableDecofString':
        return self._time

    @property
    def system_messages(self) -> 'SystemMessages':
        return self._system_messages

    @property
    def system_service_report(self) -> 'ServiceReport':
        return self._system_service_report

    @property
    def tan(self) -> 'DecofInteger':
        return self._tan

    @property
    def licenses(self) -> 'Licenses':
        return self._licenses

    @property
    def ul(self) -> 'MutableDecofInteger':
        return self._ul

    @property
    def net_conf(self) -> 'Ipconfig':
        return self._net_conf

    def system_summary(self) -> str:
        return self.__client.exec('system-summary', input_stream=None, output_type=str, return_type=None)

    def service_log(self) -> str:
        return self.__client.exec('service-log', input_stream=None, output_type=str, return_type=None)

    def error_log(self) -> str:
        return self.__client.exec('error-log', input_stream=None, output_type=str, return_type=None)

    def debug_log(self) -> str:
        return self.__client.exec('debug-log', input_stream=None, output_type=str, return_type=None)

    def system_connections(self) -> Tuple[str, int]:
        return self.__client.exec('system-connections', input_stream=None, output_type=str, return_type=int)

    def service_report(self) -> bytes:
        return self.__client.exec('service-report', input_stream=None, output_type=bytes, return_type=None)

    def service_script(self, stream_input: bytes) -> None:
        assert isinstance(stream_input, bytes), "expected type 'bytes' for parameter 'stream_input', got '{}'".format(type(stream_input))
        self.__client.exec('service-script', input_stream=stream_input, output_type=None, return_type=None)

    def change_password(self, password: str) -> None:
        assert isinstance(password, str), "expected type 'str' for parameter 'password', got '{}'".format(type(password))
        self.__client.exec('change-password', password, input_stream=None, output_type=None, return_type=None)

    def change_ul(self, ul: AccessLevel, passwd: str) -> int:
        assert isinstance(ul, AccessLevel), "expected type 'AccessLevel' for parameter 'ul', got '{}'".format(type(ul))
        assert isinstance(passwd, str), "expected type 'str' for parameter 'passwd', got '{}'".format(type(passwd))
        return self.__client.change_ul(ul, passwd)

