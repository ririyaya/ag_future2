class Sim_oc(object):
    def __init__(self, leve, table='ag15', start_i=0):  # 杠杆倍率,表名
        mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            passwd="111",
            database='koudai',  # 数据库
            auth_plugin='mysql_native_password', unix_socket='/private/tmp/mysql.sock')  # 'caching_sha2_password')  #
        d = mydb.cursor()
        sq = 'select c,h,l,ts,o from ' + table + ' order by ts'  # +' where ts>1635346800000'
        d.execute(sq)
        a = d.fetchall()
        self.c1, self.h, self.l, self.ts, self.o = [], [], [], [], []
        for i in range(0, len(a)):
            self.c1.append(round(a[i][0], 5))
            self.h.append(round(a[i][1], 5))
            self.l.append(round(a[i][2], 5))
            self.ts.append(a[i][3])
            self.o.append(round(a[i][4], 5))
        self.start_i=start_i
        self.__leve = leve

    # main 仓位,资金,持仓方向,挂单状态,信号
    mark=[1,'so']
def oc(self,mark):
    ccfx=['so','sc','bo','bc']
    gdzt=[0,1,-1]#无,有,撤回
    zj=10000
    cw=0
    xh=[0,1]
    ccfx.index(mark[2])
