# -*- coding: utf-8 -*-

# Python3 compatiability
from __future__ import print_function
import sys
if sys.version_info > (3,):
    xrange = range
    long = int
    import dbm
else:
    import anydbm as dbm

"""
Module that contains common values found in the MCS Joint Release 5 header file
src/exec/me.h and other functions useful for working with the MCS metadata.  
The header file values are:
 * ME_SSMIF_FORMAT_VERSION - SSMIF format version code
 * ME_MAX_NSTD - Maximum number of stands that can be described
 * ME_MAX_NFEE - Maximum number of FEEs that can be described
 * ME_MAX_FEEID_LENGTH - Number of characters in FEE ID name
 * ME_MAX_RACK - Maximum number of racks?
 * ME_MAX_PORT - Maximum number of ports?
 * ME_MAX_NRPD - Maxmimum number of RPD cables
 * ME_MAX_RPDID_LENGTH - Number of characters in the RPD ID name
 * ME_MAX_NSEP - Maximum number of SEP cable connections
 * ME_MAX_SEPID_LENGTH - Number of characters in the SEP ID name
 * ME_MAX_SEPCABL_LENGTH - Number of characters in the SEP cable ID name
 * ME_MAX_NARB - Maximum number of ARX boards
 * ME_MAX_NARBCH - Number of ARX channels per board
 * ME_MAX_ARBID_LENGTH - Number of characters in the ARX ID name
 * ME_MAX_NROACH - Maximum number of ROACH boards
 * ME_MAX_NROACHCH - Number of channels per ROACH board
 * ME_MAX_ROACHID_LENGTH - Number of characters in the ROACH board ID name
 * ME_MAX_NSERVER - Maximum number of servers
 * ME_MAX_SERVERID_LENGTH - Number of characters in the server ID name
 * ME_MAX_NDR - Maximum number of data recorders
 * ME_MAX_DRID_LENGTH - Number of characters in the DR ID name
 * ME_MAX_NPWRPORT - Maximum number of power ports
 * ME_MAX_SSNAME_LENGTH - Number of characters in the power port ID names, for 
                          codes used for PWR_NAME
 * LWA_MAX_NSTD - Maximum number of stands for the LWA
 * MIB_REC_TYPE_BRANCH - eType for MIB branch entries
 * MIB_REC_TYPE_VALUE - etype for MIB value entries
 * MIB_INDEX_FIELD_LENGTH - Number of characters in a MIB index field
 * MIB_LABEL_FIELD_LENGTH - Number of characters in a MIB label field
 * MIB_VAL_FIELD_LENGTH - Number of characters in a MIB value field
 * SSMIF_STRUCT - String representing the C structure of the binary SSMIF

The other functions:
 * Parse the binary packed metadata, 
"""

import re
import aipy
import math
import numpy
import ctypes
import struct
from datetime import datetime

from lsl.common import adp as adpCommon


__version__ = '0.1'
__revision__ = '$Rev: 2644 $'
__all__ = ['ME_SSMIF_FORMAT_VERSION', 'ME_MAX_NSTD', 'ME_MAX_NFEE', 'ME_MAX_FEEID_LENGTH', 'ME_MAX_RACK', 'ME_MAX_PORT', 
            'ME_MAX_NRPD', 'ME_MAX_RPDID_LENGTH', 'ME_MAX_NSEP', 'ME_MAX_SEPID_LENGTH', 'ME_MAX_SEPCABL_LENGTH', 
            'ME_MAX_NARB', 'ME_MAX_NARBCH', 'ME_MAX_ARBID_LENGTH', 'ME_MAX_NROACH', 'ME_MAX_NROACHCH', 'ME_MAX_ROACHID_LENGTH', 
            'ME_MAX_NSERVER', 'ME_MAX_SERVERID_LENGTH', 'ME_MAX_NDR', 'ME_MAX_DRID_LENGTH', 'ME_MAX_NPWRPORT', 
            'ME_MAX_SSNAME_LENGTH', 'LWA_MAX_NSTD', 'MIB_REC_TYPE_BRANCH', 'MIB_REC_TYPE_VALUE', 'MIB_INDEX_FIELD_LENGTH', 
            'MIB_LABEL_FIELD_LENGTH', 'MIB_VAL_FIELD_LENGTH', 'IS_32BIT_PYTHON', 
            'SSMIF_STRUCT', 'STATION_SETTINGS_STRUCT', 'SUBSYSTEM_STATUS_STRUCT', 'SUBSUBSYSTEM_STATUS_STRUCT', 
            'SSF_STRUCT', 'OSF_STRUCT', 'OSFS_STRUCT', 'BEAM_STRUCT', 'OSF2_STRUCT', 
            'delaytoMCSD', 'MCSDtodelay', 'gaintoMCSG', 'MCSGtogain',
            'mjdmpm2datetime', 'datetime2mjdmpm', 'status2string', 'summary2string', 'sid2string', 'cid2string', 
            'mode2string', 'parseCStruct', 'single2multi', 'applyPointingCorrection', 'MIB', 'MIBEntry', 
            '__version__', '__revision__', '__all__']


