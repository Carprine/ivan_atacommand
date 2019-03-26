#----------------------------------------------------------------------------
# SCSI-ATA Pass Through
# Created by: Yu Wang (ivanwang@marvell.com)
# Created at: Fri March  22 15:06:09 CST 2019
#----------------------------------------------------------------------------

import scsi_ata_xlat as m
import atacmds as ata 

@ata.ATA_MARVELL_SV_FAh(0xf)
def report_test_result_FAh(dev, valid, error):
    res_field = (valid & 0x1) + ((error & 0xf)<<1)
    kw = {'LBA_LOW': res_field}
    return dev, kw
    


report_test_result_FAh('/dev/sdb', 1, 0)
report_test_result_FAh('/dev/sdb', 1, 0xf)
1111
