# 需求: 商品id, 商品名称, 价格, 店铺名称, 商品链接, 总评价, 好评差评
import requests
import hashlib
import re
import csv
import time
import json

# 构建请求
headers = {
  # 用户信息, 用于检测是否有登录账号的信息(注意无论是否登录账号, 都有cookie信息)
  'cookie':  'miid=1534733114760766777; cookie2=1ed831c8c645d34d98cbe9eae6232289; _tb_token_=ebbe66531617e; _samesite_flag_=true; cancelledSubSites=empty; tracknick=tb0762414138; t=7aec55ddfa4b6562dc74718cc1836ca6; cna=x4urHx4rYysCAXrUnXLQSaLI; thw=cn; sgcookie=E100RoQFxYB1z%2BcxfNtegNGTNbVRCalKm31MYyxGUQSMH8iKGrykZjKJU%2F0iVUa%2BNUN1tf8vDQeFpCHaF2EYoLLV6J3Y4XdoORxU8Nt%2FBzIlPt41oLJgroBPxKP%2B9saA3yUe; wk_cookie2=1d96921567e410d3aa48c6cd3d0b0c02; wk_unb=UUphwoIYyV98hPf3Lg%3D%3D; uc3=nk2=F5RFh6jNB14o%2F5Ct&id2=UUphwoIYyV98hPf3Lg%3D%3D&lg2=VFC%2FuZ9ayeYq2g%3D%3D&vt3=F8dD376nxgrQyx69ZFE%3D; csg=63efb7ca; lgc=tb0762414138; dnk=tb0762414138; skt=551f523e40fa953f; existShop=MTczMzg5MzI4NA%3D%3D; uc4=nk4=0%40FY4O7oHcpA5zZZaw2vaLjLfhbNiYEYI%3D&id4=0%40U2grGRoJ5pXIcAiL2SZOL%2BoOWSlgOay6; _cc_=UtASsssmfA%3D%3D; xlly_s=1; mtop_partitioned_detect=1; _m_h5_tk=bac6652b1fd59beb52d4a9d2dd999664_1734780569066; _m_h5_tk_enc=e98108106ab522c89f41453a89dbc2a9; 3PcFlag=1734771221248; tfstk=gILIa94uYLLNLvyMtvhNCEyudA75PLg4d71JiQUUwwQdehODF9loxw-1Fdp1pylnxgBWKwIkYTWFFaOkhfkquqRHtabK3xuq60s80ZrR96ez6OQPN2MZbRRHtaVMvQYt3B2Wh2shy_B-1NC5ZTQRv_UTXOfzvTpRpGeOGs7ReLpR6GClO_ELy9IOXOfRyzpRyf_t_eEOw06eOfWKIvmY4WACCzUJ51HhLBZQz1TCO3Xv9eZ3xbfCAtddBxVwVjjWdMTZR-fBXI9FOL00-wIWvnQpPxgCWIxwp19-hu69ceY50eMbm9LhEK_pfAUCywLB0ibScWfwRCLcVeDQW99M6n7HkA4WHCR2-GYShRBkYsbOOhG8X9IR4pUVhXe_V5s0P16q1fZuqvYBnqK57JxCv1fIifG_pJjds1_E1fZuqMCGOUcs1Jeh.; isg=BD4-Uz5n1Y9N_gDYVmEoQj7tj1KAfwL5JzXsf-hGLQF-i9plXg01CTctA19Hs_oR',
  # 用户代理, 表示浏览器/设备信息
  'User-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
}

# 请求网址
url = 'https://h5api.m.taobao.com/h5/mtop.relationrecommend.wirelessrecommend.recommend/2.0/'