ME_SSMIF_FORMAT_VERSION = 8	# SSMIF format version code
ME_MAX_NSTD = 256			# Maximum number of stands that can be described
ME_MAX_NFEE = 256			# Maximum number of FEEs that can be described
ME_MAX_FEEID_LENGTH = 10		# Number of characters in FEE ID name
ME_MAX_RACK = 6			# Maximum number of racks?
ME_MAX_PORT = 50			# Maximum number of ports?
ME_MAX_NRPD = 512			# Maxmimum number of RPD cables
ME_MAX_RPDID_LENGTH = 25		# Number of characters in the RPD ID name
ME_MAX_NSEP = 512			# Maximum number of SEP cable connections
ME_MAX_SEPID_LENGTH = 25		# Number of characters in the SEP ID name
ME_MAX_SEPCABL_LENGTH = 25	# Number of characters in the SEP cable ID name
ME_MAX_NARB = 32			# Maximum number of ARX boards
ME_MAX_NARBCH = 16			# Number of ARX channels per board
ME_MAX_ARBID_LENGTH = 10		# Number of characters in the ARX ID name
ME_MAX_NROACH = 16			# Maximum number of ROACH boards
ME_MAX_NROACHCH = 32		# Number of channels per ROACH board
ME_MAX_ROACHID_LENGTH = 10	# Number of characters in the ROACH board ID name
ME_MAX_NSERVER = 7			# Maximum number of server
ME_MAX_SERVERID_LENGTH = 10	# Number of characters in the server ID name
ME_MAX_NDR = 2				# Maximum number of data recorders
ME_MAX_DRID_LENGTH = 10		# Number of characters in the DR ID name
ME_MAX_NPWRPORT = 50		# Maximum number of power ports
ME_MAX_SSNAME_LENGTH = 3		# Number of characters in the power port ID names, for codes used for PWR_NAME
LWA_MAX_NSTD = 256			# Maximum number of stands for the LWA
TPSS_FORMAT_VERSION = 6		# MCS0030 format version code
MIB_REC_TYPE_BRANCH = 0 		# eType for MIB branch entries
MIB_REC_TYPE_VALUE = 1 		# etype for MIB value entries
MIB_INDEX_FIELD_LENGTH = 12	# Number of characters in a MIB index field
MIB_LABEL_FIELD_LENGTH = 32	# Number of characters in a MIB label field
MIB_VAL_FIELD_LENGTH = 8192	# Number of characters in a MIB value field


IS_32BIT_PYTHON = True if struct.calcsize("P") == 4 else False


SSMIF_STRUCT = """
    int    iFormatVersion;           /* FORMAT_VERSION */
    char   sStationID[3];            /* STATION_ID */
    double fGeoN;                    /* GEO_N */
    double fGeoE;                    /* GEO_E */
    double fGeoEl;                   /* GEO_EL */
    int    nStd;                     /* N_STD */
    double fStdLx[ME_MAX_NSTD];      /* STD_LX[] */
    double fStdLy[ME_MAX_NSTD];      /* STD_LY[] */
    double fStdLz[ME_MAX_NSTD];      /* STD_LZ[] */
    int    iAntStd[2*ME_MAX_NSTD];   /* ANT_STD[] */
    int    iAntOrie[2*ME_MAX_NSTD];  /* ANT_ORIE[] */
    int    iAntStat[2*ME_MAX_NSTD];  /* ANT_STAT[] */
    float  fAntTheta[2*ME_MAX_NSTD]; /* ANT_THETA[] */
    float  fAntPhi[2*ME_MAX_NSTD];   /* ANT_PHI[] */
    int    eAntDesi[2*ME_MAX_NSTD];  /* ANT_DESI[] */
    %s
    int    nFEE;                     /* N_FEE */
    char   sFEEID[ME_MAX_NFEE][ME_MAX_FEEID_LENGTH+1]; /* FEE_ID[] */
    int    iFEEStat[ME_MAX_NFEE];    /* FEE_STAT[] */
    int    eFEEDesi[ME_MAX_NFEE];    /* FEE_DESI[] */
    float  fFEEGai1[ME_MAX_NFEE];    /* FEE_GAI1[] */
    float  fFEEGai2[ME_MAX_NFEE];    /* FEE_GAI2[] */
    int    iFEEAnt1[ME_MAX_NFEE];    /* FEE_ANT1[] */
    int    iFEEAnt2[ME_MAX_NFEE];    /* FEE_ANT2[] */
    int    iFEERack[ME_MAX_NFEE];    /* FEE_RACK[] */
    int    iFEEPort[ME_MAX_NFEE];    /* FEE_PORT[] */
    int    nRPD;                     /* N_RPD */
    char   sRPDID[ME_MAX_NRPD][ME_MAX_RPDID_LENGTH+1]; /* RPD_ID[] */
    int    iRPDStat[ME_MAX_NRPD];    /* RPD_STAT[] */
    int    eRPDDesi[ME_MAX_NRPD];    /* RPD_DESI[] */
    float  fRPDLeng[ME_MAX_NRPD];    /* RPD_LENG[] */
    float  fRPDVF[ME_MAX_NRPD];      /* RPD_VF[] */
    float  fRPDDD[ME_MAX_NRPD];      /* RPD_DD[] */
    float  fRPDA0[ME_MAX_NRPD];      /* RPD_A0[] */
    float  fRPDA1[ME_MAX_NRPD];      /* RPD_A1[] */
    float  fRPDFref[ME_MAX_NRPD];    /* RPD_FREF[] */
    float  fRPDStr[ME_MAX_NRPD];     /* RPD_STR[] */
    int    iRPDAnt[ME_MAX_NRPD];     /* RPD_ANT[] */
    int    nSEP;                     /* N_SEP */
    char   sSEPID[ME_MAX_NSEP][ME_MAX_SEPID_LENGTH+1]; /* SEP_ID[] */
    int    iSEPStat[ME_MAX_NSEP];    /* SEP_STAT[] */
    char   sSEPCabl[ME_MAX_NSEP][ME_MAX_SEPCABL_LENGTH+1]; /* SEP_Cabl[] */
    float  fSEPLeng[ME_MAX_NSEP];    /* SEP_LENG[] */
    int    eSEPDesi[ME_MAX_NSEP];    /* SEP_DESI[] */
    float  fSEPGain[ME_MAX_NSEP];    /* SEP_GAIN[] */
    int    iSEPAnt[ME_MAX_NSEP];     /* SEP_ANT[] */
    int    nARB;                     /* N_ARB */
    int    nARBCH;                   /* N_ARBCH */
    char   sARBID[ME_MAX_NARB][ME_MAX_ARBID_LENGTH+1]; /* ARB_ID[] */
    int    iARBSlot[ME_MAX_NARB];    /* ARB_SLOT[] */
    int    eARBDesi[ME_MAX_NARB];    /* ARB_DESI[] */
    int    iARBRack[ME_MAX_NARB];    /* ARB_RACK[] */
    int    iARBPort[ME_MAX_NARB];    /* ARB_PORT[] */
    int    eARBStat[ME_MAX_NARB][ME_MAX_NARBCH];       /* ARB_STAT[][] */
    float  fARBGain[ME_MAX_NARB][ME_MAX_NARBCH];        /* ARB_GAIN[][] */
    int    iARBAnt[ME_MAX_NARB][ME_MAX_NARBCH];        /* ARB_ANT[][] */
    char   sARBIN[ME_MAX_NARB][ME_MAX_NARBCH][ME_MAX_ARBID_LENGTH+1]; /* ARB_IN[][] */
    char   sARBOUT[ME_MAX_NARB][ME_MAX_NARBCH][ME_MAX_ARBID_LENGTH+1]; /* ARB_OUT[][] */
    int    nRoach;                     /* N_ROACH */
    int    nRoachCh;                   /* N_ROACHCH */
    char   sRoachID[ME_MAX_NROACH][ME_MAX_ROACHID_LENGTH+1]; /* ROACH_ID[] */
    char   sRoachSlot[ME_MAX_NROACH][ME_MAX_ROACHID_LENGTH+1]; /* ROACH_SLOT[] */
    int    eRoachDesi[ME_MAX_NROACH]; /* ROACH_DESI[] */
    int    eRoachStat[ME_MAX_NROACH][ME_MAX_NROACHCH];       /* ROACH_STAT[][] */
    char   sRoachINR[ME_MAX_NROACH][ME_MAX_NROACHCH][ME_MAX_ROACHID_LENGTH+1]; /* ROACH_INR[][] */
    char   sRoachINC[ME_MAX_NROACH][ME_MAX_NROACHCH][ME_MAX_ROACHID_LENGTH+1]; /* ROACH_INC[][] */
    int    iRoachAnt[ME_MAX_NROACH][ME_MAX_NROACHCH];        /* ROACH_ANT[][] */
    int    nServer;                     /* N_SERVER */
    char   sServerID[ME_MAX_NSERVER][ME_MAX_SERVERID_LENGTH+1]; /* SERVER_ID[] */
    char   sServerSlot[ME_MAX_NSERVER][ME_MAX_SERVERID_LENGTH+1]; /* SERVER_SLOT[] */
    int    eServerStat[ME_MAX_NSERVER];       /* SERVER_STAT[] */
    int    eServerDesi[ME_MAX_NSERVER];       /* SERVER_DESI[] */
    int    nDR;                     /* N_DR */
    int    eDRStat[ME_MAX_NDR];       /* DR_STAT[] */
    char   sDRID[ME_MAX_NDR][ME_MAX_DRID_LENGTH+1]; /* DR_ID[] */
    char   sDRPC[ME_MAX_NDR][ME_MAX_DRID_LENGTH+1]; /* DR_PC[] */
    int    iDRDP[ME_MAX_NDR];       /* DR_DP[] */
    int    nPwrRack;                /* N_PWR_RACK */
    int    nPwrPort[ME_MAX_RACK];   /* N_PWR_PORT[] */
    int    ePwrSS[ME_MAX_RACK][ME_MAX_NPWRPORT]; /* PWR_SS[][], converted to a LWA_SID_ value */
    char   sPwrName[ME_MAX_RACK][ME_MAX_NPWRPORT][ME_MAX_SSNAME_LENGTH+1]; /* PWR_NAME[][] */
    int    eCRA;                /* MCS_CRA */
    float  fPCAxisTh; /* PC_AXIS_TH */
    float  fPCAxisPh; /* PC_AXIS_PH */
    float  fPCRot;    /* PC_ROT */
""" % ("short int junk;\n" if IS_32BIT_PYTHON else "")


