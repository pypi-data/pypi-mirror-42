# -*- coding: utf-8 -*-
# ==============================================================================
# Imports
# ==============================================================================
import re
import sys
import pytest
import openstack
import pytest_rpc.helpers as helpers
from time import sleep
from warnings import warn
from openstack.exceptions import ConfigException
from paramiko import SSHClient, AutoAddPolicy, HostKeys
from paramiko.ssh_exception import NoValidConnectionsError

# Shakes tiny fist at Python 2.7!
try:
    # noinspection PyCompatibility
    from ConfigParser import ConfigParser, NoOptionError, NoSectionError
except ImportError:
    # noinspection PyCompatibility
    from configparser import ConfigParser, NoOptionError, NoSectionError


# ==============================================================================
# Globals
# ==============================================================================
# See https://bit.ly/2RGmytn for origin
semantic_pattern = (r'^([0-9]|[1-9][0-9]*)\.'
                    r'([0-9]|[1-9][0-9]*)\.'
                    r'([0-9]|[1-9][0-9]*)'
                    r'(?:-([0-9A-Za-z-]+'
                    r'(?:\.[0-9A-Za-z-]+)*))?(?:\+[0-9A-Za-z-]+)?$')
semantic_regex = re.compile(semantic_pattern)

# Needed for Python 2.7 and 3.x compatibility
if sys.version_info.major == 3:
    # noinspection PyShadowingBuiltins
    unicode = str


# ==============================================================================
# Fixtures
# ==============================================================================
@pytest.fixture
def openstack_properties():
    """This fixture returns a dictionary of OpenStack facts and variables from
    Ansible which can be used to manipulate OpenStack objects. (i.e. create
    server instances)

    Returns:
        dict: a static dictionary of data about OpenStack.
    """

    os_properties = {
        'image_name': 'Cirros-0.3.5',
        'cirros_image': 'Cirros-0.3.5',
        'ubuntu_image': 'Ubuntu 16.04',
        'network_name': 'GATEWAY_NET',
        'private_net': 'PRIVATE_NET',
        'test_network': 'TEST-VXLAN',
        'gateway_network_subnet': 'GATEWAY_NET_SUBNET',
        'private_network_subnet': 'PRIVATE_NET_SUBNET',
        'flavor': 'm1.tiny',
        'tiny_flavor': 'm1.tiny',
        'small_flavor': 'm1.small',
        'zone': 'nova',
        'key_name': 'rpc_support',
        'public_key_path': '/root/.ssh/rpc_support.pub',
        'private_key_path': '/root/.ssh/rpc_support',
        'security_group': 'rpc-support',
        'os_version_file_path': '/etc/openstack-release',
        'os_version_ini_path': '/etc/openstack-release.ini',
        'os_version': '99.99.99',   # Indicates that the version is unset.
        'os_version_major': 99,
        'os_version_minor': 99,
        'os_version_patch': 99,
        'os_version_codename': 'master'  # Master branch for missing version
    }

    # Retrieve OpenStack version information
    try:
        os_version_ini = ConfigParser()
        os_version_ini.read(unicode(os_properties['os_version_ini_path']))

        # Extract OpenStack version semantics
        os_properties['os_version_codename'] = \
            os_version_ini.get('default', 'DISTRIB_CODENAME').replace('"', '')
        os_properties['os_version'] = \
            os_version_ini.get('default',
                               'DISTRIB_RELEASE').replace('"', '').lstrip('r')
        os_properties['os_version_major'] = \
            int(semantic_regex.match(os_properties['os_version']).group(1))
        os_properties['os_version_minor'] = \
            int(semantic_regex.match(os_properties['os_version']).group(2))
        os_properties['os_version_patch'] = \
            int(semantic_regex.match(os_properties['os_version']).group(3))
    except (IOError, OSError, NoOptionError, NoSectionError, AttributeError):
        warn(UserWarning("Failed to parse OpenStack version file!"))

    return os_properties


