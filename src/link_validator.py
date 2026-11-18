from urllib.parse import urlparse


class LinkValidator:
    @staticmethod
    def is_valid(link):
        link = link.strip()
        if not link or " " in link:
            return False
        try:
            parsed = urlparse(link)
            host = parsed.hostname
        except ValueError:
            return False
        if parsed.scheme not in ("http", "https") or not host:
            return False
        return host == "localhost" or "." in host