STATION_SETTINGS_STRUCT = """
    signed short int mrp_asp; // SESSION_MRP_ASP // MRP_ASP
    signed short int mrp_dp;  // SESSION_MRP_DP_ // MRP_DP_
    signed short int mrp_dr1; // SESSION_MRP_DR1 // MRP_DR1
    signed short int mrp_dr2; // SESSION_MRP_DR2 // MRP_DR2
    signed short int mrp_dr3; // SESSION_MRP_DR3 // MRP_DR3
    signed short int mrp_dr4; // SESSION_MRP_DR4 // MRP_DR4
    signed short int mrp_dr5; // SESSION_MRP_DR5 // MRP_DR5
    signed short int mrp_shl; // SESSION_MRP_SHL // MRP_SHL
    signed short int mrp_mcs; // SESSION_MRP_MCS // MRP_MCS
    signed short int mup_asp; // SESSION_MUP_ASP // MUP_ASP
    signed short int mup_dp;  // SESSION_MUP_DP_ // MUP_DP_
    signed short int mup_dr1; // SESSION_MUP_DR1 // MUP_DR1
    signed short int mup_dr2; // SESSION_MUP_DR2 // MUP_DR2
    signed short int mup_dr3; // SESSION_MUP_DR3 // MUP_DR3
    signed short int mup_dr4; // SESSION_MUP_DR4 // MUP_DR4
    signed short int mup_dr5; // SESSION_MUP_DR5 // MUP_DR5
    signed short int mup_shl; // SESSION_MUP_SHL // MUP_SHL
    signed short int mup_mcs; // SESSION_MUP_MCS // MUP_MCS
    signed short int fee[LWA_MAX_NSTD];     // OBS_FEE[LWA_MAX_NSTD][2]  // FEE[LWA_MAX_NSTD]
    signed short int asp_flt[LWA_MAX_NSTD]; // OBS_ASP_FLT[LWA_MAX_NSTD] // ASP_FLT[LWA_MAX_NSTD]
    signed short int asp_at1[LWA_MAX_NSTD]; // OBS_ASP_AT1[LWA_MAX_NSTD] // ASP_AT1[LWA_MAX_NSTD]
    signed short int asp_at2[LWA_MAX_NSTD]; // OBS_ASP_AT2[LWA_MAX_NSTD] // ASP_AT2[LWA_MAX_NSTD]
    signed short int asp_ats[LWA_MAX_NSTD]; // OBS_ASP_ATS[LWA_MAX_NSTD] // ASP_ATS[LWA_MAX_NSTD]
    signed short int tbf_gain; // OBS_TBF_GAIN // TBF_GAIN
    signed short int tbn_gain; // OBS_TBN_GAIN // TBN_GAIN
    signed short int drx_gain; // OBS_DRX_GAIN // DRX_GAIN
"""


