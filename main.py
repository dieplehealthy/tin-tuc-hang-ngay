import feedparser
import json
from jinja2 import Environment, FileSystemLoader
from datetime import datetime
import pytz

# Múi giờ Việt Nam
VIETNAM_TZ = pytz.timezone('Asia/Ho_Chi_Minh')

def get_sources():
    """Đọc danh sách các nguồn tin từ tệp sources.json."""
    with open('sources.json', 'r', encoding='utf-8') as f:
        return json.load(f)

def get_articles(sources, max_articles_per_source=10):
    """Lấy các bài viết mới nhất từ tất cả các nguồn."""
    all_articles = []
    for source in sources:
        try:
            print(f"Đang lấy tin từ: {source['name']}...")
            feed = feedparser.parse(source['url'])
            # Lấy số bài viết giới hạn từ mỗi nguồn
            for entry in feed.entries[:max_articles_per_source]:
                all_articles.append({
                    'title': entry.title,
                    'link': entry.link,
                    'summary': entry.get('summary', 'Không có tóm tắt.'),
                    'published': entry.get('published', 'Không rõ ngày'),
                    'source': source['name']
                })
        except Exception as e:
            print(f"Lỗi khi lấy tin từ {source['name']}: {e}")
    return all_articles

def generate_html(articles):
    """Tạo tệp HTML từ dữ liệu bài viết bằng Jinja2."""
    # Thiết lập môi trường Jinja2 để tải template từ thư mục hiện tại
    env = Environment(loader=FileSystemLoader('.'))
    template = env.get_template('template.html')

    # Lấy thời gian hiện tại theo múi giờ Việt Nam và định dạng nó
    now_vietnam = datetime.now(VIETNAM_TZ)
    update_time_str = now_vietnam.strftime('%H:%M:%S ngày %d-%m-%Y')

    # Render template với dữ liệu
    html_content = template.render(
        articles=articles, 
        update_time=update_time_str
    )

    # Ghi nội dung đã render ra tệp index.html
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print(f"Đã tạo tệp index.html thành công với {len(articles)} bài viết.")
    print(f"Thời gian cập nhật: {update_time_str}")

if __name__ == "__main__":
    sources_list = get_sources()
    articles_list = get_articles(sources_list)
    
    # Sắp xếp tất cả các bài viết theo một tiêu chí nào đó nếu muốn (ví dụ: thời gian)
    # Bước này phức tạp hơn vì định dạng thời gian từ RSS có thể không đồng nhất.
    # Hiện tại, chúng ta sẽ để theo thứ tự lấy tin.
    
    generate_html(articles_list)