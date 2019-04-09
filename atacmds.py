#----------------------------------------------------------------------------
# SCSI-ATA Pass Through
# Created by: Yu Wang (ivanwang@marvell.com)
# Created at: Fri March  22 14:18:20 CST 2019
#----------------------------------------------------------------------------

import ata_info as info
from scsi_ata_xlat import SCSI_ATA_PASS_TRHU_12
from functools import wraps

class ATA_MARVELL_SV_FAh(SCSI_ATA_PASS_TRHU_12):
    r"""
    CMD FAh: Marvell SV Test Vendor Command
    
    This class is used as decorator only, with specified params 
    sub_opcode, ata protocol. See more in ata_common_func.py.
    The decorated func must return a str type dev name, and a keyword
    with key 'LBA_LOW', which in sub_opcode 0xf means result field.
      
    
    @sub_opcode : 0xf need to be specified when sending test report
    to device.
        @ res_field = (valid & 0x1) + ((error & 0xf)<<1)
    
    @ata protocol : defalt by NON_DATA
    
    """
    
    def __init__(self, sub_opc, protcl = info.NON_DATA):
        super(ATA_MARVELL_SV_FAh, self).__init__(protcl)
        self.sub_opcode = sub_opc

        #fixed cdb in ATA Command 0xFA
        self.child_cdb = {
                   'CDB_2': 0x0,
                   'FEATURES': 0x0,
                   'SECTOR_COUNT': self.sub_opcode,
                   'LBA_MID': 0x0, 
                   'LBA_HIGH': 0x0,
                   'COMMAND': 0xfa
                    }
                   
    def __call__(self, func):
        @wraps(func)
        def wrapper (*args, **kwargs):
            self.dev, kw_result = func(*args, **kwargs)
            #build result field
            if (self.sub_opcode == 0xf):        
                #merge result field   (LBA_LOW)
                self.child_cdb = dict(self.child_cdb, **kw_result)
            else:
                ##create new key word LBA_LOW
                self.child_cdb['LBA_LOW'] = 0x0
            self.exe_shell()
        return wrapper

        
class ATA_WRITE_DMA_CAh(SCSI_ATA_PASS_TRHU_12):
    r"""
    CMD CAh: ATA DMA Write
    
    This class is used as decorator only, with specified params  ata 
    protocol. See more in ata_common_func.py.
    The decorated func must return a str type dev, i_file ,bs and 
    kw with key 'LBA_LOW', 'LBA_MID', 'LBA_HIGH', 'SECTOR_COUNT'
    
    @ata protocol : defalt by DMA
    @i_file :  input file name 
    @bs : block size (512)
    
    """
    def __init__(self , protcl = info.DMA, block = 1, length_mode = 2, dir = 0):
        super(ATA_WRITE_DMA_CAh, self).__init__(protcl)
        self.block = block   # block mode
        self.length_mode = length_mode  # xfer length is specified in SECTOR_COUNT field
        self.dir = dir # xfer direction is WRITE 
        self.child_cdb = {
                    'CDB_2': ((self.dir << 3) + (self.block << 2) + self.length_mode),
                    'FEATURES': 0x0,
                    'COMMAND': 0xca
                    }
                    
    def __call__(self, func):
        @wraps(func)
        def wrapper (*args, **kwargs):
            self.dev, i_file, bs, kw = func(*args, **kwargs)
            count = kw.get('SECTOR_COUNT', 0)
            if (self.block == 1): # block mode
                xfer_size = count * bs  
            self.params = '-i {file} -s {size} '.format(file = i_file, size = xfer_size)
            self.child_cdb = dict(self.child_cdb, **kw)
            self.exe_shell()
        return wrapper
        
class ATA_READ_DMA_C8h(SCSI_ATA_PASS_TRHU_12):
    r"""
    CMD C8h: ATA DMA Read
    
    This class is used as decorator only, with specified params  ata 
    protocol. See more in ata_common_func.py.
    The decorated func must return a str type dev, o_file ,bs and 
    kw with key 'LBA_LOW', 'LBA_MID', 'LBA_HIGH', 'SECTOR_COUNT'
    
    @ata protocol : defalt by DMA
    @o_file :  output file name 
    @bs : block size (512)
    
    """
    def __init__(self , protcl = info.DMA, block = 1, length_mode = 2, dir = 1):
        super(ATA_READ_DMA_C8h, self).__init__(protcl)
        self.block = block   # block mode
        self.length_mode = length_mode  # xfer length is specified in SECTOR_COUNT field
        self.dir = dir # xfer direction is READ 
        self.child_cdb = {
                    'CDB_2': ((self.dir << 3) + (self.block << 2) + self.length_mode),
                    'FEATURES': 0x0,
                    'COMMAND': 0xc8
                    }
                    
    def __call__(self, func):
        @wraps(func)
        def wrapper (*args, **kwargs):
            self.dev, o_file, bs, kw = func(*args, **kwargs)
            count = kw.get('SECTOR_COUNT', 0)
            if (self.block == 1): # block mode
                xfer_size = count * bs  
            self.params = '-o {file} -r {size} '.format(file = o_file, size = xfer_size)
            self.child_cdb = dict(self.child_cdb, **kw)
            self.exe_shell()
        return wrapper