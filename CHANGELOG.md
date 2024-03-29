# Semantic Versioning Changelog

# [2.6.0](https://github.com/pycasbin/flask-authz/compare/v2.5.1...v2.6.0) (2024-03-29)


### Features

* update Python version to 3.9+, update CI Python version ([d9031b5](https://github.com/pycasbin/flask-authz/commit/d9031b55b758543870b8dc4fa09efe898db93da3))
* upgrade CI Node.js version to 20 ([039ac95](https://github.com/pycasbin/flask-authz/commit/039ac95403da29511c303fd86b3a91f37f1ce7c3))

## [2.5.1](https://github.com/pycasbin/flask-authz/compare/v2.5.0...v2.5.1) (2023-11-19)


### Bug Fixes

* fix requirement files ([617a955](https://github.com/pycasbin/flask-authz/commit/617a9550f4fc4362c4a0e296a6aeefca0bc1cb34))
* update CI script ([4183a17](https://github.com/pycasbin/flask-authz/commit/4183a17781a13ff9dcb0ef8fcf263fd7a242c521))

# [2.5.0](https://github.com/pycasbin/flask-authz/compare/v2.4.0...v2.5.0) (2022-01-30)


### Bug Fixes

* cleanup requirements ([43cc46e](https://github.com/pycasbin/flask-authz/commit/43cc46ec96dca7efd48d47dd35b4e3cc01412475))
* correct python-version to string instead of float, misleading the ci. ([c0ac1c8](https://github.com/pycasbin/flask-authz/commit/c0ac1c8ee1b16d3acf26a1768294780c619b602b))
* Specify a fixed version for nodejs in the release ci workflow ([f6268b6](https://github.com/pycasbin/flask-authz/commit/f6268b6fa932658d48b769ffd619f1ac3d252005))


### Features

* add python 3.10 to release workflow ([55e090c](https://github.com/pycasbin/flask-authz/commit/55e090c90acbecc0329a795007b2ee2193a21a92))
* add python 3.9 and 3.10 to ci using focal distribution ([789d93d](https://github.com/pycasbin/flask-authz/commit/789d93d906c4d84ad404a142cb0a0528e6538bc2))

# [2.4.0](https://github.com/pycasbin/flask-authz/compare/v2.3.0...v2.4.0) (2021-07-23)


### Bug Fixes

* pin casbin_sqlalchemy_adapter==0.3.2 to be able to run test cases using casbin==1.0.4 ([c914768](https://github.com/pycasbin/flask-authz/commit/c91476810cee8f12d2423adcbfdf0eafa9539347))
* remove duplicated test ([155bf94](https://github.com/pycasbin/flask-authz/commit/155bf9464769afe80979b1534dd270c28892ee70))
* support default delimiter for sanitize_group_headers() ([0683ca3](https://github.com/pycasbin/flask-authz/commit/0683ca395babd033a6dcc5d540e6398e8b156f4e))


### Features

* add condition when using whitespace delimiter to handle more valid scenarios ([d22efa3](https://github.com/pycasbin/flask-authz/commit/d22efa3bcc5f8738d8690fb241eb1deff9599bdb))

# [2.3.0](https://github.com/pycasbin/flask-authz/compare/v2.2.0...v2.3.0) (2021-05-15)


### Features

* Update requirements.txt for latest casbin version and .github actions test added ([#28](https://github.com/pycasbin/flask-authz/issues/28)) ([d54f9d4](https://github.com/pycasbin/flask-authz/commit/d54f9d4318438ad18e20c1ab60a6b51f8c93ced7))
