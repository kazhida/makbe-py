


class DeviceInfoService:

    def __init__(self, software_revision, manufacturer):
        self.manufacturer_name = None
        self.model_number = None
        self.serial_number = None
        self.hw_revision = None
        self.fw_revision = None
        self.sw_revision = None
        self.system_id = None
        self.pnp_id = None
        self.certification_data = None
        self.software_revision = software_revision
        self.manufacturer = manufacturer
