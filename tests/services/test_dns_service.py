from services.dns_service import DNSService


def test_dns_put_get():
    dns = DNSService()

    dns.put("8.8.8.8", "google.com")

    assert dns.get("8.8.8.8") == "google.com"


def test_dns_missing():
    dns = DNSService()

    assert dns.get("1.1.1.1") is None