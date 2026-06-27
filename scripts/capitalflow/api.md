# 柱状图fetch接口
## 行业资金流
1. 今日排行
```
curl 'https://data.eastmoney.com/dataapi/bkzj/getbkzj?key=f62&code=m%3A90%2Bs%3A4' \
  -H 'Accept: */*' \
  -H 'Accept-Language: zh-CN,zh;q=0.9' \
  -H 'Connection: keep-alive' \
  -b 'qgqp_b_id=2811034bbb8be0a803dd44a1d4bc6439; st_nvi=B_R4snS65CIm-zdxLQJJXdd9c; nid18=07da937ef8413b08c931d7708ccd213f; nid18_create_time=1782135615399; gviem=FNx5J-pKBN6R_6uGDQIzL8948; gviem_create_time=1782135615399; websitepoptg_api_time=1782483166763; st_si=41375670201268; fullscreengg=1; fullscreengg2=1; st_asi=delete; st_pvi=74492257636238; st_sp=2026-02-25%2023%3A30%3A16; st_inirUrl=https%3A%2F%2Fwww.google.com%2F; st_sn=32; st_psi=20260627153146977-113300300820-7876171354' \
  -H 'Referer: https://data.eastmoney.com/bkzj/hy.html?stat=10' \
  -H 'Sec-Fetch-Dest: empty' \
  -H 'Sec-Fetch-Mode: cors' \
  -H 'Sec-Fetch-Site: same-origin' \
  -H 'User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36' \
  -H 'X-Requested-With: XMLHttpRequest' \
  -H 'sec-ch-ua: "Google Chrome";v="149", "Chromium";v="149", "Not)A;Brand";v="24"' \
  -H 'sec-ch-ua-mobile: ?0' \
  -H 'sec-ch-ua-platform: "Windows"'
```

2. 5日排行
```
curl 'https://data.eastmoney.com/dataapi/bkzj/getbkzj?key=f164&code=m%3A90%2Bs%3A4' \
  -H 'Accept: */*' \
  -H 'Accept-Language: zh-CN,zh;q=0.9' \
  -H 'Connection: keep-alive' \
  -b 'qgqp_b_id=2811034bbb8be0a803dd44a1d4bc6439; st_nvi=B_R4snS65CIm-zdxLQJJXdd9c; nid18=07da937ef8413b08c931d7708ccd213f; nid18_create_time=1782135615399; gviem=FNx5J-pKBN6R_6uGDQIzL8948; gviem_create_time=1782135615399; websitepoptg_api_time=1782483166763; st_si=41375670201268; fullscreengg=1; fullscreengg2=1; st_pvi=74492257636238; st_sp=2026-02-25%2023%3A30%3A16; st_inirUrl=https%3A%2F%2Fwww.google.com%2F; st_sn=34; st_psi=20260627153552848-113200313000-4083020338; st_asi=20260627153552848-113200313000-4083020338-hqdyweb.fbkbg-1' \
  -H 'Referer: https://data.eastmoney.com/bkzj/hy.html?stat=10' \
  -H 'Sec-Fetch-Dest: empty' \
  -H 'Sec-Fetch-Mode: cors' \
  -H 'Sec-Fetch-Site: same-origin' \
  -H 'User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36' \
  -H 'X-Requested-With: XMLHttpRequest' \
  -H 'sec-ch-ua: "Google Chrome";v="149", "Chromium";v="149", "Not)A;Brand";v="24"' \
  -H 'sec-ch-ua-mobile: ?0' \
  -H 'sec-ch-ua-platform: "Windows"'
```
  
3. 10日排行
```
curl 'https://data.eastmoney.com/dataapi/bkzj/getbkzj?key=f174&code=m%3A90%2Bs%3A4' \
  -H 'Accept: */*' \
  -H 'Accept-Language: zh-CN,zh;q=0.9' \
  -H 'Connection: keep-alive' \
  -b 'qgqp_b_id=2811034bbb8be0a803dd44a1d4bc6439; st_nvi=B_R4snS65CIm-zdxLQJJXdd9c; nid18=07da937ef8413b08c931d7708ccd213f; nid18_create_time=1782135615399; gviem=FNx5J-pKBN6R_6uGDQIzL8948; gviem_create_time=1782135615399; websitepoptg_api_time=1782483166763; st_si=41375670201268; fullscreengg=1; fullscreengg2=1; st_pvi=74492257636238; st_sp=2026-02-25%2023%3A30%3A16; st_inirUrl=https%3A%2F%2Fwww.google.com%2F; st_sn=34; st_psi=20260627153552848-113200313000-4083020338; st_asi=20260627153552848-113200313000-4083020338-hqdyweb.fbkbg-1' \
  -H 'Referer: https://data.eastmoney.com/bkzj/hy.html?stat=10' \
  -H 'Sec-Fetch-Dest: empty' \
  -H 'Sec-Fetch-Mode: cors' \
  -H 'Sec-Fetch-Site: same-origin' \
  -H 'User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36' \
  -H 'X-Requested-With: XMLHttpRequest' \
  -H 'sec-ch-ua: "Google Chrome";v="149", "Chromium";v="149", "Not)A;Brand";v="24"' \
  -H 'sec-ch-ua-mobile: ?0' \
  -H 'sec-ch-ua-platform: "Windows"'
```

# resp
    以今日排行为例
```
{"rc":0,"rt":6,"svr":177542488,"lt":1,"full":1,"dlmkts":"","dsc":"0","data":{"total":128,"diff":[{"f12":"BK1036","f13":90,"f14":"半导体","f174":5243314176},{"f12":"BK0727","f13":90,"f14":"医疗服务","f174":3210997232},{"f12":"BK0473","f13":90,"f14":"证券Ⅱ","f174":2938774272},{"f12":"BK0735","f13":90,"f14":"计算机设备","f174":2020313840},{"f12":"BK0546","f13":90,"f14":"玻璃玻纤","f174":1380125952},{"f12":"BK1224","f13":90,"f14":"纺织制造","f174":490329912},{"f12":"BK1032","f13":90,"f14":"风电设备","f174":429969056},{"f12":"BK1016","f13":90,"f14":"汽车服务","f174":303598213},{"f12":"BK1254","f13":90,"f14":"动物保健Ⅱ","f174":40577457},{"f12":"BK1282","f13":90,"f14":"饮料乳品","f174":9434768},{"f12":"BK1043","f13":90,"f14":"专业服务","f174":7006720},{"f12":"BK1263","f13":90,"f14":"摩托车及其他","f174":-13893691},{"f12":"BK1227","f13":90,"f14":"特钢Ⅱ","f174":-15943710},{"f12":"BK1223","f13":90,"f14":"其他电子Ⅱ","f174":-16055808},{"f12":"BK1257","f13":90,"f14":"农业综合Ⅱ","f174":-25254191},{"f12":"BK1243","f13":90,"f14":"其他家电Ⅱ","f174":-45280626},{"f12":"BK1234","f13":90,"f14":"环保设备Ⅱ","f174":-49511008},{"f12":"BK1280","f13":90,"f14":"食品加工","f174":-52213542},{"f12":"BK1018","f13":90,"f14":"橡胶","f174":-66648109},{"f12":"BK1240","f13":90,"f14":"厨卫电器","f174":-84899846},{"f12":"BK1251","f13":90,"f14":"个护用品","f174":-95300543},{"f12":"BK1268","f13":90,"f14":"互联网电商","f174":-98857169},{"f12":"BK1260","f13":90,"f14":"渔业","f174":-103088045},{"f12":"BK0420","f13":90,"f14":"航空机场","f174":-131057552},{"f12":"BK1249","f13":90,"f14":"焦炭Ⅱ","f174":-137126561},{"f12":"BK1045","f13":90,"f14":"房地产服务","f174":-161659765},{"f12":"BK1245","f13":90,"f14":"照明设备Ⅱ","f174":-174040485},{"f12":"BK1253","f13":90,"f14":"医疗美容","f174":-191688165},{"f12":"BK0734","f13":90,"f14":"饰品","f174":-207281847},{"f12":"BK1271","f13":90,"f14":"酒店餐饮","f174":-259257334},{"f12":"BK0725","f13":90,"f14":"装修装饰Ⅱ","f174":-270246306},{"f12":"BK0484","f13":90,"f14":"贸易Ⅱ","f174":-271426386},{"f12":"BK1239","f13":90,"f14":"白色家电","f174":-315309216},{"f12":"BK1229","f13":90,"f14":"地面兵装Ⅱ","f174":-328358757},{"f12":"BK0450","f13":90,"f14":"航运港口","f174":-338349360},{"f12":"BK1270","f13":90,"f14":"专业连锁Ⅱ","f174":-383893650},{"f12":"BK0476","f13":90,"f14":"装修建材","f174":-386126048},{"f12":"BK0440","f13":90,"f14":"家居用品","f174":-401898080},{"f12":"BK1281","f13":90,"f14":"休闲食品","f174":-414120165},{"f12":"BK1273","f13":90,"f14":"体育Ⅱ","f174":-425484767},{"f12":"BK0424","f13":90,"f14":"水泥","f174":-437936095},{"f12":"BK1226","f13":90,"f14":"普钢","f174":-447920144},{"f12":"BK0738","f13":90,"f14":"多元金融","f174":-463447056},{"f12":"BK1252","f13":90,"f14":"化妆品","f174":-467212084},{"f12":"BK1028","f13":90,"f14":"燃气Ⅱ","f174":-478485347},{"f12":"BK1219","f13":90,"f14":"电视广播Ⅱ","f174":-481959959},{"f12":"BK1042","f13":90,"f14":"医药商业","f174":-549443233},{"f12":"BK1255","f13":90,"f14":"林业Ⅱ","f174":-585371942},{"f12":"BK1266","f13":90,"f14":"文娱用品","f174":-602425724},{"f12":"BK1241","f13":90,"f14":"黑色家电","f174":-623920426},{"f12":"BK1278","f13":90,"f14":"调味发酵品Ⅱ","f174":-646875712},{"f12":"BK1228","f13":90,"f14":"冶钢原料","f174":-697234902},{"f12":"BK0740","f13":90,"f14":"教育","f174":-730177271},{"f12":"BK1258","f13":90,"f14":"饲料","f174":-734813383},{"f12":"BK1267","f13":90,"f14":"造纸","f174":-772350415},{"f12":"BK1259","f13":90,"f14":"养殖业","f174":-773544144},{"f12":"BK0422","f13":90,"f14":"物流","f174":-790298897},{"f12":"BK1225","f13":90,"f14":"服装家纺","f174":-832143632},{"f12":"BK0421","f13":90,"f14":"铁路公路","f174":-833431824},{"f12":"BK1038","f13":90,"f14":"光学光电子","f174":-836548608},{"f12":"BK1261","f13":90,"f14":"种植业","f174":-887004202},{"f12":"BK0739","f13":90,"f14":"工程机械","f174":-907954544},{"f12":"BK1246","f13":90,"f14":"房屋建设Ⅱ","f174":-918240201},{"f12":"BK1044","f13":90,"f14":"生物制品","f174":-939263584},{"f12":"BK0471","f13":90,"f14":"化学纤维","f174":-945771664},{"f12":"BK1272","f13":90,"f14":"旅游及景区","f174":-952017520},{"f12":"BK0539","f13":90,"f14":"综合Ⅱ","f174":-970110928},{"f12":"BK1248","f13":90,"f14":"专业工程","f174":-983231568},{"f12":"BK1230","f13":90,"f14":"航海装备Ⅱ","f174":-1004522288},{"f12":"BK1218","f13":90,"f14":"出版","f174":-1008186769},{"f12":"BK1288","f13":90,"f14":"金属新材料","f174":-1025225696},{"f12":"BK1244","f13":90,"f14":"小家电","f174":-1033359418},{"f12":"BK1269","f13":90,"f14":"旅游零售Ⅱ","f174":-1044914317},{"f12":"BK1041","f13":90,"f14":"医疗器械","f174":-1101574752},{"f12":"BK1256","f13":90,"f14":"农产品加工","f174":-1193382914},{"f12":"BK1221","f13":90,"f14":"数字媒体","f174":-1203000848},{"f12":"BK1236","f13":90,"f14":"轨交设备Ⅱ","f174":-1216504288},{"f12":"BK1247","f13":90,"f14":"基础建设","f174":-1260655680},{"f12":"BK1275","f13":90,"f14":"油服工程","f174":-1294964311},{"f12":"BK1222","f13":90,"f14":"影视院线","f174":-1369051064},{"f12":"BK0726","f13":90,"f14":"工程咨询服务Ⅱ","f174":-1388261936},{"f12":"BK1279","f13":90,"f14":"非白酒","f174":-1430849875},{"f12":"BK1265","f13":90,"f14":"包装印刷","f174":-1471455840},{"f12":"BK1020","f13":90,"f14":"非金属材料Ⅱ","f174":-1514746656},{"f12":"BK0451","f13":90,"f14":"房地产开发","f174":-1519708720},{"f12":"BK1040","f13":90,"f14":"中药Ⅱ","f174":-1559430576},{"f12":"BK0482","f13":90,"f14":"一般零售","f174":-1591502016},{"f12":"BK1019","f13":90,"f14":"化学原料","f174":-1717890624},{"f12":"BK0731","f13":90,"f14":"农化制品","f174":-1751765696},{"f12":"BK1274","f13":90,"f14":"炼化及贸易","f174":-1796246880},{"f12":"BK1046","f13":90,"f14":"游戏Ⅱ","f174":-1837392096},{"f12":"BK0910","f13":90,"f14":"专用设备","f174":-1901074688},{"f12":"BK1264","f13":90,"f14":"商用车","f174":-1948179152},{"f12":"BK1235","f13":90,"f14":"环境治理","f174":-2015918800},{"f12":"BK1034","f13":90,"f14":"其他电源设备Ⅱ","f174":-2167111536},{"f12":"BK1030","f13":90,"f14":"电机Ⅱ","f174":-2334619216},{"f12":"BK1276","f13":90,"f14":"油气开采Ⅱ","f174":-2741928253},{"f12":"BK0474","f13":90,"f14":"保险Ⅱ","f174":-3285309840},{"f12":"BK1031","f13":90,"f14":"光伏设备","f174":-3744381696},{"f12":"BK0736","f13":90,"f14":"通信服务","f174":-4067986704},{"f12":"BK0475","f13":90,"f14":"银行Ⅱ","f174":-4248135280},{"f12":"BK0732","f13":90,"f14":"贵金属","f174":-4261423152},{"f12":"BK1232","f13":90,"f14":"航天装备Ⅱ","f174":-4263785184},{"f12":"BK1233","f13":90,"f14":"军工电子Ⅱ","f174":-4307575024},{"f12":"BK1220","f13":90,"f14":"广告营销","f174":-4331230944},{"f12":"BK0545","f13":90,"f14":"通用设备","f174":-4446838272},{"f12":"BK1231","f13":90,"f14":"航空装备Ⅱ","f174":-4720069696},{"f12":"BK1242","f13":90,"f14":"家电零部件Ⅱ","f174":-4734241680},{"f12":"BK0465","f13":90,"f14":"化学制药","f174":-4888059024},{"f12":"BK1250","f13":90,"f14":"煤炭开采","f174":-5928571264},{"f12":"BK0457","f13":90,"f14":"电网设备","f174":-6143436032},{"f12":"BK1262","f13":90,"f14":"乘用车","f174":-6791306976},{"f12":"BK0454","f13":90,"f14":"塑料","f174":-7127072560},{"f12":"BK1277","f13":90,"f14":"白酒Ⅱ","f174":-7411409952},{"f12":"BK0538","f13":90,"f14":"化学制品","f174":-8073031168},{"f12":"BK0737","f13":90,"f14":"软件开发","f174":-8258542480},{"f12":"BK1015","f13":90,"f14":"能源金属","f174":-8427581840},{"f12":"BK1238","f13":90,"f14":"IT服务Ⅱ","f174":-8688139376},{"f12":"BK1039","f13":90,"f14":"电子化学品Ⅱ","f174":-8902487040},{"f12":"BK1237","f13":90,"f14":"自动化设备","f174":-10744312576},{"f12":"BK0481","f13":90,"f14":"汽车零部件","f174":-11206093824},{"f12":"BK1287","f13":90,"f14":"工业金属","f174":-12011981824},{"f12":"BK1037","f13":90,"f14":"消费电子","f174":-13820847872},{"f12":"BK1027","f13":90,"f14":"小金属","f174":-14993239296},{"f12":"BK0428","f13":90,"f14":"电力","f174":-16037965312},{"f12":"BK0459","f13":90,"f14":"元件","f174":-19556851712},{"f12":"BK1033","f13":90,"f14":"电池","f174":-24228280832},{"f12":"BK0448","f13":90,"f14":"通信设备","f174":-56682109696}]}}
```

