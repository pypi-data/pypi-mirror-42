import os
import base64

from aloft.process import execute
from aloft import aws
from aloft import k8s
from aloft import chart_config
from aloft import output
from aloft import volume
from tempfile import NamedTemporaryFile


def apply_charts(release_id, chart_set, charts, sandbox_name, options):
    release_config = chart_config.get_release_config(chart_set, release_id, sandbox_name)
    namespace = release_config['namespace']
    if not options.get('dry_run'):
        k8s.create_namespace(namespace)
        volume.restore_volumes(release_id, chart_set, charts, sandbox_name)

    for chart in charts:
        value_filenames = chart_config.generate_value_files(release_id, chart_set, chart, release_config)
        config = chart_config.get_chart_config_for_chart(chart_set, chart)
        secrets_config = chart_config.get_secrets_config_for_chart(chart_set, chart)
        apply_chart(chart, config, namespace, value_filenames, secrets_config, options)

    if not options.get('dry_run') and release_config.get('lockVolumes', False):
        volume.lock_volumes(release_id, chart_set, charts, sandbox_name)


def apply_chart(chart, config, namespace, value_filenames, secrets_config, options):
    base_chart_config_directory = chart_config.get_base_chart_config_directory()
    chart_directory = f'{base_chart_config_directory}/charts/{chart}'
    value_args = ' '.join(map(lambda filename: f'-f {filename}', value_filenames))
    release_name = get_release_name(chart, namespace)
    options['helm_timout'] = config.get('helmTimeout')
    helm_args = get_helm_args(options)

    if not options.get('dry_run'):
        create_secrets(chart, secrets_config, namespace)
        if not options.get('no_hooks'):
            execute_install_hook('pre-install', chart_directory)
    execute(f'helm dependencies build {chart_directory}')
    execute(f'helm upgrade {helm_args}-i {release_name} --namespace {namespace} {chart_directory} {value_args}')
    if not options.get('dry_run') and not options.get('no_hooks'):
        execute_install_hook('post-install', chart_directory)


def delete_charts(release_id, chart_set, charts, sandbox_name, options):
    release_config = chart_config.get_release_config(chart_set, release_id, sandbox_name)
    namespace = release_config['namespace']

    for chart in charts:
        secrets_config = chart_config.get_secrets_config_for_chart(chart_set, chart)
        delete_chart(chart, namespace, secrets_config, options)

    if not options.get('dry_run'):
        k8s.delete_namespace_if_empty(namespace)
        volume.remove_released_volume_resources(release_id, chart_set, charts, sandbox_name)


def delete_chart(chart, namespace, secrets_config, options):
    base_chart_config_directory = chart_config.get_base_chart_config_directory()
    chart_directory = f'{base_chart_config_directory}/charts/{chart}'
    release_name = get_release_name(chart, namespace)
    helm_args = get_helm_args(options)

    if not options.get('dry_run') and not options.get('no_hooks'):
        execute_install_hook('pre-uninstall', chart_directory)
    execute(f'helm delete {helm_args}--purge {release_name}', ['not found'])
    if not options.get('dry_run') and not options.get('no_hooks'):
        delete_secrets(chart, secrets_config, namespace)
        execute_install_hook('post-uninstall', chart_directory)


def get_helm_args(options):
    helm_args = ''

    if options:
        helm_timeout = options.get('helm_timout')
        if helm_timeout:
            helm_args += f'--timeout {helm_timeout} '
        if options.get('debug'):
            helm_args += '--debug '
        if options.get('dry_run'):
            helm_args += '--dry-run '
        if options.get('no_hooks'):
            helm_args += '--no-hooks '

    return helm_args


def get_release_name(chart, namespace):
    release_name = chart

    if chart != namespace:
        release_name = f'{namespace}-{chart}'

    return release_name


def create_secrets(chart, secrets_config, namespace):

    if secrets_config:
        create_standard_secrets(secrets_config, chart, namespace)
        create_docker_secrets(secrets_config, namespace)


def create_standard_secrets(secrets_config, chart, namespace):
    secret_args = ''
    secret_keys = []
    temp_filenames = []

    try:
        for item in secrets_config.get('items', []):
            vault_key = item.get('vaultKey', None)
            secret_key = item.get('secretKey', None)
            encoded = item.get('encoded', False)

            if secret_key:
                secret_keys.append(secret_key)
                secret_value = aws.get_secret(vault_key)

                if secret_value:
                    if encoded:
                        secret_value = base64.standard_b64decode(secret_value).decode('utf-8')

                    temp_file = NamedTemporaryFile(mode='w+t', delete=False)
                    temp_file.write(secret_value)
                    temp_file.flush()
                    temp_filenames.append(temp_file.name)
                    secret_args = f'{secret_args} --from-file={secret_key}={temp_file.name}'

        if secret_args:
            secrets_name = secrets_config.get('secretName', f'{chart}-secret')
            output.print_action(f'Creating secret {secrets_name} with keys {secret_keys}')
            execute(f'kubectl -n {namespace} delete secret {secrets_name}', ['NotFound'], quiet=False)
            execute(f'kubectl -n {namespace} create secret generic {secrets_name} {secret_args}', quiet=False)

    finally:
        if temp_filenames:
            rm_args = ' '.join(temp_filenames)
            execute(f'rm -f {rm_args}')


def create_docker_secrets(secrets_config, namespace):
    for secret in secrets_config.get('dockerRegistrySecrets', []):
        vault_username_key = secret.get('vaultUsernameKey', None)
        vault_password_key = secret.get('vaultPasswordKey', None)

        docker_username = aws.get_secret(vault_username_key)
        docker_password = aws.get_secret(vault_password_key)

        output.print_action(f'Creating docker-registry secret {secret["secretName"]}'
                            f' with username {vault_username_key} and password {vault_password_key}')
        execute(f'kubectl -n {namespace} delete secret {secret["secretName"]}', ['NotFound'], quiet=True)
        execute(f'kubectl -n {namespace} create secret docker-registry {secret["secretName"]}'
                f' --docker-server={secret["dockerServer"]} --docker-username={docker_username}'
                f' --docker-password={docker_password} --docker-email={secret["dockerEmail"]}', quiet=True)


def delete_secrets(chart, secrets_config, namespace):
    if secrets_config:
        secrets_name = secrets_config.get('secretName', f'{chart}-secret')
        execute(f'kubectl -n {namespace} delete secret {secrets_name}', ['NotFound'])

        for secret in secrets_config.get('dockerRegistrySecrets', []):
            execute(f'kubectl -n {namespace} delete secret {secret["secretName"]}', ['NotFound'])


def execute_install_hook(hook_type, chart_directory):
    hook_script = f'{chart_directory}/hooks/{hook_type}'

    if os.path.exists(hook_script):
        execute(hook_script)