# sign 加密参数
em_token = 'bac6652b1fd59beb52d4a9d2dd999664' # 好像不经常变, 但是太长时间会发生变化
eC = 1734773488651 # 时间戳
eS = '12574478' # 这个值貌似在所有情况下都不变 猜测是一个常数
ep_data = '{"appId":"34385","params":"{\\"device\\":\\"HMA-AL00\\",\\"isBeta\\":\\"false\\",\\"grayHair\\":\\"false\\",\\"from\\":\\"nt_history\\",\\"brand\\":\\"HUAWEI\\",\\"info\\":\\"wifi\\",\\"index\\":\\"4\\",\\"rainbow\\":\\"\\",\\"schemaType\\":\\"auction\\",\\"elderHome\\":\\"false\\",\\"isEnterSrpSearch\\":\\"true\\",\\"newSearch\\":\\"false\\",\\"network\\":\\"wifi\\",\\"subtype\\":\\"\\",\\"hasPreposeFilter\\":\\"false\\",\\"prepositionVersion\\":\\"v2\\",\\"client_os\\":\\"Android\\",\\"gpsEnabled\\":\\"false\\",\\"searchDoorFrom\\":\\"srp\\",\\"debug_rerankNewOpenCard\\":\\"false\\",\\"homePageVersion\\":\\"v7\\",\\"searchElderHomeOpen\\":\\"false\\",\\"search_action\\":\\"initiative\\",\\"sugg\\":\\"_4_1\\",\\"sversion\\":\\"13.6\\",\\"style\\":\\"list\\",\\"ttid\\":\\"600000@taobao_pc_10.7.0\\",\\"needTabs\\":\\"true\\",\\"areaCode\\":\\"CN\\",\\"vm\\":\\"nw\\",\\"countryNum\\":\\"156\\",\\"m\\":\\"pc\\",\\"page\\":2,\\"n\\":48,\\"q\\":\\"%E5%92%96%E5%95%A1\\",\\"qSource\\":\\"url\\",\\"pageSource\\":\\"a21bo.jianhua/a.201856.d13\\",\\"tab\\":\\"all\\",\\"pageSize\\":\\"48\\",\\"totalPage\\":\\"100\\",\\"totalResults\\":\\"16015\\",\\"sourceS\\":\\"0\\",\\"sort\\":\\"_coefp\\",\\"bcoffset\\":\\"-8\\",\\"ntoffset\\":\\"12\\",\\"filterTag\\":\\"\\",\\"service\\":\\"\\",\\"prop\\":\\"\\",\\"loc\\":\\"\\",\\"start_price\\":null,\\"end_price\\":null,\\"startPrice\\":null,\\"endPrice\\":null,\\"categoryp\\":\\"\\",\\"ha3Kvpairs\\":null,\\"couponFilter\\":0,\\"myCNA\\":\\"x4urHx4rYysCAXrUnXLQSaLI\\"}"}'

# 加密后的值 需要确认函数 eE() 是否为 MD5 加密
# 判断依据: 由0-9, a-f 16个字符组成, 长度为32
# 直接在控制台中测试 eE('123456') 与标准的 MD 5 加密结果一致, 因此可以确认 eE() 函数为 MD5 加密
string = em_token + "&" + str(eC) + "&" + eS + "&" + ep_data
MD5 = hashlib.md5()
MD5.update(string.encode('utf-8'))
sign = MD5.hexdigest()
print(sign)
# 请求方法': GET
# 请求参数': 查询参数, 查询参数是放在url中的
dec_params = {
  'jsv': '2.7.4',
  'appKey': eS,
  't': eC,
  'sign': sign,
  'api': 'mtop.relationrecommend.wirelessrecommend.recommend',
  'v': '2.0',
  'timeout': '10000',
  'type': 'jsonp',
  'dataType': 'jsonp',
  'callback': 'mtopjsonp6',
  'data': ep_data,
}

# 发送请求
response = requests.get(url = url, params = dec_params, headers = headers)

# 获取相应的文本数据
info = response.text
# 解析数据
json_match = re.search(r'mtopjsonp\d+\((.*?)\)\s*$', info, re.DOTALL)
if json_match:
  print('匹配到 JSON 数据')
  json_str = json_match.group(1)
else:
  print('未匹配到 JSON 数据')
print(info[:1500])
# 把 json 字符串数据转换成 json 字典
json_data = json.loads(json_str)
# 提取商品信息所在的列表
itemsArray = json_data['data']['itemsArray']

with open('data.csv', mode = 'w', encoding = 'utf-8', newline = '') as file:
    fieldnames = ['商品名称', '商品原价', '商品售价', '店铺名称', '商品链接']
    writer = csv.DictWriter(file, fieldnames = fieldnames)
    writer.writeheader()
    for item in itemsArray:
      dict = {
        '商品名称': item['title'].replace('<span class=H>', '').replace('</span>', ''),
        '商品原价': item['price'],
        '商品售价': item['priceShow']['price'],
        '店铺名称': item['nick'],
        '商品链接': 'https:' + item['auctionURL'],
      }
      writer.writerow(dict)

def main() -> None:
  print('程序运行')

if __name__ == '__main__':
  main()