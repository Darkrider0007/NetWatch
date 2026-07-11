import webbrowser


class BrowserService:

    @staticmethod
    def virustotal(path):

        webbrowser.open(

            "https://www.virustotal.com/gui/home/upload"

        )

    @staticmethod
    def whois(ip):

        webbrowser.open(

            f"https://www.abuseipdb.com/check/{ip}"

        )