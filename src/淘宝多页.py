"""
需要确认的值:
cookie
em_token
"""

import requests
import hashlib
import re
import csv
import time
import json

eS = '12574478' # 这个值貌似在所有情况下都不变 猜测是一个常数
em_token = 'bac6652b1fd59beb52d4a9d2dd999664' # 好像不经常变, 但是太长时间会发生变化

# 构建请求
headers = {
  # 用户信息, 用于检测是否有登录账号的信息(注意无论是否登录账号, 都有cookie信息)
  'cookie':  'miid=1534733114760766777; cookie2=1ed831c8c645d34d98cbe9eae6232289; _tb_token_=ebbe66531617e; _samesite_flag_=true; cancelledSubSites=empty; tracknick=tb0762414138; t=7aec55ddfa4b6562dc74718cc1836ca6; cna=x4urHx4rYysCAXrUnXLQSaLI; thw=cn; sgcookie=E100RoQFxYB1z%2BcxfNtegNGTNbVRCalKm31MYyxGUQSMH8iKGrykZjKJU%2F0iVUa%2BNUN1tf8vDQeFpCHaF2EYoLLV6J3Y4XdoORxU8Nt%2FBzIlPt41oLJgroBPxKP%2B9saA3yUe; wk_cookie2=1d96921567e410d3aa48c6cd3d0b0c02; wk_unb=UUphwoIYyV98hPf3Lg%3D%3D; uc3=nk2=F5RFh6jNB14o%2F5Ct&id2=UUphwoIYyV98hPf3Lg%3D%3D&lg2=VFC%2FuZ9ayeYq2g%3D%3D&vt3=F8dD376nxgrQyx69ZFE%3D; csg=63efb7ca; lgc=tb0762414138; dnk=tb0762414138; skt=551f523e40fa953f; existShop=MTczMzg5MzI4NA%3D%3D; uc4=nk4=0%40FY4O7oHcpA5zZZaw2vaLjLfhbNiYEYI%3D&id4=0%40U2grGRoJ5pXIcAiL2SZOL%2BoOWSlgOay6; _cc_=UtASsssmfA%3D%3D; xlly_s=1; mtop_partitioned_detect=1; _m_h5_tk=bac6652b1fd59beb52d4a9d2dd999664_1734780569066; _m_h5_tk_enc=e98108106ab522c89f41453a89dbc2a9; 3PcFlag=1734771221248; tfstk=gILIa94uYLLNLvyMtvhNCEyudA75PLg4d71JiQUUwwQdehODF9loxw-1Fdp1pylnxgBWKwIkYTWFFaOkhfkquqRHtabK3xuq60s80ZrR96ez6OQPN2MZbRRHtaVMvQYt3B2Wh2shy_B-1NC5ZTQRv_UTXOfzvTpRpGeOGs7ReLpR6GClO_ELy9IOXOfRyzpRyf_t_eEOw06eOfWKIvmY4WACCzUJ51HhLBZQz1TCO3Xv9eZ3xbfCAtddBxVwVjjWdMTZR-fBXI9FOL00-wIWvnQpPxgCWIxwp19-hu69ceY50eMbm9LhEK_pfAUCywLB0ibScWfwRCLcVeDQW99M6n7HkA4WHCR2-GYShRBkYsbOOhG8X9IR4pUVhXe_V5s0P16q1fZuqvYBnqK57JxCv1fIifG_pJjds1_E1fZuqMCGOUcs1Jeh.; isg=BD4-Uz5n1Y9N_gDYVmEoQj7tj1KAfwL5JzXsf-hGLQF-i9plXg01CTctA19Hs_oR',
  # 用户代理, 表示浏览器/设备信息
  'User-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
}

# 请求网址
url = 'https://h5api.m.taobao.com/h5/mtop.relationrecommend.wirelessrecommend.recommend/2.0/'

