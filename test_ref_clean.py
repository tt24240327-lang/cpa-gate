from urllib.parse import parse_qs, urlparse

refs = [
    "https://blog.naver.com/PostView.naver?blogId=spaceow&logNo=224180844028&redirect=Dlog&widgetTypeCall=true&topReferer=https%3A%2F%2Fsearch.naver.com%2Fsearch.naver%3Fie%3DUTF-8%26sm%3Dwhl_hty%26query%3D%25EB%258C%2580%25EA%25B5%25AC%2B%25EC%259E%25A5%25EA%25B8%25B0%25EB%258F%2599%2B%25ED%258F%25AC%25EC%259E%25A5%25EC%259D%25B4%25EC%2582%25AC&trackingCode=nx&directAccess=false",
    "https://blog.naver.com/PostList.naver?blogId=spaceow&widgetTypeCall=true&noTrackingCode=true&directAccess=true",
    "https://m.blog.naver.com/PostView.naver?blogId=test&logNo=12345"
]

print("--- Naver Ref Cleaning Test ---")
for ref in refs:
    cleaned = ref
    if 'blog.naver.com' in ref:
        try:
            parsed = urlparse(ref)
            qs = parse_qs(parsed.query)
            blog_id = qs.get('blogId', [''])[0]
            log_no = qs.get('logNo', [''])[0]
            
            if blog_id and log_no:
                # User wants: https://blog.naver.com/{id}/{logNo}
                cleaned = f"https://blog.naver.com/{blog_id}/{log_no}"
            elif blog_id:
                # Fallback: https://blog.naver.com/{id}
                cleaned = f"https://blog.naver.com/{blog_id}"
        except: pass
    print(f"Original: {ref[:60]}...")
    print(f"Cleaned : {cleaned}")
    print("-" * 20)
