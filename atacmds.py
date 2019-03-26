#----------------------------------------------------------------------------
# SCSI-ATA Pass Through
# Created by: Yu Wang (ivanwang@marvell.com)
# Created at: Fri March  22 14:18:20 CST 2019
#----------------------------------------------------------------------------

import ata_info
import scsi_ata_xlat as sg
from functools import wraps

class ATA_MARVELL_SV_FAh(object):
    def __init__(self, opc):
        self.opcode = opc
        self.protocol = ata_info.NON_DATA
        self.cdb1 = self.__get_cdb1()
        self.kw = {'CDB_1': self.cdb1,
                   'CDB_2': 0x0,
                   'FEATURES': 0x0,
                   'SECTOR_COUNT': self.opcode,
                   'LBA_MID': 0x0, 
                   'LBA_HIGH': 0x0,
                   'DEVICE': 0x0,
                   'COMMAND': 0xfa,
                   'CONTROL': 0x0
                    }
                   
    def __call__(self, func):
        @wraps(func)
        def wrapper (*args, **kwargs):
            self.dev, kw_result = func(*args, **kwargs)
            #build result field
            if (self.opcode == 0xf):        
                #merge result field   (LBA_LOW)
                self.kw = dict(self.kw, **kw_result)
            else:
                ##create new key word LBA_LOW
                self.kw['LBA_LOW'] = 0x0
            sg.SCSI_ATA_PASS_TRHU_12(self.dev, self.kw)()
        return wrapper
        
    def __get_cdb1(self):
        return self.protocol << 1
        