SUBSYSTEM_STATUS_STRUCT = """
    int summary;
    %s
    char info[256];
    long tv[2];
""" % ("short int junk;\n" if IS_32BIT_PYTHON else "",)


SUBSUBSYSTEM_STATUS_STRUCT = """
    int    eFEEStat[ME_MAX_NFEE];                      /* FEE_STAT[] */
    int    eRPDStat[ME_MAX_NRPD];                      /* RPD_STAT[] */
    int    eSEPStat[ME_MAX_NSEP];                      /* SEP_STAT[] */
    int    eARBStat[ME_MAX_NARB][ME_MAX_NARBCH];       /* ARB_STAT[][] */
    int    eRoachStat[ME_MAX_NROACH][ME_MAX_NROACHCH]; /* ROACH_STAT[][] */
    int    eServerStat[ME_MAX_NSERVER];                /* SERVER_STAT[] */
    int    eDRStat[ME_MAX_NDR];                        /* DR_STAT[] */
"""


SSF_STRUCT = """
    unsigned short int FORMAT_VERSION;
    char PROJECT_ID[9];
    unsigned int SESSION_ID;
    unsigned short int SESSION_CRA;
    signed short int SESSION_DRX_BEAM;
    char SESSION_SPC[32];
    %s
    unsigned long int SESSION_START_MJD;
    unsigned long int SESSION_START_MPM;
    unsigned long int SESSION_DUR;
    unsigned int SESSION_NOBS;
    signed short int SESSION_MRP_ASP;
    signed short int SESSION_MRP_DP_;
    signed short int SESSION_MRP_DR1;
    signed short int SESSION_MRP_DR2;
    signed short int SESSION_MRP_DR3;
    signed short int SESSION_MRP_DR4;
    signed short int SESSION_MRP_DR5;
    signed short int SESSION_MRP_SHL;
    signed short int SESSION_MRP_MCS;
    signed short int SESSION_MUP_ASP;
    signed short int SESSION_MUP_DP_;
    signed short int SESSION_MUP_DR1;
    signed short int SESSION_MUP_DR2;
    signed short int SESSION_MUP_DR3;
    signed short int SESSION_MUP_DR4;
    signed short int SESSION_MUP_DR5;
    signed short int SESSION_MUP_SHL;
    signed short int SESSION_MUP_MCS;
    signed char SESSION_LOG_SCH;
    signed char SESSION_LOG_EXE;
    signed char SESSION_INC_SMIB;
    signed char SESSION_INC_DES;
""" % ("short int junk;\n" if IS_32BIT_PYTHON else "",)


OSF_STRUCT = """
    unsigned short int FORMAT_VERSION;
    char               PROJECT_ID[9];
    unsigned int       SESSION_ID;
    signed short int   SESSION_DRX_BEAM;
    char               SESSION_SPC[32];
    unsigned int       OBS_ID; 
    unsigned long int  OBS_START_MJD;
    unsigned long int  OBS_START_MPM;
    unsigned long int  OBS_DUR;
    unsigned short int OBS_MODE;
    char               OBS_BDM[32];  /* added 140310 */
    float              OBS_RA;
    float              OBS_DEC;
    unsigned short int OBS_B;
    unsigned int       OBS_FREQ1;
    unsigned int       OBS_FREQ2;
    unsigned short int OBS_BW;
    unsigned int       OBS_STP_N;
    unsigned short int OBS_STP_RADEC;
"""


OSFS_STRUCT = """
    float              OBS_STP_C1;
    float              OBS_STP_C2;
    unsigned int       OBS_STP_T;
    unsigned int       OBS_STP_FREQ1;
    unsigned int       OBS_STP_FREQ2;
    unsigned short int OBS_STP_B;
"""


BEAM_STRUCT = """
    unsigned short int OBS_BEAM_DELAY[2*LWA_MAX_NSTD];
    signed short int   OBS_BEAM_GAIN[LWA_MAX_NSTD][2][2];
"""


OSF2_STRUCT = """
    signed short int   OBS_FEE[LWA_MAX_NSTD][2];
    signed short int   OBS_ASP_FLT[LWA_MAX_NSTD];
    signed short int   OBS_ASP_AT1[LWA_MAX_NSTD];
    signed short int   OBS_ASP_AT2[LWA_MAX_NSTD];
    signed short int   OBS_ASP_ATS[LWA_MAX_NSTD];
    unsigned int       OBS_TBF_SAMPLES;
    signed short int   OBS_TBF_GAIN;
    signed short int   OBS_TBN_GAIN;
    signed short int   OBS_DRX_GAIN;
    unsigned int       alignment;
"""


_cDecRE = re.compile(r'(?P<type>[a-z][a-z \t]+)[ \t]+(?P<name>[a-zA-Z_0-9]+)(\[(?P<d1>[\*\+A-Z_\d]+)\])?(\[(?P<d2>[\*\+A-Z_\d]+)\])?(\[(?P<d3>[\*\+A-Z_\d]+)\])?(\[(?P<d4>[\*\+A-Z_\d]+)\])?;')


