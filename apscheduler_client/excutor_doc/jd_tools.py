#-*- utf-8 -*-
import requests
import random,os

class jd_tools:
    useragent_web_list = [
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1",
        "Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6",
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6",
        "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/19.77.34.5 Safari/537.1",

        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5",
        "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.36 Safari/536.5",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
        "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_0) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",

        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",

        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.0 Safari/536.3",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",
        "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",
        'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.2; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0)',
        'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; WOW64; Trident/4.0; SLCC2; Media Center PC 6.0; InfoPath.2; MS-RTC LM 8)',
        'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; InfoPath.2)',
        'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0 Zune 3.0)',
        'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; MS-RTC LM 8)',
        'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; InfoPath.3)',
        'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; InfoPath.2; MS-RTC LM 8)',
        'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET CLR 4.0.20402; MS-RTC LM 8)',
        'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET CLR 1.1.4322; InfoPath.2)',
        'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729)',
        'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; Win64; x64; Trident/4.0; .NET CLR 2.0.50727; SLCC2; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; Tablet PC 2.0)',
        'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; Win64; x64; Trident/4.0; .NET CLR 2.0.50727; SLCC2; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET CLR 3.0.04506; Media Center PC 5.0; SLCC1)',
        'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; Win64; x64; Trident/4.0; .NET CLR 2.0.50727; SLCC2; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0)',
        'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; Win64; x64; Trident/4.0)',
        'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; Tablet PC 2.0; .NET CLR 3.0.04506; Media Center PC 5.0; SLCC1)',
        'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; FDM; Tablet PC 2.0; .NET CLR 4.0.20506; OfficeLiveConnector.1.4; OfficeLivePatch.1.3)',
        'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET CLR 3.0.04506; Media Center PC 5.0; SLCC1; Tablet PC 2.0)',
        'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET CLR 1.1.4322; InfoPath.2)',
        'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.3029; Media Center PC 6.0; Tablet PC 2.0)',
        'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; Trident/4.0; SLCC2)',
        'Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 6.0)',
        'Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 5.2; .NET CLR 1.1.4322; .NET CLR 2.0.50727; InfoPath.2; .NET CLR 3.0.04506.30)',
        'Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 5.1; Media Center PC 3.0; .NET CLR 1.0.3705; .NET CLR 1.1.4322; .NET CLR 2.0.50727; InfoPath.1)',
        'Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 5.1; FDM; .NET CLR 1.1.4322)',
        'Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 5.1; .NET CLR 1.1.4322; InfoPath.1; .NET CLR 2.0.50727)',
        'Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 5.1; .NET CLR 1.1.4322; InfoPath.1)',
        'Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 5.1; .NET CLR 1.1.4322; Alexa Toolbar; .NET CLR 2.0.50727)',
        'Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 5.1; .NET CLR 1.1.4322; Alexa Toolbar)',
        'Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 5.1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)',
        'Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 5.1; .NET CLR 1.1.4322; .NET CLR 2.0.40607)',
        'Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 5.1; .NET CLR 1.1.4322)',
        'Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 5.1; .NET CLR 1.0.3705; Media Center PC 3.1; Alexa Toolbar; .NET CLR 1.1.4322; .NET CLR 2.0.50727)',
        'Mozilla/5.0 (Windows; U; MSIE 7.0; Windows NT 6.0; en-US)',
        'Mozilla/5.0 (Windows; U; MSIE 7.0; Windows NT 6.0; el-GR)',
        'Mozilla/5.0 (MSIE 7.0; Macintosh; U; SunOS; X11; gu; SV1; InfoPath.2; .NET CLR 3.0.04506.30; .NET CLR 3.0.04506.648)',
        'Mozilla/5.0 (compatible; MSIE 7.0; Windows NT 6.0; WOW64; SLCC1; .NET CLR 2.0.50727; Media Center PC 5.0; c .NET CLR 3.0.04506; .NET CLR 3.5.30707; InfoPath.1; el-GR)',
        'Mozilla/5.0 (compatible; MSIE 7.0; Windows NT 6.0; SLCC1; .NET CLR 2.0.50727; Media Center PC 5.0; c .NET CLR 3.0.04506; .NET CLR 3.5.30707; InfoPath.1; el-GR)',
        'Mozilla/5.0 (compatible; MSIE 7.0; Windows NT 6.0; fr-FR)',
        'Mozilla/5.0 (compatible; MSIE 7.0; Windows NT 6.0; en-US)',
        'Mozilla/5.0 (compatible; MSIE 7.0; Windows NT 5.2; WOW64; .NET CLR 2.0.50727)',
        'Mozilla/4.79 [en] (compatible; MSIE 7.0; Windows NT 5.0; .NET CLR 2.0.50727; InfoPath.2; .NET CLR 1.1.4322; .NET CLR 3.0.04506.30; .NET CLR 3.0.04506.648)',
        'Mozilla/4.0 (Windows; MSIE 7.0; Windows NT 5.1; SV1; .NET CLR 2.0.50727)',
        'Mozilla/4.0 (Mozilla/4.0; MSIE 7.0; Windows NT 5.1; FDM; SV1; .NET CLR 3.0.04506.30)',
        'Mozilla/4.0 (Mozilla/4.0; MSIE 7.0; Windows NT 5.1; FDM; SV1)',
        'Mozilla/4.0 (compatible;MSIE 7.0;Windows NT 6.0)',
        'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0)',
        'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0;)',
        'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; YPC 3.2.0; SLCC1; .NET CLR 2.0.50727; Media Center PC 5.0; InfoPath.2; .NET CLR 3.5.30729; .NET CLR 3.0.30618)',
        'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; YPC 3.2.0; SLCC1; .NET CLR 2.0.50727; .NET CLR 3.0.04506)',
        'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; WOW64; SLCC1; Media Center PC 5.0; .NET CLR 2.0.50727)',
        'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; WOW64; SLCC1; .NET CLR 3.0.04506)',
        'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; WOW64; SLCC1; .NET CLR 2.0.50727; Media Center PC 5.0; InfoPath.2; .NET CLR 3.5.30729; .NET CLR 3.0.30618; .NET CLR 1.1.4322)',
    ]

    useragent_app_list = [
        'Huawei/1.0/0HUAWEI U1300/B100 Browser/Obigo-Browser/Q05A MMS/Obigo-MMS/Q05A SyncML/HW-SyncML/1.0 Java/HWJa/1.0 Profile/MIDP-2.0',
        'Huawei/1.0/0HUAWEI U1310/B100 Browser/Obigo-Browser/Q05A MMS/Obigo-MMS/Q05A SyncML/HW-SyncML/1.0 Java/HWJa/1.0 Profile/MIDP-2.0',
        'Huawei/1.0/0HUAWEI U5700/B100 Browser/Obigo-Browser/Q05A MMS/Obigo-MMS/Q05A SyncML/HW-SyncML/1.0 Java/HWJa/1.0 Profile/MIDP-2.0',
        'Huawei/1.0/0Huawei U6100/B100 Browser/Obigo-Browser/Q05A MMS/Obigo-MMS/Q05A SyncML/HW-SyncML/1.0 Java/HWJa/1.0 Profile/MIDP-2.0 Configuration/CLDC-1.1 Player/QTV-Player/5.3',
        'Huawei/1.0/U535/B000 Browser/Obigo-Browser/Q04A MMS/Obigo-MMS/Q04A SyncML/HW-SyncML/1.0 Java/QVM/4.1 Profile/MIDP-2.0 Configuration/CLDC-1.1',
        'HuaweiU3100/B000 Browser/Obigo-Browser/Q05A MMS/Obigo-MMS/Q05A SyncML/HW-SyncML/1.0 Java/HWJa/2.0 Profile/MIDP-2.0 Configuration/CLDC-1.1 Player/QTV-Player/5.3',
        'HuaweiU3200s/B000 Browser/NetFront/3.5 MMS/Obigo-MMS/Q05A SyncML/HW-SyncML/1.0 Java/HWJa/2.0 Profile/MIDP-2.0 Configuration/CLDC-1.1 Player/QTV-Player/5.3',
        'HuaweiU7510/B000 Browser/NetFront/3.5 MMS/Obigo-MMS/Q05A SyncML/HW-SyncML/1.0 Java/HWJa/2.0 Profile/MIDP-2.0 Configuration/CLDC-1.1 Player/QTV-Player/5.3',
        'HuaweiU7517/B000 Browser/NetFront/3.5 MMS/Obigo-MMS/Q05A SyncML/HW-SyncML/1.0 Java/HWJa/2.0 Profile/MIDP-2.0 Configuration/CLDC-1.1 Player/QTV-Player/5.3',
        'HuaweiU7519/B001 Browser/ACCESS NetFront/3.5 Profile/MIDP-2.0 Configuration/CLDC-1.1/QTV-Player/5.3',

        'HuaweiU7520/B000 Browser/NetFront/4.1 MMS/Obigo-MMS/Q05A SyncML/HW-SyncML/1.0 Java/HWJa/2.0 Profile/MIDP-2.0 Configuration/CLDC-1.1 Player/QTV-Player/5.3',
        'HuaweiU7525/B000 Browser/NetFront/4.1 MMS/Obigo-MMS/Q05A SyncML/HW-SyncML/1.0 Java/HWJa/2.0 Profile/MIDP-2.0 Configuration/CLDC-1.1 Player/QTV-Player/5.3',
        'HuaweiU7527/B000 Browser/NetFront/4.1 MMS/Obigo-MMS/Q05A SyncML/HW-SyncML/1.0 Java/HWJa/2.0 Profile/MIDP-2.0 Configuration/CLDC-1.1 Player/QTV-Player/5.3',
        'HuaweiU9130/B047 Browser/NetFront/3.5 MMS/Obigo-MMS/Q05A SyncML/HW-SyncML/1.0 Java/HWJa/2.0 Profile/MIDP-2.0 Configuration/CLDC-1.1 Player/QTV-Player/5.3',
        'HuaweiV840/B533 Browser/NetFront/3.5 MMS/Obigo-MMS/Q05A SyncML/HW-SyncML/1.0 Java/HWJa/2.0 Profile/MIDP-2.0 Configuration/CLDC-1.1 Player/QTV-Player/5.3',
        'K-Touch_A192_CMCC/TYM931049_7A7_V0801 MTK/6225 Release/30.08.2008 Browser/WAP2.0 Profile/MIDP-2.0 Configuration/CLDC-1.1',
        'K-Touch_E500_CMCC/1.0 RTKE_OS/01.00 TD7210/DV2 Release/16.04.2009 Browser/Techsoft-01.00.16 Profile/MIDP-2.0 Configuration/CLDC',
        'K-Touch_N2200_CMCC/TBG110022_1223_V0801 MTK/6223 Release/30.07.2008 Browser/WAP2.0',
        'K-Touch_N930_CMCC/TYM931048_7A4_V0801 MTK/6225 Release/30.06.2008 Browser/WAP2.0 Profile/MIDP-2.0 Configuration/CLDC-1.1',
        'LENOVO-A710/S013_081010/WAP2.0 Profile/MIDP-2.0 Configuration/CLDC-1.1',

        'LENOVO-E328_XJ/(2006.08.04)S110/WAP2.0 Profile/MIDP2.0 Configuration/CLDC-1.1/',
        'LENOVO-S9/(2007.05.08)S120/WAP2.0 Profile/MIDP2.0 Configuration/CLDC1.1',
        'LENOVO-i760/(2008.08.29)i760_S020_080829/WAP1.2/2.0+Profile/MIDP-1.0/2.0 Configuration/CLDC-1.1',
        'LG-A130/V100 Obigo/WAP2.0 Profile/MIDP-2.1 Configuration/CLDC-1.1',
        'LG-GD300s_CMCC A2000pH/2.30.10 Release/20.4.2009 Browser/Teleca/Q7.1 Profile/MIDP-2.0 Configuration/CLDC-1.1',
        'LG-GD510/V100 Teleca/WAP2.0 Profile/MIDP-2.1 Configuration/CLDC-1.1',
        'LG-GD570 Browser/Obigo-Q7.3 MMS/LG-MMS-V1.0/1.2 MediaPlayer/LGPlayer/1.0 Profile/MIDP-2.1 Configuration/CLDC-1.1',
        'LG-GS170 Browser/Obigo-Q7.0 MMS/LG-MMS-V1.0/1.2 Profile/MIDP-2.1 Configuration/CLDC-1.1',
        'LG-GS290/V100 Obigo/WAP2.0 Profile/MIDP-2.1 Configuration/CLDC-1.1',
        'LG-GS390/V10k Obigo/Q7.3 Profile/MIDP-2.1 Configuration/CLDC-1.1',

        'LG-GS505 Browser/Obigo-Q7.3 MMS/LG-MMS-V1.0/1.2 MediaPlayer/LGPlayer/1.0 Profile/MIDP-2.1',
        'LG-GT350/1.0 Obigo/WAP2.0 Profile/MIDP-2.1 Configuration/CLDC-1.1',
        'LG-GT405/V10a Browser/Teleca-Q7.1 MMS/LG-MMS-V1.0/1.2 MediaPlayer/LGPlayer/1.0 Java/ASVM/1.1 Profile/MIDP-2.1 Configuration/CLDC-1.1',
        'LG-GT505/v10a Browser/Teleca-Q7.1 MMS/LG-MMS-V1.0/1.2 MediaPlayer/LGPlayer/1.0 Java/ASVM/1.1 Profile/MIDP-2.1 Configuration/CLDC-1.1',
        'LG-KG98 UP.Browser/6.2.3 (GUI) MMP/1.0',
        'LG-KM330 Obigo/WAP2.0 MIDP-2.0/CLDC-1.1',
        'LG-LG145PRE AU-MIC-LG145PRE/1.0 MMP/2.0 Profile/MIDP-1.0 Configuration/CLDC-1.0',
        'LG-LX600 Polaris/6.0 MMP/2.0 Profile/MIDP-2.1 Configuration/CLDC-1.1',
        'Lenovo-E520/CMCC_S105 LMP/XM Release/2008.03.20 Profile/MIDP2.0 Configuration/CLDC1.1',
        'Lenovo-E520/CMCC_S121 LMP/XM Release/2008.07.10 Profile/MIDP2.0 Configuration/CLDC1.1',

        'Lenovo-E520/CMCC_S125 LMP/XM Release/2008.12.01 Profile/MIDP2.0 Configuration/CLDC1.1',
        'Lenovo-P790/2008.05.30 P790_S025_080530/WAP2.0 Profile/MIDP-2.0 Configuration/CLDC-1.1',
        'Lenovo-P80/CMCC_S101 LMP/XM Release/2008.08.26 Profile/MIDP2.0 Configuration/CLDC1.1',
        'Lenovo-P851/1.0 Dragonfly/3.0 Release/3.1.2007 Browser/CMS2.0.15 Profile/MIDP-2.0 Configuration/CLDC-1.1',
        'Lenovo-S5/CMCC_S106 LMP/XM Release/2007.06.29 Profile/MIDP2.0 Configuration/CLDC1.1',
        'LinuxOS/2.4.20 Release/1.31.2007 Browser/Opera8.00 Profile/MIDP-2.0 Configuration/CLDC-1.1 Software/R541_G_11.51.01P UCWEB5.1',
        'MOT-A1200e/1.0 LinuxOS/2.4.20 Release/1.31.2007 Browser/Opera8.00 Profile/MIDP-2.0 Configuration/CLDC-1.1 Software/AP: 16R_floa',
        'MOT-A1200e/1.0 LinuxOS/2.4.20 Release/1.31.2007 Browser/Opera8.00 Profile/MIDP-2.0 Configuration/CLDC-1.1 Software/R541_G_11.50.34P',
        'MOT-A1200e/1.0 LinuxOS/2.4.20 Release/1.31.2007 Browser/Opera8.00 Profile/MIDP-2.0 Configuration/CLDC-1.1 Software/R541_G_11.51.01P',
        'MOT-A1200e/1.0 LinuxOS/2.4.20 Release/1.31.2007 Browser/Opera8.00 Profile/MIDP-2.0 Configuration/CLDC-1.1 Software/R541_G_11.56.09R',

        'MOT-A1200e/R541_G_11.xx.yyR Mozilla/4.0 (compatible; MSIE 6.0 Linux; A1200e;nnn) Profile/MIDP-2.0 Configuration/CLDC-1.1 Opera 8.00[yy]',
        'MOT-A1200r/1.0 LinuxOS/2.4.20 Release/8.22.2006 Browser/Opera8.00 Profile/MIDP-2.0 Configuration/CLDC-1.1 Software/A1200R_32P_Autumn_Storm_Build2018',
        'MOT-A1200r/1.0 LinuxOS/2.4.20 Release/8.22.2006 Browser/Opera8.00 Profile/MIDP-2.0 Configuration/CLDC-1.1 Software/R532C2_G_11.30.21R',
        'MOT-A1200r/1.0 LinuxOS/2.4.20 Release/8.22.2006 Browser/Opera8.00 Profile/MIDP-2.0 Configuration/CLDC-1.1 Software/R532C2_G_11.30.32P',
        'MOT-A1200w/1.0/R541L7_G_11.10.11R Mozilla/4.0 (compatible MSIE 6.0 Linux A1200w 781) Profile/MIDP-2.0 Configuration/CLDC-1.1 Opera 8.00',
        'MOT-A1600/R542_G_11.61.30R Mozilla/4.0 (compatible; MSIE 6.0; Linux; A1600; 781) Profile/MIDP-2.0 Configuration/CLDC-1.1 Opera 8.00 [zh-cn]',
        'MOT-A1600_CMCC/1.0 LinuxOS/2.4.20 Release/6.16.2008 Browser/Opera8.00 Profile/MIDP-2.0 Configuration/CLDC-1.1 Software/R542_G_11.60.51P',
        'MOT-A3000_CMCC/1.0 Release/09.09.2008 Profile/MIDP-2.0 Configuration/CLDC-1.1 Software/WM6.1',
        'MOT-A3100/1.0 Software/WM6.1 Release/05.01.2009 Profile/MIDP-2.0 Configuration/CLDC-1.1 (compatible; MSIE 6.0; Windows CE; IEMo',
        'MOT-A668/ WAP.Browser/1.0 Profile/MIDP-2.0 Configuration/CLDC-1.0',

        'MOT-E1 iTunes/0E.30.42R MIB/2.2.1 Profile/MIDP-2.0 Configuration/CLDC-1.1',
        'MOT-E1 iTunes/0E.30.6BR MIB/2.2.1 Profile/MIDP-2.0 Configuration/CLDC-1.1',
        'MOT-E1000/80.3F.92. MIB/2.2.1 Profile/MIDP-2.0 Configuration/CLDC-1.1',
        'MOT-E1070/85.9B.D2P MIB/BER2.2 Profile/MIDP-2.0 Configuration/CLDC-1.1',
        'MOT-E398/0E.30.70R MIB/2.2.1 Profile/MIDP-2.0 Configuration/CLDC-1.1',
        'MOT-W370/0.0.87 UP.Browser/6.3.0.6.c.17 (GUI) MMP/2.0',
        'MOT-W450/0.1.58.K1/08.18.2008 Browser/UPB6.3 Software/13.105I',
        'MOT-Z6m/00.62 UP.Browser/6.2.3.4.c.1.123 (GUI) MMP/2.0',
        'MOT-v8/ 4.3_08.B MIB/2.2.1 Profile/MIDP-2.0 Configuration/CLDC-1.1',
        'MOTO-W760r/Mozilla/4.0 (compatibleMSIE 6.0Linux W760r)/R63712_U_71.xx.yyI Profile/MIDP-2.0 Configuration/CLDC-1.1 Symphony 1.0',

        'Maxon O2-X1 ver1.0',
        'Motorola-E365 UP.Browser/6.1.0.7.3 (GUI) MMP/1.0',
        'Mozilla/4.0 (BREW 3.1.5 U en-us Samsung SPH_M240 POLARIS/6.1/WAP) MMP/2.0 Configuration/CLDC-1.1',
        'Mozilla/2.0 (compatible MSIE 3.02 Windows CE Smartphone 176x220)',
        'Mozilla/4.0 (MobilePhone MM-9000/US/1.0) NetFront/3.1 MMP/2.0',
        'Mozilla/4.0 (MobilePhone RL-4930/US/1.0) NetFront/3.1 MMP/2.0',
        'Mozilla/4.0 (MobilePhone SCP-PRO700/US/1.0) NetFront/3.4 MMP/2.0',
        'Mozilla/4.0 (compatible MSIE 4.01 Windows CE PPC 240x320 SPV M1500 OpVer 3.11.1.167)',
        'Mozilla/4.0 (compatible MSIE 4.01 Windows CE PPC i-mate PDAL 240x320 PPC)',
        'Mozilla/4.0 (compatible; MSIE 6.0; Windows CE; IEMobile 7.11) Sprint MP6900SP',

        'Mozilla/5.0 (Linux U Android 1.5 en-us T-Mobile myTouch 3G Build/CRB57) AppleWebKit/528.5+ (KHTML, like Gecko) Version/3.1.2 Mobile Safari/525.20.1',
        'Mozilla/5.0 (Linux U Android 1.5 en-us morrison) AppleWebKit/525.10+ (KHTML, like Gecko) Version/3.0.4 Mobile Safari/523.12.2',
        'Mozilla/5.0 (Linux U Android 1.5 en-us motus) AppleWebKit/525.10+ (KHTML, like Gecko) Version/3.0.4 Mobile Safari/523.12.2',
        'Mozilla/5.0 (Linux U Android 1.5 en-us zeppelin) AppleWebKit/525.10+ (KHTML, like Gecko) Version/3.0.4 Mobile Safari/523.12.2',
        'Mozilla/5.0 (Linux U Android 1.5 zh-cn ME501 Build/CUPCAKE) AppleWebKit/525.10+ (KHTML, like Gecko) Version/3.0.4 Mobile Safari/523.12.2',
        'Mozilla/5.0 (Linux U Android 1.5 zh-cn ME600 Build/CUPCAKE) AppleWebKit/525.10+ (KHTML, like Gecko) Version/3.0.4 Mobile Safari/523.12.2',
        'Mozilla/5.0 (Linux U Android 1.5 zh-tw CHT8000 Build/CRB17) AppleWebKit/525.10+ (KHTML, like Gecko) Version/3.0.4 Mobile Safari/523.12.2',
        'Mozilla/5.0 (Linux U Android 1.6 en-us CBW Blaze Build/DONUT) AppleWebKit/525.10+ (KHTML, like Gecko) Version/3.0.4 Mobile Safari/523.12.2',
        'Mozilla/5.0 (Linux U Android 1.6 en-us Garminfone Build/DRC79) AppleWebKit/525.10+ (KHTML, like Gecko) Version/3.0.4 Mobile Safari/523.12.2',
        'Mozilla/5.0 (Linux U Android 1.6 zh-cn apanda-A60 Build/DONUT) AppleWebKit/528.5  (KHTML, like Gecko) Version/3.1.2 Mobile Safari/525.20.1'
    ]

    @classmethod
    def get_web_useragent(cls):
        return random.choice(cls.useragent_web_list)

    @classmethod
    def get_app_useragent(cls):
        return random.choice(cls.useragent_app_list)

    @classmethod
    def get_headers(self, headers_option):
        headers = {
            'accept': '*/*',
            'accept-encoding': 'gzip, deflate, sdch',
            'accept-language': 'zh-CN,zh;q=0.8',
            'connection': 'keep-alive',
            'origin': '',
          #  'host': '',
            'referer': '',
            'user-agent': '',
            'cookie': ''
        }

        if headers_option['host'] is not None:
            headers['host'] = headers_option['host']

        if headers_option['user-agent'] is not None:
            headers['user-agent'] = headers_option['user-agent']

        if headers_option['referer'] is not None:
            headers['referer'] = headers_option['referer']

        if headers_option['origin'] is not None:
            headers['origin'] = headers_option['origin']

        if headers_option['cookie'] is not None:
            headers['cookie'] = headers_option['cookie']

        return headers

    @classmethod
    def get_host_url(cls, host_type=0):
        host = {
            0: 'list.jd.com',
            1: 'clud.jd.com',
            2: 'item.m.jd.com',
            3: 'so.m.jd.com',
            4: 'shop.m.jd.com',
            5: 'search.jd.com'
        }
        return host.get(host_type)

    @classmethod
    def get_jd_web_cookie(cls):
        cookie = None
        return cookie

    @classmethod
    def file_is_exist(cls, filename):
        isExist = os.path.isfile(filename)
        return isExist

    @classmethod
    def dir_is_exist(cls, dirname):
        isExist = os.path.exists(dirname)
        return isExist
    @classmethod
    def get_jd_app_cookie(cls):
        cookie = None
        return cookie
