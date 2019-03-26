#----------------------------------------------------------------------------
# SCSI-ATA Pass Through
# Created by: Yu Wang (ivanwang@marvell.com)
# Created at: Fri March  22 14:28:06 CST 2019
#----------------------------------------------------------------------------

# Command Protocol
ATA_HW_RST         = 0x0
ATA_SW_RST         = 0x1

NON_DATA           = 0x3
PIO_DATA_IN        = 0x4
PIO_DATA_OUT       = 0x5
DMA                = 0x6
DMA_QUEUED         = 0x7
EXE_DEV_DIAG       = 0x8
NON_DATA_CMD_D_RST = 0x9
UDMA_DATA_IN       = 0xa
UDMA_DATA_OUT      = 0xb
FPDMA              = 0xc

RETURN_RESP_INFO   = 0xf