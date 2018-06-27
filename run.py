from lxml import html
import requests
import json
import sys
from threading import Thread

if len(sys.argv) > 1:
    count = sys.argv[1]
else:
    count = 5
headers = {
    'User-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.87 Safari/537.36',
}
response_with_list = requests.get('https://www.monster.com/jobs/search/', headers=headers)

tree_with_list = html.fromstring(response_with_list.text)
list_of_urls = json.loads(tree_with_list.xpath('//div[@id="ResultsScrollable"]/script')[0].text_content())
urls = []
for item in list_of_urls['itemListElement']:
    urls.append(item['url'])
    if count == len(urls):
        break


def get_content(url):
    print(url)
    response = requests.get(url, headers=headers)
    tree = html.fromstring(response.text)
    card = tree.xpath('//section[@class="card-content"]')
    if len(card) > 1:
        with open('result.txt', mode='w') as lock_file:
            lock_file.write('%s\n\n' % tree.xpath('//section[@class="card-content"]')[0].text_content())
            lock_file.close()
    else:
        with open('error.log', mode='a') as lock_file:
            lock_file.write('Url %s doesn\'t contain card-content\n' % url)
            lock_file.close()


threads = []
for next_url in urls:
    thread = Thread(target=get_content, args=(next_url,))
    thread.start()
    threads.append(thread)

for thread in threads:
    thread.join()

print('End')