def parseCStruct(cStruct, charMode='str', endianness='native'):
    """
    Function to take a C structure declaration and build a ctypes.Structure out 
    of it with the appropriate alignment, character interpretation*, and endianness
    (little, big, network, or native).
    
    .. note::  ctypes converts character arrays to Python strings until the first null is
    incountered.  This behavior causes problems for multi-dimension arrays of null
    filled strings.  By setting charMode to 'int', all char types are retuned as 
    bytes which can be converted to strings via chr().
    """
    
    # Figure out how to deal with character arrays
    if charMode not in ('str', 'int'):
        raise RuntimeError("Unknown character mode: '%s'" % charMode)
    if charMode == 'str':
        baseCharType = ctypes.c_char
    else:
        baseCharType = ctypes.c_byte
    
    # Hold the basic fields and dimensions
    fields = []
    dims2 = {}
    
    # Split into lines and go!
    cStruct = cStruct.split('\n')
    for line in cStruct:
        ## Skip structure declaration, blank lines, comments, and lines too short to hold a 
        ## declaration
        line = line.strip().rstrip()
        if '{' in line or '}' in line:
            continue
        if line[:2] == '//':
            continue
        if len(line) < 5:
            continue
            
        ## RegEx the line to find the type, name, and dimensions (if needed) for
        ## the next structure variable
        mtch = _cDecRE.search(line)
        if mtch is None:
            raise RuntimeError("Unparseable line: '%s'" % line)
        
        dec = mtch.group('type')
        dec = dec.rstrip()
        name = mtch.group('name')
        
        try:
            d1 = mtch.group('d1')
            if d1 is not None:
                d1 = eval(d1)
            d2 = mtch.group('d2')
            if d2 is not None:
                d2 = eval(d2)
            d3 = mtch.group('d3')
            if d3 is not None:
                d3 = eval(d3)
            d4 = mtch.group('d4')
            if d4 is not None:
                d4 = eval(d4)
        except NameError:
            raise RuntimeError("Unknown value in array index: '%s'" % line)
        
        ## Basic data types
        if dec in ('signed int', 'int'):
            typ = ctypes.c_int
        elif dec == 'unsigned int':
            typ = ctypes.c_uint
        elif dec in ('signed short int', 'signed short', 'short int', 'short'):
            typ = ctypes.c_short
        elif dec in ('unsigned short int', 'unsigned short'):
            typ = ctypes.c_ushort
        elif dec in ('signed long int', 'signed long', 'long int', 'long'):
            if IS_32BIT_PYTHON:
                typ = ctypes.c_longlong
            else:
                typ = ctypes.c_long
        elif dec in ('unsigned long int', 'unsigned long'):
            if IS_32BIT_PYTHON:
                typ = ctypes.c_uint64
            else:
                typ = ctypes.c_ulong
        elif dec in ('signed long long', 'long long'):
            typ = ctypes.c_longlong
        elif dec == 'unsigned long long':
            typ = ctypes.c_uint64
        elif dec == 'float':
            typ = ctypes.c_float
        elif dec == 'double':
            typ = ctypes.c_double
        elif dec == 'char':
            typ = baseCharType
        elif dec == 'signed char':
            typ = ctypes.c_byte
        elif dec == 'unsigned char':
            typ = ctypes.c_ubyte
        else:
            raise RuntimeError("Unparseable line: '%s' -> type: %s, name: %s, dims: %s, %s, %s %s" % (line, dec, name, d1, d2, d3, d4))
        
        ## Array identification and construction
        dims2[name] = []
        if d1 is not None:
            count = d1
            dims2[name].append(d1)
            
            if d2 is not None:
                count *= d2
                dims2[name].append(d2)
            if d3 is not None:
                count *= d3
                dims2[name].append(d3)
            if d4 is not None:
                count *= d4
                dims2[name].append(d4)
                
            typ *= count
        
        ## Append
        fields.append( (name, typ) )
    
    # ctypes creation - endianess
    endianness = endianness.lower()
    if endianness not in ('little', 'big', 'network', 'native'):
        raise RuntimeError("Unknown endianness: '%s'" % endianness)
    
    if endianness == 'little':
        endianness = ctypes.LittleEndianStructure
    elif endianness == 'big':
        endianness = ctypes.BigEndianStructure
    elif endianness == 'network':
        endianness = ctypes.BigEndianStructure
    else:
        endianness = ctypes.Structure
    
    # ctypes creation - actual
    class MyStruct(endianness):
        """
        ctypes.Structure of the correct endianness for the provided
        C structure.  
        
        In addition to the standard attributes defined for a ctypes.Structure 
        instance there are a few additional attributes related to the parsed C
        structure.  They are:
         * origC - String containing the original C structure
         * dims  - Dictionary of the dimensionallity of the data, if needed, 
                   keyed by variable name
        """
        
        origC = '\n'.join(cStruct)
        
        _fields_ = fields
        _pack_ = 8	# Pack it like we are 64-bit
        dims = dims2
        
        def __str__(self):
            """
            Print out the structure in a nice easy-to-read formation that
            captures the various structure elements, their data types, and 
            their values.
            """
            
            out = ''
            for f,d in self._fields_:
                out += '%s (%s): %s\n' % (f, d, eval("self.%s" % f))
            return out
            
        def sizeof(self):
            """
            Return the size, in bytes, of the structure.
            """
            
            return ctypes.sizeof(self)
            
        def returnDict(self):
            """
            Return the structure as a simple Python dictionary keyed off the
            structure elements.
            """
            
            output = {}
            for f,d in self._fields_:
                output[f] = eval("self.%s" % f)
            return output
    
    # Create and return
    return MyStruct()


def _twoByteSwap(value):
    return ((value & 0xFF) << 8) | ((value >> 8) & 0xFF)


def delaytoMCSD(delay):
    """
    Given a delay in ns, convert it to a course and fine portion and into 
    the form expected by MCS in a custom beamforming SDF (little endian 
    16.12 unsigned integer).

    .. versionadded:: 0.6.3
    """
    
    return _twoByteSwap( adpCommon.delaytoDPD(delay) )


def MCSDtodelay(delay):
    """
    Given delay value from an OBS_BEAM_DELAY field in a custom beamforming 
    SDF, return the delay in ns.

    .. versionadded:: 0.6.3
    """
    
    return adpCommon.DPDtodelay( _twoByteSwap(delay) )


def gaintoMCSG(gain):
    """
    Given a gain (between 0 and 1), convert it to a gain in the form 
    expected by MCS in a custom beamforming SDF (little endian 16.1 
    signed integer).

    .. versionadded::0.6.3
    """
    
    return _twoByteSwap( adpCommon.gaintoDPG(gain) )


def MCSGtogain(gain):
    """
    Given a gain value from an OBS_BEAM_GAIN field in a custom beamforming
    SDF, return the decimal equivalent.

    .. versionadded:: 0.6.3
    """
    
    return adpCommon.DPGtogain( _twoByteSwap(gain) )


