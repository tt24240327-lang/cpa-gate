import random
from flask import make_response

def generate_robots(host):
    content = f"User-agent: *\nAllow: /\nSitemap: https://{host}/sitemap.xml"
    res = make_response(content)
    res.headers["Content-Type"] = "text/plain"
    return res

def generate_sitemap(host):
    base_url = f"https://{host}"
    xml = ['<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    xml.append(f'<url><loc>{base_url}/</loc><changefreq>daily</changefreq><priority>1.0</priority></url>')
    
    r = random.Random(host)
    # Generate fake documentation links for SEO bot trapping
    for i in range(r.randint(15, 45)):
        doc_id = r.randint(1000, 9999)
        xml.append(f'<url><loc>{base_url}/?path=/archive/doc-{doc_id}</loc><changefreq>weekly</changefreq><priority>0.5</priority></url>')
    
    xml.append('</urlset>')
    res = make_response("".join(xml))
    res.headers["Content-Type"] = "application/xml"
    return res
