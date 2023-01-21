KPL/MK


\begindata

   PATH_VALUES     = ( 'C:\Users\H21\Desktop\Desktop\Behrouz\Astronomy\kernels' )

   PATH_SYMBOLS    = ( 'KKK' )

   KERNELS_TO_LOAD = ( '$KKK/naif0011.tls',
		       '$KKK/naif0012.tls',
                       '$KKK/de440.bsp',
                       '$KKK/pck00010.tpc' )

\begintext

Earth mean equator and mean equinox of date frame "EME":

\begindata
 
   FRAME_EME                     =  1890001
   FRAME_1890001_NAME            =  'EME'
   FRAME_1890001_CLASS           =  5
   FRAME_1890001_CLASS_ID        =  1890001
   FRAME_1890001_CENTER          =  399
   FRAME_1890001_RELATIVE        = 'J2000'
   FRAME_1890001_DEF_STYLE       = 'PARAMETERIZED'
   FRAME_1890001_FAMILY          = 'MEAN_EQUATOR_AND_EQUINOX_OF_DATE'
   FRAME_1890001_PREC_MODEL      = 'EARTH_IAU_1976'
   FRAME_1890001_ROTATION_STATE  = 'ROTATING'
 
\begintext

Earth true equator and true equinox of date frame "TETE":

\begindata
 
   FRAME_TETE                    =  1890002
   FRAME_1890002_NAME            =  'TETE'
   FRAME_1890002_CLASS           =  5
   FRAME_1890002_CLASS_ID        =  1890002
   FRAME_1890002_CENTER          =  399
   FRAME_1890002_RELATIVE        = 'J2000'
   FRAME_1890002_DEF_STYLE       = 'PARAMETERIZED'
   FRAME_1890002_FAMILY          = 'TRUE_EQUATOR_AND_EQUINOX_OF_DATE'
   FRAME_1890002_PREC_MODEL      = 'EARTH_IAU_1976'
   FRAME_1890002_NUT_MODEL       = 'EARTH_IAU_1980'
   FRAME_1890002_ROTATION_STATE  = 'ROTATING'
 
\begintext