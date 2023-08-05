# probator-auth-onelogin-saml

Please open issues in the [Probator](https://gitlab.com/probator/probator/issues/new?labels=auth-onelogin-saml) repository

## Description

This code enables the OneLogin service for SAML based SSO authentication for the Probator web interface.

## Configuration Options

| Option name       | Default Value                 | Type      | Description                                           |
|-------------------|-------------------------------|-----------|-------------------------------------------------------|
| strict            | True                          | bool      | Strict validation of SAML responses                   |
| debug             | False                         | bool      | Service Provider Entity ID                            |
| sp\_entity\_id    | Service Provider Entity ID    | string    | Service Provider Entity ID                            |
| sp\_acs           | *None*                        | string    | Assertion Consumer endpoint                           |
| sp\_sls           | *None*                        | string    | Single Logout Service endpoint                        |
| idp\_entity\_id   | *None*                        | string    | Identity Provider Entity ID                           |
| idp\_ssos         | *None*                        | string    | Single Sign-On Service endpoint                       |
| idp\_sls          | *None*                        | string    | Single Logout Service endpoint                        |
| idp\_x509cert     | *None*                        | string    | Base64 encoded x509 certificate for SAML validation   |

This project is based on the work for [Cloud Inquisitor](https://github.com/RiotGames/cloud-inquisitor) by Riot Games