## 概念资金流
1. 今日排行
```
curl 'https://data.eastmoney.com/dataapi/bkzj/getbkzj?key=f164&code=m%3A90%2Bt%3A3' \
  -H 'Accept: */*' \
  -H 'Accept-Language: zh-CN,zh;q=0.9' \
  -H 'Connection: keep-alive' \
  -b 'qgqp_b_id=2811034bbb8be0a803dd44a1d4bc6439; st_nvi=B_R4snS65CIm-zdxLQJJXdd9c; nid18=07da937ef8413b08c931d7708ccd213f; nid18_create_time=1782135615399; gviem=FNx5J-pKBN6R_6uGDQIzL8948; gviem_create_time=1782135615399; websitepoptg_api_time=1782483166763; st_si=41375670201268; fullscreengg=1; fullscreengg2=1; st_pvi=74492257636238; st_sp=2026-02-25%2023%3A30%3A16; st_inirUrl=https%3A%2F%2Fwww.google.com%2F; st_sn=35; st_psi=20260627153817306-113300300992-0469330211; st_asi=20260627153146977-113300300820-7876171354-dfcfwsy_dfcfwxsy_ycl_ewmxt-4' \
  -H 'Referer: https://data.eastmoney.com/bkzj/hy.html?stat=10' \
  -H 'Sec-Fetch-Dest: empty' \
  -H 'Sec-Fetch-Mode: cors' \
  -H 'Sec-Fetch-Site: same-origin' \
  -H 'User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36' \
  -H 'X-Requested-With: XMLHttpRequest' \
  -H 'sec-ch-ua: "Google Chrome";v="149", "Chromium";v="149", "Not)A;Brand";v="24"' \
  -H 'sec-ch-ua-mobile: ?0' \
  -H 'sec-ch-ua-platform: "Windows"' ;
curl 'https://data.eastmoney.com/dataapi/bkzj/getbkzj?key=f62&code=m%3A90%2Bt%3A3' \
  -H 'Accept: */*' \
  -H 'Accept-Language: zh-CN,zh;q=0.9' \
  -H 'Connection: keep-alive' \
  -b 'qgqp_b_id=2811034bbb8be0a803dd44a1d4bc6439; st_nvi=B_R4snS65CIm-zdxLQJJXdd9c; nid18=07da937ef8413b08c931d7708ccd213f; nid18_create_time=1782135615399; gviem=FNx5J-pKBN6R_6uGDQIzL8948; gviem_create_time=1782135615399; websitepoptg_api_time=1782483166763; st_si=41375670201268; fullscreengg=1; fullscreengg2=1; st_pvi=74492257636238; st_sp=2026-02-25%2023%3A30%3A16; st_inirUrl=https%3A%2F%2Fwww.google.com%2F; st_sn=35; st_psi=20260627153817306-113300300992-0469330211; st_asi=20260627153146977-113300300820-7876171354-dfcfwsy_dfcfwxsy_ycl_ewmxt-4' \
  -H 'Referer: https://data.eastmoney.com/bkzj/hy.html?stat=10' \
  -H 'Sec-Fetch-Dest: empty' \
  -H 'Sec-Fetch-Mode: cors' \
  -H 'Sec-Fetch-Site: same-origin' \
  -H 'User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36' \
  -H 'X-Requested-With: XMLHttpRequest' \
  -H 'sec-ch-ua: "Google Chrome";v="149", "Chromium";v="149", "Not)A;Brand";v="24"' \
  -H 'sec-ch-ua-mobile: ?0' \
  -H 'sec-ch-ua-platform: "Windows"'
```
2. 5日排行
```
curl 'https://data.eastmoney.com/dataapi/bkzj/getbkzj?key=f164&code=m%3A90%2Bt%3A3' \
  -H 'Accept: */*' \
  -H 'Accept-Language: zh-CN,zh;q=0.9' \
  -H 'Connection: keep-alive' \
  -b 'qgqp_b_id=2811034bbb8be0a803dd44a1d4bc6439; st_nvi=B_R4snS65CIm-zdxLQJJXdd9c; nid18=07da937ef8413b08c931d7708ccd213f; nid18_create_time=1782135615399; gviem=FNx5J-pKBN6R_6uGDQIzL8948; gviem_create_time=1782135615399; websitepoptg_api_time=1782483166763; st_si=41375670201268; fullscreengg=1; fullscreengg2=1; st_pvi=74492257636238; st_sp=2026-02-25%2023%3A30%3A16; st_inirUrl=https%3A%2F%2Fwww.google.com%2F; st_sn=35; st_psi=20260627153817306-113300300992-0469330211; st_asi=20260627153146977-113300300820-7876171354-dfcfwsy_dfcfwxsy_ycl_ewmxt-4' \
  -H 'Referer: https://data.eastmoney.com/bkzj/hy.html?stat=10' \
  -H 'Sec-Fetch-Dest: empty' \
  -H 'Sec-Fetch-Mode: cors' \
  -H 'Sec-Fetch-Site: same-origin' \
  -H 'User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36' \
  -H 'X-Requested-With: XMLHttpRequest' \
  -H 'sec-ch-ua: "Google Chrome";v="149", "Chromium";v="149", "Not)A;Brand";v="24"' \
  -H 'sec-ch-ua-mobile: ?0' \
  -H 'sec-ch-ua-platform: "Windows"'
```
3. 10日排行
```
curl 'https://data.eastmoney.com/dataapi/bkzj/getbkzj?key=f164&code=m%3A90%2Bt%3A3' \
  -H 'Accept: */*' \
  -H 'Accept-Language: zh-CN,zh;q=0.9' \
  -H 'Connection: keep-alive' \
  -b 'qgqp_b_id=2811034bbb8be0a803dd44a1d4bc6439; st_nvi=B_R4snS65CIm-zdxLQJJXdd9c; nid18=07da937ef8413b08c931d7708ccd213f; nid18_create_time=1782135615399; gviem=FNx5J-pKBN6R_6uGDQIzL8948; gviem_create_time=1782135615399; websitepoptg_api_time=1782483166763; st_si=41375670201268; fullscreengg=1; fullscreengg2=1; st_pvi=74492257636238; st_sp=2026-02-25%2023%3A30%3A16; st_inirUrl=https%3A%2F%2Fwww.google.com%2F; st_sn=35; st_psi=20260627153817306-113300300992-0469330211; st_asi=20260627153146977-113300300820-7876171354-dfcfwsy_dfcfwxsy_ycl_ewmxt-4' \
  -H 'Referer: https://data.eastmoney.com/bkzj/hy.html?stat=10' \
  -H 'Sec-Fetch-Dest: empty' \
  -H 'Sec-Fetch-Mode: cors' \
  -H 'Sec-Fetch-Site: same-origin' \
  -H 'User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36' \
  -H 'X-Requested-With: XMLHttpRequest' \
  -H 'sec-ch-ua: "Google Chrome";v="149", "Chromium";v="149", "Not)A;Brand";v="24"' \
  -H 'sec-ch-ua-mobile: ?0' \
  -H 'sec-ch-ua-platform: "Windows"' ;
curl 'https://data.eastmoney.com/dataapi/bkzj/getbkzj?key=f62&code=m%3A90%2Bt%3A3' \
  -H 'Accept: */*' \
  -H 'Accept-Language: zh-CN,zh;q=0.9' \
  -H 'Connection: keep-alive' \
  -b 'qgqp_b_id=2811034bbb8be0a803dd44a1d4bc6439; st_nvi=B_R4snS65CIm-zdxLQJJXdd9c; nid18=07da937ef8413b08c931d7708ccd213f; nid18_create_time=1782135615399; gviem=FNx5J-pKBN6R_6uGDQIzL8948; gviem_create_time=1782135615399; websitepoptg_api_time=1782483166763; st_si=41375670201268; fullscreengg=1; fullscreengg2=1; st_pvi=74492257636238; st_sp=2026-02-25%2023%3A30%3A16; st_inirUrl=https%3A%2F%2Fwww.google.com%2F; st_sn=35; st_psi=20260627153817306-113300300992-0469330211; st_asi=20260627153146977-113300300820-7876171354-dfcfwsy_dfcfwxsy_ycl_ewmxt-4' \
  -H 'Referer: https://data.eastmoney.com/bkzj/hy.html?stat=10' \
  -H 'Sec-Fetch-Dest: empty' \
  -H 'Sec-Fetch-Mode: cors' \
  -H 'Sec-Fetch-Site: same-origin' \
  -H 'User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36' \
  -H 'X-Requested-With: XMLHttpRequest' \
  -H 'sec-ch-ua: "Google Chrome";v="149", "Chromium";v="149", "Not)A;Brand";v="24"' \
  -H 'sec-ch-ua-mobile: ?0' \
  -H 'sec-ch-ua-platform: "Windows"' ;
curl 'https://data.eastmoney.com/dataapi/bkzj/getbkzj?key=f174&code=m%3A90%2Bt%3A3' \
  -H 'Accept: */*' \
  -H 'Accept-Language: zh-CN,zh;q=0.9' \
  -H 'Connection: keep-alive' \
  -b 'qgqp_b_id=2811034bbb8be0a803dd44a1d4bc6439; st_nvi=B_R4snS65CIm-zdxLQJJXdd9c; nid18=07da937ef8413b08c931d7708ccd213f; nid18_create_time=1782135615399; gviem=FNx5J-pKBN6R_6uGDQIzL8948; gviem_create_time=1782135615399; websitepoptg_api_time=1782483166763; st_si=41375670201268; fullscreengg=1; fullscreengg2=1; st_pvi=74492257636238; st_sp=2026-02-25%2023%3A30%3A16; st_inirUrl=https%3A%2F%2Fwww.google.com%2F; st_sn=35; st_psi=20260627153817306-113300300992-0469330211; st_asi=20260627153146977-113300300820-7876171354-dfcfwsy_dfcfwxsy_ycl_ewmxt-4' \
  -H 'Referer: https://data.eastmoney.com/bkzj/hy.html?stat=10' \
  -H 'Sec-Fetch-Dest: empty' \
  -H 'Sec-Fetch-Mode: cors' \
  -H 'Sec-Fetch-Site: same-origin' \
  -H 'User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36' \
  -H 'X-Requested-With: XMLHttpRequest' \
  -H 'sec-ch-ua: "Google Chrome";v="149", "Chromium";v="149", "Not)A;Brand";v="24"' \
  -H 'sec-ch-ua-mobile: ?0' \
  -H 'sec-ch-ua-platform: "Windows"'
```

