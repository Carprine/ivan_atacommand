#----------------------------------------------------------------------------
# SCSI-ATA Pass Through
# Created by: Yu Wang (ivanwang@marvell.com)
# Created at: Fri March  22 10:18:29 CST 2019
#----------------------------------------------------------------------------

import os
import ata_info as info 

class SCSI_ATA_PASS_TRHU_12(object):
    def __init__(self, dev, kw):
        self.dev = dev
        self.kw = kw
        self.scsi_opc = {'SCSI_OPC': 0xa1}
        if not self.kw.get('SCSI_OPC', False):
            self.kw = dict(self.kw , **self.scsi_opc) 
        self.kw['RESERVED'] = 0x0
       
        # dec to hex
        for key in self.kw:
            self.kw[key] = hex(self.kw[key])
        
            
        
        '''
        self.cdb1 = kw.get('CDB_1')
        self.cdb2 = kw.get('CDB_2')
        self.features = kw.get('FEATURES')
        self.sector_count = kw.get('SECTOR_COUNT')
        self.lba_low = kw.get('LBA_LOW')
        self.lba_mid = kw.get('LBA_MID')
        self.lba_high = kw.get('LBA_HIGH')
        self.device = kw.get('DEVICE')
        self.command = kw.get('COMMAND')
        self.reserved = 0x0
        self.control = kw.get('CONTROL')
        '''
    def __call__(self):
        cmd1 = 'sg_raw {dev} {cdb0} {cdb1} {cdb2} {cdb3} {cdb4} '.format(dev = self.dev, 
            cdb0 = self.kw.get('SCSI_OPC') , cdb1 = self.kw.get('CDB_1'),
            cdb2 = self.kw.get('CDB_2'), cdb3 = self.kw.get('FEATURES'), 
            cdb4 = self.kw.get('SECTOR_COUNT'))     
        cmd2 = '{cdb5} {cdb6} {cdb7} {cdb8} {cdb9} {cdb10} {cdb11}'.format(cdb5 = self.kw.get('LBA_LOW'), 
            cdb6 = self.kw.get('LBA_MID'), cdb7 = self.kw.get('LBA_HIGH'), 
            cdb8 = self.kw.get('DEVICE'), cdb9 = self.kw.get('COMMAND'), 
            cdb10 = self.kw.get('RESERVED'), cdb11 = self.kw.get('CONTROL'))
        cmd = cmd1 + cmd2
        print (cmd)
        os.system(cmd)
            