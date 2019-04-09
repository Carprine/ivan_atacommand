#----------------------------------------------------------------------------
# SCSI-ATA Pass Through
# Created by: Yu Wang (ivanwang@marvell.com)
# Created at: Fri March  22 10:18:29 CST 2019
#----------------------------------------------------------------------------

import os
import ata_info as info 

class SCSI_ATA_PASS_TRHU_12(object):
    r"""
    SCSI CMD: ATA-PASS-TRHU 0xA1
    
    This is a sg_raw based tool.
    
    This base class is used to construct 28bit ATA commands.
    All derived class specifing a ATA CMD is used as a decorator to
    construct and initiate sg_raw command line with parameters and
    command descriptor block(CDB). 
    
    Class params:
    @protcl : ATA Protocl     
    
    Derived class must construct child cdb dictionary with following 
    key:
    @'CDB_2' @'FEATURES' @'SECTOR_COUNT' @'LBA_MID' @'LBA_LOW'
    @'LBA_HIGH' @'COMMAND'
       
    See more in 12.2.2 ATA PASS-THROUGH(12) Command (Page 123 in doc
    Working Draft SCSI/ATA Translation)
    
    """
    def __init__(self, protcl):
        self.tool = 'sg_raw '
        self.dev = ''
        self.params = ''
        self.multiple_count = 0  ##only for ATA_READ_MULTIPLE & ATA_READ_MULTIPLE_EXT
        self.cdb1 = self._get_cdb1(protcl)
        self.father_cdb = {'SCSI_OPC': 0xa1, 'RESERVED': 0x0, 'CDB_1': self.cdb1,
                            'DEVICE': 0x0, 'CONTROL': 0x0}
        self.child_cdb = {}             

    def _get_cdb1(self, protcl):
        return (protcl << 1) + (self.multiple_count << 5)
        
    def exe_shell(self):
        # merge cdb
        self.kw = dict(self.father_cdb, **self.child_cdb)
        # dec to hex
        for key in self.kw:
            self.kw[key] = hex(self.kw[key])
            
        cdb_part1 ='{cdb0} {cdb1} {cdb2} {cdb3} {cdb4} '.format( 
            cdb0 = self.kw.get('SCSI_OPC') , cdb1 = self.kw.get('CDB_1'),
            cdb2 = self.kw.get('CDB_2'), cdb3 = self.kw.get('FEATURES'), 
            cdb4 = self.kw.get('SECTOR_COUNT')) 
            
        cdb_part2 = '{cdb5} {cdb6} {cdb7} {cdb8} {cdb9} {cdb10} {cdb11}'.format(
            cdb5 = self.kw.get('LBA_LOW'), cdb6 = self.kw.get('LBA_MID'), 
            cdb7 = self.kw.get('LBA_HIGH'), cdb8 = self.kw.get('DEVICE'), 
            cdb9 = self.kw.get('COMMAND'), cdb10 = self.kw.get('RESERVED'), 
            cdb11 = self.kw.get('CONTROL'))
        
        cmd = self.tool + self.params + self.dev + ' ' + cdb_part1 + cdb_part2

        print (cmd)
        os.system(cmd)
            