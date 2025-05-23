from icrawler.builtin import GoogleImageCrawler
from icrawler import ImageDownloader
import uuid

class TextDownloader(ImageDownloader):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.txt_file = open('koedo_images.txt', 'w', encoding='utf-8')
        self.txt_file.write("FileName\tImageURL\tSourcePage\n")

    def download(self, task, default_ext, timeout=5, **kwargs):
        filename = task.get('filename') or f"{uuid.uuid4()}.{default_ext}"
        task['filename'] = filename  # 明示的に入れておく

        result = super().download(task, default_ext, timeout, **kwargs)

        # たとえ result が False でも task 情報は書き出すよう変更
        file_url = task.get('file_url') or 'N/A'
        page_url = task.get('page_url') or 'N/A'
        line = f"{filename}\t{file_url}\t{page_url}\n"
        self.txt_file.write(line)
        self.txt_file.flush()
        print("Logged:", line.strip())

        return result

    def on_finish(self):
        self.txt_file.close()

crawler = GoogleImageCrawler(
    downloader_cls=TextDownloader,
    storage={'root_dir': 'koedo_images'}
)
crawler.crawl(keyword='川越　越戸　街並み', max_num=50)
