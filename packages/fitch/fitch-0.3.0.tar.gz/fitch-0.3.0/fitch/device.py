"""
MIT License

Copyright (c) 2018 williamfzc

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""
import tempfile
import os
import shutil
import atexit

from fitch.logger import logger
from fitch.utils import is_device_connected
from fitch.player import ActionPlayer
from fitch import detector

from fastcap import MNCDevice
from pyatool import PYAToolkit


class FDevice(object):
    def __init__(self, device_id: str):
        assert is_device_connected(device_id), 'device {} not connected'.format(device_id)
        self.device_id = device_id

        self.mnc = None
        self.player = None
        self.toolkit = None

        self.start()

    def start(self):
        """ start device """
        self.mnc = MNCDevice(self.device_id)
        self.player = ActionPlayer(self.device_id)
        self.toolkit = PYAToolkit(self.device_id)

        logger.info('FDevice [{}] STARTED'.format(self.device_id))

    def stop(self):
        """ stop device, and clean up """
        self.player and self.player.stop()

        self.mnc = None
        self.player = None
        self.toolkit = None

        logger.info('FDevice [{}] STOPPED'.format(self.device_id))

    def reset(self):
        """ stop and restart device """
        self.stop()
        self.start()

    def screen_shot(self) -> str:
        """ screen shot and return its path """
        temp_pic = tempfile.NamedTemporaryFile('w+', delete=False, suffix='.png')
        temp_pic_name = temp_pic.name
        self.mnc.screen_shot()
        self.mnc.export_screen(temp_pic_name)
        logger.info('SCREEN SHOT SAVED IN [{}]'.format(temp_pic_name))
        return temp_pic_name

    def find_target(self, target_path: str, save_pic: str = None) -> (list, tuple):
        """ find target pic in screen, and get its position (or None) """
        pic_path = self.screen_shot()
        result = detector.detect(target_path, pic_path)

        if save_pic:
            shutil.copy(pic_path, save_pic)
        os.remove(pic_path)

        try:
            target_point = detector.cal_location(result)
        except AssertionError:
            # if not found, return None
            return None
        return target_point

    def tap_target(self, target_path: str, duration: int = 100, save_pic: str = None):
        """ find target pic in screen, get its position, and tap it """
        target_point = self.find_target(target_path, save_pic=save_pic)
        assert target_point is not None, 'TARGET [{}] NOT FOUND IN SCREEN'.format(target_path)
        self.player.tap(target_point, duration=duration)


class FDeviceManager(object):
    _device_dict = dict()

    @classmethod
    def add(cls, target_device_id: str) -> FDevice:
        if not cls.is_device_available(target_device_id):
            new_device = FDevice(target_device_id)
            cls._device_dict[target_device_id] = new_device
            logger.info('DEVICE [{}] REGISTER FINISHED'.format(target_device_id))
            return new_device

        # or, reuse old device
        logger.info('DEVICE [{}] ALREADY REGISTERED, REUSE'.format(target_device_id))
        return cls._device_dict[target_device_id]

    @classmethod
    def remove(cls, target_device_id: str):
        if not cls.is_device_available(target_device_id):
            logger.warning('DEVICE [{}] NOT EXISTED')
            return
        target_device = cls._device_dict[target_device_id]
        target_device.stop()
        del cls._device_dict[target_device_id]

    @classmethod
    def is_device_available(cls, device_id: str) -> bool:
        return device_id in cls._device_dict

    @classmethod
    def clean(cls):
        device_id_list = list(cls._device_dict.keys())
        for each_device_id in device_id_list:
            cls.remove(each_device_id)


# TODO auto-kill or managed by developer?
atexit.register(FDeviceManager.clean)

if __name__ == '__main__':
    d = FDevice('3d33076e')
    d.screen_shot()
    d.stop()
