[![Semantic Release](https://github.com/SSI-Securities-Corporation/python-fcdata/actions/workflows/publish.yaml/badge.svg)](https://github.com/SSI-Securities-Corporation/python-fcdata/actions/workflows/publish.yaml)
# Installation
#### From tar ball (most stable)
If you download file [fc-data.py.zip](https://github.com/SSI-Securities-Corporation/python-fcdata/releases/latest/download/fc-data.py.zip), we include tarball file:
``` python
pip install dist/ssi_fc_data-2.2.1.tar.gz
```
#### Install behind proxy
```python
pip install --trusted-host pypi.org --trusted-host
files.pythonhosted.org --proxy=http://<username>:<password>@<host>:<port> ssi-fc-data
```
Or
```python
pip install --trusted-host pypi.org --trusted-host
files.pythonhosted.org --proxy=http://<username>:<password>@<host>:<port> dist/ssi_fc_data-2.2.1.tar.gz
```

#### Pypi
``` python
pip install ssi-fc-data
```

# Sample usage
## Create Config
Get `consumerID` and `consumerSecret` from [iBoard](https://iboard.ssi.com.vn/support/api-service/management)
```python
auth_type = 'Bearer'
consumerID = ''
consumerSecret = ''

url = 'https://fc-data.ssi.com.vn/'
stream_url = 'https://fc-data.ssi.com.vn/'
```

--------------------------------------------------------------------------------------------------

[![Semantic Release](https://github.com/SSI-Securities-Corporation/python-fctrading/actions/workflows/publish.yaml/badge.svg)](https://github.com/SSI-Securities-Corporation/python-fctrading/actions/workflows/publish.yaml)

# Installation
#### From tar ball (most stable)
``` python
pip install dist/ssi-fctrading-2.4.2.tar.gz
```
#### Install behind proxy
```python
pip install --trusted-host pypi.org --trusted-host
files.pythonhosted.org --proxy=http://<username>:<password>@<host>:<port> dist/ssi-fctrading-2.4.2.tar.gz
```

#### Pypi
``` python
pip install ssi_fctrading
```