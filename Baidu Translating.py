JS逆向爬取分析案例
import json
import requests
import re
import execjs


def get_sign(text="你好"):
    url = "https://fanyi.baidu.com"

    # 整理请求头
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36",
        "cookie": "REALTIME_TRANS_SWITCH=1; FANYI_WORD_SWITCH=1; HISTORY_SWITCH=1; SOUND_SPD_SWITCH=1; SOUND_PREFER_SWITCH=1; BAIDUID=C9F168C021436C5FB903DED17AFC22D3:FG=1; BIDUPSID=C9F168C021436C5FB903DED17AFC22D3; PSTM=1605177720; BDORZ=B490B5EBF6F3CD402E515D22BCDA1598; Hm_lvt_64ecd82404c51e03dc91cb9e8c025574=1605090301,1605104609,1605280782,1605281361; BDUSS=1XbWE5VFhmYmNLUURRRDNFREZJdUxyeTJVWVlZOUViZ3p5fjVNdGJDTGdOZFpmRUFBQUFBJCQAAAAAAAAAAAEAAAAn4NUTZG9uZ7fJx-8AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAOCorl~gqK5fam; BDUSS_BFESS=1XbWE5VFhmYmNLUURRRDNFREZJdUxyeTJVWVlZOUViZ3p5fjVNdGJDTGdOZFpmRUFBQUFBJCQAAAAAAAAAAAEAAAAn4NUTZG9uZ7fJx-8AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAOCorl~gqK5fam; H_PS_PSSID=32819_1452_33041_32951_33061_31253_32971_32706_33098_33100_32962_32938; delPer=0; PSINO=5; BAIDUID_BFESS=C9F168C021436C5FB903DED17AFC22D3:FG=1; yjs_js_security_passport=4fc05fc269fa1c7807a3e8362aa9b3d64da33cfd_1605515298_js; __yjsv5_shitong=1.0_7_975e821265a70e2bbd7ec4a58621adb09803_300_1605515318077_49.89.250.227_31712cd6; Hm_lpvt_64ecd82404c51e03dc91cb9e8c025574=1605517050"
    }

    # 获取请求
    r = requests.get(url, headers=headers)

    sign_i = re.findall(";window.gtk = ('.*?');", r.content.decode())[0]
    print(sign_i)

    with open("百度翻译.js", "r", encoding="utf-8") as f:
        js_content = f.read()

    # js中添加一行gtk
    js_content = js_content.replace('"320305.131321201"', sign_i)
    # print(js_content)

    # 执行js
    context = execjs.compile(js_content)
    sign = context.call("e", text)
    print(sign)
    return sign


def baidu_translate(text, sign):
    url = "https://fanyi.baidu.com/v2transapi?from=en&to=zh"
    headers = {
        "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1",
        "cookie": "REALTIME_TRANS_SWITCH=1; FANYI_WORD_SWITCH=1; HISTORY_SWITCH=1; SOUND_SPD_SWITCH=1; SOUND_PREFER_SWITCH=1; BAIDUID=C9F168C021436C5FB903DED17AFC22D3:FG=1; BIDUPSID=C9F168C021436C5FB903DED17AFC22D3; PSTM=1605177720; BDORZ=B490B5EBF6F3CD402E515D22BCDA1598; Hm_lvt_64ecd82404c51e03dc91cb9e8c025574=1605090301,1605104609,1605280782,1605281361; BDUSS=1XbWE5VFhmYmNLUURRRDNFREZJdUxyeTJVWVlZOUViZ3p5fjVNdGJDTGdOZFpmRUFBQUFBJCQAAAAAAAAAAAEAAAAn4NUTZG9uZ7fJx-8AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAOCorl~gqK5fam; BDUSS_BFESS=1XbWE5VFhmYmNLUURRRDNFREZJdUxyeTJVWVlZOUViZ3p5fjVNdGJDTGdOZFpmRUFBQUFBJCQAAAAAAAAAAAEAAAAn4NUTZG9uZ7fJx-8AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAOCorl~gqK5fam; H_PS_PSSID=32819_1452_33041_32951_33061_31253_32971_32706_33098_33100_32962_32938; delPer=0; PSINO=5; BAIDUID_BFESS=C9F168C021436C5FB903DED17AFC22D3:FG=1; yjs_js_security_passport=4fc05fc269fa1c7807a3e8362aa9b3d64da33cfd_1605515298_js; Hm_lpvt_64ecd82404c51e03dc91cb9e8c025574=1605517920; __yjsv5_shitong=1.0_7_975e821265a70e2bbd7ec4a58621adb09803_300_1605517920054_49.89.250.227_daf4bf3f"
    }
    data = {
        "query": text,
        "from": "en",
        "to": "zh",
        "token": "37d9804c22bcea81351497cd0639a5be",
        "sign": sign
    }

    response = requests.post(url=url, data=data, headers=headers)

    # print("响应\n\n", response.content.decode())

    ret = json.loads(response.content.decode())
    translate_ret = ret["trans_result"]["data"][0]["dst"]
    print(translate_ret)
    return translate_ret


if __name__ == '__main__':
    # 1. 输入要翻译的英文
    text = input("请输入要翻译的英文:")
    # 2. 计算出sign
    sign = get_sign(text)
    # 3. 发送翻译请求
    ret = baidu_translate(text, sign)
    print("英文:", text, "翻译为应为：", ret)
