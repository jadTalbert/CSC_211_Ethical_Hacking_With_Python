import dns.resolver

# Initialize a custom resolver targeting our container mapped port
custom_resolver = dns.resolver.Resolver()
custom_resolver.nameservers = ["127.0.0.1"]
custom_resolver.port = 1053

# Example query from VS Code
domain = "acme-corp.com"
for rtype in ["A", "MX", "TXT"]:
    try:
        answers = custom_resolver.resolve(domain, rtype)
        print(f"[+] {rtype} records for {domain}:")
        for rdata in answers:
            print(f"    - {rdata.to_text()}")
    except Exception as e:
        print(f"[-] {rtype} lookup failed: {e}")