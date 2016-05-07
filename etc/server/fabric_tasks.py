from fabric.api import env, local, run, cd
import dotenv
import os

# Load local .env file
from fabric.contrib.project import rsync_project, upload_project
from fabric.operations import sudo

env.local_dotenv_path = os.path.join(os.path.dirname(__file__), './server.env')
env.local_dir = os.path.dirname(__file__)
dotenv.load_dotenv(env.local_dotenv_path)

# Set Fabric env
env.use_ssh_config = True
env.hosts = [os.environ.get('HOST_NAME', ''), ]

env.digital_ocean_token = os.environ.get('DIGITAL_OCEAN_TOKEN', '')
env.aws_access_key_id = os.environ.get('AWS_ACCESS_KEY_ID', '')
env.aws_secret_access_key = os.environ.get('AWS_SECRET_ACCESS_KEY', '')

env.host_name = os.environ.get('HOST_NAME', '')

env.image_name = os.environ.get('IMAGE_NAME', '')

env.user_name = os.environ.get('SSH_USERNAME', 'root')
env.sshd_port = os.environ.get('SSH_PORT', '22')
env.key_file_private = os.environ.get('KEY_FILE_PRIVATE', '')
env.key_file_public = os.environ.get('KEY_FILE_PUBLIC', '')
env.docker_compose_version = os.environ.get('DOCKER_COMPOSE_VERSION', '1.5.2')
env.pptp_secret = os.environ.get('PPTP_SECRET', 'replace_with_real_password')


# How to create default deployment
def create_server(provider='digitalocean'):
    if provider=='digitalocean':
        local('docker-machine create '
              '--driver digitalocean '
              '--digitalocean-region=nyc2 '
              '--digitalocean-access-token={digital_ocean_token} '
              '{host_name}'.format(digital_ocean_token=env.digital_ocean_token,
                                   host_name=env.host_name))

    # for gcloud, first install gcloud and do gcloud auth login
    elif provider=='gcloud':
        local('docker-machine create '
              '--driver google '
              '--google-project zapgo-1273 '
              '--google-zone europe-west1-c '
              '--google-machine-type n1-standard-1 '
              '--google-username {user} '
              '{host_name}'.format(host_name=env.host_name, user=env.user_name))

    elif provider == 'amazon':
        local('docker-machine create '
              '--driver amazonec2 '
              '--amazonec2-instance-type t2.small '
              '--amazonec2-region eu-west-1 '
              '--amazonec2-zone a '
              '--amazonec2-vpc-id vpc-0f76b16a '
              '--amazonec2-subnet-id subnet-89ee3ffe '
              '--amazonec2-access-key={amazon_access_key_id} '
              '--amazonec2-secret-key={amazon_access_key} '
              '{host_name}'.format(amazon_access_key_id=env.aws_access_key_id,
                                   amazon_access_key=env.aws_secret_access_key,
                                   host_name=env.host_name))


def create_ssh_config():
    ip_address = local('docker-machine ip {host_name}'.format(host_name=env.host_name), capture=True)
    keyfile = '~/.docker/machine/machines/{host_name}/id_rsa'.format(host_name=env.host_name)

    ssh_config = env.ssh_config_template.format(
        host_name=env.host_name,
        ip=ip_address,
        port=env.sshd_port,
        user=env.user_name,
        keyfile=keyfile,
    )
    local('echo "\nHost {host_name}\n\tHostName {ip}\n\tPort {ssh_port}\n\tUser {user}\n\tIdentityFile {keyfile}"'
          '>> ~/.ssh/config'.format(host_name=env.host_name,
                                     ip=ip_address,
                                     ssh_port=env.sshd_port,
                                     user=env.user_name,
                                     keyfile=keyfile))
    print(ssh_config)

env.ssh_config_template = """Host {host_name}
    HostName {ip}
    Port {port}
    User {user}
    IdentityFile {keyfile}

"""

env.cloud_init_template = """#cloud-config
package_upgrade: true
packages:
  - tree
  - vim
  - htop
groups:
  - docker: [{user_name},]
users:
  - name: {user_name}
    sudo: ['ALL=(ALL) NOPASSWD:ALL']
    groups: [sudo, docker]
    shell: /bin/bash
    ssh-authorized-keys:
      - {ssh_public_key}
write_files:
  - path: /srv/docker-compose.yml
    content: |
      nginx-proxy:
        image: jwilder/nginx-proxy
        ports:
          - 80:80
          - 443:443
        volumes:
          - /srv/htdocs:/var/www:ro
          - /srv/certs:/etc/nginx/certs:ro
          - /srv/config/:/etc/nginx/vhost.d:ro
          - /var/run/docker.sock:/tmp/docker.sock:ro

runcmd:
  - touch /init.txt
  - curl -L https://github.com/docker/compose/releases/download/{docker_compose_version}/docker-compose-`uname -s`-`uname -m` > /usr/local/bin/docker-compose
  - chmod +x /usr/local/bin/docker-compose
  - mkdir -p /srv/certs /srv/config /srv/apps /srv/htdocs
  - chown -R {user_name}:{user_name} /srv/
  - sed -i -e '/^Port/s/^.*$/Port {sshd_port}/' /etc/ssh/sshd_config
  - sed -i -e '/^PermitRootLogin/s/^.*$/PermitRootLogin no/' /etc/ssh/sshd_config
  - sed -i -e '$aAllowUsers {user_name}' /etc/ssh/sshd_config
  - restart ssh
  - usermode -aG docker {user_name}
  - docker pull ubuntu
  - docker pull nginx
  - docker pull postgres
  - docker pull redis
  - docker pull rabbitmq:3-management
  - cd /srv/ && docker-compose up -d
"""

env.user_data = env.cloud_init_template.format(**{
    'user_name': env.user_name,
    'sshd_port': env.sshd_port,
    'docker_compose_version': env.docker_compose_version,
    'ssh_public_key': env.key_file_public,
    'pptp_secret': env.pptp_secret,
})


def install_server_requirements():
    # Add user to sudo:
    sudo('adduser {user} sudo'.format(user=env.user_name))

    # Install Docker Compose:
    sudo('curl -L '
        'https://github.com/docker/compose/releases/download/{docker_compose_version}/'
        'docker-compose-`uname -s`-`uname -m`'
        ' > /usr/local/bin/docker-compose'.format(docker_compose_version=env.docker_compose_version))

    sudo('chmod +x /usr/local/bin/docker-compose')

    # Add user to docker group:
    sudo('gpasswd -a {user} docker'.format(user=env.user_name))
    sudo('service docker restart')

    # Create server directory structure:
    sudo("mkdir -p /srv/certs /srv/config /srv/apps/default /srv/htdocs /srv/build")
    sudo("chown -R %s:%s /srv/" % (env.user_name, env.user_name))


def install_image_factory():
    run('docker pull zapgo/wheel-factory')

    with cd('/srv/build/'):
        fp = 'docker-image-factory-master'
        run('wget https://github.com/zapgo/docker-image-factory/archive/master.tar.gz')
        run('tar -zxvf master.tar.gz '
            '--strip=1'.format(fp=fp))
        run('rm master.tar.gz')


def nginx_ssl_setup():
    upload_project(os.path.join(env.local_dir, 'docker-services.yml'), '/srv/', use_sudo=True)
    run('docker-compose -f /srv/docker-services.yml up -d nginx-proxy letsencrypt-plugin')