@pytest.fixture
def os_api_conn():
    """Provide an authorized API connection to the 'default' cloud on the
    OpenStack infrastructure.

    Returns:
        openstack.connection.Connection: https://bit.ly/2LqgiiT
    """

    err_msg = ('The "clouds.yaml" file not found! Most likely this failure '
               'is caused by failing to apply the "ansible-role-pytest-rpc" '
               'Ansible role (https://bit.ly/2UQDU42) to the OpenStack '
               'infrastructure under test.')
    try:
        return openstack.connect(cloud='default')
    except ConfigException:
        pytest.fail(err_msg, True)


@pytest.fixture
def create_server(os_api_conn, openstack_properties):
    """Create OpenStack server instances with automatic teardown after each
    test.

    Args:
        os_api_conn (openstack.connection.Connection): An authorized API
            connection to the 'default' cloud on the OpenStack infrastructure.
        openstack_properties (dict): OpenStack facts and variables from Ansible
            which can be used to manipulate OpenStack objects.

    Returns:
        def: A factory function object.

    Raises:
        openstack.connection.exceptions.OpenStackCloudException: A server could
            not be deleted in teardown.
        UserWarning: Server not present when clean-up attempted in teardown.
    """

    servers = []  # Track inventory of server instances for teardown.

    def _factory(flavor,
                 network,
                 key_name,
                 security_groups,
                 image=None,
                 retries=10,
                 auto_ip=True,
                 timeout=600,
                 boot_volume=None,
                 show_warnings=True,
                 skip_teardown=False,
                 availability_zone=None):
        """Create an OpenStack instance.

        Note: this function uses an exponential back-off for retries which means
        the more retries specified the longer the wait between each retry. The
        total wait time is on the fibonacci sequence. (https://bit.ly/1ee23o9)

        Args:
            flavor (openstack.compute.v2.flavor.Flavor): The flavor property as
                returned from server. (https://bit.ly/2Lxwqzv)
                Name or OpenStack ID is also acceptable.
            network (openstack.network.v2.network.Network): Network dict or name
                or ID to attach the server to. Mutually exclusive with the nics
                parameter. Can also be be a list of network names or IDs or
                network dicts. (https://bit.ly/2A104IL)
            key_name (str): The name of an associated keypair.
            security_groups(list): A list of security group names.
            image (openstack.image.v2.image.Image): The image property as
                returned from server. image is required unless boot_volume is
                given. Name or OpenStack ID is also acceptable.
                (https://bit.ly/2UXESvW)
            retries (int): The maximum number of validation retry attempts.
            auto_ip (bool): Flag for specifying whether a floating IP should be
                attached to the instance automatically.
            timeout (int): Seconds to wait, defaults to 600.
            boot_volume (openstack.image.v2.volume.Volume): Volume to boot from.
                Name or OpenStack ID is also acceptable.
                (https://bit.ly/2ReINW7)
            show_warnings (bool): Flag for displaying warnings while attempting
                validate server.(VERY NOISY!)
            skip_teardown (bool): Skip automatic teardown for this server
                instance.
            availability_zone (str): Name of the availability zone for instance
                placement.

        Returns:
            openstack.compute.v2.server.Server: FYI, this class is not visible
                to the outside user until it gets instantiated.
                (https://bit.ly/2rMu7iQ)

        Raises:
            openstack.connection.exceptions.OpenStackCloudException: The server
                could not be created for some reason.
            RuntimeError: Mutually exclusive required arguments 'boot_volume' or
                'image' are not set properly!

        Example:
            >>> conn = openstack.connect(cloud='default')
            >>> image = conn.compute.find_image('test_image')
            >>> flavor = conn.compute.find_flavor('test_flavor')
            >>> network = conn.network.find_network('test_network')
            >>> key_pair_name = 'test_keypair'
            >>> security_groups = ['test-security-group']
            >>>
            >>> server = _factory(name='test_server',
            >>>                   image=image,
            >>>                   flavor=flavor,
            >>>                   network=network,
            >>>                   key_name=key_pair_name,
            >>>                   security_groups=security_groups)

            See https://bit.ly/2EDWA2S for more details.
        """

        # Configure mutually exclusive arguments.
        if image is not None and boot_volume is None:
            extra_args = {'image': image}
        elif boot_volume is not None and image is None:
            extra_args = {'boot_volume': boot_volume}
        else:
            raise RuntimeError("Mutually exclusive required arguments "
                               "'boot_volume' or 'image' are not set properly!")

        if availability_zone:
            extra_args['availability_zone'] = availability_zone

        temp_server = os_api_conn.create_server(
            wait=True,
            name="test_server_{}".format(helpers.generate_random_string()),
            flavor=flavor,
            auto_ip=False,
            network=network,
            timeout=timeout,
            key_name=key_name,
            security_groups=security_groups,
            **extra_args
        )

        # Sometimes the OpenStack object is not fully built even after waiting.
        sleep(2)

        shared_args = {'retries': retries,
                       'os_object': temp_server,
                       'os_service': 'server',
                       'os_api_conn': os_api_conn,
                       'show_warnings': show_warnings}

        # Verify that the server is on and running.
        assert helpers.expect_os_property(os_prop_name='status',
                                          expected_value='ACTIVE',
                                          **shared_args)

        assert helpers.expect_os_property(os_prop_name='OS-EXT-STS:power_state',
                                          expected_value='1',
                                          **shared_args)

        assert helpers.expect_os_property(os_prop_name='OS-EXT-STS:vm_state',
                                          expected_value='active',
                                          **shared_args)

        # Create floating IP address and attach to test server.
        if auto_ip:
            # TODO: The 'auto_ip' feature of 'create_server' is broken.
            #   (ASC-1416)
            # Delete all unattached floating IPs.
            os_api_conn.delete_unattached_floating_ips(retry=3)

            floating_ip = os_api_conn.create_floating_ip(
                wait=True,
                server=temp_server,
                network=openstack_properties['network_name'],
                timeout=600
            )

            temp_server['accessIPv4'] = floating_ip.floating_ip_address
            temp_server['access_ipv4'] = floating_ip.floating_ip_address

        if not skip_teardown:
            servers.append(temp_server)  # Add server to inventory for teardown.

        return temp_server

    yield _factory

    # Teardown
    for server in servers:
        if not os_api_conn.delete_server(name_or_id=server.id, wait=True):
            warn(UserWarning("Attempted to delete non-existent server!"
                             " ID: {}".format(server.id)))