# 表格fetch接口
## 行业资金流
1. 今日排行
```
curl 'https://data.eastmoney.com/dataapi/bkzj/getbkzj?key=f164&code=m%3A90%2Bs%3A4' \
  -H 'Accept: */*' \
  -H 'Accept-Language: zh-CN,zh;q=0.9' \
  -H 'Connection: keep-alive' \
  -b 'qgqp_b_id=2811034bbb8be0a803dd44a1d4bc6439; st_nvi=B_R4snS65CIm-zdxLQJJXdd9c; nid18=07da937ef8413b08c931d7708ccd213f; nid18_create_time=1782135615399; gviem=FNx5J-pKBN6R_6uGDQIzL8948; gviem_create_time=1782135615399; websitepoptg_api_time=1782483166763; st_si=41375670201268; fullscreengg=1; fullscreengg2=1; st_asi=delete; st_pvi=74492257636238; st_sp=2026-02-25%2023%3A30%3A16; st_inirUrl=https%3A%2F%2Fwww.google.com%2F; st_sn=44; st_psi=20260627162954792-111000300841-2309886357' \
  -H 'Referer: https://data.eastmoney.com/bkzj/hy.html?stat=10' \
  -H 'Sec-Fetch-Dest: empty' \
  -H 'Sec-Fetch-Mode: cors' \
  -H 'Sec-Fetch-Site: same-origin' \
  -H 'User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36' \
  -H 'X-Requested-With: XMLHttpRequest' \
  -H 'sec-ch-ua: "Google Chrome";v="149", "Chromium";v="149", "Not)A;Brand";v="24"' \
  -H 'sec-ch-ua-mobile: ?0' \
  -H 'sec-ch-ua-platform: "Windows"' ;
curl 'https://push2.eastmoney.com/api/qt/clist/get?cb=jQuery112303664902929155055_1782545506900&fid=f164&po=1&pz=50&pn=1&np=1&fltt=2&invt=2&ut=8dec03ba335b81bf4ebdf7b29ec27d15&fs=m%3A90+s%3A4&fields=f12%2Cf14%2Cf2%2Cf109%2Cf164%2Cf165%2Cf166%2Cf167%2Cf168%2Cf169%2Cf170%2Cf171%2Cf172%2Cf173%2Cf257%2Cf258%2Cf124%2Cf1%2Cf13' \
  -H 'Accept: */*' \
  -H 'Accept-Language: zh-CN,zh;q=0.9' \
  -H 'Connection: keep-alive' \
  -b 'qgqp_b_id=2811034bbb8be0a803dd44a1d4bc6439; st_nvi=B_R4snS65CIm-zdxLQJJXdd9c; nid18=07da937ef8413b08c931d7708ccd213f; nid18_create_time=1782135615399; gviem=FNx5J-pKBN6R_6uGDQIzL8948; gviem_create_time=1782135615399; websitepoptg_api_time=1782483166763; st_si=41375670201268; fullscreengg=1; fullscreengg2=1; st_asi=delete; st_pvi=74492257636238; st_sp=2026-02-25%2023%3A30%3A16; st_inirUrl=https%3A%2F%2Fwww.google.com%2F; st_sn=44; st_psi=20260627162954792-111000300841-2309886357' \
  -H 'Referer: https://data.eastmoney.com/bkzj/hy.html?stat=10' \
  -H 'Sec-Fetch-Dest: script' \
  -H 'Sec-Fetch-Mode: no-cors' \
  -H 'Sec-Fetch-Site: same-site' \
  -H 'User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36' \
  -H 'sec-ch-ua: "Google Chrome";v="149", "Chromium";v="149", "Not)A;Brand";v="24"' \
  -H 'sec-ch-ua-mobile: ?0' \
  -H 'sec-ch-ua-platform: "Windows"' ;
curl 'https://huaxiang.eastmoney.com/CommonRecommend.png?json=%7B%22lastModifyTime%22%3A%22_lastModifyTime_%22%2C%22type%22%3A%22pageclick%22%2C%22coord_x%22%3A-234%2C%22coord_y%22%3A475%2C%22elename%22%3A%22LI%22%2C%22uid%22%3A%22%22%2C%22bid%22%3A%222811034bbb8be0a803dd44a1d4bc6439%22%2C%22referer%22%3A%22https%3A%2F%2Fdata.eastmoney.com%2Fbkzj%2F%22%2C%22pagetype%22%3A%22%22%2C%22pageitem%22%3A%22%22%2C%22browser_height%22%3A1271%2C%22from%22%3A%22https%3A%2F%2Fdata.eastmoney.com%2Fbkzj%2Fhy.html%3Fstat%3D10%22%2C%22index_width%22%3A%221000%22%2C%22index_ad%22%3A%220%22%2C%22domainId%22%3A%22data.eastmoney.com%22%2C%22st_pvi%22%3A%2274492257636238%22%2C%22emtj_pageId%22%3A113300300820%7D' \
  -H 'Accept: image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8' \
  -H 'Accept-Language: zh-CN,zh;q=0.9' \
  -H 'Connection: keep-alive' \
  -b 'qgqp_b_id=2811034bbb8be0a803dd44a1d4bc6439; st_nvi=B_R4snS65CIm-zdxLQJJXdd9c; nid18=07da937ef8413b08c931d7708ccd213f; nid18_create_time=1782135615399; gviem=FNx5J-pKBN6R_6uGDQIzL8948; gviem_create_time=1782135615399; websitepoptg_api_time=1782483166763; st_si=41375670201268; fullscreengg=1; fullscreengg2=1; st_asi=delete; st_pvi=74492257636238; st_sp=2026-02-25%2023%3A30%3A16; st_inirUrl=https%3A%2F%2Fwww.google.com%2F; st_sn=44; st_psi=20260627162954792-111000300841-2309886357' \
  -H 'Referer: https://data.eastmoney.com/bkzj/hy.html?stat=10' \
  -H 'Sec-Fetch-Dest: image' \
  -H 'Sec-Fetch-Mode: no-cors' \
  -H 'Sec-Fetch-Site: same-site' \
  -H 'User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36' \
  -H 'sec-ch-ua: "Google Chrome";v="149", "Chromium";v="149", "Not)A;Brand";v="24"' \
  -H 'sec-ch-ua-mobile: ?0' \
  -H 'sec-ch-ua-platform: "Windows"' ;
curl 'https://data.eastmoney.com/dataapi/bkzj/getbkzj?key=f62&code=m%3A90%2Bs%3A4' \
  -H 'Accept: */*' \
  -H 'Accept-Language: zh-CN,zh;q=0.9' \
  -H 'Connection: keep-alive' \
  -b 'qgqp_b_id=2811034bbb8be0a803dd44a1d4bc6439; st_nvi=B_R4snS65CIm-zdxLQJJXdd9c; nid18=07da937ef8413b08c931d7708ccd213f; nid18_create_time=1782135615399; gviem=FNx5J-pKBN6R_6uGDQIzL8948; gviem_create_time=1782135615399; websitepoptg_api_time=1782483166763; st_si=41375670201268; fullscreengg=1; fullscreengg2=1; st_asi=delete; st_pvi=74492257636238; st_sp=2026-02-25%2023%3A30%3A16; st_inirUrl=https%3A%2F%2Fwww.google.com%2F; st_sn=44; st_psi=20260627162954792-111000300841-2309886357' \
  -H 'Referer: https://data.eastmoney.com/bkzj/hy.html?stat=10' \
  -H 'Sec-Fetch-Dest: empty' \
  -H 'Sec-Fetch-Mode: cors' \
  -H 'Sec-Fetch-Site: same-origin' \
  -H 'User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36' \
  -H 'X-Requested-With: XMLHttpRequest' \
  -H 'sec-ch-ua: "Google Chrome";v="149", "Chromium";v="149", "Not)A;Brand";v="24"' \
  -H 'sec-ch-ua-mobile: ?0' \
  -H 'sec-ch-ua-platform: "Windows"' ;
curl 'https://push2.eastmoney.com/api/qt/clist/get?cb=jQuery112303664902929155055_1782545506900&fid=f62&po=1&pz=50&pn=1&np=1&fltt=2&invt=2&ut=8dec03ba335b81bf4ebdf7b29ec27d15&fs=m%3A90+s%3A4&fields=f12%2Cf14%2Cf2%2Cf3%2Cf62%2Cf184%2Cf66%2Cf69%2Cf72%2Cf75%2Cf78%2Cf81%2Cf84%2Cf87%2Cf204%2Cf205%2Cf124%2Cf1%2Cf13' \
  -H 'Accept: */*' \
  -H 'Accept-Language: zh-CN,zh;q=0.9' \
  -H 'Connection: keep-alive' \
  -b 'qgqp_b_id=2811034bbb8be0a803dd44a1d4bc6439; st_nvi=B_R4snS65CIm-zdxLQJJXdd9c; nid18=07da937ef8413b08c931d7708ccd213f; nid18_create_time=1782135615399; gviem=FNx5J-pKBN6R_6uGDQIzL8948; gviem_create_time=1782135615399; websitepoptg_api_time=1782483166763; st_si=41375670201268; fullscreengg=1; fullscreengg2=1; st_asi=delete; st_pvi=74492257636238; st_sp=2026-02-25%2023%3A30%3A16; st_inirUrl=https%3A%2F%2Fwww.google.com%2F; st_sn=44; st_psi=20260627162954792-111000300841-2309886357' \
  -H 'Referer: https://data.eastmoney.com/bkzj/hy.html?stat=10' \
  -H 'Sec-Fetch-Dest: script' \
  -H 'Sec-Fetch-Mode: no-cors' \
  -H 'Sec-Fetch-Site: same-site' \
  -H 'User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36' \
  -H 'sec-ch-ua: "Google Chrome";v="149", "Chromium";v="149", "Not)A;Brand";v="24"' \
  -H 'sec-ch-ua-mobile: ?0' \
  -H 'sec-ch-ua-platform: "Windows"' ;
curl 'https://huaxiang.eastmoney.com/CommonRecommend.png?json=%7B%22lastModifyTime%22%3A%22_lastModifyTime_%22%2C%22type%22%3A%22pageclick%22%2C%22coord_x%22%3A-302%2C%22coord_y%22%3A466%2C%22elename%22%3A%22LI%22%2C%22uid%22%3A%22%22%2C%22bid%22%3A%222811034bbb8be0a803dd44a1d4bc6439%22%2C%22referer%22%3A%22https%3A%2F%2Fdata.eastmoney.com%2Fbkzj%2F%22%2C%22pagetype%22%3A%22%22%2C%22pageitem%22%3A%22%22%2C%22browser_height%22%3A1271%2C%22from%22%3A%22https%3A%2F%2Fdata.eastmoney.com%2Fbkzj%2Fhy.html%3Fstat%3D10%22%2C%22index_width%22%3A%221000%22%2C%22index_ad%22%3A%220%22%2C%22domainId%22%3A%22data.eastmoney.com%22%2C%22st_pvi%22%3A%2274492257636238%22%2C%22emtj_pageId%22%3A113300300820%7D' \
  -H 'Accept: image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8' \
  -H 'Accept-Language: zh-CN,zh;q=0.9' \
  -H 'Connection: keep-alive' \
  -b 'qgqp_b_id=2811034bbb8be0a803dd44a1d4bc6439; st_nvi=B_R4snS65CIm-zdxLQJJXdd9c; nid18=07da937ef8413b08c931d7708ccd213f; nid18_create_time=1782135615399; gviem=FNx5J-pKBN6R_6uGDQIzL8948; gviem_create_time=1782135615399; websitepoptg_api_time=1782483166763; st_si=41375670201268; fullscreengg=1; fullscreengg2=1; st_asi=delete; st_pvi=74492257636238; st_sp=2026-02-25%2023%3A30%3A16; st_inirUrl=https%3A%2F%2Fwww.google.com%2F; st_sn=44; st_psi=20260627162954792-111000300841-2309886357' \
  -H 'Referer: https://data.eastmoney.com/bkzj/hy.html?stat=10' \
  -H 'Sec-Fetch-Dest: image' \
  -H 'Sec-Fetch-Mode: no-cors' \
  -H 'Sec-Fetch-Site: same-site' \
  -H 'User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36' \
  -H 'sec-ch-ua: "Google Chrome";v="149", "Chromium";v="149", "Not)A;Brand";v="24"' \
  -H 'sec-ch-ua-mobile: ?0' \
  -H 'sec-ch-ua-platform: "Windows"'
```
2. 5日排行
```
curl 'https://data.eastmoney.com/dataapi/bkzj/getbkzj?key=f164&code=m%3A90%2Bs%3A4' \
  -H 'Accept: */*' \
  -H 'Accept-Language: zh-CN,zh;q=0.9' \
  -H 'Connection: keep-alive' \
  -b 'qgqp_b_id=2811034bbb8be0a803dd44a1d4bc6439; st_nvi=B_R4snS65CIm-zdxLQJJXdd9c; nid18=07da937ef8413b08c931d7708ccd213f; nid18_create_time=1782135615399; gviem=FNx5J-pKBN6R_6uGDQIzL8948; gviem_create_time=1782135615399; websitepoptg_api_time=1782483166763; st_si=41375670201268; fullscreengg=1; fullscreengg2=1; st_asi=delete; st_pvi=74492257636238; st_sp=2026-02-25%2023%3A30%3A16; st_inirUrl=https%3A%2F%2Fwww.google.com%2F; st_sn=44; st_psi=20260627162954792-111000300841-2309886357' \
  -H 'Referer: https://data.eastmoney.com/bkzj/hy.html?stat=10' \
  -H 'Sec-Fetch-Dest: empty' \
  -H 'Sec-Fetch-Mode: cors' \
  -H 'Sec-Fetch-Site: same-origin' \
  -H 'User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36' \
  -H 'X-Requested-With: XMLHttpRequest' \
  -H 'sec-ch-ua: "Google Chrome";v="149", "Chromium";v="149", "Not)A;Brand";v="24"' \
  -H 'sec-ch-ua-mobile: ?0' \
  -H 'sec-ch-ua-platform: "Windows"' ;
curl 'https://push2.eastmoney.com/api/qt/clist/get?cb=jQuery112303664902929155055_1782545506900&fid=f164&po=1&pz=50&pn=1&np=1&fltt=2&invt=2&ut=8dec03ba335b81bf4ebdf7b29ec27d15&fs=m%3A90+s%3A4&fields=f12%2Cf14%2Cf2%2Cf109%2Cf164%2Cf165%2Cf166%2Cf167%2Cf168%2Cf169%2Cf170%2Cf171%2Cf172%2Cf173%2Cf257%2Cf258%2Cf124%2Cf1%2Cf13' \
  -H 'Accept: */*' \
  -H 'Accept-Language: zh-CN,zh;q=0.9' \
  -H 'Connection: keep-alive' \
  -b 'qgqp_b_id=2811034bbb8be0a803dd44a1d4bc6439; st_nvi=B_R4snS65CIm-zdxLQJJXdd9c; nid18=07da937ef8413b08c931d7708ccd213f; nid18_create_time=1782135615399; gviem=FNx5J-pKBN6R_6uGDQIzL8948; gviem_create_time=1782135615399; websitepoptg_api_time=1782483166763; st_si=41375670201268; fullscreengg=1; fullscreengg2=1; st_asi=delete; st_pvi=74492257636238; st_sp=2026-02-25%2023%3A30%3A16; st_inirUrl=https%3A%2F%2Fwww.google.com%2F; st_sn=44; st_psi=20260627162954792-111000300841-2309886357' \
  -H 'Referer: https://data.eastmoney.com/bkzj/hy.html?stat=10' \
  -H 'Sec-Fetch-Dest: script' \
  -H 'Sec-Fetch-Mode: no-cors' \
  -H 'Sec-Fetch-Site: same-site' \
  -H 'User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36' \
  -H 'sec-ch-ua: "Google Chrome";v="149", "Chromium";v="149", "Not)A;Brand";v="24"' \
  -H 'sec-ch-ua-mobile: ?0' \
  -H 'sec-ch-ua-platform: "Windows"' ;
curl 'https://huaxiang.eastmoney.com/CommonRecommend.png?json=%7B%22lastModifyTime%22%3A%22_lastModifyTime_%22%2C%22type%22%3A%22pageclick%22%2C%22coord_x%22%3A-234%2C%22coord_y%22%3A475%2C%22elename%22%3A%22LI%22%2C%22uid%22%3A%22%22%2C%22bid%22%3A%222811034bbb8be0a803dd44a1d4bc6439%22%2C%22referer%22%3A%22https%3A%2F%2Fdata.eastmoney.com%2Fbkzj%2F%22%2C%22pagetype%22%3A%22%22%2C%22pageitem%22%3A%22%22%2C%22browser_height%22%3A1271%2C%22from%22%3A%22https%3A%2F%2Fdata.eastmoney.com%2Fbkzj%2Fhy.html%3Fstat%3D10%22%2C%22index_width%22%3A%221000%22%2C%22index_ad%22%3A%220%22%2C%22domainId%22%3A%22data.eastmoney.com%22%2C%22st_pvi%22%3A%2274492257636238%22%2C%22emtj_pageId%22%3A113300300820%7D' \
  -H 'Accept: image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8' \
  -H 'Accept-Language: zh-CN,zh;q=0.9' \
  -H 'Connection: keep-alive' \
  -b 'qgqp_b_id=2811034bbb8be0a803dd44a1d4bc6439; st_nvi=B_R4snS65CIm-zdxLQJJXdd9c; nid18=07da937ef8413b08c931d7708ccd213f; nid18_create_time=1782135615399; gviem=FNx5J-pKBN6R_6uGDQIzL8948; gviem_create_time=1782135615399; websitepoptg_api_time=1782483166763; st_si=41375670201268; fullscreengg=1; fullscreengg2=1; st_asi=delete; st_pvi=74492257636238; st_sp=2026-02-25%2023%3A30%3A16; st_inirUrl=https%3A%2F%2Fwww.google.com%2F; st_sn=44; st_psi=20260627162954792-111000300841-2309886357' \
  -H 'Referer: https://data.eastmoney.com/bkzj/hy.html?stat=10' \
  -H 'Sec-Fetch-Dest: image' \
  -H 'Sec-Fetch-Mode: no-cors' \
  -H 'Sec-Fetch-Site: same-site' \
  -H 'User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36' \
  -H 'sec-ch-ua: "Google Chrome";v="149", "Chromium";v="149", "Not)A;Brand";v="24"' \
  -H 'sec-ch-ua-mobile: ?0' \
  -H 'sec-ch-ua-platform: "Windows"'
```
3. 10日排行
```
curl 'https://data.eastmoney.com/dataapi/bkzj/getbkzj?key=f174&code=m%3A90%2Bs%3A4' \
  -H 'Accept: */*' \
  -H 'Accept-Language: zh-CN,zh;q=0.9' \
  -H 'Connection: keep-alive' \
  -b 'qgqp_b_id=2811034bbb8be0a803dd44a1d4bc6439; st_nvi=B_R4snS65CIm-zdxLQJJXdd9c; nid18=07da937ef8413b08c931d7708ccd213f; nid18_create_time=1782135615399; gviem=FNx5J-pKBN6R_6uGDQIzL8948; gviem_create_time=1782135615399; websitepoptg_api_time=1782483166763; st_si=41375670201268; fullscreengg=1; fullscreengg2=1; st_asi=delete; st_pvi=74492257636238; st_sp=2026-02-25%2023%3A30%3A16; st_inirUrl=https%3A%2F%2Fwww.google.com%2F; st_sn=44; st_psi=20260627162954792-111000300841-2309886357' \
  -H 'Referer: https://data.eastmoney.com/bkzj/hy.html?stat=10' \
  -H 'Sec-Fetch-Dest: empty' \
  -H 'Sec-Fetch-Mode: cors' \
  -H 'Sec-Fetch-Site: same-origin' \
  -H 'User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36' \
  -H 'X-Requested-With: XMLHttpRequest' \
  -H 'sec-ch-ua: "Google Chrome";v="149", "Chromium";v="149", "Not)A;Brand";v="24"' \
  -H 'sec-ch-ua-mobile: ?0' \
  -H 'sec-ch-ua-platform: "Windows"' ;
curl 'https://push2.eastmoney.com/api/qt/clist/get?cb=jQuery112303664902929155055_1782545506900&fid=f174&po=1&pz=50&pn=1&np=1&fltt=2&invt=2&ut=8dec03ba335b81bf4ebdf7b29ec27d15&fs=m%3A90+s%3A4&fields=f12%2Cf14%2Cf2%2Cf160%2Cf174%2Cf175%2Cf176%2Cf177%2Cf178%2Cf179%2Cf180%2Cf181%2Cf182%2Cf183%2Cf260%2Cf261%2Cf124%2Cf1%2Cf13' \
  -H 'Accept: */*' \
  -H 'Accept-Language: zh-CN,zh;q=0.9' \
  -H 'Connection: keep-alive' \
  -b 'qgqp_b_id=2811034bbb8be0a803dd44a1d4bc6439; st_nvi=B_R4snS65CIm-zdxLQJJXdd9c; nid18=07da937ef8413b08c931d7708ccd213f; nid18_create_time=1782135615399; gviem=FNx5J-pKBN6R_6uGDQIzL8948; gviem_create_time=1782135615399; websitepoptg_api_time=1782483166763; st_si=41375670201268; fullscreengg=1; fullscreengg2=1; st_asi=delete; st_pvi=74492257636238; st_sp=2026-02-25%2023%3A30%3A16; st_inirUrl=https%3A%2F%2Fwww.google.com%2F; st_sn=44; st_psi=20260627162954792-111000300841-2309886357' \
  -H 'Referer: https://data.eastmoney.com/bkzj/hy.html?stat=10' \
  -H 'Sec-Fetch-Dest: script' \
  -H 'Sec-Fetch-Mode: no-cors' \
  -H 'Sec-Fetch-Site: same-site' \
  -H 'User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36' \
  -H 'sec-ch-ua: "Google Chrome";v="149", "Chromium";v="149", "Not)A;Brand";v="24"' \
  -H 'sec-ch-ua-mobile: ?0' \
  -H 'sec-ch-ua-platform: "Windows"' ;
curl 'https://huaxiang.eastmoney.com/CommonRecommend.png?json=%7B%22lastModifyTime%22%3A%22_lastModifyTime_%22%2C%22type%22%3A%22pageclick%22%2C%22coord_x%22%3A-136%2C%22coord_y%22%3A476%2C%22elename%22%3A%22LI%22%2C%22uid%22%3A%22%22%2C%22bid%22%3A%222811034bbb8be0a803dd44a1d4bc6439%22%2C%22referer%22%3A%22https%3A%2F%2Fdata.eastmoney.com%2Fbkzj%2F%22%2C%22pagetype%22%3A%22%22%2C%22pageitem%22%3A%22%22%2C%22browser_height%22%3A1271%2C%22from%22%3A%22https%3A%2F%2Fdata.eastmoney.com%2Fbkzj%2Fhy.html%3Fstat%3D10%22%2C%22index_width%22%3A%221000%22%2C%22index_ad%22%3A%220%22%2C%22domainId%22%3A%22data.eastmoney.com%22%2C%22st_pvi%22%3A%2274492257636238%22%2C%22emtj_pageId%22%3A113300300820%7D' \
  -H 'Accept: image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8' \
  -H 'Accept-Language: zh-CN,zh;q=0.9' \
  -H 'Connection: keep-alive' \
  -b 'qgqp_b_id=2811034bbb8be0a803dd44a1d4bc6439; st_nvi=B_R4snS65CIm-zdxLQJJXdd9c; nid18=07da937ef8413b08c931d7708ccd213f; nid18_create_time=1782135615399; gviem=FNx5J-pKBN6R_6uGDQIzL8948; gviem_create_time=1782135615399; websitepoptg_api_time=1782483166763; st_si=41375670201268; fullscreengg=1; fullscreengg2=1; st_asi=delete; st_pvi=74492257636238; st_sp=2026-02-25%2023%3A30%3A16; st_inirUrl=https%3A%2F%2Fwww.google.com%2F; st_sn=44; st_psi=20260627162954792-111000300841-2309886357' \
  -H 'Referer: https://data.eastmoney.com/bkzj/hy.html?stat=10' \
  -H 'Sec-Fetch-Dest: image' \
  -H 'Sec-Fetch-Mode: no-cors' \
  -H 'Sec-Fetch-Site: same-site' \
  -H 'User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36' \
  -H 'sec-ch-ua: "Google Chrome";v="149", "Chromium";v="149", "Not)A;Brand";v="24"' \
  -H 'sec-ch-ua-mobile: ?0' \
  -H 'sec-ch-ua-platform: "Windows"'
```
4. resp展示
  列举了一个数据
