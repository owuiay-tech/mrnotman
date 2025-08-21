# app.py
from flask import Flask, request, Response
import requests

app = Flask(__name__)

# هذا هو الرابط الذي سيعمل كبروكسي
@app.route('/proxy')
def proxy():
    # احصل على الرابط المطلوب من المستخدم
    url = request.args.get('url')
    
    if not url:
        return "Please provide a URL parameter. Example: /proxy?url=https://example.com", 400
    
    try:
        # الخادم (في أمريكا) يقوم بطلب الموقع نيابة عنك
        headers = {
            # ننقل بعض الهيدرز من طلبك الأصلي لكي تبدو الزيارة طبيعية أكثر
            'User-Agent': request.headers.get('User-Agent'),
            'Accept': request.headers.get('Accept'),
            'Accept-Language': request.headers.get('Accept-Language'),
        }
        
        proxied_response = requests.get(url, headers=headers, stream=True)
        
        # نقوم بإنشاء رد جديد بنفس محتوى الرد الأصلي
        # ونعيده إلى متصفحك
        return Response(proxied_response.iter_content(chunk_size=1024),
                        status=proxied_response.status_code,
                        content_type=proxied_response.headers.get('Content-Type'))
                        
    except requests.exceptions.RequestException as e:
        return f"An error occurred: {e}", 500

if __name__ == '__main__':
    # هذا السطر للتشغيل المحلي فقط
    app.run(debug=True)