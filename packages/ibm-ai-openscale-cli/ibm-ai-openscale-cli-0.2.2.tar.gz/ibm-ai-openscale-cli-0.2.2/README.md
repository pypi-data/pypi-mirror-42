# ibm-ai-openscale-cli
![Status](https://img.shields.io/badge/status-beta-yellow.svg)
[![Latest Stable Version](https://img.shields.io/pypi/v/ibm-ai-openscale-cli.svg)](https://pypi.python.org/pypi/ibm-ai-openscale-cli)

This tool allows user to get started real quick by exploring the environment to understand what user has, and then provision corresponding services needed to run Watson OpenScale, then setup the models and setup monitoring conditions.

## Before you begin
* ☁️ You need an [IBM Cloud][ibm_cloud] account.
* 🔑 Create an [IBM Cloud API key](https://console.bluemix.net/docs/iam/userid_keys.html#userapikey)
* ⚠️ If you already have a Watson Machine Learning (WML) instance, ensure it's RC-enabled, learn more about this in the [migration instructions](https://console.bluemix.net/docs/resources/instance_migration.html#migrate).

## Installation

To install, use `pip` or `easy_install`:

```bash
pip install -U ibm-ai-openscale-cli
```

or

```bash
easy_install -U ibm-ai-openscale-cli
```

️️
## Usage

```
ibm-ai-openscale-cli --help
```
```
usage: -c [-h] -a APIKEY [--env {ypprod,ypqa,ys1dev,icp}]
          [--resource-group RESOURCE_GROUP] [--postgres POSTGRES] [--icd ICD]
          [--db2 DB2] [--wml WML] [--azure AZURE]
          [--azure-deployment-name AZURE_DEPLOYMENT_NAME] [--cos COS]
          [--username USERNAME] [--password PASSWORD] [--url URL]
          [--datamart-name DATAMART_NAME] [--keep-schema] [--history HISTORY]
          [--verbose] [--version]
          [--model {all,DrugSelectionModel,GermanCreditRiskModel}]
          [--reset {metrics,monitors,datamart,model}]

optional arguments:
  -h, --help            show this help message and exit
  --env {ypprod,ypqa,ys1dev,icp}
                        Environment. Default "ypprod"
  --resource-group RESOURCE_GROUP
                        Resource Group to use. If not specified, then
                        "default" group is used
  --postgres POSTGRES   Path to postgres credentials file for the datamart
                        database. If --postgres, --icd, and --db2 all are not
                        specified, then the internal Watson OpenScale database is used
  --icd ICD             Path to IBM Cloud Database credentials file for the
                        datamart database
  --db2 DB2             Path to IBM DB2 credentials file for the datamart
                        database
  --wml WML             Path to IBM WML credentials file
  --azure AZURE         Path to Microsoft Azure credentials file
  --azure-deployment-name AZURE_DEPLOYMENT_NAME
                        Name of the deployment to use from Microsoft Azure ML
                        Studio
  --cos COS             Path to IBM Cloud Object Storage credentials file
  --username USERNAME   ICP username. Required if "icp" environment is chosen
  --password PASSWORD   ICP password. Required if "icp" environment is chosen
  --url URL             ICP url. Required if "icp" environment is chosen
  --datamart-name DATAMART_NAME
                        Specify data mart name and schema, default is
                        "aiosfastpath"
  --keep-schema         Use pre-existing datamart schema, only dropping all
                        tables. If not specified, datamart schema is dropped
                        and re-created
  --history HISTORY     Days of history to preload. Default is 7
  --verbose             verbose flag
  --version             show program's version number and exit
  --model {all,DrugSelectionModel,GermanCreditRiskModel}
                        Model to set up with Watson OpenScale (default
                        "DrugSelectionModel")
  --reset {metrics,monitors,datamart,model}
                        Reset existing datamart then exit

required arguments:
  -a APIKEY, --apikey APIKEY
                        IBM Cloud APIKey
```

## Example

```sh
export APIKEY=<PLATFORM_API_KEY>
ibm-ai-openscale-cli --apikey $APIKEY
```

## FAQ

### Q: How do the reset options work?

A: The reset options each affect a different level of data in the datamart:

* `--reset metrics` : Clean up the payload logging table, monitoring history tables etc, so that it restores the system to a fresh state with datamart configured, model deployments added, all monitors configured, but no actual metrics in the system yet. The system is ready to go. Not supported for Watson OpenScale internal databases.

* `--reset monitors` : Remove all configured monitors and corresponding metrics and history, but leave the actual model deployments (if any) in the datamart. User can proceed to configure the monitors via user interface, API, or fastpath.

* `-- reset datamart` : "Factory reset" the datamart to a fresh state as if there was not any configuration.

* `-- reset model` : Delete the model and deployment from WML. Not yet supported for non-WML engines. Does not affect the datamart.

### Q: Can I use SSL for connecting to the datamart DB2 database?

A: Yes. DB2 Warehouse on Cloud databases automatically support SSL, using the VCAP json file generated on the "Service Credentials" page. For on-prem or ICP4D DB2 databases, you can specify the path on the local client machine to a copy of the DB2 server's SSL certificate "arm" file, using an "ssldsn" connection string in the VCAP json file:

```
{
  "hostname": "<ipaddr>",
  "host": "<ipaddr>",
  "username": "<uid>",
  "password": "<pw>",
  "port": 50000,
  "jdbcurl": "jdbc:db2://<ipaddr>:50000/<dbname>",
  "uri": "db2://<uid>:<pw>@<ipaddr>:50000/<dbname>",
  "db": "<dbname>",
  "dsn": "DATABASE=<dbname>;HOSTNAME=<ipaddr>;PORT=50000;PROTOCOL=TCPIP;UID=<uid>;PWD=<pw>",
  "ssldsn": "DATABASE=<dbname>;HOSTNAME=<ipaddr>;PORT=50001;PROTOCOL=TCPIP;UID=<uid>;PWD=<pw>;Security=ssl;SSLServerCertificate=/path_on_local_client_machine_to/db2server_instance.arm;"
}
```

If SSL connections are not needed, or not configured on the DB2 server, you can remove the "ssldsn" tag and ibm-ai-openscale-cli will use the non-SSL "dsn" tag instead. If the VCAP has both dsn and ssldsn tags, ibm-ai-openscale-cli will use "ssldsn" tag to create an SSL connection.

## Python version

✅ Tested on Python 3.4, 3.5, and 3.6.

## Contributing

See [CONTRIBUTING.md][CONTRIBUTING].

## License

This library is licensed under the [Apache 2.0 license][license].

[ibm_cloud]: https://cloud.ibm.com
[responses]: https://github.com/getsentry/responses
[requests]: http://docs.python-requests.org/en/latest/
[CONTRIBUTING]: ./CONTRIBUTING.md
[license]: http://www.apache.org/licenses/LICENSE-2.0
