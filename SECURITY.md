# Security and privacy

[简体中文](SECURITY.zh-CN.md)

Never commit tokens, private keys, cookies, session URLs, personal data, private hostnames, live IP addresses, SSH commands, proxy settings, or unredacted machine logs.

If a secret is committed:

1. rotate or revoke it immediately;
2. report the incident privately to the maintainers;
3. remove it from reachable history using an approved history-rewrite procedure;
4. document the sanitized impact without repeating the secret.

Deleting the newest file is not sufficient because Git retains history. Security reports should not be filed as public Issues when they contain exploitable details.
