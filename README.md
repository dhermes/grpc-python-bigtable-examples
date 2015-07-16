# Example Calls with `gcloud-python-bigtable`

Make sure you have downloaded [`homebrew`][2] on OS X or
[`linuxbrew`][3] on Linux. (On Linux, also be sure to
add `brew` to `${PATH}` as instructed.)

## Running Sample API Calls

To list clusters run

```bash
make list_clusters
```

This consistently fails (at least with a service account). If
you'd like to run it with a user account instead of a service
account, you first will need to mint an account with

```bash
gcloud login
```

using the [`gcloud` CLI tool][8]. After doing this, you can
use that token by adding a flag to the `make` command:

```bash
make list_clusters USE_APP_DEFAULT=True
```

To list tables in a cluster

```bash
make list_tables
```

This will need to be a cluster you have created (see
"Creating a Cluster in the UI" below).

To list zones available to a project (via the Cluster Admin API)

```bash
make list_zones
```

(Since this uses the Cluster Admin API, it fails with a service
account, so use `USE_APP_DEFAULT=True`.)

To do the same, but with the low-level API:

```bash
make list_zones_low_level
```

This uses the low-level gRPC API rather than a generated service stub.
It was created with [@nathanielmanistaatgoogle][11] while
debugging the service. Currently, it fails with a deadline exceeded
using both a service account (expected) and a user account.

**NOTE**: For the `make` targets which run samples, you can
also set `VERBOSE=True`, e.g.

```bash
make list_tables VERBOSE=True
```

to produce much more debug logging behavior.

## Quirky Error Messages

We've [noticed][10] that the Cluster Admin API does not
work for service accounts, but does work for user
accounts.

When running `make list_clusters` with the gRPC Python client
(using a service account) we don't get much information

```python
D0716 11:10:42.451769588   10866 frame_settings.c:230]       adding 983041 for initial_window change
Traceback (most recent call last):
  File "grpc_list_clusters.py", line 35, in <module>
    result_pb = response.result()
  File "/usr/local/lib/python2.7/dist-packages/grpc/framework/alpha/_reexport.py", line 96, in result
    raise _reexport_error(e)
grpc.framework.alpha.exceptions.ExpirationError
```

When [running][9] the same request with the gRPC golang client (via
`make run_cluster` in that gist), the error produced is

```
2015/07/16 11:07:56 rpc error: code = 7 desc = "Project has not enabled the API. Please use Google Developers Console to activate the API for your project."
```

This is also produced when [using][10] the BigTable JSON API

```json
{
  "error": {
    "code": 403,
    "message": "Project has not enabled the API. Please use Google Developers Console to activate the API for your project.",
    "status": "PERMISSION_DENIED",
    ...
}
```

## Installing Dependencies

1.  If you have not already done so, install the [gRPC][5]
    core C/C++ libraries:

    ```bash
    make _install_core
    ```

    Since this uses `brew` to install, this cannot be run as
    root (via `sudo`).

1.  Next, install the Python [`grpcio` library][4] via:

    ```bash
    [sudo] make _install_grpc_py
    ```

    This will use `pip install` (if you don't have Python's
    `pip`, please [install][6] it).

    You may wish to run this as root (via `sudo`) so it can
    be included with your machine's Python libraries. If
    not, you'll need to use a Python [virtual environment][7]
    so that non-privileged (i.e. non-`sudo`) installs
    are allowed.

1.  Finally, "install" `gcloud-python-bigtable` via:

    ```bash
    make _python_deps
    ```

    This will be run before every command, so you can put it
    off until running commands.

## Enabling the BigTable API

1.  Visit [Google Cloud Console][1]
1.  Either create a new project or visit an existing one
1.  In the project, click **"APIs & auth > APIs"**. The URI
    should be of the form

    ```
    https://console.developers.google.com/project/{project-id}/apiui/apis/library
    ```

1.  On this page, search for **bigtable**, and click both `Cloud Bigtable API`
    and `Cloud Bigtable Table Admin API`.
1.  For each API, click "Enable API" (if not already enabled)

## Getting a Service Account Keyfile

1.  Visit [Google Cloud Console][1]
1.  Either create a new project or visit an existing one
1.  In the project, click **"APIs & auth > Credentials"**. The URI
    should be of the form

    ```
    https://console.developers.google.com/project/{project-id}/apiui/credential
    ```

1.  On this page, click "Create new Client ID", select "Service account" as
    your "Application type" and then download the JSON key provided. The
    downloaded file should resemble `keyfile.json.sample`.

After downloading, move this key to the local directory holding this code.

## Creating a Cluster in the UI

1.  Visit [Google Cloud Console][1]
1.  Either create a new project or visit an existing one
1.  In the project, click **"Storage > Cloud Bigtable"**. The URI
    should be of the form

    ```
    https://console.developers.google.com/project/{project-id}/bigtable/clusters
    ```

1.  On this page, click **Create a cluster** and take note of the "Cluster ID"
    and "Zone" you use when creating it.

## Setting Up Local Files

You will need configuration for your own account and the code
pulls this from `config.py.sample`

1.  Execute

    ```bash
    cp config.py.sample config.py
    ```

1.  Edit `config.py` to match your own project

    1.  The `PROJECT_ID` in `config.py` to match the project ID
        in the project you used above. (Make sure you use the
        Project ID, not the Project Number)
    1.  You may name `CLUSTER` and `ZONE` anything you like, but these
        should come from a cluster that already exists (see above for
        how to create a cluster).
    1.  Change `KEYFILE_PATH` to the path of the service account key
        file that you downloaded above.
    1.  Change `TIMEOUT_SECONDS` to an integer to be used for forcing
        requests to timeout after inactivity. The default value (`10`)
        should be sufficient.

[1]: https://console.developers.google.com/
[2]: http://brew.sh/
[3]: https://github.com/Homebrew/linuxbrew#install-linuxbrew-tldr
[4]: https://github.com/grpc/grpc/tree/master/src/python
[5]: http://www.grpc.io/
[6]: https://pip.pypa.io/en/latest/installing.html
[7]: http://docs.python-guide.org/en/latest/dev/virtualenvs/
[8]: https://cloud.google.com/sdk/gcloud/
[9]: https://gist.github.com/dhermes/d27070c90a9862213a3b
[10]: https://github.com/GoogleCloudPlatform/gcloud-python/issues/872#issuecomment-121793405
[11]: https://github.com/nathanielmanistaatgoogle
