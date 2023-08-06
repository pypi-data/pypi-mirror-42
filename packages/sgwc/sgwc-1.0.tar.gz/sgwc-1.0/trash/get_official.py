from sgwc import get_official, wechat

# official = get_official('LOL313298553')
# print(official)
# print(official.recent_article)

official = wechat.Official.from_url('http://mp.weixin.qq.com/profile?src=3&timestamp=1550497727&ver=1&signature=i3AiuGb1QwOB5GTeaDJ9C324EzC2B1LrBch1ex6AMI-RrICdniG0z4bU-NfL-A3qx7qJ57qn0KnQgN2AyQ-OnA==')
print(official)
print(official.recent_article)
print(official.authenticate)
print(official.articles)

