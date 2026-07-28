import webbrowser


class BrowserService:

    VIRUSTOTAL_FILE_URL = (
        "https://www.virustotal.com/gui/file/"
    )

    @staticmethod
    def virustotal(sha256: str):

        if not sha256:
            return False

        normalized_hash = sha256.strip().lower()

        if not normalized_hash:
            return False

        webbrowser.open(
            f"{BrowserService.VIRUSTOTAL_FILE_URL}"
            f"{normalized_hash}"
        )

        return True

    @staticmethod
    def whois(ip: str):

        if not ip:
            return False

        webbrowser.open(
            f"https://www.abuseipdb.com/check/{ip}"
        )

        return True