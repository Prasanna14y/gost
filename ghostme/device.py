import logging
from dataclasses import dataclass

logger = logging.getLogger(__name__)


@dataclass
class DeviceInfo:
    udid: str
    name: str
    model: str
    ios_version: str


def list_devices() -> list[DeviceInfo]:
    try:
        from pymobiledevice3.usbmux import list_devices as usbmux_list
        from pymobiledevice3.lockdown import create_using_usbmux

        devices = []
        for mux_device in usbmux_list():
            try:
                lockdown = create_using_usbmux(serial=mux_device.serial)
                info = DeviceInfo(
                    udid=lockdown.udid,
                    name=lockdown.display_name,
                    model=lockdown.product_type,
                    ios_version=lockdown.product_version,
                )
                devices.append(info)
            except Exception as e:
                logger.warning("Failed to query device %s: %s", mux_device.serial, e)
        return devices
    except ImportError:
        logger.error("pymobiledevice3 is not installed")
        return []
    except Exception as e:
        logger.error("Failed to list devices: %s", e)
        return []


def _get_lockdown(udid: str | None = None):
    from pymobiledevice3.usbmux import list_devices as usbmux_list
    from pymobiledevice3.lockdown import create_using_usbmux

    if udid:
        return create_using_usbmux(serial=udid)

    mux_devices = usbmux_list()
    if not mux_devices:
        raise ConnectionError("No iOS device connected. Please connect your iPhone via USB.")
    return create_using_usbmux(serial=mux_devices[0].serial)


def set_location(lat: float, lon: float, udid: str | None = None) -> dict:
    try:
        lockdown = _get_lockdown(udid)

        try:
            from pymobiledevice3.services.simulate_location import DtSimulateLocation
            service = DtSimulateLocation(lockdown)
            service.set(lat, lon)
        except ImportError:
            from pymobiledevice3.services.dvt.instruments.location_simulation import LocationSimulation
            from pymobiledevice3.services.dvt.dvt_secure_socket_proxy import DvtSecureSocketProxyService
            with DvtSecureSocketProxyService(lockdown) as dvt:
                LocationSimulation(dvt).simulate_location(lat, lon)

        return {
            "success": True,
            "message": f"Location set to ({lat}, {lon})",
            "lat": lat,
            "lon": lon,
        }
    except ConnectionError:
        raise
    except Exception as e:
        logger.exception("Failed to set location")
        raise RuntimeError(f"Failed to set location: {e}") from e


def reset_location(udid: str | None = None) -> dict:
    try:
        lockdown = _get_lockdown(udid)

        try:
            from pymobiledevice3.services.simulate_location import DtSimulateLocation
            service = DtSimulateLocation(lockdown)
            service.clear()
        except ImportError:
            from pymobiledevice3.services.dvt.instruments.location_simulation import LocationSimulation
            from pymobiledevice3.services.dvt.dvt_secure_socket_proxy import DvtSecureSocketProxyService
            with DvtSecureSocketProxyService(lockdown) as dvt:
                LocationSimulation(dvt).clear_simulated_location()

        return {"success": True, "message": "Location reset to real GPS"}
    except ConnectionError:
        raise
    except Exception as e:
        logger.exception("Failed to reset location")
        raise RuntimeError(f"Failed to reset location: {e}") from e