def mjdmpm2datetime(mjd, mpm):
    """
    Convert a MJD, MPM pair to a UTC-aware datetime instance.
    
    .. versionadded:: 0.5.2
    """
    
    unix = mjd*86400.0 + mpm/1000.0 - 3506716800.0
    return datetime.utcfromtimestamp(unix)


def datetime2mjdmpm(dt):
    """
    Convert a UTC datetime instance to a MJD, MPM pair (returned as a 
    two-element tuple).
    
    Based off: http://paste.lisp.org/display/73536
    
    .. versionadded:: 0.5.2
    """
    
    year        = dt.year             
    month       = dt.month      
    day         = dt.day    

    hour        = dt.hour
    minute      = dt.minute
    second      = dt.second     
    millisecond = dt.microsecond / 1000

    # compute MJD         
    # adapted from http://paste.lisp.org/display/73536
    # can check result using http://www.csgnetwork.com/julianmodifdateconv.html
    a = (14 - month) // 12
    y = year + 4800 - a          
    m = month + (12 * a) - 3                    
    p = day + (((153 * m) + 2) // 5) + (365 * y)   
    q = (y // 4) - (y // 100) + (y // 400) - 32045
    mjdi = int(math.floor( (p+q) - 2400000.5))
    mjd = mjdi

    # compute MPM
    mpmi = int(math.floor( (hour*3600 + minute*60 + second)*1000 + millisecond ))
    mpm = mpmi
    return (mjd, mpm)


def status2string(code):
    """
    Convert a numerical MCS status code to a string.
    """
    
    # Make sure we have an integer
    code = int(code)
    
    # Loop through the options
    if code == 0:
        return "Not installed"
    elif code == 1:
        return "Bad"
    elif code == 2:
        return "Suspect, possibly bad"
    elif code == 3:
        return "OK"
    else:
        return "Unknown status code '%i'" % code


def summary2string(code):
    """
    Convert a numerical MCS overall status code to an explination.
    """
    
    if code < 0 or code > 6:
        raise ValueError("Invalid code %i" % code)
    
    if code == 0:
        return "Not normally used"
    elif code == 1:
        return "Normal"
    elif code == 2:
        return "Warning - issue(s) found, but still fully operational"
    elif code == 3:
        return "Error - problems found which limit or prevent proper function"
    elif code == 4:
        return "Booting - initializing; not yet fully operational"
    elif code == 5:
        return "Shutdown - shutting down; not ready for operation"
    else:
        return "Status is unknown"


def sid2string(sid):
    """
    Convert a MCS subsystem ID code into a string.
    """
    
    if sid < 1 or sid > 19:
        raise ValueError("Invalid sid code %i" % sid)
    
    if sid < 9:
        return "Null subsystem #%i" % sid
    elif sid == 10:
        return "MCS"
    elif sid == 11:
        return "SHL"
    elif sid == 12:
        return "ASP"
    elif sid == 14:
        return "DR #1"
    elif sid == 15:
        return "DR #2"
    elif sid == 16:
        return "DR #3"
    elif sid == 17:
        return "DR #4"
    elif sid == 18:
        return "DR #5"
    elif sid == 19:
        return "ADP"
    else:
        raise ValueError("Invalid sid code %i" % sid)


def cid2string(cid):
    """
    Convert a MCS command code into a string.
    """
    
    if cid < 0 or cid > 41:
        raise ValueError("Invalid cid code %i" % cid)
    
    if cid == 0:
        return "MCSSHT"
    elif cid == 1:
        return "PNG"
    elif cid == 2:
        return "RPT"
    elif cid == 3:
        return "SHT"
    elif cid == 4:
        return "INI"
    elif cid == 5:
        return "TMP"
    elif cid == 6:
        return "DIF"
    elif cid == 7:
        return "PWR"
    elif cid == 8:
        return "FIL"
    elif cid == 9:
        return "AT1"
    elif cid == 10:
        return "AT2"
    elif cid == 11:
        return "ATS"
    elif cid == 12:
        return "FPW"
    elif cid == 13:
        return "RXP"
    elif cid == 14:
        return "FEP"
    elif cid == 16:
        return "TBN"
    elif cid == 17:
        return "DRX"
    elif cid == 18:
        return "BAM"
    elif cid == 19:
        return "FST"
    elif cid == 20:
        return "CLK"
    elif cid == 21:
        return "REC"
    elif cid == 22:
        return "DEL"
    elif cid == 23:
        return "STP"
    elif cid == 24:
        return "GET"
    elif cid == 25:
        return "CPY"
    elif cid == 26:
        return "DMP"
    elif cid == 27:
        return "FMT"
    elif cid == 28:
        return "DWN"
    elif cid == 29:
        return "UP_"
    elif cid == 30:
        return "SEL"
    elif cid == 31:
        return "SYN"
    elif cid == 32:
        return "TST"
    elif cid == 33:
        return "BUF"
    elif cid == 34:
        return "NUL"
    elif cid == 35:
        return "ESN"
    elif cid == 36:
        return "ESF"
    elif cid == 37:
        return "OBS"
    elif cid == 38:
        return "OBE"
    elif cid == 39:
        return "SPC"
    elif cid == 40:
        return "TBF"
    elif cid == 41:
        return "COR"
    else:
        raise ValueError("Invalid cid code %i" % cid)


def mode2string(mode):
    """
    Convert a MCS numeric observing mode into a string.
    """
    
    if mode < 1 or mode > 8:
        raise ValueError("Invalid observing mode %i" % mode)
    
    if mode == 1:
        return "TRK_RADEC"
    elif mode == 2:
        return "TRK_SOL"
    elif mode == 3:
        return "TRK_JOV"
    elif mode == 4:
        return "STEPPED"
    elif mode == 6:
        return "TBN"
    elif mode == 7:
        return "DIAG1"
    elif mode == 8:
        return "TBF"
    else:
        raise ValueError("Invalid observing mode %i" % mode)


def single2multi(inputList, dim1, dim2=None, dim3=None, dim4=None):
    if dim4 is not None:
        return _single2four(inputList, dim1, dim2, dim3, dim4)
        
    elif dim3 is not None:
        return _single2three(inputList, dim1, dim2, dim3)

    elif dim2 is not None:
        return _single2two(inputList, dim1, dim2)
        
    else:
        return list(inputList)


def _single2two(inputList, dim1, dim2):
    """
    Convert a flatten list into a two-dimensional list.  This is useful
    for converting flat lists of ctypes into their two-dimensional forms.
    """
    
    if dim1*dim2 < len(inputList):
        raise ValueError("Incompatiable dimensions: input=%i, output=%i by %i" % (len(inputList), dim1, dim2))
    
    outputList = []
    for i in xrange(dim1):
        outputList.append( [None for k in xrange(dim2)] )
        for j in xrange(dim2):
            try:
                outputList[i][j] = inputList[dim2*i+j]
            except IndexError:
                pass
    
    return outputList


def _single2three(inputList, dim1, dim2, dim3):
    """
    Convert a flatten list into a three-dimensional list.  This is useful
    for converting flat lists of ctypes into their three-dimensional forms.
    """
    
    if dim1*dim2*dim3 < len(inputList):
        raise ValueError("Incompatiable dimensions: input=%i, output=%i by %i by %i" % (len(inputList), dim1, dim2, dim3))
    
    outputList = []
    for i in xrange(dim1):
        outputList.append( [[None for l in xrange(dim3)] for k in xrange(dim2)] )
        for j in xrange(dim2):
            for k in xrange(dim3):
                try:
                    outputList[i][j][k] = inputList[dim2*dim3*i+dim3*j+k]
                except IndexError:
                    pass
    
    return outputList


def _single2four(inputList, dim1, dim2, dim3, dim4):
    """
    Convert a flatten list into a four-dimensional list.  This is useful
    for converting flat lists of ctypes into their four-dimensional forms.
    """
    
    if dim1*dim2*dim3*dim4 < len(inputList):
        raise ValueError("Incompatiable dimensions: input=%i, output=%i by %i by %i by %i" % (len(inputList), dim1, dim2, dim3, dim4))
    
    outputList = []
    for i in xrange(dim1):
        outputList.append( [[[None for m in xrange(dim4)] for l in xrange(dim3)] for k in xrange(dim2)] )
        for j in xrange(dim2):
            for k in xrange(dim3):
                for l in xrange(dim4):
                    try:
                        outputList[i][j][k][l] = inputList[dim2*dim3*dim4*i+dim3*dim4*j+dim4*k+l]
                    except IndexError:
                        pass
    
    return outputList


def _getRotationMatrix(theta, phi, psi, degrees=True):
    """
    Generate the rotation matrix for a rotation about a specified axis.
    
    http://en.wikipedia.org/wiki/Rotation_matrix#Rotation_matrix_from_axis_and_angle
    """
    
    if degrees:
        theta = theta * numpy.pi/180.0
        phi   = phi * numpy.pi/180.0
        psi   = psi * numpy.pi/180.0
        
    # Axis
    u = numpy.array([numpy.cos(phi)*numpy.sin(theta), numpy.sin(phi)*numpy.sin(theta), numpy.cos(theta)])
    
    # Rotation matrix
    rot  = numpy.eye(3)*numpy.cos(psi) 
    rot += numpy.sin(psi)*numpy.array([[0, -u[2], u[1]], [u[2], 0, -u[0]], [-u[1], u[0], 0]]) 
    rot += (1-numpy.cos(psi))*numpy.tensordot(u, u, axes=0)
    
    return rot


def applyPointingCorrection(az, el, theta, phi, psi, lat=34.070, degrees=True):
    """
    Given a azimuth and elevation pair, and an axis to rotate about, 
    perform the rotation.
    
    http://en.wikipedia.org/wiki/Rotation_matrix#Rotation_matrix_from_axis_and_angle
    """
    
    # Get the rotation matrix
    rot = _getRotationMatrix(theta, phi, psi, degrees=degrees)
    
    # Convert the az,alt coordinates to the unit vector
    if degrees:
        xyz = aipy.coord.azalt2top((az*numpy.pi/180.0, el*numpy.pi/180.0))
    else:
        xyz = aipy.coord.azalt2top((az, el))
        
    # Rotate
    xyzP = numpy.dot(rot, xyz)
    
    azP, elP = aipy.coord.top2azalt(xyzP)
    if degrees:
        azP *= 180/numpy.pi
        elP *= 180/numpy.pi
        
    return azP, elP


class MIB(object):
    """
    Class to represent an entire MCS MIB.
    
    .. versionadded:: 0.6.5
    """
    
    def __init__(self):
        self.entries = {}
        self.mapper = {}
        self.invMapper = {}
        
    def __str__(self):
        """
        Describe the MIB as a string.
        """
        
        nEntry = len(self.entries.keys())
        times = [self.entries[k].updateTime for k in self.entries.keys()]
        return "MIB containing %i entries from %s to %s" % (nEntry, min(times), max(times))
        
    def __getitem__(self, key):
        """
        Allow access to the MIB through either the index of name.
        """
        
        try:
            return self.entries[key]
        except KeyError:
            return self.entries[self.invMapper[key]]
            
    def keys(self, name=False):
        """
        Return a list of entry indicies (or names if the 'name' keyword is set 
        to True) for the MIB.
        """
        
        if name:
            # Index -> Name
            output = []
            for k in self.entries.keys():
                try:
                    output.append( self.mapper[k] )
                except KeyError:
                    output.append(k)
            return output
        else:
            # Index
            return self.entries.keys()
            
    def parseInitFile(self, filename):
        """
        Given a MCS MIB initialization file, i.e., ASP_MIB_init.dat, create a 
        dictionary that maps indicies to human-readable names that can be used
        to clarify a MIBEntry.  Return this dictionary.
        """
        
        # Open the file
        with open(filename, 'r') as fh:
            # Go!
            self.mapper = {}
            self.invMapper = {}
            for line in fh:
                ## Parse out the line
                line = line.replace('\n', '')
                eType, index, name, default, dbmType, icdType = line.split(None, 5)
                
                ## Skip over branches
                if eType == 'B':
                    continue
                    
                ## Remember the mapping
                self.mapper[index] = name
                self.invMapper[name] = index
                
        # Done
        return True
        
    def fromFile(self, filename, initFilename=None):
        """
        Given the name of a GDBM database file, initialize the MIB.  
        Optionally, use the name of the MCS MIB initialization file to
        help convert indicies to names.
        """
        
        # Parse the init. file (if we have one)
        if initFilename is not None:
            self.parseInitFile(initFilename)
            
        # Make sure we have the .pag file
        if filename[-4:] == '.dir':
            filename = filename.replace('.dir', '.pag')
            
        # Open the database
        db = dbm.open(filename, 'ru')
        
        # Go!
        entry = db.firstkey()
        while entry is not None:
            value = db[entry]
            
            try:
                record = MIBEntry()
                record.fromEntry(value)
                self.entries[record.index] = record
                
            except ValueError:
                pass
                
            entry = db.nextkey(entry)
        db.close()
        
        # Done
        return True


class MIBEntry(object):
    """
    Class for accessing and storing MCS MIB information contained in a GDBM 
    database.
    
    .. versionadded:: 0.6.5
    """
    
    def __init__(self):
        """
        Create the MIBEntry instance and fill with dummy values.
        """
        
        # Basic information straight out of the mcs.h/record structure
        self.eType = 0
        self.index = ''
        self.value = ''
        self.dbmType = ''
        self.icdType = ''
        self._tv = (0, 0)
        
        # Additional information determined from the basic information
        self.updateTime = datetime.utcfromtimestamp(0)
        
    def __str__(self):
        """
        Represent the class as a string for display purposes.
        """
        
        return "Index: %s; Value: %s; Updated at %s" % (self.index, self.value, self.updateTime)
        
    def _parseValue(self, value, dataType):
        """
        Convert an encoded value to something Pythonic (if possible).
        
        Understood codes:
         * NUL:   No data stored (e.g., branch head entry)
         * a####: printable (i.e., ASCII minus escape codes), #### = number of characters
                  e.g., "a3" means 3 printable ASCII-encoded characters
         * r####: raw data (not printable), #### = number of bytes
                  e.g., "r1024" means 1024 bytes of raw data
         * i1u:   integer, 1 byte,  unsigned, little-endian (=uint8)
         * i2u:   integer, 2 bytes, unsigned, litte-endian (=uint16)
         * i4u:   integer, 4 bytes, unsigned, little-endian (=uint32)
         * i4s:   integer, 4 bytes, signed, little-endian (=int32)
         * i8u:   integer, 8 bytes, unsigned, litte-endian (=uint64)
         * f4:    float, 4 bytes, little-endian (=float32)
         * f4r:   float, 4 bytes, big-ending (=float32)
        """
        
        if dataType == 'NUL':
            try:
                value = str(value, 'utf-8')
            except TypeError:
                value = str(value)
            return value
        elif dataType[0] == 'a':
            try:
                value = str(value, 'utf-8')
            except TypeError:
                value = str(value)
            return value
        elif dataType[0] == 'r':
            try:
                value = str(value, 'utf-8')
            except TypeError:
                value = str(value)
            return value

        elif dataType[:3] == 'i1u':
            try:
                return struct.unpack('<1B', value)[0]
            except struct.error:
                return 0
        elif dataType[:3] == 'i2u':
            try:
                return struct.unpack('<1H', value)[0]
            except struct.error:
                return 0
        elif dataType[:3] == 'i4u':
            try:
                return struct.unpack('<1I', value)[0]
            except struct.error:
                return 0
        elif dataType[:3] == 'i4s':
            try:
                return struct.unpack('<1i', value)[0]
            except struct.error:
                return 0
        elif dataType[:3] == 'i8u':
            try:
                return struct.unpack('<1Q', value)[0]
            except struct.error:
                return 0
        elif dataType[:3] == 'f4r':
            try:
                return struct.unpack('>1f', value)[0]
            except struct.error:
                return 0.0
        elif dataType[:2] == 'f4':
            try:
                return struct.unpack('<1f', value)[0]
            except struct.error:
                return 0.0
        else:
            raise ValueError("Unknown data type '%s'" % dataType)
            
    def fromEntry(self, value):
        """
        Given an MIB entry straight out of a GDBM database, populate the 
        MIBEntry instance.
        
        .. note::
            The MIBEntry class does not currently support branch entries.  
            Entries of this type will raise a ValueError.
            
        .. note::
            The MIBEntry class currently only support entries with indicies
            that start with a number.  All other indicies will raise a 
            ValueError.
        """
        
        # Initialize a new structure to parse the binary string
        record = parseCStruct("""
            int eType;
            char index[%i];
            char val[%i];
            char type_dbm[6];
            char type_icd[6];
            long tv[2];
            """ % (MIB_INDEX_FIELD_LENGTH, MIB_VAL_FIELD_LENGTH), endianness='little')
            
        # Squeeze the binary string into the structure using ctypes magic
        temp = ctypes.create_string_buffer(value)
        ctypes.memmove(ctypes.addressof(record), ctypes.addressof(temp), ctypes.sizeof(record))
        
        # Bytes to Unicode for Python3
        try:
            index   = str(record.index, 'utf-8')
            dbmType = str(record.type_dbm, 'utf-8')
            icdType = str(record.type_icd, 'utf-8')
        except Exception as e:
            index   = str(record.index)
            dbmType = str(record.type_dbm)
            icdType = str(record.type_icd)
            
        # Validate
        if record.eType == MIB_REC_TYPE_BRANCH:
            raise ValueError("Cannot interpret MIB branch entries")
        try:
            if index[0] not in ('0', '1', '2', '3', '4', '5', '6', '7', '8', '9'):
                raise ValueError("Entry index '%s' does not appear to be numeric" % record.index)
        except IndexError:
            raise ValueError("Entry index '%s' does not appear to be numeric" % record.index)
            
        # Basic information
        self.eType = int(record.eType)
        self.index = index
        self.value = self._parseValue(record.val, dbmType)
        self.dbmType = dbmType
        self.icdType = icdType
        self._tv = (int(record.tv[0]), int(record.tv[1]))
        
        # Time
        self.updateTime = datetime.utcfromtimestamp(record.tv[0] + record.tv[1]/1e9)
        
        return True
