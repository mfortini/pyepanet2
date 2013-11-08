 %module pyepanet2
 %{
 /* Put header files here or function declarations like below */
#include "epanet2.h"
 %}

%include "cstring.i"
 
#define EN_ELEVATION    0    /* Node parameters */
#define EN_BASEDEMAND   1
#define EN_PATTERN      2
#define EN_EMITTER      3
#define EN_INITQUAL     4
#define EN_SOURCEQUAL   5
#define EN_SOURCEPAT    6
#define EN_SOURCETYPE   7
#define EN_TANKLEVEL    8
#define EN_DEMAND       9
#define EN_HEAD         10
#define EN_PRESSURE     11
#define EN_QUALITY      12
#define EN_SOURCEMASS   13
#define EN_INITVOLUME   14
#define EN_MIXMODEL     15
#define EN_MIXZONEVOL   16

#define EN_TANKDIAM     17
#define EN_MINVOLUME    18
#define EN_VOLCURVE     19
#define EN_MINLEVEL     20
#define EN_MAXLEVEL     21
#define EN_MIXFRACTION  22
#define EN_TANK_KBULK   23

#define EN_DIAMETER     0    /* Link parameters */
#define EN_LENGTH       1
#define EN_ROUGHNESS    2
#define EN_MINORLOSS    3
#define EN_INITSTATUS   4
#define EN_INITSETTING  5
#define EN_KBULK        6
#define EN_KWALL        7
#define EN_FLOW         8
#define EN_VELOCITY     9
#define EN_HEADLOSS     10
#define EN_STATUS       11
#define EN_SETTING      12
#define EN_ENERGY       13

#define EN_DURATION     0    /* Time parameters */
#define EN_HYDSTEP      1
#define EN_QUALSTEP     2
#define EN_PATTERNSTEP  3
#define EN_PATTERNSTART 4
#define EN_REPORTSTEP   5
#define EN_REPORTSTART  6
#define EN_RULESTEP     7
#define EN_STATISTIC    8
#define EN_PERIODS      9

#define EN_NODECOUNT    0    /* Component counts */
#define EN_TANKCOUNT    1
#define EN_LINKCOUNT    2
#define EN_PATCOUNT     3
#define EN_CURVECOUNT   4
#define EN_CONTROLCOUNT 5

#define EN_JUNCTION     0    /* Node types */
#define EN_RESERVOIR    1
#define EN_TANK         2

#define EN_CVPIPE       0    /* Link types */
#define EN_PIPE         1
#define EN_PUMP         2
#define EN_PRV          3
#define EN_PSV          4
#define EN_PBV          5
#define EN_FCV          6
#define EN_TCV          7
#define EN_GPV          8

#define EN_NONE         0    /* Quality analysis types */
#define EN_CHEM         1
#define EN_AGE          2
#define EN_TRACE        3

#define EN_CONCEN       0    /* Source quality types */
#define EN_MASS         1
#define EN_SETPOINT     2
#define EN_FLOWPACED    3

#define EN_CFS          0    /* Flow units types */
#define EN_GPM          1
#define EN_MGD          2
#define EN_IMGD         3
#define EN_AFD          4
#define EN_LPS          5
#define EN_LPM          6
#define EN_MLD          7
#define EN_CMH          8
#define EN_CMD          9

#define EN_TRIALS       0   /* Misc. options */
#define EN_ACCURACY     1
#define EN_TOLERANCE    2
#define EN_EMITEXPON    3
#define EN_DEMANDMULT   4

#define EN_LOWLEVEL     0   /* Control types */
#define EN_HILEVEL      1
#define EN_TIMER        2
#define EN_TIMEOFDAY    3

#define EN_AVERAGE      1   /* Time statistic types.    */
#define EN_MINIMUM      2 
#define EN_MAXIMUM      3
#define EN_RANGE        4

#define EN_MIX1         0   /* Tank mixing models */
#define EN_MIX2         1
#define EN_FIFO         2
#define EN_LIFO         3

#define EN_NOSAVE       0   /* Save-results-to-file flag */
#define EN_SAVE         1
#define EN_INITFLOW     10  /* Re-initialize flow flag   */

/*** Updated 11/24/06 for inp2shp ***/
#define EN_CONST_HP     0   /*    constant horsepower              */
#define EN_POWER_FUNC   1   /*    power function                   */
#define EN_CUSTOM       2   /*    user-defined custom curve        */
#define EN_NOCURVE      3


%cstring_bounded_output(char *elementid, 64);

 int    ENepanet(char *, char *, char *, void (*) (char *));
 int    ENopen(char *, char *, char *);
 int    ENsaveinpfile(char *);
 int    ENclose(void);

 int    ENsolveH(void);
 int    ENsaveH(void);
 int    ENopenH(void);
 int    ENinitH(int);
 int    ENrunH(long *OUTPUT);
 int    ENnextH(long *OUTPUT);
 int    ENcloseH(void);
 int    ENsavehydfile(char *);
 int    ENusehydfile(char *);

 int    ENsolveQ(void);
 int    ENopenQ(void);
 int    ENinitQ(int);
 int    ENrunQ(long *OUTPUT);
 int    ENnextQ(long *OUTPUT);
 int    ENstepQ(long *OUTPUT);
 int    ENcloseQ(void);

 int    ENwriteline(char *);
 int    ENreport(void);
 int    ENresetreport(void);
 int    ENsetreport(char *);

 int    ENgetcontrol(int, int *OUTPUT, int *OUTPUT, float *OUTPUT, int *OUTPUT, float *OUTPUT);
 int    ENgetcount(int, int *OUTPUT);
 int    ENgetoption(int, float *OUTPUT);
 int    ENgettimeparam(int, long *OUTPUT);
 int    ENgetflowunits(int *OUTPUT);
 int    ENgetpatternindex(char *, int *OUTPUT);
 int    ENgetpatternid(int, char *elementid);
 int    ENgetpatternlen(int, int *OUTPUT);
 int    ENgetpatternvalue(int, int, float *OUTPUT);
 int    ENgetqualtype(int *, int *OUTPUT);
 int    ENgeterror(int, char *, int);

 int    ENgetnodeindex(char *, int *OUTPUT);
 int    ENgetnodeid(int, char *elementid);
 int    ENgetnodetype(int, int *OUTPUT);
 int    ENgetnodevalue(int, int, float *OUTPUT);

 int    ENgetlinkindex(char *, int *OUTPUT);
 int    ENgetlinkid(int, char *elementid);
 int    ENgetlinktype(int, int *OUTPUT);
 int    ENgetlinknodes(int, int *OUTPUT, int *OUTPUT);
 int    ENgetlinkvalue(int, int, float *OUTPUT);

 int    ENgetversion(int *OUTPUT);

 int    ENsetcontrol(int, int, int, float, int, float);
 int    ENsetnodevalue(int, int, float);
 int    ENsetlinkvalue(int, int, float);
 int    ENaddpattern(char *);
 int    ENsetpattern(int, float *, int);
 int    ENsetpatternvalue(int, int, float);
 int    ENsettimeparam(int, long);
 int    ENsetoption(int, float);
 int    ENsetstatusreport(int);
 int    ENsetqualtype(int, char *, char *, char *);