# 获取加密的 sign 和 ep_data
def get_sign(eC: int, page: int, totalResults: str, bc_offset: str, nt_offset: str, sourceS: str, em_token: str) -> tuple[str, str]:
  # sign 加密参数
  params = {
    "device": "HMA-AL00",
    "isBeta": "false",
    "grayHair": "false",
    "from": "nt_history",
    "brand": "HUAWEI",
    "info": "wifi",
    "index": "4",
    "rainbow": "",
    "schemaType": "auction",
    "elderHome": "false",
    "isEnterSrpSearch": "true",
    "newSearch": "false",
    "network": "wifi",
    "subtype": "",
    "hasPreposeFilter": "false",
    "prepositionVersion": "v2",
    "client_os": "Android",
    "gpsEnabled": "false",
    "searchDoorFrom": "srp",
    "debug_rerankNewOpenCard": "false",
    "homePageVersion": "v7",
    "searchElderHomeOpen": "false",
    "search_action": "initiative",
    "sugg": "_4_1",
    "sversion": "13.6",
    "style": "list",
    "ttid": "600000@taobao_pc_10.7.0",
    "needTabs": "true",
    "areaCode": "CN",
    "vm": "nw",
    "countryNum": "156",
    "m": "pc",
    "page": page, # 传参
    "n": 48,
    "q": "%E5%92%96%E5%95%A1",
    "qSource": "url",
    "pageSource": "a21bo.jianhua/a.201856.d13",
    "tab": "all",
    "pageSize": "48",
    "totalPage": "100",
    "totalResults": totalResults, # 传参
    "sourceS": sourceS, # 传参
    "sort": "_coefp",
    "bcoffset": bc_offset, # 传参
    "ntoffset": nt_offset, # 传参
    "filterTag": "",
    "service": "",
    "prop": "",
    "loc": "",
    "start_price": None,
    "end_price": None,
    "startPrice": None,
    "endPrice": None,
    "categoryp": "",
    "ha3Kvpairs": None,
    "couponFilter": 0,
    "myCNA": "x4urHx4rYysCAXrUnXLQSaLI"
  }
  
  info_data = {
    "appId":"34385",
    "params": json.dumps(params),
  }
  
  ep_data = json.dumps(info_data).replace(" ", "")
  string = em_token + "&" + str(eC) + "&" + eS + "&" + ep_data
  MD5 = hashlib.md5()
  MD5.update(string.encode('utf-8'))
  sign = MD5.hexdigest()
  return sign, ep_data

def make_request(page: int, totalResults: str, bc_offset: str, nt_offset: str, sourceS: str) -> json:
  # 生成毫秒级时间戳
  eC = int(time.time() * 1000)
  sign, ep_data = get_sign(
    eC = eC,
    page = page,
    totalResults = totalResults,
    bc_offset = bc_offset,
    nt_offset = nt_offset,
    sourceS = sourceS,
    em_token = em_token
  )
  # 生成解密后的请求参数
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
  response_text = response.text
  # 正则表达式提取 json 字符串
  json_match = re.search(r'mtopjsonp\d+\((.*?)\)\s*$', response_text, re.DOTALL)
  if json_match:
    print('匹配到 JSON 数据')
    json_str = json_match.group(1)
    print(json_str[:1000])
    json_data = json.loads(json_str)
    return json_data
  else:
    print('未匹配到 JSON 数据')

def get_recursion_params(json_data: json):
  """
  获取下一页的参数内容
  bcoffset
  ntoffset
  totalResults
  sourceS
  """
  bc_offset = json_data['data']['mainInfo']['bcoffset']
  nt_offset = json_data['data']['mainInfo']['ntoffset']
  totalResults = json_data['data']['mainInfo']['totalResults']
  sourceS = json_data['data']['mainInfo']['sourceS']
  return bc_offset, nt_offset, totalResults, sourceS

def get_items_info(json_data: json, page: int) -> None:
  # 提取商品信息所在的列表
  itemsArray = json_data['data']['itemsArray']
  mode = 'a' if page > 1 else 'w'
  with open('data.csv', mode = mode, encoding = 'utf-8', newline = '') as file:
      fieldnames = ['商品名称', '商品原价', '商品售价', '店铺名称', '商品链接']
      writer = csv.DictWriter(file, fieldnames = fieldnames)
      if page == 1:
        writer.writeheader()
      for item in itemsArray:
        writer.writerow({
          '商品名称': item['title'].replace('<span class=H>', '').replace('</span>', ''),
          '商品原价': item['price'],
          '商品售价': item['priceShow']['price'],
          '店铺名称': item['nick'],
          '商品链接': 'https:' + item['auctionURL'],
        })


def main() -> None:
  # 初始化
  totalResults = '4800'
  sourceS = '0'
  bc_offset = '""'
  nt_offset = '""'
  for page in range(1, 21):
    print(f"正在采集第{page}页...")
    json_data = make_request(page, totalResults, bc_offset, nt_offset, sourceS)
    bc_offset, nt_offset, totalResults, sourceS = get_recursion_params(json_data)
    get_items_info(json_data, page)
    time.sleep(3)

if __name__ == '__main__':
  main()