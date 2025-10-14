def main():
    print("Hello from webhard-test!")


if __name__ == "__main__":
    main()
#!/usr/bin/env python3
import os
from pathlib import Path
from flask import Flask, render_template_string, send_from_directory, abort, request
from werkzeug.utils import safe_join

# 공유할 루트 디렉터리 (환경변수 SHARE_DIR 없으면 현재 디렉터리)
ROOT = Path(os.environ.get("SHARE_DIR", ".")).resolve()

app = Flask(__name__)

PAGE = """
<!DOCTYPE html>
<html lang="ko">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{{ rel_path if rel_path else 'Files' }} - Simple File Server</title>
  <style>
    body{font-family:system-ui, -apple-system, Segoe UI, Roboto, Helvetica, Arial, sans-serif; margin:40px;}
    h1{margin:0 0 16px 0;}
    .path{color:#666;margin-bottom:20px;}
    table{border-collapse:collapse;width:100%;}
    th,td{padding:10px;border-bottom:1px solid #eee; text-align:left;}
    a{text-decoration:none;}
    .muted{color:#888;font-size:12px;}
  </style>
</head>
<body>
  <h1>📁 {{ rel_path if rel_path else 'Files' }}</h1>
  <div class="path">Root: {{ root }}</div>

  {% if parent_link %}
    <p><a href="{{ parent_link }}">⬅ 상위 폴더</a></p>
  {% endif %}

  <table>
    <thead>
      <tr><th>이름</th><th class="muted">크기</th></tr>
    </thead>
    <tbody>
      {% for d in dirs %}
        <tr>
          <td>📂 <a href="{{ d.href }}">{{ d.name }}</a></td>
          <td class="muted">폴더</td>
        </tr>
      {% endfor %}
      {% for f in files %}
        <tr>
          <td>📄 <a href="{{ f.href }}">{{ f.name }}</a></td>
          <td class="muted">{{ f.size }}</td>
        </tr>
      {% endfor %}
    </tbody>
  </table>
</body>
</html>
"""

def human_size(n: int) -> str:
    units = ["B","KB","MB","GB","TB"]
    s = 0
    while n >= 1024 and s < len(units)-1:
        n //= 1024
        s += 1
    return f"{n} {units[s]}"

@app.route("/", defaults={"subpath": ""})
@app.route("/<path:subpath>")
def index(subpath):
    # 디렉터리 탐색
    abs_path = safe_join(str(ROOT), subpath)
    if abs_path is None:
        abort(404)
    abs_path = Path(abs_path).resolve()
    if not abs_path.exists() or ROOT not in abs_path.parents and abs_path != ROOT:
        abort(404)

    # 파일이면 바로 다운로드 처리
    if abs_path.is_file():
        rel_dir = str(abs_path.parent.relative_to(ROOT))
        if rel_dir == ".":
            rel_dir = ""
        return send_from_directory(
            directory=str(ROOT / rel_dir),
            path=abs_path.name,
            as_attachment=True,            # 다운로드로 저장
            download_name=abs_path.name    # 파일명 유지
        )

    # 디렉터리 목록 렌더
    items = sorted(abs_path.iterdir(), key=lambda p: (p.is_file(), p.name.lower()))
    dirs = []
    files = []
    for p in items:
        name = p.name
        href = (("/" + str(Path(subpath) / name)) if subpath else ("/" + name))
        if p.is_dir():
            dirs.append({"name": name, "href": href})
        else:
            try:
                size = human_size(p.stat().st_size)
            except Exception:
                size = "-"
            files.append({"name": name, "href": href, "size": size})

    # 상위 폴더 링크
    parent_link = None
    if subpath:
        parent = str(Path(subpath).parent)
        parent_link = "/" + parent if parent != "." else "/"

    rel_path = str(Path(subpath)) if subpath else ""
    return render_template_string(
        PAGE,
        rel_path=rel_path,
        root=str(ROOT),
        parent_link=parent_link,
        dirs=dirs,
        files=files
    )

if __name__ == "__main__":
    host = os.environ.get("HOST", "0.0.0.0")
    port = int(os.environ.get("PORT", "8080"))
    debug = os.environ.get("DEBUG", "0") == "1"
    print(f"* Serving {ROOT} on http://{host}:{port}")
    app.run(host=host, port=port, debug=debug)