```
jQuery112303664902929155055_1782545506900({
    "rc": 0,
    "rt": 6,
    "svr": 183637030,
    "lt": 1,
    "full": 1,
    "dlmkts": "",
    "dsc": "0",
    "data": {
        "total": 128,
        "diff": [{
            "f1": 2,
            "f2": 3485.92,
            "f12": "BK1036",
            "f13": 90,
            "f14": "半导体",
            "f124": 1782459587,
            "f160": 21.41,
            "f174": 5243314176.0,
            "f175": 0.1,
            "f176": 1527042048.0,
            "f177": 0.03,
            "f178": 3716272128.0,
            "f179": 0.07,
            "f180": -19148230656.0,
            "f181": -0.38,
            "f182": 13836906240.0,
            "f183": 0.27,
            "f260": "海光信息",
            "f261": "688041",
            "f262": 1
        }, 
```

## 概念资金流
1. 今日排行
```
curl 'https://data.eastmoney.com/dataapi/bkzj/getbkzj?key=f62&code=m%3A90%2Bt%3A3' \
  -H 'Accept: */*' \
  -H 'Accept-Language: zh-CN,zh;q=0.9' \
  -H 'Connection: keep-alive' \
  -b 'qgqp_b_id=2811034bbb8be0a803dd44a1d4bc6439; st_nvi=B_R4snS65CIm-zdxLQJJXdd9c; nid18=07da937ef8413b08c931d7708ccd213f; nid18_create_time=1782135615399; gviem=FNx5J-pKBN6R_6uGDQIzL8948; gviem_create_time=1782135615399; websitepoptg_api_time=1782483166763; st_si=41375670201268; fullscreengg=1; fullscreengg2=1; st_asi=delete; st_pvi=74492257636238; st_sp=2026-02-25%2023%3A30%3A16; st_inirUrl=https%3A%2F%2Fwww.google.com%2F; st_sn=44; st_psi=20260627162954792-111000300841-2309886357' \
  -H 'Referer: https://data.eastmoney.com/bkzj/hy.html?stat=10' \
  -H 'Sec-Fetch-Dest: empty' \
  -H 'Sec-Fetch-Mode: cors' \
  -H 'Sec-Fetch-Site: same-origin' \
  -H 'User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36' \
  -H 'X-Requested-With: XMLHttpRequest' \
  -H 'sec-ch-ua: "Google Chrome";v="149", "Chromium";v="149", "Not)A;Brand";v="24"' \
  -H 'sec-ch-ua-mobile: ?0' \
  -H 'sec-ch-ua-platform: "Windows"' ;
curl 'https://push2.eastmoney.com/api/qt/clist/get?cb=jQuery112303664902929155055_1782545506900&fid=f62&po=1&pz=50&pn=1&np=1&fltt=2&invt=2&ut=8dec03ba335b81bf4ebdf7b29ec27d15&fs=m%3A90+t%3A3&fields=f12%2Cf14%2Cf2%2Cf3%2Cf62%2Cf184%2Cf66%2Cf69%2Cf72%2Cf75%2Cf78%2Cf81%2Cf84%2Cf87%2Cf204%2Cf205%2Cf124%2Cf1%2Cf13' \
  -H 'Accept: */*' \
  -H 'Accept-Language: zh-CN,zh;q=0.9' \
  -H 'Connection: keep-alive' \
  -b 'qgqp_b_id=2811034bbb8be0a803dd44a1d4bc6439; st_nvi=B_R4snS65CIm-zdxLQJJXdd9c; nid18=07da937ef8413b08c931d7708ccd213f; nid18_create_time=1782135615399; gviem=FNx5J-pKBN6R_6uGDQIzL8948; gviem_create_time=1782135615399; websitepoptg_api_time=1782483166763; st_si=41375670201268; fullscreengg=1; fullscreengg2=1; st_asi=delete; st_pvi=74492257636238; st_sp=2026-02-25%2023%3A30%3A16; st_inirUrl=https%3A%2F%2Fwww.google.com%2F; st_sn=44; st_psi=20260627162954792-111000300841-2309886357' \
  -H 'Referer: https://data.eastmoney.com/bkzj/hy.html?stat=10' \
  -H 'Sec-Fetch-Dest: script' \
  -H 'Sec-Fetch-Mode: no-cors' \
  -H 'Sec-Fetch-Site: same-site' \
  -H 'User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36' \
  -H 'sec-ch-ua: "Google Chrome";v="149", "Chromium";v="149", "Not)A;Brand";v="24"' \
  -H 'sec-ch-ua-mobile: ?0' \
  -H 'sec-ch-ua-platform: "Windows"' ;
curl 'https://huaxiang.eastmoney.com/CommonRecommend.png?json=%7B%22lastModifyTime%22%3A%22_lastModifyTime_%22%2C%22type%22%3A%22pageclick%22%2C%22coord_x%22%3A-304%2C%22coord_y%22%3A471%2C%22elename%22%3A%22LI%22%2C%22uid%22%3A%22%22%2C%22bid%22%3A%222811034bbb8be0a803dd44a1d4bc6439%22%2C%22referer%22%3A%22https%3A%2F%2Fdata.eastmoney.com%2Fbkzj%2F%22%2C%22pagetype%22%3A%22%22%2C%22pageitem%22%3A%22%22%2C%22browser_height%22%3A1271%2C%22from%22%3A%22https%3A%2F%2Fdata.eastmoney.com%2Fbkzj%2Fhy.html%3Fstat%3D10%22%2C%22index_width%22%3A%221000%22%2C%22index_ad%22%3A%220%22%2C%22domainId%22%3A%22data.eastmoney.com%22%2C%22st_pvi%22%3A%2274492257636238%22%2C%22emtj_pageId%22%3A113300300820%7D' \
  -H 'Accept: image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8' \
  -H 'Accept-Language: zh-CN,zh;q=0.9' \
  -H 'Connection: keep-alive' \
  -b 'qgqp_b_id=2811034bbb8be0a803dd44a1d4bc6439; st_nvi=B_R4snS65CIm-zdxLQJJXdd9c; nid18=07da937ef8413b08c931d7708ccd213f; nid18_create_time=1782135615399; gviem=FNx5J-pKBN6R_6uGDQIzL8948; gviem_create_time=1782135615399; websitepoptg_api_time=1782483166763; st_si=41375670201268; fullscreengg=1; fullscreengg2=1; st_asi=delete; st_pvi=74492257636238; st_sp=2026-02-25%2023%3A30%3A16; st_inirUrl=https%3A%2F%2Fwww.google.com%2F; st_sn=44; st_psi=20260627162954792-111000300841-2309886357' \
  -H 'Referer: https://data.eastmoney.com/bkzj/hy.html?stat=10' \
  -H 'Sec-Fetch-Dest: image' \
  -H 'Sec-Fetch-Mode: no-cors' \
  -H 'Sec-Fetch-Site: same-site' \
  -H 'User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36' \
  -H 'sec-ch-ua: "Google Chrome";v="149", "Chromium";v="149", "Not)A;Brand";v="24"' \
  -H 'sec-ch-ua-mobile: ?0' \
  -H 'sec-ch-ua-platform: "Windows"'
```
2. 5日排行
```
curl 'https://data.eastmoney.com/dataapi/bkzj/getbkzj?key=f62&code=m%3A90%2Bt%3A3' \
  -H 'Accept: */*' \
  -H 'Accept-Language: zh-CN,zh;q=0.9' \
  -H 'Connection: keep-alive' \
  -b 'qgqp_b_id=2811034bbb8be0a803dd44a1d4bc6439; st_nvi=B_R4snS65CIm-zdxLQJJXdd9c; nid18=07da937ef8413b08c931d7708ccd213f; nid18_create_time=1782135615399; gviem=FNx5J-pKBN6R_6uGDQIzL8948; gviem_create_time=1782135615399; websitepoptg_api_time=1782483166763; st_si=41375670201268; fullscreengg=1; fullscreengg2=1; st_asi=delete; st_pvi=74492257636238; st_sp=2026-02-25%2023%3A30%3A16; st_inirUrl=https%3A%2F%2Fwww.google.com%2F; st_sn=44; st_psi=20260627162954792-111000300841-2309886357' \
  -H 'Referer: https://data.eastmoney.com/bkzj/hy.html?stat=10' \
  -H 'Sec-Fetch-Dest: empty' \
  -H 'Sec-Fetch-Mode: cors' \
  -H 'Sec-Fetch-Site: same-origin' \
  -H 'User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36' \
  -H 'X-Requested-With: XMLHttpRequest' \
  -H 'sec-ch-ua: "Google Chrome";v="149", "Chromium";v="149", "Not)A;Brand";v="24"' \
  -H 'sec-ch-ua-mobile: ?0' \
  -H 'sec-ch-ua-platform: "Windows"' ;
curl 'https://push2.eastmoney.com/api/qt/clist/get?cb=jQuery112303664902929155055_1782545506900&fid=f62&po=1&pz=50&pn=1&np=1&fltt=2&invt=2&ut=8dec03ba335b81bf4ebdf7b29ec27d15&fs=m%3A90+t%3A3&fields=f12%2Cf14%2Cf2%2Cf3%2Cf62%2Cf184%2Cf66%2Cf69%2Cf72%2Cf75%2Cf78%2Cf81%2Cf84%2Cf87%2Cf204%2Cf205%2Cf124%2Cf1%2Cf13' \
  -H 'Accept: */*' \
  -H 'Accept-Language: zh-CN,zh;q=0.9' \
  -H 'Connection: keep-alive' \
  -b 'qgqp_b_id=2811034bbb8be0a803dd44a1d4bc6439; st_nvi=B_R4snS65CIm-zdxLQJJXdd9c; nid18=07da937ef8413b08c931d7708ccd213f; nid18_create_time=1782135615399; gviem=FNx5J-pKBN6R_6uGDQIzL8948; gviem_create_time=1782135615399; websitepoptg_api_time=1782483166763; st_si=41375670201268; fullscreengg=1; fullscreengg2=1; st_asi=delete; st_pvi=74492257636238; st_sp=2026-02-25%2023%3A30%3A16; st_inirUrl=https%3A%2F%2Fwww.google.com%2F; st_sn=44; st_psi=20260627162954792-111000300841-2309886357' \
  -H 'Referer: https://data.eastmoney.com/bkzj/hy.html?stat=10' \
  -H 'Sec-Fetch-Dest: script' \
  -H 'Sec-Fetch-Mode: no-cors' \
  -H 'Sec-Fetch-Site: same-site' \
  -H 'User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36' \
  -H 'sec-ch-ua: "Google Chrome";v="149", "Chromium";v="149", "Not)A;Brand";v="24"' \
  -H 'sec-ch-ua-mobile: ?0' \
  -H 'sec-ch-ua-platform: "Windows"' ;
curl 'https://huaxiang.eastmoney.com/CommonRecommend.png?json=%7B%22lastModifyTime%22%3A%22_lastModifyTime_%22%2C%22type%22%3A%22pageclick%22%2C%22coord_x%22%3A-304%2C%22coord_y%22%3A471%2C%22elename%22%3A%22LI%22%2C%22uid%22%3A%22%22%2C%22bid%22%3A%222811034bbb8be0a803dd44a1d4bc6439%22%2C%22referer%22%3A%22https%3A%2F%2Fdata.eastmoney.com%2Fbkzj%2F%22%2C%22pagetype%22%3A%22%22%2C%22pageitem%22%3A%22%22%2C%22browser_height%22%3A1271%2C%22from%22%3A%22https%3A%2F%2Fdata.eastmoney.com%2Fbkzj%2Fhy.html%3Fstat%3D10%22%2C%22index_width%22%3A%221000%22%2C%22index_ad%22%3A%220%22%2C%22domainId%22%3A%22data.eastmoney.com%22%2C%22st_pvi%22%3A%2274492257636238%22%2C%22emtj_pageId%22%3A113300300820%7D' \
  -H 'Accept: image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8' \
  -H 'Accept-Language: zh-CN,zh;q=0.9' \
  -H 'Connection: keep-alive' \
  -b 'qgqp_b_id=2811034bbb8be0a803dd44a1d4bc6439; st_nvi=B_R4snS65CIm-zdxLQJJXdd9c; nid18=07da937ef8413b08c931d7708ccd213f; nid18_create_time=1782135615399; gviem=FNx5J-pKBN6R_6uGDQIzL8948; gviem_create_time=1782135615399; websitepoptg_api_time=1782483166763; st_si=41375670201268; fullscreengg=1; fullscreengg2=1; st_asi=delete; st_pvi=74492257636238; st_sp=2026-02-25%2023%3A30%3A16; st_inirUrl=https%3A%2F%2Fwww.google.com%2F; st_sn=44; st_psi=20260627162954792-111000300841-2309886357' \
  -H 'Referer: https://data.eastmoney.com/bkzj/hy.html?stat=10' \
  -H 'Sec-Fetch-Dest: image' \
  -H 'Sec-Fetch-Mode: no-cors' \
  -H 'Sec-Fetch-Site: same-site' \
  -H 'User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36' \
  -H 'sec-ch-ua: "Google Chrome";v="149", "Chromium";v="149", "Not)A;Brand";v="24"' \
  -H 'sec-ch-ua-mobile: ?0' \
  -H 'sec-ch-ua-platform: "Windows"' ;
curl 'https://data.eastmoney.com/dataapi/bkzj/getbkzj?key=f164&code=m%3A90%2Bt%3A3' \
  -H 'Accept: */*' \
  -H 'Accept-Language: zh-CN,zh;q=0.9' \
  -H 'Connection: keep-alive' \
  -b 'qgqp_b_id=2811034bbb8be0a803dd44a1d4bc6439; st_nvi=B_R4snS65CIm-zdxLQJJXdd9c; nid18=07da937ef8413b08c931d7708ccd213f; nid18_create_time=1782135615399; gviem=FNx5J-pKBN6R_6uGDQIzL8948; gviem_create_time=1782135615399; websitepoptg_api_time=1782483166763; st_si=41375670201268; fullscreengg=1; fullscreengg2=1; st_asi=delete; st_pvi=74492257636238; st_sp=2026-02-25%2023%3A30%3A16; st_inirUrl=https%3A%2F%2Fwww.google.com%2F; st_sn=44; st_psi=20260627162954792-111000300841-2309886357' \
  -H 'Referer: https://data.eastmoney.com/bkzj/hy.html?stat=10' \
  -H 'Sec-Fetch-Dest: empty' \
  -H 'Sec-Fetch-Mode: cors' \
  -H 'Sec-Fetch-Site: same-origin' \
  -H 'User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36' \
  -H 'X-Requested-With: XMLHttpRequest' \
  -H 'sec-ch-ua: "Google Chrome";v="149", "Chromium";v="149", "Not)A;Brand";v="24"' \
  -H 'sec-ch-ua-mobile: ?0' \
  -H 'sec-ch-ua-platform: "Windows"' ;
curl 'https://push2.eastmoney.com/api/qt/clist/get?cb=jQuery112303664902929155055_1782545506900&fid=f164&po=1&pz=50&pn=1&np=1&fltt=2&invt=2&ut=8dec03ba335b81bf4ebdf7b29ec27d15&fs=m%3A90+t%3A3&fields=f12%2Cf14%2Cf2%2Cf109%2Cf164%2Cf165%2Cf166%2Cf167%2Cf168%2Cf169%2Cf170%2Cf171%2Cf172%2Cf173%2Cf257%2Cf258%2Cf124%2Cf1%2Cf13' \
  -H 'Accept: */*' \
  -H 'Accept-Language: zh-CN,zh;q=0.9' \
  -H 'Connection: keep-alive' \
  -b 'qgqp_b_id=2811034bbb8be0a803dd44a1d4bc6439; st_nvi=B_R4snS65CIm-zdxLQJJXdd9c; nid18=07da937ef8413b08c931d7708ccd213f; nid18_create_time=1782135615399; gviem=FNx5J-pKBN6R_6uGDQIzL8948; gviem_create_time=1782135615399; websitepoptg_api_time=1782483166763; st_si=41375670201268; fullscreengg=1; fullscreengg2=1; st_asi=delete; st_pvi=74492257636238; st_sp=2026-02-25%2023%3A30%3A16; st_inirUrl=https%3A%2F%2Fwww.google.com%2F; st_sn=44; st_psi=20260627162954792-111000300841-2309886357' \
  -H 'Referer: https://data.eastmoney.com/bkzj/hy.html?stat=10' \
  -H 'Sec-Fetch-Dest: script' \
  -H 'Sec-Fetch-Mode: no-cors' \
  -H 'Sec-Fetch-Site: same-site' \
  -H 'User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36' \
  -H 'sec-ch-ua: "Google Chrome";v="149", "Chromium";v="149", "Not)A;Brand";v="24"' \
  -H 'sec-ch-ua-mobile: ?0' \
  -H 'sec-ch-ua-platform: "Windows"' ;
curl 'https://huaxiang.eastmoney.com/CommonRecommend.png?json=%7B%22lastModifyTime%22%3A%22_lastModifyTime_%22%2C%22type%22%3A%22pageclick%22%2C%22coord_x%22%3A-212%2C%22coord_y%22%3A471%2C%22elename%22%3A%22LI%22%2C%22uid%22%3A%22%22%2C%22bid%22%3A%222811034bbb8be0a803dd44a1d4bc6439%22%2C%22referer%22%3A%22https%3A%2F%2Fdata.eastmoney.com%2Fbkzj%2F%22%2C%22pagetype%22%3A%22%22%2C%22pageitem%22%3A%22%22%2C%22browser_height%22%3A1271%2C%22from%22%3A%22https%3A%2F%2Fdata.eastmoney.com%2Fbkzj%2Fhy.html%3Fstat%3D10%22%2C%22index_width%22%3A%221000%22%2C%22index_ad%22%3A%220%22%2C%22domainId%22%3A%22data.eastmoney.com%22%2C%22st_pvi%22%3A%2274492257636238%22%2C%22emtj_pageId%22%3A113300300820%7D' \
  -H 'Accept: image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8' \
  -H 'Accept-Language: zh-CN,zh;q=0.9' \
  -H 'Connection: keep-alive' \
  -b 'qgqp_b_id=2811034bbb8be0a803dd44a1d4bc6439; st_nvi=B_R4snS65CIm-zdxLQJJXdd9c; nid18=07da937ef8413b08c931d7708ccd213f; nid18_create_time=1782135615399; gviem=FNx5J-pKBN6R_6uGDQIzL8948; gviem_create_time=1782135615399; websitepoptg_api_time=1782483166763; st_si=41375670201268; fullscreengg=1; fullscreengg2=1; st_asi=delete; st_pvi=74492257636238; st_sp=2026-02-25%2023%3A30%3A16; st_inirUrl=https%3A%2F%2Fwww.google.com%2F; st_sn=44; st_psi=20260627162954792-111000300841-2309886357' \
  -H 'Referer: https://data.eastmoney.com/bkzj/hy.html?stat=10' \
  -H 'Sec-Fetch-Dest: image' \
  -H 'Sec-Fetch-Mode: no-cors' \
  -H 'Sec-Fetch-Site: same-site' \
  -H 'User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36' \
  -H 'sec-ch-ua: "Google Chrome";v="149", "Chromium";v="149", "Not)A;Brand";v="24"' \
  -H 'sec-ch-ua-mobile: ?0' \
  -H 'sec-ch-ua-platform: "Windows"'
```
3. 10日排行
```
curl 'https://data.eastmoney.com/dataapi/bkzj/getbkzj?key=f62&code=m%3A90%2Bt%3A3' \
  -H 'Accept: */*' \
  -H 'Accept-Language: zh-CN,zh;q=0.9' \
  -H 'Connection: keep-alive' \
  -b 'qgqp_b_id=2811034bbb8be0a803dd44a1d4bc6439; st_nvi=B_R4snS65CIm-zdxLQJJXdd9c; nid18=07da937ef8413b08c931d7708ccd213f; nid18_create_time=1782135615399; gviem=FNx5J-pKBN6R_6uGDQIzL8948; gviem_create_time=1782135615399; websitepoptg_api_time=1782483166763; st_si=41375670201268; fullscreengg=1; fullscreengg2=1; st_asi=delete; st_pvi=74492257636238; st_sp=2026-02-25%2023%3A30%3A16; st_inirUrl=https%3A%2F%2Fwww.google.com%2F; st_sn=44; st_psi=20260627162954792-111000300841-2309886357' \
  -H 'Referer: https://data.eastmoney.com/bkzj/hy.html?stat=10' \
  -H 'Sec-Fetch-Dest: empty' \
  -H 'Sec-Fetch-Mode: cors' \
  -H 'Sec-Fetch-Site: same-origin' \
  -H 'User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36' \
  -H 'X-Requested-With: XMLHttpRequest' \
  -H 'sec-ch-ua: "Google Chrome";v="149", "Chromium";v="149", "Not)A;Brand";v="24"' \
  -H 'sec-ch-ua-mobile: ?0' \
  -H 'sec-ch-ua-platform: "Windows"' ;
curl 'https://push2.eastmoney.com/api/qt/clist/get?cb=jQuery112303664902929155055_1782545506900&fid=f62&po=1&pz=50&pn=1&np=1&fltt=2&invt=2&ut=8dec03ba335b81bf4ebdf7b29ec27d15&fs=m%3A90+t%3A3&fields=f12%2Cf14%2Cf2%2Cf3%2Cf62%2Cf184%2Cf66%2Cf69%2Cf72%2Cf75%2Cf78%2Cf81%2Cf84%2Cf87%2Cf204%2Cf205%2Cf124%2Cf1%2Cf13' \
  -H 'Accept: */*' \
  -H 'Accept-Language: zh-CN,zh;q=0.9' \
  -H 'Connection: keep-alive' \
  -b 'qgqp_b_id=2811034bbb8be0a803dd44a1d4bc6439; st_nvi=B_R4snS65CIm-zdxLQJJXdd9c; nid18=07da937ef8413b08c931d7708ccd213f; nid18_create_time=1782135615399; gviem=FNx5J-pKBN6R_6uGDQIzL8948; gviem_create_time=1782135615399; websitepoptg_api_time=1782483166763; st_si=41375670201268; fullscreengg=1; fullscreengg2=1; st_asi=delete; st_pvi=74492257636238; st_sp=2026-02-25%2023%3A30%3A16; st_inirUrl=https%3A%2F%2Fwww.google.com%2F; st_sn=44; st_psi=20260627162954792-111000300841-2309886357' \
  -H 'Referer: https://data.eastmoney.com/bkzj/hy.html?stat=10' \
  -H 'Sec-Fetch-Dest: script' \
  -H 'Sec-Fetch-Mode: no-cors' \
  -H 'Sec-Fetch-Site: same-site' \
  -H 'User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36' \
  -H 'sec-ch-ua: "Google Chrome";v="149", "Chromium";v="149", "Not)A;Brand";v="24"' \
  -H 'sec-ch-ua-mobile: ?0' \
  -H 'sec-ch-ua-platform: "Windows"' ;
curl 'https://huaxiang.eastmoney.com/CommonRecommend.png?json=%7B%22lastModifyTime%22%3A%22_lastModifyTime_%22%2C%22type%22%3A%22pageclick%22%2C%22coord_x%22%3A-304%2C%22coord_y%22%3A471%2C%22elename%22%3A%22LI%22%2C%22uid%22%3A%22%22%2C%22bid%22%3A%222811034bbb8be0a803dd44a1d4bc6439%22%2C%22referer%22%3A%22https%3A%2F%2Fdata.eastmoney.com%2Fbkzj%2F%22%2C%22pagetype%22%3A%22%22%2C%22pageitem%22%3A%22%22%2C%22browser_height%22%3A1271%2C%22from%22%3A%22https%3A%2F%2Fdata.eastmoney.com%2Fbkzj%2Fhy.html%3Fstat%3D10%22%2C%22index_width%22%3A%221000%22%2C%22index_ad%22%3A%220%22%2C%22domainId%22%3A%22data.eastmoney.com%22%2C%22st_pvi%22%3A%2274492257636238%22%2C%22emtj_pageId%22%3A113300300820%7D' \
  -H 'Accept: image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8' \
  -H 'Accept-Language: zh-CN,zh;q=0.9' \
  -H 'Connection: keep-alive' \
  -b 'qgqp_b_id=2811034bbb8be0a803dd44a1d4bc6439; st_nvi=B_R4snS65CIm-zdxLQJJXdd9c; nid18=07da937ef8413b08c931d7708ccd213f; nid18_create_time=1782135615399; gviem=FNx5J-pKBN6R_6uGDQIzL8948; gviem_create_time=1782135615399; websitepoptg_api_time=1782483166763; st_si=41375670201268; fullscreengg=1; fullscreengg2=1; st_asi=delete; st_pvi=74492257636238; st_sp=2026-02-25%2023%3A30%3A16; st_inirUrl=https%3A%2F%2Fwww.google.com%2F; st_sn=44; st_psi=20260627162954792-111000300841-2309886357' \
  -H 'Referer: https://data.eastmoney.com/bkzj/hy.html?stat=10' \
  -H 'Sec-Fetch-Dest: image' \
  -H 'Sec-Fetch-Mode: no-cors' \
  -H 'Sec-Fetch-Site: same-site' \
  -H 'User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36' \
  -H 'sec-ch-ua: "Google Chrome";v="149", "Chromium";v="149", "Not)A;Brand";v="24"' \
  -H 'sec-ch-ua-mobile: ?0' \
  -H 'sec-ch-ua-platform: "Windows"' ;
curl 'https://data.eastmoney.com/dataapi/bkzj/getbkzj?key=f164&code=m%3A90%2Bt%3A3' \
  -H 'Accept: */*' \
  -H 'Accept-Language: zh-CN,zh;q=0.9' \
  -H 'Connection: keep-alive' \
  -b 'qgqp_b_id=2811034bbb8be0a803dd44a1d4bc6439; st_nvi=B_R4snS65CIm-zdxLQJJXdd9c; nid18=07da937ef8413b08c931d7708ccd213f; nid18_create_time=1782135615399; gviem=FNx5J-pKBN6R_6uGDQIzL8948; gviem_create_time=1782135615399; websitepoptg_api_time=1782483166763; st_si=41375670201268; fullscreengg=1; fullscreengg2=1; st_asi=delete; st_pvi=74492257636238; st_sp=2026-02-25%2023%3A30%3A16; st_inirUrl=https%3A%2F%2Fwww.google.com%2F; st_sn=44; st_psi=20260627162954792-111000300841-2309886357' \
  -H 'Referer: https://data.eastmoney.com/bkzj/hy.html?stat=10' \
  -H 'Sec-Fetch-Dest: empty' \
  -H 'Sec-Fetch-Mode: cors' \
  -H 'Sec-Fetch-Site: same-origin' \
  -H 'User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36' \
  -H 'X-Requested-With: XMLHttpRequest' \
  -H 'sec-ch-ua: "Google Chrome";v="149", "Chromium";v="149", "Not)A;Brand";v="24"' \
  -H 'sec-ch-ua-mobile: ?0' \
  -H 'sec-ch-ua-platform: "Windows"' ;
curl 'https://push2.eastmoney.com/api/qt/clist/get?cb=jQuery112303664902929155055_1782545506900&fid=f164&po=1&pz=50&pn=1&np=1&fltt=2&invt=2&ut=8dec03ba335b81bf4ebdf7b29ec27d15&fs=m%3A90+t%3A3&fields=f12%2Cf14%2Cf2%2Cf109%2Cf164%2Cf165%2Cf166%2Cf167%2Cf168%2Cf169%2Cf170%2Cf171%2Cf172%2Cf173%2Cf257%2Cf258%2Cf124%2Cf1%2Cf13' \
  -H 'Accept: */*' \
  -H 'Accept-Language: zh-CN,zh;q=0.9' \
  -H 'Connection: keep-alive' \
  -b 'qgqp_b_id=2811034bbb8be0a803dd44a1d4bc6439; st_nvi=B_R4snS65CIm-zdxLQJJXdd9c; nid18=07da937ef8413b08c931d7708ccd213f; nid18_create_time=1782135615399; gviem=FNx5J-pKBN6R_6uGDQIzL8948; gviem_create_time=1782135615399; websitepoptg_api_time=1782483166763; st_si=41375670201268; fullscreengg=1; fullscreengg2=1; st_asi=delete; st_pvi=74492257636238; st_sp=2026-02-25%2023%3A30%3A16; st_inirUrl=https%3A%2F%2Fwww.google.com%2F; st_sn=44; st_psi=20260627162954792-111000300841-2309886357' \
  -H 'Referer: https://data.eastmoney.com/bkzj/hy.html?stat=10' \
  -H 'Sec-Fetch-Dest: script' \
  -H 'Sec-Fetch-Mode: no-cors' \
  -H 'Sec-Fetch-Site: same-site' \
  -H 'User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36' \
  -H 'sec-ch-ua: "Google Chrome";v="149", "Chromium";v="149", "Not)A;Brand";v="24"' \
  -H 'sec-ch-ua-mobile: ?0' \
  -H 'sec-ch-ua-platform: "Windows"' ;
curl 'https://huaxiang.eastmoney.com/CommonRecommend.png?json=%7B%22lastModifyTime%22%3A%22_lastModifyTime_%22%2C%22type%22%3A%22pageclick%22%2C%22coord_x%22%3A-212%2C%22coord_y%22%3A471%2C%22elename%22%3A%22LI%22%2C%22uid%22%3A%22%22%2C%22bid%22%3A%222811034bbb8be0a803dd44a1d4bc6439%22%2C%22referer%22%3A%22https%3A%2F%2Fdata.eastmoney.com%2Fbkzj%2F%22%2C%22pagetype%22%3A%22%22%2C%22pageitem%22%3A%22%22%2C%22browser_height%22%3A1271%2C%22from%22%3A%22https%3A%2F%2Fdata.eastmoney.com%2Fbkzj%2Fhy.html%3Fstat%3D10%22%2C%22index_width%22%3A%221000%22%2C%22index_ad%22%3A%220%22%2C%22domainId%22%3A%22data.eastmoney.com%22%2C%22st_pvi%22%3A%2274492257636238%22%2C%22emtj_pageId%22%3A113300300820%7D' \
  -H 'Accept: image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8' \
  -H 'Accept-Language: zh-CN,zh;q=0.9' \
  -H 'Connection: keep-alive' \
  -b 'qgqp_b_id=2811034bbb8be0a803dd44a1d4bc6439; st_nvi=B_R4snS65CIm-zdxLQJJXdd9c; nid18=07da937ef8413b08c931d7708ccd213f; nid18_create_time=1782135615399; gviem=FNx5J-pKBN6R_6uGDQIzL8948; gviem_create_time=1782135615399; websitepoptg_api_time=1782483166763; st_si=41375670201268; fullscreengg=1; fullscreengg2=1; st_asi=delete; st_pvi=74492257636238; st_sp=2026-02-25%2023%3A30%3A16; st_inirUrl=https%3A%2F%2Fwww.google.com%2F; st_sn=44; st_psi=20260627162954792-111000300841-2309886357' \
  -H 'Referer: https://data.eastmoney.com/bkzj/hy.html?stat=10' \
  -H 'Sec-Fetch-Dest: image' \
  -H 'Sec-Fetch-Mode: no-cors' \
  -H 'Sec-Fetch-Site: same-site' \
  -H 'User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36' \
  -H 'sec-ch-ua: "Google Chrome";v="149", "Chromium";v="149", "Not)A;Brand";v="24"' \
  -H 'sec-ch-ua-mobile: ?0' \
  -H 'sec-ch-ua-platform: "Windows"' ;
curl 'https://data.eastmoney.com/dataapi/bkzj/getbkzj?key=f174&code=m%3A90%2Bt%3A3' \
  -H 'Accept: */*' \
  -H 'Accept-Language: zh-CN,zh;q=0.9' \
  -H 'Connection: keep-alive' \
  -b 'qgqp_b_id=2811034bbb8be0a803dd44a1d4bc6439; st_nvi=B_R4snS65CIm-zdxLQJJXdd9c; nid18=07da937ef8413b08c931d7708ccd213f; nid18_create_time=1782135615399; gviem=FNx5J-pKBN6R_6uGDQIzL8948; gviem_create_time=1782135615399; websitepoptg_api_time=1782483166763; st_si=41375670201268; fullscreengg=1; fullscreengg2=1; st_asi=delete; st_pvi=74492257636238; st_sp=2026-02-25%2023%3A30%3A16; st_inirUrl=https%3A%2F%2Fwww.google.com%2F; st_sn=44; st_psi=20260627162954792-111000300841-2309886357' \
  -H 'Referer: https://data.eastmoney.com/bkzj/hy.html?stat=10' \
  -H 'Sec-Fetch-Dest: empty' \
  -H 'Sec-Fetch-Mode: cors' \
  -H 'Sec-Fetch-Site: same-origin' \
  -H 'User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36' \
  -H 'X-Requested-With: XMLHttpRequest' \
  -H 'sec-ch-ua: "Google Chrome";v="149", "Chromium";v="149", "Not)A;Brand";v="24"' \
  -H 'sec-ch-ua-mobile: ?0' \
  -H 'sec-ch-ua-platform: "Windows"' ;
curl 'https://push2.eastmoney.com/api/qt/clist/get?cb=jQuery112303664902929155055_1782545506900&fid=f174&po=1&pz=50&pn=1&np=1&fltt=2&invt=2&ut=8dec03ba335b81bf4ebdf7b29ec27d15&fs=m%3A90+t%3A3&fields=f12%2Cf14%2Cf2%2Cf160%2Cf174%2Cf175%2Cf176%2Cf177%2Cf178%2Cf179%2Cf180%2Cf181%2Cf182%2Cf183%2Cf260%2Cf261%2Cf124%2Cf1%2Cf13' \
  -H 'Accept: */*' \
  -H 'Accept-Language: zh-CN,zh;q=0.9' \
  -H 'Connection: keep-alive' \
  -b 'qgqp_b_id=2811034bbb8be0a803dd44a1d4bc6439; st_nvi=B_R4snS65CIm-zdxLQJJXdd9c; nid18=07da937ef8413b08c931d7708ccd213f; nid18_create_time=1782135615399; gviem=FNx5J-pKBN6R_6uGDQIzL8948; gviem_create_time=1782135615399; websitepoptg_api_time=1782483166763; st_si=41375670201268; fullscreengg=1; fullscreengg2=1; st_asi=delete; st_pvi=74492257636238; st_sp=2026-02-25%2023%3A30%3A16; st_inirUrl=https%3A%2F%2Fwww.google.com%2F; st_sn=44; st_psi=20260627162954792-111000300841-2309886357' \
  -H 'Referer: https://data.eastmoney.com/bkzj/hy.html?stat=10' \
  -H 'Sec-Fetch-Dest: script' \
  -H 'Sec-Fetch-Mode: no-cors' \
  -H 'Sec-Fetch-Site: same-site' \
  -H 'User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36' \
  -H 'sec-ch-ua: "Google Chrome";v="149", "Chromium";v="149", "Not)A;Brand";v="24"' \
  -H 'sec-ch-ua-mobile: ?0' \
  -H 'sec-ch-ua-platform: "Windows"' ;
curl 'https://huaxiang.eastmoney.com/CommonRecommend.png?json=%7B%22lastModifyTime%22%3A%22_lastModifyTime_%22%2C%22type%22%3A%22pageclick%22%2C%22coord_x%22%3A-114%2C%22coord_y%22%3A478%2C%22elename%22%3A%22LI%22%2C%22uid%22%3A%22%22%2C%22bid%22%3A%222811034bbb8be0a803dd44a1d4bc6439%22%2C%22referer%22%3A%22https%3A%2F%2Fdata.eastmoney.com%2Fbkzj%2F%22%2C%22pagetype%22%3A%22%22%2C%22pageitem%22%3A%22%22%2C%22browser_height%22%3A1271%2C%22from%22%3A%22https%3A%2F%2Fdata.eastmoney.com%2Fbkzj%2Fhy.html%3Fstat%3D10%22%2C%22index_width%22%3A%221000%22%2C%22index_ad%22%3A%220%22%2C%22domainId%22%3A%22data.eastmoney.com%22%2C%22st_pvi%22%3A%2274492257636238%22%2C%22emtj_pageId%22%3A113300300820%7D' \
  -H 'Accept: image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8' \
  -H 'Accept-Language: zh-CN,zh;q=0.9' \
  -H 'Connection: keep-alive' \
  -b 'qgqp_b_id=2811034bbb8be0a803dd44a1d4bc6439; st_nvi=B_R4snS65CIm-zdxLQJJXdd9c; nid18=07da937ef8413b08c931d7708ccd213f; nid18_create_time=1782135615399; gviem=FNx5J-pKBN6R_6uGDQIzL8948; gviem_create_time=1782135615399; websitepoptg_api_time=1782483166763; st_si=41375670201268; fullscreengg=1; fullscreengg2=1; st_asi=delete; st_pvi=74492257636238; st_sp=2026-02-25%2023%3A30%3A16; st_inirUrl=https%3A%2F%2Fwww.google.com%2F; st_sn=44; st_psi=20260627162954792-111000300841-2309886357' \
  -H 'Referer: https://data.eastmoney.com/bkzj/hy.html?stat=10' \
  -H 'Sec-Fetch-Dest: image' \
  -H 'Sec-Fetch-Mode: no-cors' \
  -H 'Sec-Fetch-Site: same-site' \
  -H 'User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36' \
  -H 'sec-ch-ua: "Google Chrome";v="149", "Chromium";v="149", "Not)A;Brand";v="24"' \
  -H 'sec-ch-ua-mobile: ?0' \
  -H 'sec-ch-ua-platform: "Windows"'
```