@pytest.fixture
def create_volume(os_api_conn, openstack_properties):
    """Create OpenStack volumes with automatic teardown after each test.

    Args:
        os_api_conn (openstack.connection.Connection): An authorized API
            connection to the 'default' cloud on the OpenStack infrastructure.
        openstack_properties (dict): OpenStack facts and variables from Ansible
            which can be used to manipulate OpenStack objects.

    Returns:
        def: A factory function object.

    Raises:
        openstack.connection.exceptions.OpenStackCloudException: A volume could
            not be deleted in teardown.
    """

    volumes = []  # Track inventory of server instances for teardown.

    def _factory(size,
                 image=None,
                 retries=10,
                 timeout=600,
                 bootable=False,
                 show_warnings=True,
                 skip_teardown=False):
        """Create an OpenStack volume.

        Args:
            size (int): Size, in GB of the volume to create.
            image (openstack.image.v2.image.Image): Image name, ID or object
                from which to create the volume. Name or OpenStack ID is also
                acceptable.
            retries (int): The maximum number of validation retry attempts.
            timeout (int): Seconds to wait, defaults to 600.
            bootable (bool): Make this volume bootable.
            show_warnings (bool): Flag for displaying warnings while attempting
                validate server.(VERY NOISY!)
            skip_teardown (bool): Skip automatic teardown for this server
                instance.

        Returns:
            openstack.compute.v2.server.Server: FYI, this class is not visible
                to the outside user until it gets instantiated.
                (https://bit.ly/2rMu7iQ)

        Raises:
            openstack.connection.exceptions.OpenStackCloudException: The volume
                could not be created for some reason.
            openstack.connection.exceptions.OpenStackCloudTimeout: Wait time
                exceeded.
        """

        temp_volume = os_api_conn.create_volume(
            size=size,
            wait=True,
            name="test_volume_{}".format(helpers.generate_random_string()),
            image=image,
            timeout=timeout,
            bootable=bootable
        )

        # Verify that the volume is available.
        assert helpers.expect_os_property(retries=retries,
                                          os_object=temp_volume,
                                          os_service='volume',
                                          os_api_conn=os_api_conn,
                                          os_prop_name='status',
                                          show_warnings=show_warnings,
                                          expected_value='available')

        if not skip_teardown:
            volumes.append(temp_volume)  # Add volume to inventory for teardown.

        return temp_volume

    yield _factory

    # Teardown
    for volume in volumes:
        os_api_conn.delete_volume(name_or_id=volume.id, wait=True)


