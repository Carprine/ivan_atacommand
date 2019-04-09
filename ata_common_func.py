#----------------------------------------------------------------------------
# SCSI-ATA Pass Through
# Created by: Yu Wang (ivanwang@marvell.com)
# Created at: Fri March  22 15:06:09 CST 2019
#----------------------------------------------------------------------------

import ata_info as info
import scsi_ata_xlat as m
import atacmds as cmd

@cmd.ATA_MARVELL_SV_FAh(0xf, info.NON_DATA)
def report_test_result_FAh(dev, valid, error):
    res_field = (valid & 0x1) + ((error & 0xf)<<1)
    kw = {'LBA_LOW': res_field}
    return dev, kw
    
@cmd.ATA_WRITE_DMA_CAh(info.DMA)
def write_dma_CAh(dev, i_file, count, lba24, bs = 512):
    kw = {
        'LBA_LOW': (lba24 & 0xff),
        'LBA_MID': ((lba24 >> 8) & 0xff),
        'LBA_HIGH': ((lba24 >> 16) & 0xff),
        'SECTOR_COUNT': count
        }
    return dev, i_file, bs, kw

@cmd.ATA_READ_DMA_C8h(info.DMA)
def read_dma_C8h(dev, o_file, count, lba24, bs = 512):
    kw = {
        'LBA_LOW': (lba24 & 0xff),
        'LBA_MID': ((lba24 >> 8) & 0xff),
        'LBA_HIGH': ((lba24 >> 16) & 0xff),
        'SECTOR_COUNT': count
        }
    return dev, o_file, bs, kw

    
#write_dma_CAh('/dev/sdb', 'input.txt', 32, 0)
#read_dma_C8h('/dev/sdb', 'output.txt', 32, 0)