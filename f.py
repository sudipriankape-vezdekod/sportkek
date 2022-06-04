import requests
while True:
    name = input().strip()
    r = requests.get("https://codeforces.com/profile/"+name,allow_redirects=True, cookies={"RCPC": "19ab7ba3f0aac77d6bb6e62833d5897e"},).content.decode()
    i = r.index('_UserActivityFrame_counterValue')+len('_UserActivityFrame_counterValue')+2
    print(name, "решил",r[i:i+10].split()[0], "задач")
