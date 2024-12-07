from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
import math
import ctypes
import pythoncom





class Volume:
    def get_system_volume():
        # Get default audio device
        pythoncom.CoInitialize()
        devices = AudioUtilities.GetSpeakers()
        interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
        volume = ctypes.cast(interface, ctypes.POINTER(IAudioEndpointVolume))
        volume

        # Get current volume level (0.0 to 1.0)
        current_volume = volume.GetMasterVolumeLevelScalar()
        return current_volume * 100  # Convert to percentage
    

    def set_system_volume(percentage):
        if not (0 <= percentage <= 100):
            raise ValueError("Percentage must be between 0 and 100")

        # Get default audio device
        pythoncom.CoInitialize()
        devices = AudioUtilities.GetSpeakers()
        interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
        volume = ctypes.cast(interface, ctypes.POINTER(IAudioEndpointVolume))

        # Convert percentage to scalar (0.0 to 1.0)
        scalar_volume = percentage / 100
        volume.SetMasterVolumeLevelScalar(scalar_volume, None)
        current_volume = volume.GetMasterVolumeLevelScalar()
        return str(current_volume * 100)  # Convert to percentage


    def increase_system_volume(percentage=10):
        if not (0 <= percentage <= 100):
            raise ValueError("Percentage must be between 0 and 100")
        # Get default audio device
        pythoncom.CoInitialize()
        devices = AudioUtilities.GetSpeakers()
        interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
        volume = ctypes.cast(interface, ctypes.POINTER(IAudioEndpointVolume))

        # Convert percentage to scalar (0.0 to 1.0)
        scalar_volume = percentage / 100
        current_volume = volume.GetMasterVolumeLevelScalar()
        if(scalar_volume+current_volume>1):
            volume.SetMasterVolumeLevelScalar(1, None)
            
            current_volume = volume.GetMasterVolumeLevelScalar()
            return str(current_volume * 100)  # Convert to percentage
        else:
            volume.SetMasterVolumeLevelScalar(scalar_volume+current_volume, None)
            current_volume = volume.GetMasterVolumeLevelScalar()
            return str(current_volume * 100)  # Convert to percentage


    def decrease_system_volume(percentage=10):
        if not (0 <= percentage <= 100):
            raise ValueError("Percentage must be between 0 and 100")
        # Get default audio device
        pythoncom.CoInitialize()
        devices = AudioUtilities.GetSpeakers()
        interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
        volume = ctypes.cast(interface, ctypes.POINTER(IAudioEndpointVolume))

        # Convert percentage to scalar (0.0 to 1.0)
        scalar_volume = percentage / 100
        current_volume = volume.GetMasterVolumeLevelScalar()
        if(current_volume-scalar_volume<0):
            volume.SetMasterVolumeLevelScalar(0, None)
            current_volume = volume.GetMasterVolumeLevelScalar()
            return str(current_volume * 100)  # Convert to percentage
        else:
            volume.SetMasterVolumeLevelScalar(current_volume-scalar_volume, None)
            current_volume = volume.GetMasterVolumeLevelScalar()
            return str(current_volume * 100)  # Convert to percentage
    



    
    