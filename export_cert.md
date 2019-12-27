### FYI to export a cert...

```
➜  certutil -K -d sql:$HOME/.pki/nssdb 

certutil: Checking token "NSS Certificate DB" in slot "NSS User Private Key and Certificate Services"
< 0> rsa      3f9a4d76e760a3e9c94548c4aae21b4cfb4c90b9   rblaffor - com
➜ pk12util -d sql:$HOME/.pki/nssdb -o out.p12 -n "rblaffor - com"
Enter password for PKCS12 file: 
Re-enter password: 
pk12util: PKCS12 EXPORT SUCCESSFUL
➜  ll out.p12 
-rw------- 1 rblaffor staff 6.4K Dec 13 17:34 out.p12
```
