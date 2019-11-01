import openstack

conn = openstack.connect(cloud='aws', region_name='us-east-1')

def create_keypair(conn):
    keypair = conn.compute.find_keypair("mykey")

    if not keypair:
        print("Create Key Pair:")

        keypair = conn.compute.create_keypair(name="mykey")

        print(keypair)

        try:
            os.mkdir(SSH_DIR)
        except OSError as e:
            if e.errno != errno.EEXIST:
                raise e

        with open('mykeyfile', 'w') as f:
            f.write("%s" % keypair.private_key)

        os.chmod('mykeyfile', 0o400)

    return keypair

def create_server(conn):
    print("Create Server:")

    image = conn.compute.find_image("bionic")
    flavor = conn.compute.find_flavor("m1.tiny")
    network = conn.network.find_network("internal")
    keypair = create_keypair(conn)

    server = conn.compute.create_server(
        name="openstackSDK", image_id=image.id, flavor_id=flavor.id,
        networks=[{"uuid": network.id}], key_name=keypair.name)

create_server(conn)