@pytest.fixture
def ssh_connect(openstack_properties):
    """Create a connection to a server via SSH.

    Args:
        openstack_properties (dict): OpenStack facts and variables from Ansible
            which can be used to manipulate OpenStack objects.

    Returns:
        def: A factory function object.
    """

    connections = []  # Track inventory of SSH connections for teardown.

    def _factory(hostname,
                 username,
                 retries=10,
                 key_filename=None,
                 auth_timeout=180):
        """Connect to a server via SSH.

        Note: this function uses an exponential back-off for retries which means
        the more retries specified the longer the wait between each retry. The
        total wait time is on the fibonacci sequence. (https://bit.ly/1ee23o9)

        Args:
            hostname (str): The server to connect to.
            username (str): The username to authenticate as.
                (defaults to the current local username)
            retries (int): The maximum number of validation retry attempts.
            key_filename (str): The filename, or list of filenames, of optional
                private key(s) and/or certs to try for authentication. (Default
                is to use the 'rpc_support' key.
            auth_timeout (float): An optional timeout (in seconds) to wait for
                an authentication response.

        Returns:
            paramiko.client.SSHClient: A client already connected to the target
                server.

        Raises:
            paramiko.BadHostKeyException: If the server’s host key could not be
                verified.
            paramiko.AuthenticationException: If authentication failed.
            paramiko.SSHException: If there was any other error connecting or
                establishing an SSH session.
            paramiko.ssh_exception.NoValidConnectionsError: Connection refused
                by host. (SSH service is probably not running or host is not
                fully booted)
            socket.error: If a socket error occurred while connecting.
        """

        temp_connection = SSHClient()
        temp_connection.set_missing_host_key_policy(AutoAddPolicy())

        for attempt in range(1, retries + 1):
            try:
                temp_connection.connect(
                    hostname=hostname,
                    username=username,
                    key_filename=(
                        key_filename or openstack_properties['private_key_path']
                    ),
                    auth_timeout=auth_timeout
                )
            except NoValidConnectionsError:
                if attempt != retries + 1:
                    sleep(attempt)
                else:
                    raise   # Re-raise

        connections.append(temp_connection)

        return temp_connection

    yield _factory

    # Teardown
    for connection in connections:
        connection.close()

    HostKeys().clear()  # Clear the 'known_hosts' file.


@pytest.fixture
def tiny_cirros_server(create_server, openstack_properties):
    """Create an 'm1.tiny' server instance with a Cirros image.

    Args:
        create_server (def): A factory function for generating servers.
        openstack_properties(dict): OpenStack facts and variables from Ansible
            which can be used to manipulate OpenStack objects.

    Returns:
        openstack.compute.v2.server.Server: FYI, this class is not visible
            to the outside user until it gets instantiated.
            (https://bit.ly/2rMu7iQ)
    """

    return create_server(
        image=openstack_properties['cirros_image'],
        flavor=openstack_properties['tiny_flavor'],
        network=openstack_properties['test_network'],
        key_name=openstack_properties['key_name'],
        show_warnings=False,
        security_groups=[openstack_properties['security_group']]
    )


@pytest.fixture
def small_ubuntu_server(create_server, openstack_properties):
    """Create a 'm1.small' server instance with an Ubuntu image.

    Args:
        create_server (def): A factory function for generating servers.
        openstack_properties(dict): OpenStack facts and variables from Ansible
            which can be used to manipulate OpenStack objects.

    Returns:
        openstack.compute.v2.server.Server: FYI, this class is not visible
            to the outside user until it gets instantiated.
            (https://bit.ly/2rMu7iQ)
    """

    temp_server = create_server(
        image=openstack_properties['ubuntu_image'],
        flavor=openstack_properties['small_flavor'],
        network=openstack_properties['test_network'],
        key_name=openstack_properties['key_name'],
        show_warnings=False,
        security_groups=[openstack_properties['security_group']]
    )

    sleep(120)  # OS boot takes a very long time.

    return temp_server
