import pyodbc

def AccessDB():
    server = '221.161.62.124,2433'
    database = 'hansun'
    username = 'Han_Eng_Back'
    password = 'HseAdmin1991'
    cnxn = pyodbc.connect('DRIVER={ODBC Driver 13 for SQL Server};SERVER='+server
                      +';데이터베이스='+database+';UID='+username+';PWD='+password)
    cursor = cnxn.cursor()
    cursor.execute(""" select a.Workno, g.GoodNo, i.GoodNo, g.GoodCd, i.GoodCd,
            a.OrderQty, a.DeliveryDate, 
            case when i.Class3 = '061038' then '단조' else 'HEX' end as Gubun,
            REPLACE(REPLACE(i.Spec, 'HEX.', ''),'HEX','') as Spec
     from TWorkreport_Han_Eng a
     left outer join TGood g on a.Goodcd = g.GoodCd
     left outer join TGood i on a.Raw_Materialcd = i.GoodCd
     where Workdate between '20171001' and '20171031'
       and DeliveryDate between '20171116' and '20171231'
       and PmsYn = 'N'
       and ContractYn = '1'
       and g.Class2 not in ('060002', '060006')
       and i.Class3 in ('061038', '061039')

declare @iaccunit char(3),
        @ifactory char(3),
        @iGoodcd varchar(8),
        @iWorkno varchar(20)

    set @iaccunit = '001' set @ifactory = '00a' set @iGoodcd = '00011281' set @iWorkno = '171019-018'


        select ISNULL(a.guid            ,'') as guid          ,
               ISNULL(a.workno          ,'') as workno        ,
               ISNULL(a.seq             , 0) as seq           ,
               --RTRIM(ISNULL(@IDTag            ,'')) as IDTag         ,
               ISNULL(a.Operationseq    ,'') as Operationseq  ,
               ISNULL(a.Operationcd     ,'') as Operationcd   ,
               ISNULL(m1.minornm        ,'') as Operationnm   ,
               ISNULL(a.Workdirection   ,'') as Workdirection ,
               ISNULL(a.Shopcd          ,'') as Shopcd        ,
               ISNULL(m2.minornm        ,'') as Shopnm        ,
               ISNULL(a.cnc             ,'') as cnc           ,
               ISNULL(m3.minornm        ,'') as cncnm         ,
               ISNULL(a.Operationdate   ,'') as Operationdate ,
               ISNULL(a.Workpno         ,'') as Workpno       ,
               ISNULL(m.[name]          ,'') as Workpnonm     ,
               --ISNULL(a.Qty             , 0) as Qty           ,
               ISNULL(a.[Check]         ,'') as [Check]       ,
               --ISNULL(a.Remark          ,'') as Remark        ,
               ISNULL(a.Remark          ,'')
        from TWorkreportItem_Han_Eng a
            left outer join TMan    m on a.workpno = m.pno
            left outer join TMinor m1 on a.Operationcd = m1.minorcd
            left outer join TMinor m2 on a.Shopcd = m2.minorcd
            left outer join TMinor m3 on a.cnc = m3.minorcd
        where a.Accunit = @iAccunit
          and a.Factory = @iFactory
          and a.Workno = @iWorkno
        order by seq



    --    작업지시서 품번 정보
    select isnull(g.GoodCd          ,'') as GoodCd        ,
           isnull(g.GoodNo          ,'') as GoodNo        ,
           isnull(g.Spec            ,'') as Spec          ,
           isnull(a.Lot_Min         , 0) as Lot_Min       ,
           isnull(a.Lot_Max         , 0) as Lot_Max       ,
           isnull(a.guid            ,'') as guid          ,
           isnull(m5.MinorNm        ,'') as Class5nm      ,
           isnull(a.seq             , 0) as seq           ,
           isnull(a.Operationseq    ,'') as Operationseq  ,
           isnull(a.Operationcd     ,'') as Operationcd   ,
           isnull(m1.minornm        ,'') as Operationnm   ,
           isnull(a.Workdirection   ,'') as Workdirection ,
           isnull(a.Shopcd          ,'') as Shopcd        ,
           isnull(m2.minornm        ,'') as Shopnm        ,
           isnull(a.cnc             ,'') as cnc           ,
           isnull(m3.minornm        ,'') as cncnm         ,
           isnull(a.Remark          ,'') as Remark
    from TGood_Process a
        left outer join TGood g on a.Goodcd = g.GoodCd
        left outer join TMinor m5 on g.Class5 = m5.MinorCd
        left outer join TMinor m1 on a.Operationcd = m1.minorcd
        left outer join TMinor m2 on a.Shopcd = m2.minorcd
        left outer join TMinor m3 on a.cnc = m3.minorcd
    where a.accunit = @iAccunit
      and a.factory = @iFactory
      and a.Goodcd = @iGoodcd

    --    작업지시서 품번별 공정 정보
    select isnull(a.Accunit         ,'') as Accunit            ,
               isnull(a.Factory         ,'') as Factory            ,
               isnull(a.Guid            ,'') as Guid               ,
               isnull(a.Deptcd          ,'') as Deptcd             ,
               isnull(d.DeptNm          ,'') as deptnm             ,
               isnull(a.Pno             ,'') as Pno                ,
               isnull(m.[Name]          ,'') as pnonm              ,
               isnull(a.Dwgno           ,'') as Dwgno              ,
               isnull(a.Goodcd          ,'') as Goodcd             ,
               isnull(g.GoodNo          ,'') as Goodno             ,
               isnull(g.Spec            ,'') as spec               ,
               isnull(g.Class2          ,'') as Class2             ,
               isnull(g.Class3          ,'') as Class3             ,
               isnull(g.Class4          ,'') as Class4             ,
               isnull(g.Class5          ,'') as Class5             ,
               isnull(m2.MinorNm        ,'') as Class2nm           ,
               isnull(m3.MinorNm        ,'') as Class3nm           ,
               isnull(m4.MinorNm        ,'') as Class4nm           ,
               isnull(m5.MinorNm        ,'') as Class5nm           ,
               isnull(a.HCN             ,'') as HCN                ,
               isnull(a.Marking         ,'') as Marking            ,
               isnull(a.Raw_Materialcd  ,'') as RM_Goodcd          ,
               isnull(gg.GoodNo         ,'') as RM_Goodno          ,
               isnull(gg.Spec           ,'') as RM_Spec            ,
               isnull(a.Requirement     , 0) as Requirement        ,
               isnull(a.Whole_Length    , 0) as W_Length           ,
               isnull(a.Crepno          ,'') as Crepno             ,
               isnull(a.Modpno          ,'') as Modpno             ,
               isnull(a.Remark          ,'') as Remark
        from TGood_Workreport_Info a
            left outer join TDept d on a.deptcd = d.deptcd
            left outer join TMan m on a.pno = m.pno
            left outer join TGood g on a.goodcd = g.goodcd
            left outer join TMinor m2 on g.class2 = m2.minorcd
            left outer join TMinor m3 on g.class3 = m3.minorcd
            left outer join TMinor m4 on g.class4 = m4.minorcd
            left outer join TMinor m5 on g.class5 = m5.minorcd
            left outer join TGood gg on a.Raw_Materialcd = gg.goodcd
        where a.Accunit = @iAccunit
          and a.Factory = @iFactory
        order by g.Class2, g.Class3, g.Class4, g.GoodNo  """

            )
    row = cursor.fetchone()
    while row:
        print(row[0])
        row = cursor.fetchone()

    return row