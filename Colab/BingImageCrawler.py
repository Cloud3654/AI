# Install
!pip install icrawler

# Crawler
from icrawler.builtin import BingImageCrawler
keyword = input('Input Search: ')
num_images = int(input('Number of images to crawl: '))
crawler = BingImageCrawler(downloader_threads = 4, storage = {'root_dir': f'./{keyword}'})
crawler.crawl(keyword = keyword, max_num = num_images)
print ('Image Crawled!')
