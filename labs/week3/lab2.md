```python
import dns.resolver

# Initialize a custom resolver targeting our container mapped port
custom_resolver = dns.resolver.Resolver()
custom_resolver.nameservers = ["127.0.0.1"]
custom_resolver.port = 1053

## DNS set up for query execution
baseDomain = "acme-corp.com"

#list of possible submain names to query(e.g. www.acme-corp.com, mail.acme-corp.com, etc.)
subDomains = ["","www","ftp","dev-api","ns1","mail"]

#possible DNS record types to query
dnsRecords = ["A", "MX", "TXT"]

######################################################################################
#WHITE-HAT HACKERS: ADD COMMENTS TO EXPLAIN YOUR CODE AND THE PURPOSE OF THIS SCRIPT #
#######################################################################################
for sub in subDomains:
    if sub == "":
        domain = baseDomain
    else:
        domain = f"{sub}.{baseDomain}"
    print(f"\n[+] Querying DNS records for: {domain}")
    for rtype in dnsRecords:
        try:
            answers = custom_resolver.resolve(domain, rtype)
            print(f"[+] {rtype} records for {domain}:")
            for rdata in answers:
                print(f"    - {rdata.to_text()}")
        except Exception as e:
            print(f"[-] {rtype} lookup failed for {domain}: {e}")
```